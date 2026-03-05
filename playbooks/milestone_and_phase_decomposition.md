# Playbook: Milestone and Phase Decomposition

Break large multi-month initiatives into phases with clear gates and checkpoints.

## When to Use

Use this playbook for:
- Q1/Q2/Q3 initiatives (multi-sprint work)
- Major feature launches
- Cross-team projects
- Strategic bets

Do NOT use for: Single sprint features (use story breakdown instead).

## Step-by-Step Process

### Step 1: Define Initiative Scope (30 minutes)

Start with the big initiative:

```
Initiative: Product Search and Discovery

Vision: Enable users to quickly find products through search, 
filters, and personalized recommendations.

User Outcomes:
- Find products 10x faster than browsing categories
- Refine results with intelligent filters
- See relevant recommendations

Business Goals:
- Increase conversion by 15% (bounce rate reduction)
- Reduce average time-to-product from 5 min to 1 min
- Support 100k+ monthly search queries

Timeline: 12 weeks (3 phases)
Teams: Frontend (2), Backend (2), Design (1), QA (1)
```

### Step 2: Break Into Phases (30 minutes)

Divide large initiative into 3-4 phases:

```
Phase 1: MVP Search (Weeks 1-4)
Goal: Enable basic search functionality
Milestone: Users can search and see results

Phase 2: Filtering (Weeks 5-8)
Goal: Add category, price, rating filters
Milestone: Users can refine results

Phase 3: Personalization (Weeks 9-12)
Goal: Add recommendations and saved searches
Milestone: Personalized experience
```

Each phase:
- Self-contained (can be deployed independently)
- Has clear entry/exit criteria
- Takes 3-4 weeks max
- Has clear success metrics

### Step 3: Map Epics to Phases (20 minutes)

Link work items to phases:

```
Phase 1 Epics:
- EPIC-SEARCH-CORE: Core search UI and API
  - STORY-2025-0001: Search input component
  - STORY-2025-0002: Results display
  - STORY-2025-0003: Search API integration
  - STORY-2025-0004: Loading and error states
  
- EPIC-SEARCH-QUALITY: Testing and optimization
  - STORY-2025-0005: Performance testing
  - STORY-2025-0006: Accessibility audit

Phase 2 Epics:
- EPIC-FILTERS: Filtering and refinement
  - STORY-2025-0010: Category filter
  - STORY-2025-0011: Price range filter
  - STORY-2025-0012: Filter state management

[Phase 3...]
```

### Step 4: Define Phase Gates (15 minutes)

For each phase, define entry and exit criteria:

```
Phase 1 Gate:

Entry Criteria:
- ✓ Design complete for Phase 1 screens
- ✓ API contract defined with Backend team
- ✓ Stories estimated and assigned
- ✓ QA plan in place

Exit Criteria (Definition of Done):
- ✓ All Phase 1 stories marked Done
- ✓ Search results return in < 2 sec (90th percentile)
- ✓ Accessibility: WCAG AA passed
- ✓ QA: All functional tests passing
- ✓ Performance: 99% uptime during testing
- ✓ Design: Pixel-perfect match to Figma
- ✓ Security: No vulnerabilities (security audit)
- ✓ Analytics: Tracking configured
```

### Step 5: Establish Rollback Plan (10 minutes)

For each phase, plan how to revert if needed:

```
Phase 1 Rollback:
- If search results > 3 sec latency: Disable search, revert to category browse
- If security issue found: Hot-fix or rollback to previous version
- If 404 spike: Check API health, rollback if needed
- Communication: Notify users, provide ETA for fix

Rollback checklist:
- [ ] Database migrations reversible
- [ ] Feature flags implemented (can disable)
- [ ] Monitoring alerts configured
- [ ] On-call rotation for phase
- [ ] Runbook documented
```

### Step 6: Set Success Metrics (15 minutes)

Define how you'll measure each phase's success:

