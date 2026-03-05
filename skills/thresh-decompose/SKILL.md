---
name: thresh-decompose
description: "Mass Figma-to-Jira pipeline: analyzes designs (Figma links, frames, or screenshots), identifies components and dependencies, generates stories with acceptance criteria, wires the work graph, and chains directly into /thresh-publish for epic/story creation in Jira. Trigger with 'decompose', 'break down designs', 'figma to stories', 'design to stories', 'figma to jira', 'create stories from screens', or 'screen analysis'."
---

# thresh-decompose

Mass pipeline that transforms Figma designs into a fully linked epic/story structure in Jira. Analyzes screens, identifies reusable components, infers user journeys, generates sized stories with acceptance criteria, wires dependency relationships into work_graph.json, and chains directly into /thresh-publish.

**Core principle**: Stories are NEVER written to local files. They are drafted in the conversation, confirmed with the user, then published directly to Jira via /thresh-publish.

## Inputs (any combination)

- **Figma URLs** — frame links, page links, or file links (uses Figma MCP)
- **Screenshots** — folder of PNGs/JPGs (user provides path or uploads)
- **Figma component references** — specific node IDs
- **Existing UX references** — from ui_registry.json

## Context to Load

Before starting, read:
- `product/context/ui_registry.json` — existing components (avoid duplication)
- `product/work_graph.json` — existing stories and dependencies
- `jira_config.json` — project key, issue types, custom fields
- Query Jira for existing epics and stories in the project

## Pipeline

### Phase 1: Input & Strategy

**1a. Collect design sources**

Ask the user for their designs. Accept any format:
```
What designs should I decompose? I can work with:
• Figma URLs (frame, page, or file links)
• A folder of screenshots
• Specific Figma node IDs

Paste links or provide a path:
```

**1b. Choose decomposition strategy**

```
How should I break screens into stories?

[A] Screen-level — One story per screen (fast, less overhead)
    Best for: Small teams, tight timelines

[B] Component + Screen — Separate stories for reusable components
    Best for: Larger teams, design system, parallel development

[C] Shared components only — Component stories only if used in 2+ screens
    Best for: Balanced reuse without overhead
```

Store preference in memory for future runs.

### Phase 2: Screen Analysis

For each design input:

**2a. View and analyze**
- If Figma URL: Use Figma MCP to get design context (get_design_context) and screenshot
- If screenshot: View the image directly
- For each screen, document:
  - **Purpose**: What this screen does (login, checkout, dashboard, etc.)
  - **Components identified**: Buttons, forms, cards, navigation, modals
  - **Data displayed**: What data this screen shows/collects
  - **User actions**: What the user can do on this screen
  - **Flow position**: Entry point, mid-flow step, confirmation, error state

**2b. Component deduplication**
- Check each component against `ui_registry.json` for existing matches
- Check Jira via `searchJiraIssuesUsingJql` for existing component stories
- Mark as: EXISTING (reuse) or NEW (needs story)

**2c. Cross-screen analysis**
After all screens are analyzed:
- Identify shared components across screens
- Group screens into user journeys/flows
- Identify screen-to-screen navigation paths
- Build a dependency map (which screens must exist before others make sense)

### Phase 3: Story Generation

**3a. Epic structure**
Group related screens into epics:
```
📦 Epic: [Flow Name] (e.g., "Checkout Flow")
├── 📋 [Screen 1 story]
├── 📋 [Screen 2 story] ← blocked_by: Screen 1
├── 📋 [Shared Component story] ← no blockers (can parallelize)
└── 📋 [Screen 3 story] ← blocked_by: Screen 2, Shared Component
```

**3b. Generate each story in chat**

For each story, draft with full structure:

```
STORY: [Title]
Epic: [Parent epic name]
Type: Story | Task
Points: [estimate based on complexity — XS=1, S=2, M=3, L=5, XL=8]

As a [user type],
I want to [action on this screen]
So that [benefit/outcome].

ACCEPTANCE CRITERIA:

AC1: [Title] — [Summary]
  GIVEN [context]
  WHEN [action]
  THEN [outcome]

AC2: [Title] — [Summary]
  GIVEN [context]
  WHEN [action]
  THEN [outcome]

[Continue for all visible requirements...]

EDGE CASES (inferred):
  [RECOMMENDED] Empty state — what shows when no data
  [RECOMMENDED] Loading state — skeleton/spinner during fetch
  [RECOMMENDED] Error state — graceful failure with retry
  [RECOMMENDED] Offline state — no network handling

COMPONENTS: [list]
BLOCKED BY: [story IDs]
BLOCKS: [story IDs]
FIGMA REF: [URL or node ID]
```

