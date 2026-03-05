# Intelligence Record Standard

Framework for capturing and tracking product decisions, insights, and organizational knowledge.

## Two Record Types

### 1. Decision Records (DEC-*)
Significant decisions made during product development. Used for decisions that affect implementation, strategy, or team alignment.

### 2. Insight Records (INS-*)
Patterns, learnings, and non-decision intelligence. Used for observations, risks, and recommendations that don't constitute formal decisions.

## Decision Record Format

### Required Fields

**decision_id** (required, string)
- Format: `DEC-YYYYMMDD-NNN`
- Example: `DEC-20250206-001`
- Rules: Auto-generate with date and sequence number
- Uniqueness: Must be unique

**date** (required, ISO date)
- Format: YYYY-MM-DD
- Description: Date decision was made
- Example: `2025-02-06`

**source** (required, string)
- Format: Jira issue key + comment link or meeting notes reference
- Example: `JIRA-5423 Comment #42` or `Confluence: Design Sync Feb 6`
- Description: Where the decision originated
- Rule: Always link back to source

**decision_statement** (required, string, concise)
- Max 1-2 sentences
- Description: The decision itself, clearly stated
- Example: "We will use Stripe for payment processing instead of building in-house."
- Rules: Start with "We will..." or "The team decided to..."

**alternatives_considered** (required, array)
- Format: List of alternatives evaluated
- Example:
  - "Use Adyen instead of Stripe"
  - "Build custom payment system"
  - "Use Braintree"
- Rules: Include at least 2 alternatives

**rationale** (required, string)
- Length: 3-5 sentences
- Description: Why this decision was made
- Example: "Stripe provides the most comprehensive payment integrations with the lowest lift for international expansion. Adyen has higher costs. Building in-house would delay launch by 4 weeks."
- Rule: Must be specific; no vague justifications

**impact_scope** (required, array of story IDs)
- Format: List of stories affected by this decision
- Example: `[STORY-2025-0100, STORY-2025-0101, STORY-2025-0102]`
- Rule: Must include at least one affected story
- Use case: Enables impact analysis and traceability

**decided_by** (required, email)
- Format: email@company.com
- Example: `pm@company.com`
- Description: Team member who made final call
- Rule: Must be a real person (not a role)

**confidence** (required, enum)
- Options: High, Medium, Low
- Description: How confident is the team in this decision?
- Rules:
  - High: Evidence-based, well-researched, low risk of reversal
  - Medium: Reasonable but some unknowns; may need revisit
  - Low: Exploratory; expect to change; high uncertainty
- Example: `Medium`

**status** (optional, enum)
- Options: Active, Superseded, Revoked
- Default: Active
- Description: Current state of the decision
- Examples:
  - Active: Currently in effect
  - Superseded: Replaced by DEC-20250210-003
  - Revoked: No longer applies
- Rule: Track decision lifecycle

**notes** (optional, string)
- Description: Additional context or follow-up items
- Example: "Revisit payment provider in Q2 based on volume and costs."

## Decision Record Example

```yaml
decision_id: DEC-20250206-001
date: 2025-02-06
source: JIRA-5423 Comment #42
decision_statement: We will use Stripe for payment processing instead of building in-house or using alternative providers.
alternatives_considered:
  - Use Adyen payment gateway
  - Build custom payment system in-house
  - Integrate Braintree
rationale: |
  Stripe offers the most comprehensive payment integrations with strong support for international expansion, 
  which is critical for Q2 growth. Adyen has higher per-transaction costs. Building in-house would delay 
  launch by 4 weeks and introduce operational risk. Stripe has the best developer experience and 
  documentation for our tech stack.
impact_scope:
  - STORY-2025-0100
  - STORY-2025-0101
  - STORY-2025-0102
  - EPIC-CHECKOUT
decided_by: alice@company.com
confidence: High
status: Active
notes: |
  - Setup Stripe account in production by Feb 15
  - Revisit payment provider in Q2 based on transaction volume and costs
  - Document Stripe integration patterns for team reuse
```

## Insight Record Format

Insight records capture patterns and learnings without formal decision status.

### Required Fields

**insight_id** (required, string)
- Format: `INS-YYYYMMDD-NNN`
- Example: `INS-20250206-001`

**date** (required, ISO date)
- Format: YYYY-MM-DD

**category** (required, enum)
- Options: pattern, risk, recommendation, learning, constraint
- Description: Type of insight

**description** (required, string)
- Max 2-3 sentences
- Example: "Users abandon search after 3 seconds if results don't load. Latency > 3s correlates with 40% abandonment rate."

**source** (required, string)
- Example: "Analytics: Search funnel Q1 2025" or "User testing session Feb 4"

**related_stories** (optional, array of story IDs)
- Example: `[STORY-2025-0001, STORY-2025-0002]`

**impact** (optional, string)
- Description: Potential impact if acted upon or ignored
- Example: "Search performance optimization could increase conversion by 3-5%"

**created_by** (required, email)
- Format: email@company.com

### Insight Record Example

```yaml
insight_id: INS-20250206-001
date: 2025-02-06
category: pattern
description: |
  Users abandon search after 3 seconds if results don't appear. Analytics show 40% abandonment 
  rate for queries with latency > 3 seconds. This is our primary churn point in search funnel.
source: Analytics - Search Funnel Q1 2025
related_stories:
  - STORY-2025-0001  # Search feature
  - STORY-2025-0005  # Performance optimization
impact: Optimizing search latency could increase conversion by 3-5% based on similar products.
created_by: analytics@company.com
```

## Provenance and Traceability

All records must include:
1. **Source link**: Reference to where decision originated (Jira, meeting, Slack, email)
2. **Owner**: Person responsible for implementing or communicating decision
3. **Impact scope**: Stories and systems affected
4. **Revision history**: Date and reason for status changes

## Decision Record Checklist

Before publishing a decision record:
- [ ] decision_id is unique
- [ ] source links back to original discussion
- [ ] decision_statement is clear and specific
- [ ] at least 2 alternatives considered
- [ ] rationale explains why chosen option was best
- [ ] confidence level is honest (not artificially High)
- [ ] impact_scope includes at least one story
- [ ] decided_by is a real person
- [ ] shared with affected teams

## Accessing Intelligence

Decisions and insights are searchable by:
- Date range
- Category (pattern, risk, etc.)
- Related stories
- Confidence level
- Status (Active, Superseded, Revoked)

Use intelligence to:
- Prevent duplicate decisions
- Track decision reversals
- Understand feature constraints
- Manage organizational risk
- Build team knowledge base
