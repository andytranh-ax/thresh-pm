# Offboard Intelligence Synthesizer Agent

## Purpose
When an engagement ends or major phase completes, synthesize all accumulated intelligence into a knowledge transfer document that preserves critical context for successors.

---

## Trigger Conditions

Agent activates when:
1. **Engagement Ending**: Last sprint complete, team member leaving, project concluding
2. **Major Phase Complete**: Major feature shipped, architecture milestone reached
3. **Explicit Request**: PM or team lead requests knowledge transfer document
4. **Handoff to New Team**: Work moving to different team or external partner

---

## Data Collection Process

### Step 1: Gather Decision History
- Scan `product/context/product_decisions/` for all decisions made during engagement
- Extract key decision records (DEC-XXXX files)
- Organize by category: Architecture, Features, Process, Team Structure, Risk Management
- Include: decision date, decision maker, rationale, outcomes, follow-up decisions

### Step 2: Analyze Team Patterns
- Extract from `product/metrics/team_patterns.md`:
  - Developer expertise map (who knows what)
  - Performance metrics (velocity trends, defect rates)
  - Historical sprint patterns
  - Known bottlenecks and blockers
  - Growth areas and skill gaps
  - Bus factor analysis (knowledge concentration)

### Step 3: Scan Sprint History
- Collect metrics from last 6 sprints:
  - Planned vs delivered points
  - Carry-over patterns
  - Velocity trend (increasing/stable/declining)
  - Defect rates
  - Unplanned work percentage
  - Key blockers and root causes

### Step 4: Technical Debt Inventory
Query codebase and issue tracker for:
- TECH-DEBT tagged stories (open or deferred)
- Known bugs that aren't critical (backlog)
- Deprecated code that needs refactoring
- Test coverage gaps
- Performance optimization opportunities
- Security debt or temporary fixes

### Step 5: Context and Product Files
Extract key info from:
- `product/context/CLAUDE.md` - Product vision, sprint goals, team structure
- `product/context/product_vision.md` - Strategic direction, roadmap
- `product/context/ui_registry.md` - Component library state
- Jira custom fields and workflow state

### Step 6: Unresolved Questions
Search all decision records, stories, and comments for:
- Open questions marked with "?" or "QUESTION:"
- Stories blocked with no clear resolution
- Design questions pending review
- Architecture decisions left undecided
- Known risks with no mitigation plan

---

## Output: Knowledge Transfer Document

Create comprehensive document at `product/context/OFFBOARD-[DATE].md`:

