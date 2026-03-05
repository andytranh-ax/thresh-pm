---
description: Reconcile a product roadmap against the current Jira backlog. Identify gaps, duplicates, orphaned work, and misalignment between strategy and execution. Generates actionable recommendations.
---

# /thresh-reconcile — Roadmap vs Backlog Reconciliation

> Compare what you planned to build against what's actually in the backlog. Find gaps, duplicates, and drift.

## When to Use
- Quarterly planning — align roadmap themes with backlog reality
- After customer synthesis — compare new feature candidates against existing backlog
- Engagement kickoff — understand gap between stated roadmap and actual work
- Mid-cycle review — detect drift between roadmap commitments and sprint work

## Inputs

### Roadmap Source (one of)
- **Google Drive document** — search for roadmap doc via Drive connector
- **Uploaded file** — `.md`, `.csv`, `.xlsx`, `.pptx` dropped into `product/roadmap/`
- **Jira epics** — query all epics for the project as the de facto roadmap
- **Synthesis output** — `product/customer_data/synthesis.json` feature candidates as the "should-build" list

### Backlog Source
- **Jira live query** — all stories/tasks in backlog + current/next sprint
- **Work graph** — `product/work_graph.json` for dependency context

### Context
- `product/metrics/velocity.json` — capacity constraints
- `product/metrics/team_profiles.json` — skill constraints

## Process

### Step 1: Parse Roadmap
Extract roadmap items into a normalized format:
```json
{
  "id": "R-001",
  "theme": "Onboarding",
  "title": "Guided setup wizard",
  "target_quarter": "Q2 2026",
  "priority": "P1",
  "owner": "Product",
  "customer_evidence": "theme-001",
  "estimated_effort": "L"
}
```
Source can be structured (spreadsheet, Jira epics) or unstructured (slide deck, doc). For unstructured, extract themes and items using semantic parsing.

### Step 2: Pull Backlog
Query Jira for all issues in the project:
- Epics, stories, tasks, bugs
- Include status, sprint assignment, labels, components
- Map to work_graph.json nodes where they exist

### Step 3: Match and Score
For each roadmap item, find matching backlog items:
- **Exact match**: Jira epic/story directly implements the roadmap item (linked or tagged)
- **Partial match**: Stories exist that cover part of the roadmap item
- **No match**: Roadmap item has no corresponding backlog work

For each backlog item, check roadmap alignment:
- **Aligned**: Clearly maps to a roadmap theme
- **Opportunistic**: Useful but not on the roadmap
- **Orphaned**: No clear strategic connection
- **Tech debt**: Infrastructure work (may or may not align)

### Step 4: Gap Analysis
Produce four lists:

**Roadmap gaps** — things on the roadmap with no backlog coverage:
- How critical is the gap? (based on priority + customer evidence)
- Estimated stories needed to close the gap
- Recommended next action (decompose, de-scope, or defer)

**Backlog orphans** — work in the backlog not connected to any roadmap theme:
- What percentage of current sprint is orphaned work?
- Should these be killed, re-themed, or promoted to roadmap?

**Duplicates** — multiple backlog items covering the same roadmap intent:
- Stories that overlap significantly
- Recommend: merge, split, or clarify scope

**Capacity forecast** — given velocity and team profiles:
- Can the roadmap be delivered in the stated timeframe?
- Which items are at risk based on current velocity?
- What needs to be cut or deferred to fit?

### Step 5: Output

#### Structured JSON → `product/reconciliation.json`
```json
{
  "schema_version": "1.0",
  "last_updated": "...",
  "roadmap_items": 15,
  "backlog_items": 87,
  "coverage": {
    "fully_covered": 6,
    "partially_covered": 5,
    "not_covered": 4
  },
  "backlog_alignment": {
    "aligned": 52,
    "opportunistic": 18,
    "orphaned": 12,
    "tech_debt": 5
  },
  "gaps": [...],
  "orphans": [...],
  "duplicates": [...],
  "capacity_forecast": {
    "deliverable_this_quarter": 8,
    "at_risk": 4,
    "must_defer": 3
  },
  "recommendations": [...]
}
```

### Step 6: Integration
- Gaps feed into `/thresh-decompose` to generate missing stories
- Orphans can be bulk-labeled in Jira via `/thresh-publish`
- Capacity forecast updates `product/metrics/velocity.json` projections
- Customer evidence from synthesis.json links to gap severity

## Reconciliation with Customer Synthesis
When run after `/thresh-synthesize`:
- Feature candidates from synthesis become the "should-build" roadmap
- Match against existing backlog to find what's already planned vs what's new
- Score new feature candidates by: customer evidence strength × backlog gap size
- Output a "customer-driven roadmap delta" — what to add, what to reprioritize

## Incremental Mode
After initial reconciliation, subsequent runs:
- Compare against previous `reconciliation.json`
- Highlight changes: new gaps, closed gaps, new orphans, resolved orphans
- Track coverage trend over time (are we getting more or less aligned?)