**3c. Present full structure for approval**

Show the user the complete epic/story tree with:
- Total epics and stories count
- Dependency graph (visual tree)
- Point estimates per epic
- New vs existing components
- Stories that can be parallelized vs sequential

Wait for user approval before proceeding.

### Phase 4: Work Graph Update

After user approves the story structure:

**4a. Add stories to work_graph.json**

For each story:
```json
{
  "nodes": {
    "[local_id]": {
      "title": "[story title]",
      "type": "story",
      "parent_epic": "[epic_id]",
      "status": "Draft",
      "points": [estimate],
      "components": ["ComponentA", "ComponentB"],
      "figma_ref": "[url or node_id]",
      "jira_key": null
    }
  },
  "edges": [
    { "from": "[story_id]", "to": "[dependency_id]", "type": "blocked_by" },
    { "from": "[story_id]", "to": "[related_id]", "type": "relates_to" }
  ]
}
```

**4b. Update unblocked_stories and critical_path**

Recalculate:
- `unblocked_stories` — stories with zero unresolved blocked_by edges
- `critical_path` — longest dependency chain through the new stories
- `component_index` — map component names to story IDs that implement them

**4c. Update ui_registry.json**

Add newly identified screens and components:
```json
{
  "id": "UX-[NNN]",
  "name": "[Screen/Component Name]",
  "type": "screen | component",
  "figma_ref": "[url]",
  "story_id": "[local_id]",
  "jira_key": null,
  "status": "planned"
}
```

### Phase 5: Chain to Publish

After work graph is updated, offer to publish immediately:

```
✅ Decomposition complete:
  • [N] epics, [M] stories generated
  • [P] story points total
  • [X] new components, [Y] existing reused
  • [Z] dependency relationships wired

Ready to publish to Jira? This will:
  1. Create epics in [PROJECT]
  2. Create stories linked to epics
  3. Set blocked_by/relates_to links between issues
  4. Update work_graph.json with Jira keys

Run /thresh-publish to proceed, or review stories first.
```

If user says yes → invoke /thresh-publish directly, passing the stories from work_graph.json that have `jira_key: null` and `status: Draft`.

## Handling Large Decompositions

For designs with 10+ screens:

1. **Batch processing**: Analyze screens in groups of 5, confirming each batch before continuing
2. **Progressive approval**: Show epic structure after each batch, allow adjustments
3. **Context management**: Don't load all screen analyses simultaneously — process → summarize → move on
4. **Incremental graph updates**: Write to work_graph.json after each batch, not all at end

## Rules

> [!IMPORTANT]
> **NEVER write stories to local markdown files.** Stories are drafted in the conversation and published to Jira. This is core rule #1.

> [!IMPORTANT]
> **Always analyze screens ONE AT A TIME** by viewing the actual image or Figma frame. Never guess UI details without seeing the design.

> [!CAUTION]
> **Before creating component stories, ALWAYS check Jira** using searchJiraIssuesUsingJql and check ui_registry.json. Duplicate component stories waste sprint capacity.

> [!TIP]
> **Group screens by flow first** (checkout, onboarding, settings) before generating stories. This ensures proper epic hierarchy and cleaner dependency chains.

## Integration Points

| Tool | When Used | Purpose |
|------|-----------|---------|
| Figma MCP (get_design_context) | Phase 2 | Get design details and screenshots |
| Figma MCP (get_screenshot) | Phase 2 | Visual analysis of frames |
| Jira MCP (searchJiraIssuesUsingJql) | Phase 2, 3 | Check existing components/stories |
| product/context/ui_registry.json | Phase 2, 4 | Component dedup, new screen registration |
| product/work_graph.json | Phase 2, 4 | Dependency graph updates |
| /thresh-publish | Phase 5 | Create epics/stories in Jira |

## Output

This skill does NOT create files in product/stories/ or product/epics/.

It updates:
- `product/work_graph.json` — new nodes + edges + recalculated paths
- `product/context/ui_registry.json` — new screens and components
- Jira (via /thresh-publish) — epics and stories with links
