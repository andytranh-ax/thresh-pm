# Synthesize Workflow

## Quick Start
1. Drop customer data files into `product/customer_data/raw/`
2. Run `/thresh-synthesize`
3. Claude inventories files, confirms scope
4. Processes in batches, extracts signals
5. Clusters into themes, scores by priority
6. Generates feature candidates
7. Outputs to `product/customer_data/synthesis.json` + `.md`

## Supported File Patterns
- `product/customer_data/raw/interviews/*.md` — interview transcripts
- `product/customer_data/raw/surveys/*.csv` — survey exports
- `product/customer_data/raw/tickets/*.csv` — support ticket exports
- `product/customer_data/raw/nps/*.csv` — NPS/CSAT data
- `product/customer_data/raw/reviews/*.csv` — app store reviews
- `product/customer_data/raw/analytics/*.md` — analytics summaries

## Chaining
- `/thresh-synthesize` → `/thresh-reconcile` (compare features against backlog)
- `/thresh-synthesize` → `/thresh-decompose` (break top features into stories)
- `/thresh-synthesize` → `/thresh-refine` (use pain points as AC context)
