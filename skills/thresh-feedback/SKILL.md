---
description: Bulk triage of feature requests and feedback from multiple channels. Categorize, deduplicate, score, and route into the synthesis pipeline. Handles Slack threads, support tickets, Productboard exports, app reviews, and ad-hoc feedback.
---

# /thresh-feedback — Bulk Feedback Triage

> Process hundreds of feature requests and feedback items. Categorize, deduplicate, score, and merge into synthesis.

## When to Use
- Regular cadence — weekly triage of incoming feedback
- After a release — process post-launch feedback surge
- Engagement kickoff — bulk import historical feedback
- Before planning — ensure all voices are represented in synthesis

## Inputs

### Supported Sources
- **CSV/JSON exports** from Productboard, Canny, UserVoice, Aha! → `product/customer_data/raw/`
- **Support ticket exports** from Zendesk, Intercom, Freshdesk → `product/customer_data/raw/tickets/`
- **App store reviews** (.csv) → `product/customer_data/raw/reviews/`
- **Slack threads** via Slack connector — search by channel, reaction, or keyword
- **NPS/CSAT verbatims** (.csv) → `product/customer_data/raw/nps/`
- **Manual entries** — PM pastes feedback directly in chat

### Context
- `product/customer_data/synthesis.json` — existing themes for matching
- `product/context/glossary.json` — normalize terminology
- `product/work_graph.json` — match requests to existing stories

## Process

### Step 1: Ingest and Normalize
For each source, extract a normalized feedback item:
```json
{
  "id": "fb-0001",
  "source": "zendesk",
  "source_id": "TICKET-12345",
  "date": "2026-02-28",
  "customer": {
    "segment": "enterprise",
    "plan": "pro",
    "tenure_months": 18
  },
  "text": "We need a way to bulk export reports as PDF. Currently we screenshot each one.",
  "sentiment": "negative",
  "category": null,
  "theme_match": null,
  "jira_match": null
}
```

### Step 2: Categorize
Assign each item to a category:
- **Feature request** — customer wants something new
- **Bug report** — something is broken
- **Usability issue** — something works but is painful
- **Praise** — something is great (track for satisfaction signals)
- **Question** — customer needs help (not a product signal)
- **Out of scope** — not actionable (pricing complaint, competitor comparison, etc.)

### Step 3: Match to Existing Data
For each feature request or usability issue:
1. **Theme match**: Compare against synthesis.json themes using semantic similarity. If confidence > 0.7, link to existing theme. Otherwise flag as potential new theme.
2. **Jira match**: Compare against work_graph.json nodes. If a story already addresses this request, link it. This answers "how many customers are asking for something we're already building?"
3. **Deduplication**: Group near-identical requests. Count unique customers, not duplicate messages.

### Step 4: Score
For unmatched (new) items, score by:
- **Frequency**: How many unique customers requested this?
- **Revenue signal**: What's the combined ARR/MRR of requesting customers? (if segment data available)
- **Segment concentration**: Is this one segment or cross-cutting?
- **Urgency indicators**: Keywords like "blocker", "dealbreaker", "will churn", "critical"
- **Recency**: Weighted toward recent feedback

### Step 5: Output

#### Triage Report → `product/customer_data/feedback_triage.json`
```json
{
  "schema_version": "1.0",
  "last_updated": "...",
  "total_items_processed": 340,
  "breakdown": {
    "feature_requests": 156,
    "bug_reports": 89,
    "usability_issues": 52,
    "praise": 28,
    "questions": 10,
    "out_of_scope": 5
  },
  "matched_to_existing_themes": 118,
  "matched_to_existing_stories": 67,
  "new_theme_candidates": 12,
  "duplicates_collapsed": 43,
  "top_unaddressed_requests": [
    {
      "text": "Bulk PDF export for reports",
      "frequency": 23,
      "segments": ["enterprise", "agency"],
      "urgency": "high",
      "revenue_signal": "$450K ARR",
      "jira_match": null,
      "theme_match": null,
      "recommendation": "New theme candidate — high frequency, high revenue signal"
    }
  ]
}
```

### Step 6: Merge into Synthesis
After PM reviews triage:
- Confirmed new themes → add to synthesis.json
- Matched items → increment evidence counts in existing themes
- Run `/thresh-synthesize` in incremental mode to merge

### Step 7: Chain
- `/thresh-feedback` → `/thresh-synthesize` (merge new signals)
- `/thresh-feedback` → `/thresh-prioritize` (re-rank with new evidence)
- `/thresh-feedback` → `/thresh-reconcile` (check if new requests change roadmap gaps)

## Scheduled Mode
Set up as a Cowork scheduled task for weekly triage:
- Every Monday, scan for new files in `product/customer_data/raw/`
- Process any new exports
- Write triage report
- Notify PM: "23 new feedback items processed. 3 new theme candidates need review."

## Context Window Rules
- Process feedback items in batches of 50
- Write intermediate results to `product/customer_data/intermediate/`
- For CSVs > 500 rows, use Python pandas for initial categorization
- Only load synthesis.json once at start (not per batch)
