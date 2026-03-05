# /decompose — Mass Design → Jira Pipeline

Transform Figma designs or screenshots into a fully linked epic/story structure in Jira. Analyzes screens, identifies components, wires dependencies, and publishes directly.

## What This Does

1. **Collects designs** — Figma URLs, screenshots folder, or node IDs
2. **Chooses strategy** — Screen-level, Component+Screen, or Shared-only decomposition
3. **Analyzes each screen** — Identifies UI elements, components, interactions, and flow position
4. **Deduplicates components** — Checks ui_registry.json and Jira for existing components
5. **Infers user journeys** — Groups screens into flows, maps navigation paths
6. **Generates stories** — Full acceptance criteria with GIVEN/WHEN/THEN, edge cases, sizing
7. **Wires dependencies** — blocked_by, relates_to relationships across all stories
8. **Updates work graph** — Adds nodes, edges, recalculates critical path
9. **Chains to /thresh-publish** — Creates epics and stories in Jira with proper linking

## Usage

```
/decompose
```

Then provide Figma URLs, a screenshot folder path, or upload images directly.

## Key Rules

- Stories are drafted in the conversation, **never written to local files**
- Every story must have a Figma reference (URL or screenshot path)
- Components are checked against Jira and ui_registry before creating new ones
- Dependencies are wired in work_graph.json before publishing
- Large decompositions (10+ screens) are processed in batches of 5

## Output

Updates `product/work_graph.json` and `product/context/ui_registry.json`, then chains to `/thresh-publish` to create issues in Jira.
