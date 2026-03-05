---
name: thresh-team-health
description: Analyzes completed work by developer to build expertise profiles, calculate defect quality signals, and recommend story assignments. Trigger with "team health", "developer profiles", "expertise", "who should work on", "assignment recommendations", "team capacity", or "workload".
---

# thresh-team-health

Analyzes developer work history (last 30 days) to build expertise profiles, calculate defect rates, spot capacity issues, and recommend optimal story assignments.

## Quick Steps

1. Read CLAUDE.md for Jira context and team roster
2. Read existing team patterns from product/metrics/team_profiles.json
3. For each developer, query last 30 days completed work (Done stories)
4. Calculate stories completed, points delivered, cycle time, and tagged areas
5. Query defects linked to their completed stories
6. Calculate defect rate (flag if > 0.25)
7. Build expertise profile with strengths, growth areas, capacity signal
8. Identify best fit story types for each developer
9. Recommend assignments for unassigned sprint stories
10. Update team_patterns.md with new analysis
11. Present per-developer summary and assignment recommendations table

For the full step-by-step workflow, read `references/workflow.md`.
