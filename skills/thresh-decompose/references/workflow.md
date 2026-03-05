# thresh-decompose — Detailed Workflow Reference

This document provides the full step-by-step workflow for the mass Figma-to-Jira decomposition pipeline. The SKILL.md has the overview; this has the implementation details.

## Phase 1: Input & Strategy

### 1a. Collect Design Sources

Accept any combination of:
- **Figma frame URLs**: `https://figma.com/design/:fileKey/:fileName?node-id=X-Y`
- **Figma page URLs**: Will enumerate all frames on the page
- **Screenshot folder**: Local path to PNG/JPG files
- **Uploaded images**: Directly in the conversation

For Figma URLs, extract `fileKey` and `nodeId` from the URL pattern.

### 1b. Decomposition Strategy

Present three options:
- **A: Screen-level** — One story per screen. Best for small teams (1-2 devs).
- **B: Component + Screen** — Separate stories for reusable components. Best for larger teams (3+).
- **C: Shared components only** — Component stories only if used in 2+ screens. Balanced approach.

Store the choice in memory for future decompose runs.

## Phase 2: Screen Analysis

### 2a. View Each Screen

For each design input:

**If Figma URL:**
1. Call `get_design_context` with the extracted fileKey and nodeId
2. Call `get_screenshot` for visual reference
3. Extract component names, layout structure, and design tokens from the response

**If screenshot:**
1. View the image directly
2. Describe all visible UI elements

**For each screen, document:**
```
Screen: [Name]
Purpose: [What this screen does]
Flow: [Which user journey — checkout, onboarding, settings, etc.]
Position: [entry | step-N | confirmation | error]
Components identified:
  - [Component 1] — [existing in ui_registry | NEW]
  - [Component 2] — [existing | NEW]
User actions: [What the user can do]
Data displayed: [What information is shown]
Navigation: [Where does the user go from here]
```

### 2b. Component Deduplication

For each component identified:

1. Check `product/context/ui_registry.json`:
   ```json
   // Look for matching entries by name or similar purpose
   ```

2. Query Jira for existing component stories:
   ```
   project = [PROJECT] AND (summary ~ "[Component Name]" OR labels = "[component-label]") AND issuetype in (Story, Task)
   ```

3. Mark each component:
   - **EXISTING** — found in registry or Jira, reuse (include reference ID)
   - **NEW** — not found, needs a story (if strategy B or C applies)

### 2c. Cross-Screen Analysis

After all screens are analyzed individually:

1. **Identify shared components**: Components that appear in 2+ screens
2. **Group into flows**: Map screens to user journeys
3. **Build navigation graph**: Which screen leads to which
4. **Determine story dependencies**:
   - Screen B requires Screen A's navigation to exist
   - Screen C requires a shared component built in Screen B's story
   - Component stories block screen stories that use them

## Phase 3: Story Generation

### 3a. Epic Structure

Create one epic per user flow:
```
📦 Epic: [Flow Name] (e.g., "Mobile Checkout Flow")
│
├── 📋 Component: SharedHeader [CMP-001] (if strategy B/C + shared)
├── 📋 Component: PaymentForm [CMP-002] (if strategy B/C + shared)
│
├── 📋 Screen: Cart Review [UX-101] (entry)
│     blocked_by: CMP-001
├── 📋 Screen: Shipping Form [UX-102]
│     blocked_by: UX-101
├── 📋 Screen: Payment [UX-103]
│     blocked_by: UX-102, CMP-002
├── 📋 Screen: Confirmation [UX-104]
│     blocked_by: UX-103
└── 📋 Screen: Error Handling [UX-105]
      relates_to: UX-101, UX-102, UX-103
```

### 3b. Story Format

Each story is drafted in the conversation (NEVER to local files) with:

