---
description: Prepare structured customer interview scripts and process transcripts into the Thresh synthesis pipeline. Outputs structured JSON that feeds directly into /thresh-synthesize.
---

# /thresh-interview — Customer Interview Pipeline

> Prepare interviews. Process transcripts. Feed structured signals into the synthesis pipeline.

## Two Modes

### Mode 1: Prepare Interview Script
Generate a tailored interview script based on engagement context.

**Inputs:**
- `product/customer_data/synthesis.json` (if exists) — focus questions on existing pain point gaps
- `product/context/stakeholders.json` — understand who we're interviewing
- `product/context/glossary.json` — use the customer's language
- PM provides: interviewee role, segment, research goal

**Process:**
1. Load existing synthesis to identify gaps in evidence
2. Generate a JTBD-based interview script with:
   - Opening rapport questions (2-3 min)
   - Context-setting questions — "Walk me through how you currently..."
   - Pain point probing — open-ended, not leading
   - Workflow-specific questions based on the product area
   - JTBD triggers — "When did you last try to [job]? What happened?"
   - Satisfaction signals — "What's working well that we shouldn't break?"
   - Closing — "What's the one thing that would make the biggest difference?"
3. For each question, include:
   - The question itself
   - Why we're asking (internal note for interviewer)
   - Follow-up probes if the answer is vague
   - What theme/gap in synthesis.json this question targets (if applicable)
4. Output: markdown interview guide, optimized for printing or screen-sharing

**Key design principle:** Questions are targeted at gaps in existing synthesis data, not generic. If synthesis.json shows weak evidence on "onboarding friction," the script emphasizes onboarding questions.

### Mode 2: Process Transcript
Extract structured signals from an interview transcript and feed into the synthesis pipeline.

**Inputs:**
- Interview transcript (`.md`, `.txt`, or `.docx` in `product/customer_data/raw/interviews/`)
- `product/customer_data/synthesis.json` (if exists) — for matching to existing themes

**Process:**
1. Read transcript
2. Extract structured signals:

```json
{
  "interview_id": "interview-024",
  "date": "2026-03-05",
  "interviewee": {
    "role": "Engineering Manager",
    "segment": "enterprise",
    "company_size": "500+",
    "persona": "technical_buyer"
  },
  "jobs_to_be_done": [
    {
      "job": "Quickly understand which PRs are blocked and why",
      "context": "Morning standup prep",
      "current_solution": "Manually checks GitHub + Slack",
      "satisfaction": "low"
    }
  ],
  "pain_points": [
    {
      "description": "Can't see cross-team dependencies without checking 3 tools",
      "intensity": "high",
      "frequency": "daily",
      "workaround": "Maintains a personal spreadsheet",
      "existing_theme_match": "theme-003"
    }
  ],
  "satisfaction_signals": [
    {
      "feature": "Dashboard overview",
      "sentiment": "positive",
      "quote": "The dashboard is the first thing I check every morning"
    }
  ],
  "quotes": [
    {
      "text": "I spend 30 minutes every morning just figuring out what's blocked",
      "context": "Discussing dependency visibility",
      "theme_match": "theme-003"
    }
  ],
  "new_signals": [
    "Wants automated daily digest of cross-team blockers — not currently a theme"
  ]
}
```

3. Match signals against existing themes in synthesis.json:
   - Existing theme? Increment frequency, add evidence
   - New signal? Flag as potential new theme
4. Write structured output to `product/customer_data/processed/interview-024.json`
5. Suggest: "Run `/thresh-synthesize` to merge this into the master synthesis"

**Key design principle:** Output is structured JSON that feeds directly into the synthesis pipeline. Themes are matched against existing data. New signals are flagged for review, not silently added.

## Context Window Rules
- Interview transcripts can be long. If > 200 lines, process in sections
- Never load more than one transcript at a time
- Write processed output immediately, don't accumulate in context
