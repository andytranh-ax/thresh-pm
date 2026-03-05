# /team-health — Developer Fit & Capacity Intelligence

Analyzes completed work by developer to build expertise profiles, spot capacity issues, and recommend story assignments.

## Step 1: Read Context

Read CLAUDE.md for client info, Jira Cloud ID, project keys, and team roster. Read `product/metrics/team_profiles.json` for existing team intelligence.

## Step 2: Pull Developer History (Last 30 Days)

For each developer in the Team Roster, query Jira:

```
project = [DEFAULT_PROJECT] AND assignee = "[JIRA_DISPLAY_NAME]" AND status = Done AND resolved >= -30d ORDER BY resolved DESC
```

For each developer, calculate:
- **Stories completed**: count
- **Story points delivered**: sum
- **Avg cycle time**: days from In Progress → Done
- **Tags worked on**: which tags/components they've touched most (from labels or components)
- **Epics contributed to**: which epics their work fell under

## Step 3: Defect Quality Signal

For each developer, query for defects linked to their completed stories:

```
issuetype in (Bug, Defect) AND issueFunction in linkedIssuesOf("assignee = '[NAME]' AND resolved >= -30d")
```

If that JQL function isn't available, check defects manually by reading issue links on their completed stories. Calculate:
- **Defect count**: bugs filed against their stories
- **Defect rate**: defects / stories completed (flag if > 0.25)
- **Severity distribution**: how many Critical vs Minor

## Step 4: Build Expertise Profile

For each developer, summarize:
- **Strengths**: tags/components with high completion rate + low defect rate
- **Growth areas**: tags/components with higher defect rates or longer cycle times
- **Capacity signal**: are they consistently completing their sprint load, or often carrying over?
- **Best fit for**: types of stories they excel at (e.g., "UI components", "API integration", "data migration")

## Step 5: Story Assignment Recommendations

If there are unassigned stories in the current sprint, recommend assignments based on:
1. **Expertise match**: developer has successfully completed similar stories before
2. **Capacity**: developer has room in their current sprint load
3. **Growth opportunity**: if no perfect match, who would benefit from stretching into this area

Use confidence scores: High (strong match + capacity), Medium (good match or capacity concern), Low (stretch assignment).

## Step 6: Update Team Patterns

Write the updated profiles to `product/metrics/team_profiles.json`. Preserve any existing notes and append new data. Include the date of last analysis.

## Output Format

Present a clean per-developer summary, then the assignment recommendations table. Keep it actionable — the user should be able to assign stories immediately after reading this.