```
STORY: [Title]
Epic: [Parent epic]
Type: Story
Points: [1|2|3|5|8 — Fibonacci]
Components: [list]
Figma ref: [URL or node ID]

As a [user type],
I want to [action],
So that [benefit].

ACCEPTANCE CRITERIA:

AC1: [Title] — [Summary]
  GIVEN [context]
  WHEN [action]
  THEN [outcome]
  AND [additional outcome if needed]

AC2: [Title] — [Summary]
  GIVEN [context]
  WHEN [action]
  THEN [outcome]

[...continue for all visible requirements]

EDGE CASES:
  [RECOMMENDED] AC-E1: Empty state
  [RECOMMENDED] AC-E2: Loading state
  [RECOMMENDED] AC-E3: Error state
  [RECOMMENDED] AC-E4: Offline state
  [RECOMMENDED] AC-E5: Accessibility

DEPENDENCIES:
  blocked_by: [IDs]
  blocks: [IDs]
  relates_to: [IDs]

TECHNICAL NOTES:
  - [API endpoints needed]
  - [State management considerations]
  - [Data model implications]
```

### 3c. Sizing Guide

| Points | Complexity | Example |
|--------|-----------|---------|
| 1 (XS) | Trivial | Static content screen, single text change |
| 2 (S)  | Simple | Form with 2-3 fields, basic validation |
| 3 (M)  | Moderate | Screen with API integration, multiple states |
| 5 (L)  | Complex | Multi-step form, real-time updates, complex logic |
| 8 (XL) | Very complex | Payment flow, file upload, offline sync |

Stories > 8 points: flag for splitting before approval.
Stories > 13 points: MUST split — too large to estimate accurately.

### 3d. Present for Approval

Show the complete structure:
```
📊 Decomposition Summary

Epics: [N]
Stories: [M] ([P] total story points)
New components: [X]
Existing components reused: [Y]
Dependency chains: [longest chain length]

[Show the full tree with all epics and stories]

Parallelizable: [list of stories with no blockers]
Sequential: [critical path stories]

Approve this structure? I'll update the work graph and chain to /thresh-publish.
```

## Phase 4: Work Graph Update

### 4a. Add Nodes

For each approved story, add to `product/work_graph.json`:

```json
{
  "[local_id]": {
    "title": "[story title]",
    "type": "story",
    "parent_epic": "[epic_local_id]",
    "status": "Draft",
    "points": 3,
    "components": ["ComponentA"],
    "figma_ref": "https://figma.com/...",
    "jira_key": null
  }
}
```

### 4b. Add Edges

For each dependency relationship:
```json
{ "from": "[story_id]", "to": "[dependency_id]", "type": "blocked_by" }
{ "from": "[story_id]", "to": "[related_id]", "type": "relates_to" }
```

### 4c. Recalculate Derived Fields

- **unblocked_stories**: Stories where all `blocked_by` targets have `status != Draft`
- **critical_path**: Longest chain of `blocked_by` edges through new stories
- **component_index**: Map each component name to the list of story IDs that implement/use it

### 4d. Update ui_registry.json

Add new entries:
```json
{
  "id": "UX-[NNN]",
  "name": "[Screen or Component Name]",
  "type": "screen",
  "figma_ref": "[url]",
  "story_id": "[local_id]",
  "jira_key": null,
  "status": "planned"
}
```

## Phase 5: Chain to /thresh-publish

Present the publish prompt:
```
✅ Work graph updated. Ready to publish to Jira.

This will create:
  • [N] epics in [PROJECT]
  • [M] stories linked to those epics
  • [E] blocked_by links
  • [R] relates_to links

All stories will be set to "To Do" status with story points.
Figma references will be added to each issue description.

Proceed with /thresh-publish?
```

If approved, invoke /thresh-publish. It will:
1. Create epics first (parent issues)
2. Create stories with `parent` or `epic link` set
3. Create issue links for all dependencies
4. Update work_graph.json with real Jira keys
5. Update ui_registry.json with real Jira keys

## Large Decomposition Handling (10+ Screens)

1. **Batch by flow**: Process one user journey at a time (5 screens per batch)
2. **Confirm each batch**: Show the partial tree, get approval, continue
3. **Write work graph incrementally**: Save after each batch (prevents data loss)
4. **Manage context**: After analyzing a batch, summarize and clear the detailed screen analyses from working memory
5. **Cross-batch dependencies**: Track shared components across batches, wire dependencies at the end
