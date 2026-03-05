# Playbook: Risk and Regression Detection

Identify risky stories and regressions before they hit production. Run weekly.

## When to Run

Every Friday or before sprint end to identify risk:
- Stories that are too big
- Unassigned blockers
- Missing edge case ACs
- High impact changes

Time: 15 minutes

## Step-by-Step Process

### Step 1: Flag Large Stories (2 minutes)

```
Scan all "In Progress" and "Done" stories:

For each story:
[ ] Points > 8? YES → Risk: Story should have been split
    Action: Check if it was split during development
    If not: Use as feedback for estimation process
    
[ ] Points = 8 exactly? YES → Borderline risk
    Action: Ensure it has extra QA attention
    
[ ] Points ≤ 5? → Normal range, no action
```

Example output:
```
Risk Alert: Large Stories This Sprint
- STORY-2025-0050 (8pts): Borderline, ensure QA coverage
- STORY-2025-0051 (5pts + 5pts): Well split, OK

Recommendation: None - splitting worked well this sprint
```

### Step 2: Check for Missing Edge Case ACs (2 minutes)

```
For stories "In Progress" or "Done":

[ ] Has AC1, AC2, AC3 (functional ACs)? 
    If NO → Risk: Missing core behavior specs
    Action: Halt development, add ACs before continuing

[ ] Has AC-E1, AC-E2, AC-E3 (edge cases)?
    If NO → Risk: Edge cases not covered
    Action: Add edge case ACs for:
    - Empty state
    - Error state
    - Performance/accessibility (if applicable)
```

Example:
```
Risk Alert: Missing Edge Case ACs
- STORY-2025-0045: Has AC1, AC2, AC3 but NO edge cases
  Missing: Empty state, error state, accessibility
  Action: Add AC-E1, AC-E2, AC-E3 before code review

- STORY-2025-0046: Complete AC coverage ✓
```

### Step 3: Identify Unassigned Blockers (2 minutes)

```
For all stories marked blocked_by:

For each blocker:
[ ] Is the blocking story assigned? 
    If NO → Risk: Dependency may slip
    Action: Assign blocker immediately
    
[ ] Is the blocking story in earlier sprint?
    If NO → Risk: May not finish in time
    Action: Escalate to PM for sprint planning

[ ] Is the blocked story assigned?
    If NO → Risk: Can't start when ready
    Action: Assign after blocker completes
```

Example:
```
Risk Alert: Blocking Dependencies
- STORY-2025-0050 blocked by STORY-2025-0001
  Status: STORY-2025-0001 unassigned
  Risk: HIGH - may delay sprint
  Action: Assign STORY-2025-0001 today
  
- STORY-2025-0051 blocked by STORY-2025-0002
  Status: STORY-2025-0002 in current sprint ✓
  Risk: LOW - on track
```

### Step 4: Calculate Sprint Risk Score (3 minutes)

```
For the sprint overall:

Risk Factors (1 point each):
[ ] Any stories > 8pts? +1
[ ] Stories with missing edge case ACs? +2 (per story)
[ ] Unassigned blockers? +1 (per blocker)
[ ] Blocked stories > 30% of sprint? +1
[ ] Estimation accuracy < 70% last sprint? +1
[ ] Same team member has > 5 blockers? +1

Risk Score Calculation:
0-1: Low risk (green)
2-3: Medium risk (yellow) - monitor
4-5: High risk (red) - escalate
6+: Critical risk (red alert) - emergency response

Example:
- 2 stories > 8pts = 2 points
- STORY-2025-0045 missing edge cases = 2 points
- 1 unassigned blocker = 1 point
Total = 5 points = HIGH RISK (red)

Action: Escalate to PM, request help
```

### Step 5: Regression Detection (3 minutes)

```
Check for high-impact changes that could cause regressions:

Look for stories that:
[ ] Touch shared components (used by > 3 other stories)?
    Example: Modifying CMP-SEARCH-INPUT affects 10 stories
    Action: Flag for comprehensive testing
    
[ ] Modify core systems (auth, payments, data)?
    Action: Extra code review scrutiny
    
[ ] Have breaking API changes?
    Action: Coordinate rollout with dependent teams
    
[ ] Modify database schema?
    Action: Plan migration, rollback strategy

Risk: Each flagged item = +1 to regression risk
High regression risk (> 2 items) → Extra QA time
```

Example:
```
Regression Risk Alert
- STORY-2025-0046 modifies CMP-SEARCH-INPUT
  Impact radius: 8 other stories use this component
  Risk: HIGH - potential regression across search features
  Action: Comprehensive testing required, test all dependent stories

- STORY-2025-0047 adds new API endpoint
  Impact: 3 frontend stories depend on this
  Risk: MEDIUM - coordinate rollout
  Action: Plan feature flag for gradual rollout
```

### Step 6: Quality Metrics Review (2 minutes)

```
Check previous sprint quality:
[ ] Defects per story (target: < 1 defect per 5 stories)
[ ] Estimation accuracy (target: > 80%)
[ ] Test coverage (target: > 80%)
[ ] Accessibility issues (target: 0 critical, < 3 minor)

Example:
Previous Sprint Quality:
- Defects: 4 defects in 20 stories = 0.2 per story ✓ Good
- Estimation: 17 of 20 estimated accurately = 85% ✓ Good
- Test coverage: 82% ✓ Good
- A11y issues: 2 minor, 0 critical ✓ Good

Overall: Quality metrics healthy, no action needed
```

## Weekly Risk Report

```
WEEKLY RISK REPORT - 2025-02-07

SPRINT: Sprint-25

Overall Risk Score: 4/10 (MEDIUM) 🟡

Story Risks:
- STORY-2025-0050 (8pts): Borderline size - extra QA
- STORY-2025-0045: Missing edge case ACs - add before review
- STORY-2025-0001: Unassigned blocker - assign today

Regression Risks:
- STORY-2025-0046: Impacts 8 dependent stories - comprehensive test
- STORY-2025-0047: API changes - coordinate rollout

Quality Trend:
- Defects: 0.2 per story ✓
- Estimation: 85% accurate ✓
- Test coverage: 82% ✓

Recommendations:
1. Assign blocker for STORY-2025-0001 today
2. Add edge case ACs to STORY-2025-0045 before code review
3. Plan comprehensive test suite for STORY-2025-0046
4. Continue with current quality practices - metrics are healthy

Escalations: None

Status: GREEN - Sprint on track with minor mitigations
```

## Action Items

From risk report, create action items:

```
Due Today:
[ ] Assign STORY-2025-0001 (blocker)
[ ] Add ACs to STORY-2025-0045

Due Tomorrow:
[ ] Schedule extra QA time for STORY-2025-0046

Due This Sprint:
[ ] Test all dependent stories for STORY-2025-0046
[ ] Plan feature flag for STORY-2025-0047 API rollout

Monitor:
[ ] STORY-2025-0050 progress (large story)
```

## Success Criteria

Risk detection working when:
- Large stories caught early and split
- Missing ACs identified before dev
- Blocked dependencies unblocked quickly
- Regressions prevented through comprehensive testing
- Sprint completes with high quality (minimal defects)
