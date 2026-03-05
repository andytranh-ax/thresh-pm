---
name: thresh-briefing
description: Full morning intelligence report covering sprint health, overnight changes, defects, PR stalls, and recommended focus areas. Trigger with "briefing", "morning report", "sprint status", "daily standup", "what happened overnight", "project status", or similar.
---

# thresh-briefing

Generates a one-command morning briefing that covers sprint health, overnight drift, defect radar, and PR stalls in a single pass. Provides actionable recommendations for the day.

## Quick Steps

1. Read CLAUDE.md for Jira Cloud ID, project key, and sprint board config
2. Query active sprint to get story status breakdown and velocity trajectory
3. Query last 24 hours for drift — status changes, new issues, scope changes
4. Query recent defects (7 days) and calculate defect-to-story ratio
5. Check for linked PRs on In Progress and In Review stories
6. Identify PR stalls and unlinked stories
7. Recommend top 3 focus areas (unblock others, triage defects, nudge PRs)
8. Present as scannable report with High/Medium/Low confidence scores
9. Optionally post summary to Slack if connected

For the full step-by-step workflow, read `references/workflow.md`.
