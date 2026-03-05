# /forecast — Sprint Completion Predictions

Predicts sprint completion probability using historical velocity, current work graph state, and team capacity.

## What This Does

1. **Loads velocity data** from `product/metrics/velocity.json`
2. **Loads work graph** from `product/work_graph.json` for blocked items
3. **Loads team profiles** from `product/metrics/team_profiles.json` for capacity
4. **Queries Jira** for current sprint scope and progress
5. **Calculates three-point estimate**: optimistic, expected, pessimistic
6. **Identifies risks**: blocked stories, unestimated items, capacity mismatches
7. **Reports confidence level** and specific actions to improve it

## Usage

```
/forecast
```

## Output

Sprint completion forecast with:
- Probability of completing all committed stories
- Stories at risk (blocked, unestimated, overly complex)
- Recommended scope adjustments if completion probability < 70%
- Historical accuracy of previous forecasts (if available)
