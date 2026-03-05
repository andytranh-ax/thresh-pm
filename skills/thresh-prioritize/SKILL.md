---
description: Prioritize features and backlog items using customer evidence, dependency data, capacity constraints, and multiple frameworks. Reads from synthesis.json, work_graph.json, and Jira. Outputs a ranked, actionable priority list.
---

# /thresh-prioritize — Evidence-Based Prioritization

> Prioritize features using real data, not gut feel. Combines customer evidence, engineering constraints, and strategic alignment.

## When to Use
- After `/thresh-synthesize` — prioritize feature candidates
- Before sprint planning — rank backlog items for commitment
- Quarterly planning — stack-rank roadmap themes
- Scope negotiation — data-backed trade-off decisions

## Inputs
- `product/customer_data/synthesis.json` — customer evidence per theme/feature
- `product/work_graph.json` — dependency constraints, blocked items
- `product/metrics/velocity.json` — capacity reality
- `product/metrics/team_profiles.json` — skill constraints
- `product/reconciliation.json` (if exists) — roadmap alignment context
- Jira live query — current backlog state
- PM provides: strategic goals, time horizon, constraints

## Frameworks Available

### 1. RICE (default for feature candidates)
- **Reach**: How many users/segments affected? (from synthesis.json segment data)
- **Impact**: How severe is the pain? (from synthesis.json intensity scores)
- **Confidence**: How strong is the evidence? (from synthesis.json evidence counts)
- **Effort**: How much work? (from work_graph.json story points, or T-shirt estimate)

Score = (Reach × Impact × Confidence) / Effort

### 2. ICE (quick scoring)
- **Impact**: Customer evidence strength × strategic alignment
- **Confidence**: Evidence count + team familiarity
- **Ease**: Inverse of effort + dependency count

### 3. Value vs Complexity Matrix (visual)
- X-axis: Implementation complexity (story points + dependency depth + team stretch)
- Y-axis: Customer value (evidence strength × segment breadth × pain intensity)
- Quadrant classification: Quick Wins, Strategic Bets, Fill-Ins, Avoid

### 4. Weighted Scoring (custom)
PM defines weights for dimensions. Default weights:
- Customer evidence strength: 30%
- Strategic alignment: 25%
- Effort/feasibility: 20%
- Dependency risk: 15%
- Team readiness: 10%

### 5. MoSCoW (for scope negotiation)
- Must: Critical path items + items with customer evidence > threshold
- Should: High-value items that fit capacity
- Could: Medium-value, no dependency pressure
- Won't: Low evidence, high effort, or orphaned

## Process

### Step 1: Assemble Item List
Collect items to prioritize from one or more sources:
- Feature candidates from synthesis.json
- Backlog items from Jira (epics or stories)
- Roadmap items from reconciliation.json
- Ad-hoc items provided by PM

### Step 2: Enrich Each Item
For each item, pull:
- Customer evidence score (from synthesis.json themes)
- Dependency count and depth (from work_graph.json)
- Effort estimate (from Jira story points or T-shirt)
- Team readiness (from team_profiles.json — does anyone have expertise?)
- Current status (from Jira — already in progress? blocked?)

### Step 3: Score and Rank
Apply selected framework. Output:

```json
{
  "schema_version": "1.0",
  "last_updated": "...",
  "framework": "RICE",
  "items": [
    {
      "rank": 1,
      "id": "FC-001",
      "title": "Guided setup wizard",
      "source": "synthesis:theme-001",
      "scores": {
        "reach": 4200,
        "impact": 3,
        "confidence": 0.85,
        "effort": 5,
        "total": 2142
      },
      "customer_evidence": {
        "theme": "Onboarding friction",
        "frequency": 47,
        "intensity": "high",
        "segments": ["new_users", "smb"]
      },
      "constraints": {
        "dependencies": 2,
        "team_readiness": "high",
        "blocked_by": []
      },
      "recommendation": "Commit — strong evidence, team ready, no blockers"
    }
  ],
  "summary": {
    "top_5_quick_wins": [...],
    "top_5_strategic_bets": [...],
    "recommended_defer": [...],
    "capacity_fit": "12 of 15 items fit in Q2 at current velocity"
  }
}
```

### Step 4: Output
- Write ranked results to `product/prioritization.json`
- Optionally: update Jira priorities via `/thresh-publish`
- When the PM asks for a summary, present the ranked list conversationally

## Key Difference from Generic Prioritization
- Scores are computed from **actual data** in your synthesis, work graph, and velocity files
- Not a theoretical exercise — linked to real Jira items and real capacity
- Dependency constraints are factored in (a high-value item blocked by 3 others scores lower on feasibility)
- Team readiness is real (from team_profiles.json, not assumed)
- Results chain into execution: ranked items → `/thresh-decompose` → `/thresh-publish` → Jira

## Context Window Rules
- Load synthesis.json and work_graph.json upfront
- Query Jira in batches if > 50 backlog items
- Write prioritization.json immediately after scoring
