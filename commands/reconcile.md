# /thresh-reconcile

Reconcile product roadmap against current Jira backlog. Identify gaps, orphans, duplicates, and capacity constraints.

## Usage
Run `/thresh-reconcile` to compare your roadmap against what's actually in the backlog.

## Steps
1. Read the skill: `skills/thresh-reconcile/SKILL.md`
2. Identify roadmap source (ask PM: Drive doc? Jira epics? Uploaded file? Synthesis output?)
3. Parse roadmap into normalized items
4. Query Jira for full backlog
5. Match roadmap items to backlog coverage
6. Identify gaps, orphans, and duplicates
7. Forecast capacity using velocity.json and team_profiles.json
8. Write `product/reconciliation.json` and `reconciliation.md`
9. Suggest next actions: "/thresh-decompose to fill gaps" or "/thresh-publish to label orphans"