```markdown
# Knowledge Transfer: [Project/Phase] - Offboarded [DATE]

## Executive Summary
[1-2 paragraph overview of phase/engagement, key accomplishments, current status]

---

## Section 1: Critical Decisions Made

### Architecture Decisions
| Decision | Date | Made By | Rationale | Status |
|----------|------|---------|-----------|--------|
| Migrate to PostgreSQL | 2025-01-15 | Alice Chen | Performance improvement | Implemented |
| OAuth2 for authentication | 2025-02-01 | Bob Smith | Enterprise customer requirement | In Progress |
| Microservices approach | 2024-12-10 | Carol White | Scalability, team autonomy | Approved, Q2 rollout |

### Feature Decisions
| Feature | Decision | Date | Status |
|---------|----------|------|--------|
| Mobile App | Build native iOS/Android | 2025-01-05 | Shipped v1 |
| Dark Mode | Phase 2, after core features | 2025-01-20 | Backlog |
| Analytics | Segment integration | 2025-02-01 | In Progress |

### Process Decisions
| Process | Decision | Impact |
|---------|----------|--------|
| Code Review | Require 2+ approvals | Improved quality, +30% PR time |
| Testing | Automated E2E for critical paths | Reduced defect escape rate |
| Deployments | Feature flags for safe rollout | Enabled faster iteration |

---

## Section 2: Team Intelligence

### Developer Expertise Map

#### Alice Chen (Engineering Lead)
- **Expertise**: Backend systems, database optimization, architecture decisions
- **Confidence Level**: Expert
- **Recent Projects**: Authentication migration, database tuning
- **Mentor To**: Bob, Carol (junior devs)
- **Go-To For**: Scaling issues, API design, architecture questions
- **Growth Areas**: Frontend work (opportunity for stretch assignment)

#### Bob Smith (Full-Stack Developer)
- **Expertise**: React frontend, API integration, mobile features
- **Confidence Level**: Advanced
- **Recent Projects**: Mobile UI redesign, OAuth2 integration
- **Mentor To**: David (intern)
- **Go-To For**: Frontend bugs, React patterns, UI performance
- **Growth Areas**: DevOps, infrastructure (willing to learn)

#### Carol White (QA Lead)
- **Expertise**: Test automation, E2E testing, security testing
- **Confidence Level**: Advanced
- **Recent Projects**: Mobile test automation, API contract testing
- **Go-To For**: Test strategy, critical path verification
- **Growth Areas**: Performance testing, load testing

#### David Park (Junior Developer)
- **Expertise**: Coding fundamentals, learning React, documentation
- **Confidence Level**: Intermediate
- **Recent Projects**: Bug fixes, UI polish, documentation
- **Mentor To**: None yet
- **Go-To For**: Help with recent code, implementation questions
- **Growth Areas**: Full-stack work, architectural thinking (early career)

### Team Metrics (Last 6 Sprints)
| Sprint | Planned | Delivered | Carry-Over | Velocity | Defects | Notes |
|--------|---------|-----------|-----------|----------|---------|-------|
| S23 | 40 | 38 | 2 | 38 | 2 | Alice on PTO |
| S24 | 45 | 42 | 3 | 42 | 3 | Normal flow |
| S25 | 50 | 48 | 2 | 48 | 2 | Good sprint |
| S26 | 40 | 38 | 2 | 38 | 4 | OAuth2 complexity |
| S27 | 45 | 44 | 1 | 44 | 2 | Mobile launch prep |
| S28 | 50 | 46 | 4 | 46 | 3 | Unexpected bugs |

**Velocity Trend**: Stable at 40-48 pts/sprint (healthy)
**Defect Rate**: ~3% (good), spike in S26 due to OAuth2 complexity
**Carry-Over Rate**: ~4% (low - good), except S28 (investigate)

### Critical Skills and Bus Factor

**Bus Factor Analysis** (number of people who can do the work):
- **Backend architecture**: Only Alice (BUS FACTOR: 1 - RISK) → Bob should shadow
- **Mobile native**: Only Bob (BUS FACTOR: 1 - RISK) → Pair Carol on next mobile feature
- **Test automation**: Carol + Bob (BUS FACTOR: 2 - OK)
- **Frontend**: Bob + David (BUS FACTOR: 2 - OK)
- **Database**: Alice + external consultant (BUS FACTOR: 2 - OK)

**Recommendations**:
1. Pair Alice with Bob on next architecture decision
2. Have Bob mentor David on React patterns (transfer knowledge)
3. Include Carol in mobile app testing to reduce Bob's solo dependency
4. Schedule Alice to teach team about backend architecture (brown bag)

### Known Bottlenecks
1. **Deployment**: Carol is only person comfortable with prod deployments
   - Impact: Deployments delayed if Carol unavailable
   - Recommendation: Train Bob or Alice on deployment process

2. **Database Optimization**: Alice is sole expert
   - Impact: Query tuning work blocked without Alice
   - Recommendation: Document common optimization patterns

3. **Authentication**: Currently mid-migration from sessions to OAuth2
   - Impact: New features need coordination with auth work
   - Recommendation: Use feature flags to decouple

---

## Section 3: Technical Debt Inventory

### High Priority (Address Next Sprint)
- [ ] **Legacy API endpoints**: 5 endpoints still using old session auth (should deprecate)
  - Effort: 3 points
  - Impact: Blocks new clients, security risk if exposed
  - Owner: Alice

- [ ] **Test coverage gaps**: Mobile app at 62% coverage (target: 80%)
  - Effort: 5 points
  - Impact: Missing regression coverage, risky refactoring
  - Owner: Carol

- [ ] **Database indexing**: Certain queries still slow despite migration
  - Effort: 2 points
  - Impact: User experience, performance
  - Owner: Alice

### Medium Priority (Next 2-3 Sprints)
- [ ] **Refactor React component library**: Multiple similar components, should consolidate
  - Effort: 8 points
  - Impact: Maintenance burden, inconsistency
  - Owner: Bob

- [ ] **Upgrade Node.js**: Currently on v18, v20 has improvements
  - Effort: 3 points
  - Impact: Security patches, performance
  - Owner: Alice (with Bob)

- [ ] **API documentation**: OpenAPI spec outdated
  - Effort: 4 points
  - Impact: Integration friction, onboarding delays
  - Owner: Bob or David

### Low Priority (Backlog)
- [ ] Migrate from Webpack to Vite (performance improvement)
- [ ] Add dark mode (feature, not technical debt)
- [ ] Refactor logging system (works, but improvements possible)

---

## Section 4: Unresolved Questions and Blockers

### Open Architectural Questions
1. **Caching Strategy**: Should we add Redis? Trade-offs: complexity vs latency
   - Status: Approved in principle, waiting for scale testing results
   - Next Step: Run load test in S29

2. **GraphQL Adoption**: Should we migrate from REST to GraphQL?
   - Status: Ongoing debate, Bob pro, Alice cautious
   - Next Step: POC in spike story

### Blocked Stories
1. **PROJ-450**: "Implement real-time notifications" 
   - Blocked by: Database migration completion (PROJ-405)
   - Expected unblock: 2025-02-28
   - Owner: Bob

2. **PROJ-520**: "Mobile analytics v2"
   - Blocked by: API design decision (waiting PM approval)
   - Expected unblock: Unknown
   - Owner: David

### Design Decisions Pending
1. **API Rate Limiting**: What limits should we set for mobile? (prevent DOS)
   - Status: Proposed: 1000 req/min per user
   - Waiting: Alice's review
   - Impact: Affects mobile app UX

2. **Error Message Strategy**: Should errors include error codes or user-friendly messages?
   - Status: Debated in PROJ-380 comments
   - Consensus: Both (codes for logs, user-friendly for UI)
   - Action: Update API design doc

---

## Section 5: Sprint Health & Patterns

### Velocity Trend
Stable between 38-48 points/sprint. No concerning trend.
- **Prediction for next sprint**: 45 points (conservative estimate)
- **Confidence**: High (based on 6 sprint history)

### Common Blockers (Rank Ordered)
1. **Waiting for design** (13 instances) - Affects frontend stories
2. **Database schema not finalized** (8 instances) - Blocks backend work
3. **External API documentation unclear** (6 instances) - Blocks integrations
4. **Missing test data** (5 instances) - Delays QA

### Recommendations
1. Implement design review SLA (24 hours)
2. Finalize database schema before sprint starts
3. Request clearer API docs from external partners, or add spike story
4. Generate/mock test data early in sprint

---

## Section 6: Known Risks and Mitigations

| Risk | Probability | Impact | Current Mitigation | Additional Actions |
|------|-------------|--------|-------------------|-------------------|
| Alice leaves | Low | Critical (architecture knowledge) | Bob shadowing | Document architecture decisions |
| OAuth2 migration fails | Medium | High (blocking work) | Feature flag approach | Have rollback plan |
| Mobile app performance | Medium | Medium (user experience) | Monitoring in place | Load test in S29 |
| Database corruption | Low | Critical (data loss) | Backups daily | Test restore procedure |
| Key integration fails | Low | High (user signup) | Third-party monitoring | Have manual fallback |

---

## Section 7: Recommended Next Steps

### For Successor Team (Immediate - Week 1)
1. Read this document and CLAUDE.md
2. Schedule 1:1s with each team member (learn their context)
3. Review recent decision records (understand why things are as they are)
4. Identify 2 people to shadow for each critical area
5. Run through deployment checklist (understand process)

### For Team (Next Sprint)
1. Address high-priority technical debt (3 items listed in Section 3)
2. Unblock PROJ-450 by completing database migration
3. Schedule Alice to document backend architecture
4. Run load test to validate caching strategy decision

### For Product (Next Phase)
1. Complete OAuth2 migration (currently 80% done)
2. Achieve 80% test coverage for mobile app
3. Train second person on deployment process
4. Consolidate React component library (architectural improvement)

---

## Section 8: Key Contacts and Knowledge Holders

| Area | Primary | Secondary | Tertiary |
|------|---------|-----------|----------|
| Backend/Architecture | Alice Chen | Bob Smith | External consultant |
| Frontend/React | Bob Smith | David Park | - |
| Mobile | Bob Smith | Carol White | - |
| Testing/QA | Carol White | Bob Smith | - |
| DevOps/Deployment | Carol White | Alice Chen | - |
| Database | Alice Chen | External consultant | - |
| Product Vision | PM (unavailable now) | Alice Chen | - |

---

## Appendix: Document References

- Decision Records: `product/context/product_decisions/`
- Team Patterns: `product/metrics/team_patterns.md`
- Product Vision: `product/context/product_vision.md`
- Current Sprint: `product/context/CLAUDE.md`
- UI Registry: `product/context/ui_registry.md`
- Jira Project: [link to Jira]
- Figma Design System: [link to Figma]

---

**Document Created**: [DATE]
**Phase/Engagement**: [PROJECT NAME]
**Period**: [START DATE] to [END DATE]
**Prepared By**: Thresh Intelligence System
**Last Updated**: [DATE]
```

---

## Integration Points

Output document becomes reference source for:
1. New team members onboarding
2. Future phase planning
3. Risk assessment for similar work
4. Historical pattern analysis
5. Knowledge gap identification
