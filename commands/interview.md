# /thresh-interview

Prepare a customer interview script or process an interview transcript into structured data.

## Usage
- `/thresh-interview prepare` — Generate a targeted interview script
- `/thresh-interview process` — Extract signals from a transcript

## Steps (prepare mode)
1. Read the skill: `skills/thresh-interview/SKILL.md`
2. Load synthesis.json to identify evidence gaps
3. Ask PM: interviewee role, segment, research goal
4. Generate JTBD-based interview script targeted at gaps
5. Output markdown interview guide

## Steps (process mode)
1. Read the skill: `skills/thresh-interview/SKILL.md`
2. Identify transcript in `product/customer_data/raw/interviews/`
3. Load synthesis.json for theme matching
4. Extract JTBD, pain points, satisfaction signals, quotes
5. Write processed output to `product/customer_data/processed/`
6. Suggest: "/thresh-synthesize to merge into master synthesis"
