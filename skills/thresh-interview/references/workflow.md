# Interview Workflow

## Mode 1: Prepare Script
1. Load synthesis.json (identify evidence gaps)
2. Load stakeholders.json + glossary.json
3. PM specifies: interviewee role, segment, research goal
4. Generate targeted JTBD interview script
5. Output markdown guide

## Mode 2: Process Transcript
1. Read transcript from product/customer_data/raw/interviews/
2. Load synthesis.json for theme matching
3. Extract: JTBD, pain points, satisfaction signals, quotes
4. Match signals to existing themes
5. Flag new signals not matching any theme
6. Write to product/customer_data/processed/interview-XXX.json
7. Suggest: /thresh-synthesize to merge into master synthesis

## Chaining
- /thresh-interview (prepare) → conduct interview → /thresh-interview (process) → /thresh-synthesize
