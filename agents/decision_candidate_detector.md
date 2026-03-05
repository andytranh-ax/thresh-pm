# Decision Candidate Detector Agent

## Purpose
Automatically identify critical decisions made in Jira comments, design docs, and discussions, then capture them as formal decision records for historical tracking and knowledge management.

---

## Decision Trigger Patterns

### High-Confidence Triggers (Explicit Decision Language)

Search for exact phrases in comment text:

- "**decided** to [action]" - "We decided to use GraphQL"
- "**agreed** [action]" - "We agreed on a microservices approach"
- "**approved** [subject]" - "Design approved for production"
- "**go with** [option]" - "Let's go with PostgreSQL"
- "**let's do** [action]" - "Let's do a gradual rollout"
- "**final answer** is [decision]" - "Final answer: we're shipping this in v2.0"
- "**confirmed** [decision]" - "Confirmed: auth will use OAuth2"
- "**signed off** on [subject]" - "Signed off on the API design"
- "**green light** for [action]" - "Green light for mobile rewrite"
- "**thumbs up**" - When explicit decision follows context

### Medium-Confidence Triggers (Decision Language Without Named Authority)

- "we've decided [action]" - implicit group decision
- "the decision is [action]" - formal but no person named
- "decided against [alternative]" - explicit rejection
- "chose [option] over [alternative]" - clear selection
- "will go with [option]" - future tense commitment

### Low-Confidence Triggers (Implied Decisions from Status Change)

- Story status moves to: In Progress → might indicate decision to start work
- Story status moves to: Closed/Done → decision to ship/complete
- Pull request status: Merged → decision to accept code
- Epic status: Started → decision to begin epic work

---

## JQL Query Template for Automated Scanning

```jql
(
  text ~ "decided to"
  OR text ~ "agreed"
  OR text ~ "approved"
  OR text ~ "go with"
  OR text ~ "let's do"
  OR text ~ "final answer"
  OR text ~ "confirmed"
  OR text ~ "signed off"
  OR text ~ "green light"
  OR text ~ "thumbs up"
)
AND updated >= -14d
ORDER BY updated DESC
```

Apply to comments on: PROJ in (relevant projects) where PROJ = project key.

---

## Confidence Scoring

### High Confidence (Score 85-100)
- Explicit decision trigger phrase + Named person + Named decision + Timestamp present
- Example: "Alice: We decided to migrate to Postgres for performance. Approved 2025-01-15."
- Action: Capture as formal decision record immediately

### Medium Confidence (Score 60-84)
- Decision trigger phrase + Clear decision statement, but no named person OR no timestamp
- Example: "We decided to use gRPC for internal services" (no person named)
- Action: Capture decision, flag for confirmation comment requesting decision author

### Low Confidence (Score 30-59)
- Implied decision from status change or vague language
- Example: Story moved to "In Progress" = decision to start
- Action: Flag for manual review, low priority capture

### No Confidence (Score 0-29)
- Generic language, no decision pattern matched
- Example: "We should probably think about authentication" (not a decision)
- Action: Ignore

---

## Cross-Reference Logic

Before capturing decision, check:

1. **Existing Decisions**: Query `product/context/product_decisions/` directory for same decision already recorded
   - If identical decision exists with same date/person → deduplicate
   - If conflicting decision exists → flag for conflict resolution

2. **Product Context**: Check `product/context/product_vision.md` and `product/context/CLAUDE.md`
   - Does decision align with product strategy?
   - Does decision contradict sprint goal?
   - Flag any misalignment for product manager attention

3. **Related Stories**: Check Jira stories referencing the decision
   - Link decision to all affected stories
   - Note implementation stories that depend on this decision

---

## Decision Record Format

Matching `intelligence_record_standard.md` schema:

