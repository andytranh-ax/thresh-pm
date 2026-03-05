# /thresh-forecast — Sprint Forecast

> Predict sprint completion likelihood using velocity data and work graph.

## When to Use
- Sprint planning — will we finish everything?
- Mid-sprint check — are we on track?
- Scope negotiation — what if we add/remove stories?

## Inputs
- `product/metrics/velocity.json` — historical velocity data
- `product/work_graph.json` — dependency graph (blocked items)
- `product/metrics/team_profiles.json` — individual capacity
- Jira live query — current sprint progress

## Process

### 1. Gather Current State
- Query Jira for current sprint: items, statuses, points
- Load velocity.json for rolling average
- Load work_graph.json for blocked items

### 2. Calculate Forecast
Use three-point estimation from historical velocity:
- **Optimistic** (P90): Best 3-sprint velocity
- **Most likely** (P50): Rolling average velocity
- **Pessimistic** (P10): Worst 3-sprint velocity

Compare each against remaining work:
- Remaining points = total planned - completed - in review
- Blocked points = items with unresolved `blocks` edges in work graph
- Net remaining = remaining points (flag blocked separately)

### 3. Risk Factors
Adjust forecast for:
- **Blocked stories**: Subtract from achievable unless unblock date is known
- **Carry-over trend**: If carry_over_rate > 15%, reduce optimistic estimate
- **Team capacity**: If developers are out, reduce proportionally using team_profiles
- **Sprint age**: If past midpoint with < 40% done, flag red

### 4. Output Format
Present as a brief sprint health card:
```
Sprint: [name] | Day [X] of [Y]
Planned: [X] pts | Done: [X] pts | In Progress: [X] pts | Blocked: [X] pts

Forecast:
  Optimistic: [X] pts completable (P90)
  Likely:     [X] pts completable (P50)
  Pessimistic:[X] pts completable (P10)

Risk: [🟢 On Track | 🟡 At Risk | 🔴 Behind]
[Key risk factors listed]
```

## Notes
- Never present forecasts as certainties — always use ranges
- Flag if velocity data has fewer than 3 sprints (low confidence)
- Distinguish between "blocked" and "not started" — they have different implications
