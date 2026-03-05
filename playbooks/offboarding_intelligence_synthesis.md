# Playbook: Offboarding Intelligence Synthesis

End-of-engagement process for contractors, rotating team members, or project leads. Package and transfer knowledge to ensure continuity.

## When to Use

Use when:
- Contractor engagement ending
- Team member transitioning out
- Project lead handing off work
- Institutional knowledge at risk

Time: 2-4 hours depending on engagement length

## Step-by-Step Process

### Step 1: Compile All Decisions (30 minutes)

Gather all decisions made during engagement:

```
Search intelligence records:
[ ] All DEC-* records created during engagement
[ ] Categorize by topic:
    - Technical decisions (arch, database, APIs)
    - Product decisions (scope, priority, timelines)
    - Process decisions (testing, deployment, standards)
[ ] For each decision:
    - Document rationale
    - Document alternatives considered
    - Document impact (which stories affected)
    - Note if still Active, Superseded, or Revoked

Example format:
DEC-20250115-001: Use PostgreSQL for product data
- Rationale: ACID compliance needed for inventory
- Alternatives: MongoDB (rejected - no transactions)
- Impact: All backend stories use PostgreSQL
- Status: Active
- Owner: bob@company.com
```

### Step 2: Export Team Patterns (30 minutes)

Synthesize patterns observed during engagement:

```
Document patterns in:
- Estimation accuracy (do points match effort?)
- Code quality (common issues found in review)
- Testing effectiveness (defect escape rate)
- Component reuse (which components most used)
- Dependency patterns (common blocking scenarios)
- Edge case coverage (missing ACs)

Example:
Pattern: Edge Case Misses
- Finding: 30% of stories missing edge case ACs
- Impact: 5 defects during QA phase
- Root cause: No checklist for AC completeness
- Recommendation: Create [Accessibility], [Error State], [Performance] checklists

Pattern: Over-Estimation
- Finding: Large stories (5pts+) tend to underestimate
- Impact: 20% velocity miss last sprint
- Root cause: Underestimating coordination complexity
- Recommendation: Add +1pt buffer for cross-team stories
```

### Step 3: Document Tech Debt (30 minutes)

Capture unfinished work and known limitations:

```
Format: Tech Debt Register

Item: Search API N+1 query problem
- Description: Each product in results requires separate API call
- Impact: Search latency 3+ seconds for 100 results
- Effort to Fix: 2-3 points (add JOIN to API)
- Priority: HIGH - blocks performance improvements
- Recommended For: Next sprint
- Owner: backend team

Item: CMP-SEARCH-INPUT accessibility gap
- Description: Search input missing ARIA labels
- Impact: Screen readers don't announce input purpose
- Effort to Fix: 2 points (add ARIA attributes)
- Priority: MEDIUM - affects a11y compliance
- Recommended For: Q2 a11y sprint
- Owner: frontend team

Item: Mobile responsive search
- Description: Search filters not responsive on mobile
- Impact: Filters stack vertically, hard to use on phone
- Effort to Fix: 5 points (redesign filter panel)
- Priority: LOW - mobile features lower priority
- Recommended For: Backlog
- Owner: frontend team
```

### Step 4: Create Handoff Document (30 minutes)

Compile into structured handoff:

```
HANDOFF DOCUMENT - Search and Discovery Initiative

Prepared By: alice@company.com (contractor)
Date: 2025-02-07
Duration: 3-month engagement
Next Owner: bob@company.com (continuing employee)

Executive Summary:
Search initiative 60% complete. MVP launched with 85% adoption.
Filtering and personalization phases planned for Q2.

Key Decisions Made:
1. Use Stripe for payments (DEC-20250106-001)
2. PostgreSQL for product data (DEC-20250110-002)
3. React + TanStack Query for frontend (DEC-20250115-003)

Team Patterns Discovered:
1. Edge cases need explicit checklist (30% of stories missing)
   → Add [Accessibility], [Error State], [Edge Case] to AC template

2. Large stories underestimate coordination (>5pts have 20% variance)
   → Add +1pt buffer for cross-team stories

3. Search latency is key metric (every 1s costs 5% conversion)
   → Prioritize performance work next

Tech Debt to Address:
1. Search API N+1 query (HIGH priority, 2-3pts)
2. Mobile responsive filters (MEDIUM priority, 5pts)
3. Search input a11y (MEDIUM priority, 2pts)

Stories in Flight:
- STORY-2025-0050: Phase 2 filtering (5pts, blocked by 0001, ~70% complete)
- STORY-2025-0051: Phase 3 personalization (8pts, needs splitting)

Recommendations for Next Owner:
1. Split STORY-2025-0051 into smaller stories (3pts + 5pts)
2. Add tech debt stories to Q2 backlog (5 total points)
3. Run a11y audit before Phase 2 launch (1 day effort)
4. Implement feature flag for gradual rollout (prevents regression)

Contacts and Resources:
- Design lead: carol@company.com (knows design system)
- Backend lead: dave@company.com (owns search API)
- QA lead: eve@company.com (has test scenarios)

Code Repositories:
- Frontend: github.com/company/product-web
- Backend: github.com/company/product-api
- Docs: docs.company.com/search-api

Key Metrics:
- Search adoption: 85% of sessions
- Search latency P90: 1.8 seconds
- Defect escape rate: 0% (no production bugs)
- User satisfaction: 4.2/5

Success Criteria for Phases:
- Phase 2 (Filtering): Q2 end with 60% filter adoption
- Phase 3 (Personalization): Q3 end with 30% recommendation adoption
```