```
Phase 1: MVP Search
Metric: Search completion rate
- Baseline: 0% (new feature)
- Target: 80% of sessions use search at least once
- Measurement: Analytics event "search_submitted"

Metric: Search latency
- Target: P90 < 2 seconds
- Measurement: Server-side timing logs

Metric: Zero critical bugs
- Target: 0 severity:critical defects in production
- Measurement: Error tracking (Sentry)

Phase 2: Filtering
Metric: Filter adoption rate
- Target: 60% of search results use filters
- Measurement: Analytics event "filter_applied"

Metric: Result narrowing
- Target: Avg 20 results on first page (vs 100 unfiltered)
- Measurement: Results per page analytics
```

### Step 7: Create Phase Timeline (20 minutes)

Build Gantt-style view:

```
Week 1-4 (Phase 1):
- Sprint 1 (Week 1-2): Core search UI + API
- Sprint 2 (Week 3-4): Quality + Testing

Week 5-8 (Phase 2):
- Sprint 3 (Week 5-6): Filtering implementation
- Sprint 4 (Week 7-8): Filter integration + Testing

Week 9-12 (Phase 3):
- Sprint 5 (Week 9-10): Recommendations
- Sprint 6 (Week 11-12): Polish + Launch prep

Critical Path:
- Phase 1 Completion: Week 4 (needed before Phase 2 can start)
- Phase 2 Completion: Week 8 (needed before Phase 3 can start)
- Phase 3 Completion: Week 12 (launch ready)
```

### Step 8: Risk Register (10 minutes)

Identify risks by phase:

```
Phase 1 Risks:
- Search API performance: Concern if > 2 sec
  Mitigation: Load testing week 2, caching strategy
  Owner: Backend lead
  
- Accessibility issues: Unknown until testing
  Mitigation: Early a11y audit week 2
  Owner: QA lead

Phase 2 Risks:
- Filter complexity: Too many filter combinations
  Mitigation: User research on common filters
  Owner: Product

Phase 3 Risks:
- ML model training: Recommendations need data
  Mitigation: Phase 1 & 2 collect search data
  Owner: Data team
```

### Step 9: Communication Plan (5 minutes)

How you'll keep stakeholders informed:

```
Weekly (Every Monday):
- Phase progress update to leadership
- Metrics dashboard review
- Risk status

At Each Phase Gate:
- Go/No-go decision meeting
- Stakeholder sign-off
- Decision record created

Monthly:
- Full team retrospective
- Lessons learned synthesis
- Adjust Phase 2 or 3 based on learning
```

## Phase Gate Decision

At each phase completion:

```
Decision Template:

Phase 1 Completion (End of Week 4)

Exit Criteria Status:
- ✓ All stories done
- ✓ Latency target met
- ✓ Zero critical bugs
- ✓ Accessibility passed
- ✓ Design review passed

Decision: GO to Phase 2 ✓

If any criteria not met:
- Issue: Search latency 3.5 sec (target 2 sec)
- Options: 
  a) Optimize (delay Phase 2 by 1 week)
  b) Accept slower launch (proceed with 3.5 sec)
  c) Reduce feature scope
  
Decided: Option A - Optimize for 1 week
Next Gate: Phase 1 re-assessment in 1 week
```

## Phase Completion Report

At each phase gate, document:

```
PHASE 1 COMPLETION REPORT
Date: 2025-03-07
Duration: 4 weeks

Goals Achieved:
- ✓ Search results returned in < 2 sec
- ✓ 85% user adoption (target 80%)
- ✓ WCAG AA accessibility passed
- ✓ Zero critical bugs in production

Metrics:
- Search success rate: 85%
- Average latency: 1.8 sec
- Defect escape rate: 0%
- User satisfaction: 4.2/5

Lessons Learned:
- Caching reduced latency by 40%
- Accessibility fixes early prevented later issues
- Team velocity: 15pts/week (good)

Items Carrying Over to Phase 2:
- Refinement of filter UI based on user feedback
- Performance monitoring dashboard

Decision: GO to Phase 2
Authorized by: [PM name]
Date: 2025-03-07
```

## Success Criteria

Decomposition complete when:
- Each phase self-contained and independently valuable
- 3-4 phases, 3-4 weeks each
- Clear entry and exit criteria for each phase
- Success metrics defined
- Timeline realistic and achievable
- Risk register complete
- Team alignment and sign-off
