# /thresh-synthesize

Ingest customer data in bulk and synthesize into pain points, themes, and feature candidates.

## Usage
Run `/thresh-synthesize` to process all files in `product/customer_data/raw/`.

## Steps
1. Read the skill: `skills/thresh-synthesize/SKILL.md`
2. Scan `product/customer_data/raw/` for all data files
3. Confirm scope with the PM
4. Process in batches, extract signals per source type
5. Cluster signals into unified themes
6. Score themes by frequency × intensity × breadth
7. Generate feature candidates for top pain points
8. Write `product/customer_data/synthesis.json` and `synthesis.md`
9. Suggest: "Run `/thresh-reconcile` to compare these against your backlog"
