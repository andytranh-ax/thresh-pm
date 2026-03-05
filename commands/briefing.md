# /briefing — Full Morning Intelligence Report

Your one-command morning briefing. Covers sprint health, overnight drift, defect radar, and PR stalls in a single pass.

## Step 1: Read Context

Read the CLAUDE.md in this folder to get the client name, Jira Cloud ID, default project key, and sprint board project. You need these for every query below.

## Step 2: Sprint Health Snapshot

Query Jira for the active sprint:

```
project = [DEFAULT_PROJECT] AND sprint in openSprints() ORDER BY priority DESC
```

Calculate and report:
- **Stories by status**: count of To Do / In Progress / In Review / Done
- **Sprint progress**: percentage complete (Done / Total)
- **Velocity trajectory**: at current pace, will we hit the velocity target in CLAUDE.md?
- **Top 3 blockers**: any issue with status = Blocked or flagged, with who owns it and how long it's been stuck
- **Unassigned work**: stories in the sprint with no assignee

## Step 3: Drift Watch (What Changed While You Were Away)

Query Jira for issues updated in the last 24 hours:

```
project = [DEFAULT_PROJECT] AND updated >= -1d ORDER BY updated DESC
```

Compare current status to what you'd expect. Report:
- **Status changes**: "Story X moved from In Progress → Blocked"
- **New comments**: summarize any substantive comments added (skip bot noise)
- **New issues created**: any stories or bugs added to the sprint overnight
- **Scope changes**: anything added to or removed from the active sprint

## Step 4: Defect Radar

Query Jira for recent bugs/defects linked to stories in the current sprint:

```
issuetype in (Bug, Defect) AND created >= -7d AND project = [DEFAULT_PROJECT] ORDER BY created DESC
```

Report:
- **New defects this week**: count and list with severity
- **Defects by epic**: which epics are generating the most bugs (quality signal)
- **Unresolved defects**: any bugs that have been open 5+ days
- **Defect-to-story ratio**: total defects / total stories in sprint (flag if > 0.3)

## Step 5: PR Stall Alert

Check Jira issue links for pull requests:

For each In Progress or In Review story, use `getJiraIssueRemoteIssueLinks` to check for linked PRs. Report:
- **Stories waiting on PR review**: PR exists but not merged, open 2+ days
- **Stories with no PR**: In Progress for 3+ days but no linked PR (developer may be stuck)
- **Recently merged**: PRs merged in last 24 hours (good news to celebrate)

If remote links aren't available, note this and suggest the team link PRs to Jira issues.

## Step 6: Recommended Focus

Based on everything above, recommend the top 3 things the user should focus on today. Prioritize:
1. **Unblock others first** — if you can unblock a teammate, that multiplies impact
2. **Defect triage** — new defects need severity assessment before they grow
3. **Stale PRs** — nudge reviewers on anything open 2+ days
4. **Highest priority unfinished story** — what should you personally work on

## Output Format

Present as a clean, scannable report with clear sections. Use confidence scores (High/Medium/Low) on any predictions or recommendations. Keep it concise — this should take 30 seconds to read, not 5 minutes.

If Slack MCP is connected, ask the user if they'd like the summary posted to a Slack channel.
