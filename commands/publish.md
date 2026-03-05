# /publish — Push Stories & Epics to Jira

Publishes stories from the work graph to Jira with full content fidelity, dependency linking, and epic hierarchy. Works standalone or as the final step in the /thresh-decompose pipeline.

## What This Does

1. **Reads work_graph.json** for stories with `jira_key: null` (unpublished)
2. **Validates** each story has: figma_ref, acceptance criteria, point estimate
3. **Creates epics first** — parent epics are created before child stories
4. **Creates stories** with full content in Jira description (GIVEN/WHEN/THEN preserved)
5. **Creates issue links** — blocked_by, relates_to relationships between Jira issues
6. **Updates work_graph.json** with real Jira keys
7. **Updates ui_registry.json** with real Jira keys for screens/components
8. **Reports completion** with issue keys and links

## Pre-Publish Validation

Before publishing ANY story, validate:

- **Figma ref** — stories CANNOT publish without a design reference (hard requirement)
- **Acceptance criteria** — minimum 3 ACs with GIVEN/WHEN/THEN
- **Point estimate** — must be set (1, 2, 3, 5, 8)
- **Epic assignment** — story must belong to an epic

If validation fails, report which stories are blocked and what's missing.

## Publishing Order

1. **Epics first** — create parent epics, capture Jira keys
2. **Unblocked stories** — stories with no `blocked_by` dependencies
3. **Dependent stories** — stories that depend on already-published ones
4. **Link creation** — after all issues exist, create Jira links between them

## Content Fidelity (STRICT)

When creating Jira issue descriptions:
- **Exact copy** of the full story content (user story, ACs, edge cases, technical notes)
- **No summarization** — do NOT shorten or rephrase acceptance criteria
- **Preserve format** — GIVEN/WHEN/THEN structure maintained as-is
- **Include everything** — edge cases, technical notes, component list, dependencies

## Confirmation Flow

Before publishing, present:
```
Ready to publish [N] stories to [PROJECT]:

📦 Epic: [Epic Name]
├── 📋 [Story 1] (3 pts) — [figma ref ✓]
├── 📋 [Story 2] (5 pts) — [figma ref ✓] blocked_by: Story 1
└── 📋 [Story 3] (2 pts) — [figma ref ✓] relates_to: Story 1

Total: [P] story points, [E] dependency links

Proceed? (This will create issues in Jira)
```

Wait for user confirmation before creating any issues.

## Jira MCP Tools Used

- `createJiraIssue` — Create stories and epics
- `editJiraIssue` — Update issues (e.g., add epic link after creation)
- `searchJiraIssuesUsingJql` — Check for duplicates before creating
- `getJiraIssue` — Verify creation succeeded

## After Publishing

- work_graph.json nodes updated with real `jira_key` values
- ui_registry.json entries updated with real `jira_key` values
- Report: total issues created, links created, any failures
