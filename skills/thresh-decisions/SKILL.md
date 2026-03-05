---
name: thresh-decisions
description: Scans Jira comments and status changes to identify informal decisions, cross-references against existing log, and formally captures new decisions. Trigger with "decisions", "decision log", "capture decisions", "find decisions", "what was decided", or "decision audit".
---

# thresh-decisions

Identifies decisions made informally in Jira comments and status transitions, cross-references them against existing decision log, and formally captures new decisions following the intelligence record standard.

## Quick Steps

1. Read CLAUDE.md for context and project key
2. Scan Jira for decision language in comments (last 7 days)
3. Look for keywords: "decided", "agreed", "approved", "go with", "let's do", "final answer"
4. Read full issue context using getJiraIssue
5. Cross-reference against product/context/decisions/ files
6. Present uncaptured decision candidates with source, impact, confidence
7. Let user approve/skip each decision
8. Create formal decision record (DEC-YYYYMMDD-NNN) in decisions/ directory
9. Include source reference, alternatives, and impact scope
10. Summarize capture results

For the full step-by-step workflow, read `references/workflow.md`.
