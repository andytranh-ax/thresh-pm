---
description: Ingest mass customer data (interviews, surveys, support tickets, feedback, NPS, analytics) and synthesize into pain points, themes, opportunities, and feature candidates. Outputs structured JSON for work graph integration.
---

# /thresh-synthesize — Customer Data Synthesis

> Feed in customer data in bulk. Get structured pain points, feature candidates, and opportunity scores out.

## When to Use
- Beginning of an engagement — mass ingest of customer research
- After a research sprint — batch process interview transcripts
- Ongoing — process new support tickets, NPS responses, or feedback
- Before roadmap planning — synthesize all signals into prioritized opportunities

## Supported Input Formats

### File-Based (bulk)
Drop files into `product/customer_data/raw/` and run this skill:
- **Interview transcripts** (.md, .txt, .docx) — one file per interview
- **Survey exports** (.csv, .xlsx) — columns for responses, ratings, segments
- **Support tickets** (.csv, .json) — exported from Zendesk, Intercom, etc.
- **NPS/CSAT data** (.csv) — score + verbatim comment
- **App reviews** (.csv) — rating + review text
- **Feedback board exports** (.csv, .json) — from Productboard, Canny, etc.
- **Analytics summaries** (.md, .csv) — funnel data, drop-off reports

### Connector-Based (live)
- **Google Drive**: Search for research docs by folder or tag
- **Slack**: Pull threads tagged with customer feedback
- **Jira**: Pull support-type issues (bug reports with customer context)

## Process

### Step 1: Inventory
Scan `product/customer_data/raw/` and list all files with types and sizes.
Ask the PM to confirm scope: "I found 23 interview transcripts, 1 NPS export (4,200 responses), and 340 support tickets. Process all?"

### Step 2: Extract Signals
For each source, extract structured signals:

**From interviews:**
- Jobs to be done (JTBD) — what the customer is trying to accomplish
- Pain points — specific frustrations, workarounds, unmet needs
- Satisfaction signals — what's working well
- Quotes — verbatim quotes that crystallize a theme (max 2 per interview)
- Segments — role, company size, use case, persona

**From surveys/NPS:**
- Theme clusters from free-text responses
- Score distribution by segment
- Correlation between themes and scores
- Trending themes (if historical data available)

**From support tickets:**
- Issue categories and frequency
- Severity distribution
- Time-to-resolution patterns
- Repeat offenders (same issue, different customers)

**From analytics:**
- Drop-off points and friction areas
- Feature usage patterns
- Segment-specific behavior differences

### Step 3: Cluster and Synthesize
Group signals across ALL sources into unified themes:
1. Cluster pain points by similarity (use semantic grouping, not just keyword matching)
2. Score each theme by: frequency (how many sources mention it), intensity (severity of the pain), breadth (how many segments affected), trend (growing or stable)
3. Map JTBD → pain points → existing features (or gaps)
4. Identify contradictions (segment A loves what segment B hates)

### Step 4: Generate Feature Candidates
For each high-priority pain point cluster:
1. Generate 2-3 solution hypotheses
2. Score each hypothesis: impact (addresses how much of the pain), feasibility (rough T-shirt size), confidence (how much evidence supports this)
3. Link back to supporting evidence (specific interviews, ticket counts, etc.)

### Step 5: Output

#### Structured JSON → `product/customer_data/synthesis.json`
```json
{
  "schema_version": "1.0",
  "last_updated": "2026-03-05T...",
  "sources_processed": {
    "interviews": 23,
    "nps_responses": 4200,
    "support_tickets": 340,
    "surveys": 1,
    "analytics_reports": 2
  },
  "themes": [
    {
      "id": "theme-001",
      "name": "Onboarding friction",
      "pain_points": ["..."],
      "frequency": 47,
      "intensity": "high",
      "segments_affected": ["new_users", "smb"],
      "evidence": [
        { "source": "interview-012.md", "quote": "..." },
        { "source": "nps_export.csv", "count": 89 }
      ],
      "feature_candidates": [
        {
          "title": "Guided setup wizard",
          "impact": "high",
          "feasibility": "M",
          "confidence": 0.85,
          "supporting_evidence_count": 12
        }
      ]
    }
  ],
  "jtbd_map": [...],
  "contradictions": [...],
  "segment_profiles": [...]
}
```

### Step 6: Integration
- Feature candidates can feed directly into `/thresh-reconcile` for backlog comparison
- Pain point themes link to work_graph.json stories via the `customer_evidence` field
- Segment profiles feed into `/thresh-refine` for acceptance criteria targeting

## Incremental Mode
After initial synthesis, subsequent runs only process NEW files in `raw/`:
- Compare file list against `synthesis.json` sources
- Process only new/modified files
- Merge new signals into existing themes (don't recreate from scratch)
- Flag any theme score changes (e.g., "Onboarding friction moved from #3 to #1")

## Complementary Plugins (Optional)
If the `phuryn/pm-skills` plugin is installed, synthesis output can feed into its strategy frameworks:
- Use pm-discovery's `/discover` to design experiments for top pain points
- Feed synthesis into pm-strategy's `/product-strategy` for vision alignment
- These are optional enhancements — Thresh's pipeline works standalone

## Context Window Management
Customer data can be massive. Rules:
- Never load all raw files at once
- Process files in batches of 5-10
- Write intermediate results to `product/customer_data/intermediate/` as JSON
- Final synthesis reads intermediates, not raw files
- For NPS/survey CSVs > 1000 rows, process in chunks via Python pandas
