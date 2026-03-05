---
name: thresh-refine
description: Structured refinement session facilitation with prep, interactive story walkthrough, and post-refinement Jira sync. Trigger with "refine", "refinement", "story refinement", "grooming", "backlog grooming", "refine stories", or "prep refinement".
---

# thresh-refine

Facilitates structured refinement sessions across three modes: prep (select stories and flag not-ready), start (walk through ACs with discussion prompts), and end (sync all decisions back to Jira).

## Quick Steps

1. **Prep Mode:** Show team capacity, stories selected, readiness status, and agenda
2. Apply rule validation (check catalog for business rule coverage in ACs)
3. **Start Mode:** Display functional intent and walk through each AC with discussion prompts
4. Capture open questions, decisions, and assignments during walkthrough
5. Log scope changes and point updates as they happen
6. **End Mode:** Summarize decisions and open questions
7. Validate story status (Ready for Dev vs Blocked)
8. Sync all updates to Jira using editJiraIssue and transitionJiraIssue

For the full step-by-step workflow, read `references/workflow.md`.
