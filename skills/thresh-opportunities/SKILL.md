---
description: Build and maintain an Opportunity Solution Tree (Teresa Torres) integrated with Thresh's structured data. Maps outcomes to opportunities to solutions to experiments, all linked to synthesis.json evidence and work_graph.json stories.
---

# /thresh-opportunities — Opportunity Solution Tree

> Map the path from desired outcomes to validated solutions. Backed by real customer evidence.

## When to Use
- After `/thresh-synthesize` — structure pain points into an opportunity tree
- Strategic planning — connect business outcomes to discovery work
- Before decomposition — ensure stories trace back to validated opportunities
- Stakeholder alignment — visual tree showing why we're building what we're building

## Inputs
- `product/customer_data/synthesis.json` — pain points, themes, feature candidates
- `product/work_graph.json` — existing stories and their dependencies
- `product/reconciliation.json` (if exists) — roadmap alignment
- `product/prioritization.json` (if exists) — ranked items
- PM provides: desired outcome (the business/product goal at the top of the tree)

## Process

### Step 1: Define Outcome
The PM states the desired outcome. Examples:
- "Reduce time-to-first-value for new users from 14 days to 3 days"
- "Increase enterprise retention from 85% to 92%"
- "Reduce support ticket volume by 40%"

### Step 2: Map Opportunities
Pull from synthesis.json themes to populate the opportunity layer:
- Each theme becomes an opportunity node
- Score each opportunity by: evidence strength, segment impact, strategic alignment
- Group opportunities by segment if multiple personas are affected differently

```
Outcome: Reduce time-to-first-value to 3 days
├── Opportunity: Onboarding friction (theme-001, evidence: 47 signals, intensity: high)
│   ├── Pain: "Can't figure out where to start" (23 mentions)
│   ├── Pain: "Setup wizard is 12 steps" (18 mentions)
│   └── Pain: "No progress indicator" (6 mentions)
├── Opportunity: Documentation gaps (theme-004, evidence: 31 signals, intensity: medium)
│   ├── Pain: "Can't find API docs" (19 mentions)
│   └── Pain: "Examples are outdated" (12 mentions)
└── Opportunity: Integration complexity (theme-007, evidence: 22 signals, intensity: high)
    ├── Pain: "OAuth flow breaks on mobile" (15 mentions)
    └── Pain: "No sandbox environment" (7 mentions)
```

### Step 3: Map Solutions
For each opportunity, pull feature candidates from synthesis.json + existing backlog:

```
Opportunity: Onboarding friction
├── Solution: Guided setup wizard (synthesis FC-001, RICE: 2142)
│   └── Existing: PROJ-234 (in backlog, 5pts, unblocked)
├── Solution: Progress tracker component (synthesis FC-002, RICE: 1890)
│   └── Existing: none → needs decomposition
└── Solution: Simplified 3-step onboarding (synthesis FC-003, RICE: 1650)
    └── Existing: PROJ-189 (in progress, 8pts)
```

### Step 4: Map Experiments
For each solution without strong evidence (confidence < 0.7):
- Suggest experiments to validate before building
- Types: prototype test, A/B test, fake door, concierge, Wizard of Oz
- If `phuryn/pm-skills` is installed, optionally link to its experiment frameworks

```
Solution: Simplified 3-step onboarding (confidence: 0.55)
├── Experiment: Prototype test with 5 users (effort: S, timeline: 1 week)
├── Experiment: Fake door test on landing page (effort: XS, timeline: 3 days)
└── Decision: Don't build until confidence > 0.7
```

### Step 5: Output

#### Structured JSON → `product/opportunity_tree.json`
```json
{
  "schema_version": "1.0",
  "last_updated": "...",
  "outcome": {
    "description": "Reduce time-to-first-value to 3 days",
    "metric": "time_to_first_value_days",
    "current": 14,
    "target": 3
  },
  "opportunities": [
    {
      "id": "opp-001",
      "theme_id": "theme-001",
      "name": "Onboarding friction",
      "evidence_strength": 47,
      "intensity": "high",
      "segments": ["new_users", "smb"],
      "solutions": [
        {
          "id": "sol-001",
          "title": "Guided setup wizard",
          "feature_candidate_id": "FC-001",
          "confidence": 0.85,
          "jira_keys": ["PROJ-234"],
          "status": "ready_to_build",
          "experiments": []
        },
        {
          "id": "sol-003",
          "title": "Simplified 3-step onboarding",
          "feature_candidate_id": "FC-003",
          "confidence": 0.55,
          "jira_keys": ["PROJ-189"],
          "status": "needs_validation",
          "experiments": [
            {
              "type": "prototype_test",
              "effort": "S",
              "timeline": "1 week",
              "success_criteria": "4/5 users complete onboarding in < 5 min"
            }
          ]
        }
      ]
    }
  ],
  "unlinked_backlog_items": ["PROJ-456", "PROJ-789"],
  "opportunities_without_solutions": ["opp-004"]
}
```

### Step 6: Integration
- Solutions with `status: ready_to_build` → `/thresh-decompose` for story creation
- Solutions with `status: needs_validation` → experiment tracking
- `unlinked_backlog_items` → flag as orphans in `/thresh-reconcile`
- Tree provides the **"why"** traceability: story → solution → opportunity → outcome → customer evidence

## Key Difference from Generic OST
- Opportunities are populated from **real synthesis data**, not brainstormed
- Solutions link to **existing Jira stories** in the backlog
- Confidence scores come from **evidence counts**, not gut feel
- Experiments are only suggested where confidence is low
- The tree is a **living document** that updates as synthesis and backlog change

## Incremental Updates
When synthesis.json updates (new interviews, new data):
- Re-score opportunity evidence strength
- Flag new themes as potential new opportunity branches
- Flag solutions whose confidence crossed the 0.7 threshold → ready to build
