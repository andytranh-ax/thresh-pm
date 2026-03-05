# Feedback Triage Workflow

1. Scan product/customer_data/raw/ for new feedback files
2. Load synthesis.json for theme matching
3. Load work_graph.json for story matching
4. Normalize all feedback items to standard format
5. Categorize: feature request, bug, usability, praise, question, out of scope
6. Match to existing themes and stories
7. Score unmatched items by frequency, revenue signal, urgency
8. Deduplicate near-identical requests
9. Output to product/customer_data/feedback_triage.json + .md
10. PM reviews new theme candidates
11. Suggest: /thresh-synthesize to merge confirmed signals

## Scheduled Mode
Can run as weekly Cowork scheduled task — auto-processes new files every Monday.

## Chaining
- /thresh-feedback → /thresh-synthesize → /thresh-prioritize → /thresh-reconcile
