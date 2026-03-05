# /risk — Per-Story Risk Scoring

Scores each story in the current sprint across 4 risk dimensions and flags high-risk items for PM attention.

## What This Does

1. **Queries Jira** for current sprint stories
2. **Loads work graph** from `product/work_graph.json` for dependency data
3. **Loads team profiles** from `product/metrics/team_profiles.json` for assignment data
4. **Scores each story** across 4 dimensions (0-3 each, total 0-12):
   - **Dependency risk** — How many blockers? Are any blocked stories themselves at risk?
   - **Complexity risk** — Story points, number of ACs, integration points
   - **Assignment risk** — Is assignee experienced with this type of work? Are they overloaded?
   - **Pattern risk** — Does this match patterns that historically slip? (late estimates, vague ACs)
5. **Ranks stories** by total risk score
6. **Recommends mitigations** for high-risk items (score ≥ 8)

## Usage

```
/risk
```

## Output

Risk-ranked story table with per-dimension scores, total risk score, and specific mitigation recommendations for anything scoring 8+.
