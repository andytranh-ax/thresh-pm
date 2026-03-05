# Playbook: After Sync - Run Decision Candidates

Post-standup process to identify and capture important decisions from team discussions.

## When to Run

After team syncs/standups where decisions were made:
- Design sync
- Engineering standup
- Product sync
- Architecture review
- Sprint planning

## Time Budget

5-10 minutes depending on discussion complexity

## Step-by-Step Process

### Step 1: Review Last 24h Jira Comments (2 minutes)

```
Search Jira for recent activity:
1. Go to Jira
2. Search: assignee was updated before -1d
3. Review all comments added in last 24h
4. Look for decision keywords:
   - "We decided to..."
   - "We will..."
   - "Going forward, we're..."
   - "Chosen approach..."
   - "Alternative considered..."
```

### Step 2: Run Decision Candidate Detector (3 minutes)

Scan comments for decision signals:

```
For each comment, ask:
✓ Does it state a decision? (We will X, We decided to Y)
✓ Is it a new decision? (Not already recorded)
✓ Does it have rationale? (Why this was chosen)
✓ Does it affect multiple stories? (Impact scope)
✓ Did key stakeholders weigh in? (Decided by whom)

If YES to all: → Candidate for decision record

If some NO: → Note for clarification
```

### Step 3: Extract Decision Info (2 minutes)

For each candidate, gather:

```
Decision: "Use Stripe for payment processing"

From comment by: alice@company.com
Date: 2025-02-06
Source: JIRA-5423 Comment #42
Related stories: [STORY-2025-0100, STORY-2025-0101]
Confidence: High (well researched)
Alternatives considered: [Adyen, Braintree, Build in-house]
```

### Step 4: Present Findings to Team (2 minutes)

```
Slack post to #engineering:

"Decision Candidates from Today's Syncs:

1. Use Stripe for payments (confidence: HIGH)
   - Source: JIRA-5423 Comment #42
   - Decided by: alice@company.com
   - Affects: 3 stories in Checkout
   - Record this decision? [Yes/No]

2. API caching strategy (confidence: MEDIUM)
   - Source: Architecture sync notes
   - Decided by: bob@company.com
   - Affects: Backend infrastructure
   - Record this decision? [Yes/No]

Please confirm or ask for clarification."
```

### Step 5: Create Decision Records (3 minutes)

For approved decisions, create formal record:

```yaml
decision_id: DEC-20250206-001
date: 2025-02-06
source: JIRA-5423 Comment #42
decision_statement: We will use Stripe for payment processing.
alternatives_considered:
  - Use Adyen payment gateway
  - Build custom payment system
  - Use Braintree
rationale: |
  Stripe offers best integration options for international expansion.
  Adyen has higher costs. Building in-house delays launch by 4 weeks.
impact_scope:
  - STORY-2025-0100
  - STORY-2025-0101
  - STORY-2025-0102
decided_by: alice@company.com
confidence: High
status: Active
```

See intelligence_record_standard.md for full format.

### Step 6: Link to Affected Stories (1 minute)

```
In Jira, link decision to stories:

For each story in impact_scope:
  1. Open story
  2. Add comment: "Related to DEC-20250206-001 (Stripe payment choice)"
  3. Add link: relates to DEC-20250206-001

This enables tracing decisions back to implementation.
```

## Output Example

Decision candidates report:

```
After Sync Decision Candidates - 2025-02-06

Decisions Identified: 2
- Use Stripe for payments (APPROVED)
- Cache search results for 1 hour (PENDING CLARIFICATION)

Decisions Recorded: 1
- DEC-20250206-001: Stripe payment provider

Decisions Needing Clarification: 1
- Cache strategy: Need to confirm cache invalidation approach

Next Actions:
- Clarify cache strategy in tomorrow's sync
- Add DEC-20250206-001 to decision library
- Link Stripe decision to Checkout stories
```

## Quick Checklist

Before submitting decision record:
- [ ] Decision statement is clear
- [ ] At least 2 alternatives considered
- [ ] Rationale explains why chosen option is best
- [ ] Impact scope identified (which stories)
- [ ] Decided by field populated
- [ ] Confidence level is honest
- [ ] Source links back to discussion

## Common Decision Types

**Technical Decisions:**
- Architecture choices (Stripe, custom auth, caching strategy)
- Technology selections (React vs Vue, PostgreSQL vs MongoDB)
- Performance targets (< 2 second latency)

**Product Decisions:**
- Feature scope (include or exclude)
- Priority (which feature first)
- Timeline (launch date commitment)

**Process Decisions:**
- Code review requirements
- Testing standards
- Deployment process

**Not a Decision:**
- Status updates ("finished story X")
- Questions ("should we...?")
- General discussion without conclusion