### Step 5: Create Risk Handoff (15 minutes)

Alert next owner to risks:

```
RISKS FOR NEXT OWNER

Risk 1: Performance Regression
- Issue: Phase 2 filtering may slow down search
- Concern: If not optimized, could lose 5% conversion
- Mitigation: Load test with 1M+ products, implement caching
- Owner: Backend team

Risk 2: A11y Compliance Gap
- Issue: Current search UI not WCAG AA compliant
- Concern: May face accessibility audit failure
- Mitigation: Audit by Friday, fix critical issues before Phase 2
- Owner: Frontend team

Risk 3: Large Story (STORY-2025-0051)
- Issue: Personalization story is 8pts (should be 5-5 split)
- Concern: May not fit in sprint, estimate variance
- Mitigation: Split into smaller stories in refinement
- Owner: Product team

Risk 4: Unresolved Design Questions
- Issue: Phase 3 personalization UI not fully mocked
- Concern: May discover scope issues during dev
- Mitigation: Complete design review before Phase 3 sprint
- Owner: Design lead
```

### Step 6: Create Knowledge Base Entry (30 minutes)

Document learnings for future reference:

```
KNOWLEDGE BASE: Search Initiative Retrospective

What Worked Well:
1. Phase-based breakdown: Clear milestones enabled team alignment
2. Edge case discovery: [RECOMMENDED] tags helped prioritize risky ACs
3. Performance testing early: Caught N+1 query before Phase 1 launch
4. Cross-team coordination: Daily standups prevented rework

What Could Be Better:
1. Accessibility: Should have a11y expert earlier
2. Estimation: Large stories (5-8pts) still inaccurate by 20%
3. Dependency chains: Phase 1→2→3 was too linear, limited parallelization
4. Design review: Design finalizations blocked dev work

Key Learnings:
1. Search latency directly impacts conversion (every 1s = 5% loss)
2. Filter complexity grows exponentially (simple 3 filters become complex)
3. Edge case coverage prevents 90% of bugs (invest in ACs)
4. Performance is feature (users care more about speed than features)

Recommendations for Future Initiatives:
1. Require a11y expert in design phase (not retrofit later)
2. Implement estimation check: if >5pts, require split approval
3. Limit transitive dependency chains to 2 levels max
4. Complete design review before development starts

Team Skill Development:
- Alice: Learned PostgreSQL optimization, became expert on search API
- Bob: Improved estimation accuracy (went from 70% to 90%)
- Carol: Mastered component design patterns, mentored 2 designers
- Dave: Led successful multi-phase delivery, ready for larger initiatives
```

### Step 7: Schedule Overlap Period (1 week)

Plan transition:

```
Week 1 (Last week of current owner):
- Day 1: Handoff document review + Q&A
- Day 2-3: Walk through code, architecture, current issues
- Day 4: Pair programming on upcoming work
- Day 5: Next owner shadows ongoing standup, takes notes

Deliverables from Current Owner:
[ ] Handoff document signed and dated
[ ] Tech debt register created
[ ] All decision records up to date
[ ] Code documented (comments on complex logic)
[ ] Runbook for common tasks (deploy, rollback, debug)

Commitments from Next Owner:
[ ] Read handoff document (1 hour)
[ ] Review all decisions and patterns (2 hours)
[ ] Meet with stakeholders (design, backend, QA) (2 hours)
[ ] Create 90-day plan based on risks and recommendations
```

## Success Criteria

Offboarding complete when:
- All decisions documented in intelligence records
- Tech debt register created with priorities
- Handoff document delivered and reviewed
- Risks identified and mitigated plan created
- Next owner confident in continuing work
- Zero institutional knowledge lost
- Continuity uninterrupted (no velocity loss post-transition)
