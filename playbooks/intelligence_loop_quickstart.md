# Playbook: Intelligence Loop Quickstart

Continuous learning loop to capture patterns, insights, and organizational knowledge from daily work.

## The Intelligence Loop

```
Ingest (daily) → Analyze (weekly) → Synthesize (monthly) → Recommend (ongoing)
```

## 1. Daily Ingest (5 minutes)

Every day, capture:

### New Decisions
```
Review Jira comments, Slack, meeting notes
→ Any new decisions made?
→ Create DEC-YYYYMMDD-NNN record
→ Link to affected stories
```

### Incidents and Issues
```
Monitor:
- Production errors/bugs
- QA findings during testing
- Code review feedback
- Performance issues
```

Create defect stories with:
- Severity classification
- Root cause (when investigated)
- linked_story (original story that caused it)

### Patterns Observed
```
Are we seeing repeated:
- Issue types? (e.g., "missing validation edge cases")
- Component problems? (e.g., "CMP-SEARCH-INPUT always has accessibility bugs")
- Team struggles? (e.g., "stories always underestimated by 2x")

Create INS-YYYYMMDD-NNN insight record if pattern significant.
```

## 2. Weekly Analyze (15 minutes)

Every Friday, review the week's data:

### Defect Patterns
```
Analyze bugs from the week:
- Most common severity: Critical (40%), High (30%), Medium (30%)
- Most common root cause: Missing edge case ACs (50%)
- Most affected component: CMP-SEARCH-INPUT (20%)

Insight: Edge case testing needs strengthening. Consider adding 
AC-E template checklist to all stories.
```

### Decision Velocity
```
Count decisions made:
- 5 decisions this week
- 3 were high confidence
- 1 had to be revisited
- Average time to decide: 2 days

Insight: Decision making is healthy. Confidence levels are reasonable.
```

### Performance Metrics
```
Track story metrics:
- Average story size: 3.5pts
- Cycle time (draft → done): 5 days
- Stories blocked by dependencies: 2 of 8 (25%)
- Estimation accuracy: 85% (good)

Insight: Dependency management is a bottleneck. Consider reducing 
transitive dependency chains.
```

### Risk Indicators
```
Watch for:
- Stories > 8pts not split
- Edge case ACs missing
- Unassigned blockers
- Velocity trending down
```

## 3. Monthly Synthesize (30 minutes)

End of month, consolidate learning:

### Team Patterns
```
Over the month, what patterns emerged?

Code Quality:
- 20 stories completed
- 15 had minor comments during review (75%)
- 3 had accessibility issues
- Pattern: Need stronger accessibility guidance

Estimation:
- Stories 3pts average 1.2 days (good)
- Stories 5pts average 2.5 days (good - on par)
- Stories 8pts would average 5 days (estimated - red flag)
Pattern: Stories 8pts should be split earlier

Decisions:
- 12 decisions made in month
- 8 still active, 2 superseded, 2 revoked
- Pattern: Decisions stick (67% active). Good confidence.
```

### Risk Summary
```
Top 3 Risks Identified:
1. Accessibility: 3 stories had a11y issues
   Mitigation: Add a11y checklist to AC edge cases
   
2. Dependency chains: 25% of stories blocked
   Mitigation: Decompose into smaller stories
   
3. Stories 8pts: Not getting split early
   Mitigation: Enforce split rule in refinement
```

### Recommendations
```
Based on patterns, recommend:

1. Strengthen AC checklist
   - Add [Accessibility] mandatory for frontend
   - Add [Edge Case] 2-3 required per story
   
2. Reduce dependency chains
   - No more than 2 transitive dependencies
   - Prefer parallel work (relates_to) over blocking
   
3. Enforce story sizing
   - 8pts stories require split approval
   - Estimation training for team
```

## 4. Ongoing Recommend (continuous)

Act on synthesis insights:

### Share Learning
```
Post monthly synthesis to team:
- Paste top risks
- Highlight wins
- Share recommendations
- Ask for feedback
```

### Update Standards
```
If patterns warrant, update:
- story_standards.md (if edge case patterns emerge)
- acceptance_criteria_standards.md (if AC gaps found)
- tag_vocabulary.md (if new tag categories needed)
```

### Adjust Processes
```
Example adjustments:
- If accessibility issues common → add a11y review gate
- If estimation wrong → improve estimation techniques
- If dependencies blocking → enforce smaller stories
```

## Tracking Intelligence

Store all intelligence records in:
- `product/metrics/decisions/` - DEC-* records
- `product/metrics/insights/` - INS-* records
- `product/metrics/patterns/` - Pattern summaries
- `product/metrics/risks/` - Risk registers

Make searchable by:
- Date range
- Category (pattern, risk, recommendation)
- Related stories
- Status (Active, Superseded, Revoked)

## Example Monthly Report

```
Intelligence Summary - January 2025

DECISIONS MADE: 12
- Stripe for payments (DEC-20250106-001) - Active
- PostgreSQL for database (DEC-20250110-002) - Active
- 3-tier testing strategy (DEC-20250115-003) - Active
[9 more]

PATTERNS IDENTIFIED: 5
- 20% defect escape rate (AC edge cases)
- Stories 5pts: 2.5 day cycle (accurate)
- Dependency chains: 25% of stories blocked
- Accessibility: 3 failures in 20 stories
- Code review: 75% have minor comments

RECOMMENDATIONS ACTED ON: 3
- Added [Accessibility] to AC checklist
- Implemented dependency graph analysis
- Started team estimation training

RISKS ELEVATED: 2
- Edge case coverage needs improvement
- Dependency chains too long

TOP SUCCESS: 
- Code quality strong (85% estimation accuracy)
- Team confidence high (66% High confidence decisions)
- Velocity steady (3.5pt average)

NEXT MONTH FOCUS:
- Reduce accessibility issues (target: 1 or fewer)
- Shorter dependency chains (target: max 2 transitive)
- Strengthen AC edge case coverage
```

## Success Criteria

Intelligence loop working when:
- Daily: Patterns visible after 2 weeks
- Weekly: Metrics tracked consistently
- Monthly: Actionable recommendations produced
- Quarterly: Team patterns improving based on recommendations