```yaml
---
decision_id: DEC-2025-01-15-001
title: Migrate to PostgreSQL for improved performance and scalability
status: approved
date_decided: 2025-01-15
decided_by: Alice Chen (Engineering Lead)
confidence: high
context_story: PROJ-1234
related_stories:
  - PROJ-1235
  - PROJ-1236

## Decision
Use PostgreSQL instead of MongoDB for primary data store.

## Rationale
- Performance benchmarks show 3x faster query performance for our access patterns
- Better support for complex queries and transactions
- Existing team experience with SQL
- Cost optimization: reduced RAM requirements

## Alternatives Considered
1. **MongoDB** (current) - High flexibility but slower performance
2. **DynamoDB** - Serverless but limited query capability
3. **Cassandra** - Good performance but operational complexity

## Trade-offs
- Migration timeline: 4-6 weeks
- Engineering effort: 3 people full-time
- Risk: data consistency during migration
- Benefit: 40% reduction in query latency

## Implementation Stories
- PROJ-1235: Provision PostgreSQL cluster
- PROJ-1236: Migrate user data
- PROJ-1237: Update application queries
- PROJ-1238: Performance testing and optimization

## Follow-up Questions
- Migration strategy for zero-downtime cutover?
- Rollback plan if performance doesn't match benchmarks?
- Backup and disaster recovery procedures?
```

---

## False Positive Filtering

### Ignore These Patterns

1. **Bot Comments**: Any comment from bot accounts (GitHub Actions, CI/CD, automated systems)
   - Filter: `comment.author != github-actions AND comment.author != jenkins AND ...`

2. **Casual Statements**: Decision-sounding language in casual context
   - "I decided to have lunch at noon" (personal decision, not work decision)
   - Pattern: Ignore if decision is about personal time, food, location unrelated to product

3. **Hypothetical or Exploratory**: "We could decide to..." "Should we..." "What if we..."
   - These are options, not decisions
   - Require explicit past/present tense confirmation

4. **Negations**: "We decided NOT to..." captures rejection, which is a decision (VALID)
   - This is a true decision and should be captured

5. **Duplicate Detection**: Same decision captured multiple times in same thread
   - Mark second/third mentions as "reference to DEC-XXX" not new decision
   - Only capture unique decisions once per decision context

---

## Detection Workflow

1. **Run JQL Query**: Scan last 14 days of Jira comments
2. **Extract Candidates**: Collect all comments matching trigger patterns
3. **Score Confidence**: Apply confidence scoring algorithm
4. **Filter False Positives**: Remove bot comments, casual language, hypotheticals
5. **Check Duplicates**: Against existing decision records
6. **Cross-Reference**: Against product context and related stories
7. **Capture Records**: Create decision record YAML for all high/medium confidence decisions
8. **Flag Conflicts**: If decision contradicts existing decision or sprint goal
9. **Notify PM**: Flag any conflicting or scope-impacting decisions for review

---

## Example: High-Confidence Decision Capture

**Jira Comment**:
```
Alice Chen - 2025-01-15 10:30 AM

After testing with the prototype, we've decided to move the authentication 
migration to OAuth2. This gives us better integration with enterprise customers 
and reduces security maintenance burden. Approved by architecture team.

Impacts: All user-facing apps need to migrate. Timeline: 3 sprints.
```

**Detection**:
- Trigger: "decided to" ✓
- Named person: Alice Chen ✓
- Timestamp: 2025-01-15 ✓
- Decision: OAuth2 authentication ✓
- **Confidence Score**: 95 (high)

**Captured Record**:
```yaml
decision_id: DEC-2025-01-15-002
title: Migrate authentication to OAuth2
status: approved
date_decided: 2025-01-15
decided_by: Alice Chen (Engineering Lead)
confidence: high
jira_comment_url: https://jira.example.com/browse/PROJ-1250?focusedCommentId=12345
```

---

## Example: False Positive Filter

**Jira Comment**:
```
jenkins-bot - 2025-01-15 11:00 AM

Build passed. We decided to run all tests. Details in CI log.
```

**Detection**:
- Trigger: "decided to" ✓
- Named person: jenkins-bot (automatic bot) ✗
- Decision: generic/system-generated
- **Confidence Score**: 0 (bot comment)
- **Action**: IGNORE

---

## Storage and Indexing

Captured decisions stored as individual YAML files:
- Directory: `product/context/product_decisions/`
- Filename: `DEC-YYYY-MM-DD-###.md`
- Index file: `product/context/product_decisions/index.md` (for quick lookup)
- Searchable fields: title, decision_id, status, date_decided, decided_by, impact

---

## Integration Points

1. **Product Drift Detector**: Use captured decisions to validate sprint stories align with approved decisions
2. **Story Writer Agent**: Reference relevant decisions when writing stories
3. **Change Impact Analyzer**: Use decision records to understand why changes were made
4. **Offboard Intelligence Synthesizer**: Include key decisions in knowledge transfer docs
