# /thresh-risk — Story Risk Scoring

> Assess risk level for individual stories or entire sprints using dependency, complexity, and team signals.

## When to Use
- Before sprint commitment — which stories are risky?
- During refinement — does this story need de-risking?
- Mid-sprint — which in-progress items might slip?

## Inputs
- `product/work_graph.json` — dependency graph
- `product/metrics/team_profiles.json` — developer expertise
- `product/metrics/velocity.json` — historical patterns
- Jira live query — current story details

## Risk Dimensions

### 1. Dependency Risk (0-3)
From work_graph.json:
- 0 = No dependencies
- 1 = Dependencies exist, all resolved/done
- 2 = 1-2 unresolved blockers
- 3 = 3+ unresolved blockers or chain depth > 2

### 2. Complexity Risk (0-3)
From story attributes:
- 0 = ≤ 3 points, single component
- 1 = 3-5 points, single component
- 2 = 5-8 points or multi-component
- 3 = 8+ points or touches > 3 components

### 3. Assignment Risk (0-3)
From team_profiles.json:
- 0 = Assigned to expert (confidence > 0.8)
- 1 = Assigned to competent developer (confidence 0.5-0.8)
- 2 = Assigned to stretch developer (confidence < 0.5) or unassigned
- 3 = Assigned to someone with high defect rate in this area

### 4. Pattern Risk (0-3)
From velocity.json + team_profiles.json:
- 0 = Similar stories historically completed on time
- 1 = Mild carry-over trend for this type
- 2 = Stories of this size/type frequently carry over
- 3 = No historical data (novel area)

## Scoring
- **Total Risk Score** = sum of all dimensions (0-12)
- **🟢 Low** (0-3): Safe to commit
- **🟡 Medium** (4-6): Monitor closely, have contingency
- **🔴 High** (7-9): Consider de-scoping or splitting
- **⚫ Critical** (10-12): Do not commit without mitigation plan

## Output Format
```
Story: [KEY] — [Title]
Risk Score: [X]/12 [emoji]

  Dependency: [X]/3 — [reason]
  Complexity: [X]/3 — [reason]
  Assignment: [X]/3 — [reason]
  Pattern:    [X]/3 — [reason]

Recommendation: [commit | monitor | split | descope]
Mitigation: [suggested action if score > 6]
```

## Sprint-Level View
When scoring an entire sprint:
- Score each story individually
- Highlight any story scored 🔴 or ⚫
- Calculate sprint risk = (sum of high-risk story points / total planned points)
- Flag if sprint risk > 30%

## Notes
- Risk scores are advisory — they inform discussion, not dictate decisions
- Update scores as sprint progresses (blockers resolve, reassignments happen)
- Log risk assessments in session summaries for trend tracking
