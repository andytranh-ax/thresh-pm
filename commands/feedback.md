# /thresh-feedback

Bulk triage of feature requests and feedback. Categorize, deduplicate, score, and route into synthesis.

## Usage
Run `/thresh-feedback` to process all new feedback files.

## Steps
1. Read the skill: `skills/thresh-feedback/SKILL.md`
2. Scan `product/customer_data/raw/` for new feedback files
3. Load synthesis.json for theme matching, work_graph.json for story matching
4. Normalize, categorize, match, deduplicate
5. Score unmatched items by frequency, revenue signal, urgency
6. Write `product/customer_data/feedback_triage.json` and `feedback_triage.md`
7. Present new theme candidates for PM review
8. Suggest: "/thresh-synthesize to merge confirmed signals"
