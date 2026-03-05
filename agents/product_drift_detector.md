# Product Drift Detector Agent

## Purpose
Monitor sprint alignment. Detect when current stories are drifting away from sprint goal, allowing early intervention before resources are wasted on off-goal work.

---

## Inputs

1. **Current Sprint Stories**: All stories in current sprint (status: backlog, in-progress, done)
2. **Sprint Goal**: From `product/context/CLAUDE.md` under "Current Sprint Goal"
3. **Team Capacity**: Planned points for sprint
4. **Historical Patterns**: From `product/metrics/team_patterns.md`

---

## Process

### Step 1: Extract Sprint Goal Keywords
Parse sprint goal to identify 3-5 core keywords/themes:

**Example Goal**: "Deliver mobile authentication v2 with OAuth2 and improve login performance"
**Keywords**: 
- Mobile
- Authentication 
- OAuth2
- Performance
- Login

### Step 2: Categorize Current Stories
For each story in sprint, check if it maps to sprint goal keywords:

**Strong Alignment** (story directly implements goal):
- Story title or description contains ≥2 goal keywords
- Story is on critical path for sprint goal
- Points: count toward sprint goal

**Weak Alignment** (story tangentially related):
- Story contains 1 goal keyword but in different context
- Story supports goal but not directly implementing
- Example: "Update testing framework" supports quality but isn't mobile auth

**No Alignment** (story is off-goal):
- Story contains 0 goal keywords
- Story is unrelated to sprint goal
- Example: "Refactor legacy database queries" during "mobile auth" sprint

### Step 3: Detect Drift Types

#### Type 1: Scope Creep
New stories added mid-sprint that weren't in original sprint plan.

**Detection**:
- Story created during sprint (date_created is in current sprint)
- Story was not in initial sprint backlog
- Count: X stories added mid-sprint

**Risk**: Dilutes focus from sprint goal

**Example**: "Add dark mode toggle" added on day 3 of mobile auth sprint

#### Type 2: Goal Drift  
Stories in sprint don't align with stated sprint goal.

**Detection**:
- Story has 0 goal keywords
- Story points are being spent
- % of sprint goal stories: (goal-aligned points / total sprint points)

**Threshold**: If ≤70% of sprint points are goal-aligned, flag as HIGH drift

**Example**: Sprint goal = "Mobile auth", but 30% of points spent on "Database optimization"

#### Type 3: Priority Inversion
Low-priority work being completed before high-priority work.

**Detection**:
- Check story priority field vs completion order
- If story marked "low" is in done, but "high" priority story is still backlog → inversion
- Count: X stories with priority inversion

**Risk**: High-value work might not ship

**Example**: 
- PROJ-100 (Priority: High, Mobile Login) - Still In Progress
- PROJ-101 (Priority: Low, UI Polish) - Already Done

---

## Drift Score Calculation

**Drift Score** = 0-100 (0 = perfect alignment, 100 = completely off-goal)

```
Drift = (Scope Creep Penalty + Goal Drift Penalty + Priority Inversion Penalty) / 3

Scope Creep Penalty:
  - 0 points: No stories added mid-sprint
  - 25 points: 1-2 stories added mid-sprint
  - 50 points: 3-5 stories added mid-sprint
  - 100 points: 6+ stories added mid-sprint (severe)

Goal Drift Penalty:
  - 0 points: 90-100% of sprint points are goal-aligned
  - 20 points: 80-89% goal-aligned (minor drift)
  - 50 points: 60-79% goal-aligned (moderate drift)
  - 100 points: <60% goal-aligned (severe drift)

Priority Inversion Penalty:
  - 0 points: No priority inversions (high/critical stories done before low)
  - 30 points: 1-2 inversions detected
  - 60 points: 3-5 inversions detected
  - 100 points: 6+ inversions or high-priority critical work still undone
```

**Interpretation**:
- Drift 0-20: Excellent alignment, no intervention needed
- Drift 21-40: Minor drift, monitor but acceptable
- Drift 41-60: Moderate drift, discuss with team
- Drift 61-80: High drift, recommend stopping new work to focus on goal
- Drift 81-100: Severe drift, sprint goal is at risk, escalate to PM

---

## Output Report

```markdown
## Product Drift Analysis - Sprint [XX]

### Sprint Goal
"Deliver mobile authentication v2 with OAuth2 and improve login performance"

**Goal Keywords**: Mobile, Authentication, OAuth2, Performance, Login

### Alignment Summary
- **Total Sprint Points**: 40
- **Goal-Aligned Points**: 28 (70%)
- **Tangentially-Related Points**: 8 (20%)
- **Off-Goal Points**: 4 (10%)

**Drift Score: 35/100 (Moderate - Monitor)**

### Stories by Alignment

**Strongly Aligned (28 pts)**:
- PROJ-234: Implement OAuth2 login (8 pts)
- PROJ-235: Mobile auth UI redesign (8 pts)
- PROJ-236: Login performance optimization (8 pts)
- PROJ-237: Password reset via email (4 pts)

**Weakly Aligned (8 pts)**:
- PROJ-238: Update testing framework (5 pts) - Supports quality goals
- PROJ-239: Database indexing (3 pts) - Supports performance goals

**Off-Goal (4 pts)**:
- PROJ-240: Refactor legacy API (4 pts) - Technical debt, not mobile auth

### Drift Type Analysis

**Scope Creep**: 2 stories added mid-sprint
- PROJ-239: Database indexing (added day 3)
- PROJ-240: Refactor legacy API (added day 5)

**Goal Drift**: 70% of sprint points are goal-aligned (threshold: 70%)
- Status: AT THRESHOLD - Acceptable but watch for further creep

**Priority Inversion**: 1 story with priority inversion
- PROJ-238 (Priority: Low) - Done
- PROJ-236 (Priority: High) - Still In Progress

### Recommended Actions
1. **Stop adding new stories** until sprint goal is clearly achieved
2. **Reprioritize**: Complete PROJ-236 (high priority) before PROJ-238 (low priority)
3. **Discuss PROJ-240**: Refactoring legacy API is off-goal. Move to next sprint's backlog or justify business case.
4. **Monitor PROJ-239**: Database indexing is supporting work but adds complexity. Ensure it doesn't block mobile auth delivery.
5. **Next steps**: Review with PM - is refactoring critical, or should we defer it?

### Outlook
Sprint is currently **ON TRACK** for goal delivery. One more significant scope addition would make goal at risk.
```

---

## Thresholds and Actions

| Drift Score | Status | Action |
|------------|--------|--------|
| 0-20 | Excellent | No intervention needed. Celebrate alignment. |
| 21-40 | Good | Monitor. Discuss any new scope additions with PM. |
| 41-60 | Moderate | Team discussion: prioritize goal vs. other work. Stop new mid-sprint additions. |
| 61-80 | High Risk | Escalate to PM. Consider removing off-goal work. Focus team on critical path. |
| 81-100 | Critical | Stop sprint. Reset priorities. Return to core goal. |

---

## Integration

**Triggered by**:
- Daily sprint board refresh
- When new story added to sprint mid-sprint
- When story status changes
- End of sprint retrospective

**Output to**:
- Sprint dashboard (visible to PM and team leads)
- Weekly status report
- Sprint retrospective analysis

**Correlate with**:
- `product/metrics/team_patterns.md` - Historical sprint drift patterns
- `intelligence_record_standard.md` - Decisions that impact sprint goal
- Velocity trends - If drift is increasing sprint to sprint
