# PRD Standards

Lightweight guide for Product Requirements Documents. This is intentionally concise — full PRD generation is handled by the product-management:feature-spec skill.

## Document Length
Keep PRDs to 2-5 pages maximum. Detailed specs belong in individual user stories, not PRDs.

## Required Sections

### 1. Problem Statement
What problem are we solving? Why does it matter?
- 2-3 sentences describing the user pain point
- Data or evidence supporting the problem (user feedback, metrics, etc.)
- Business impact or strategic importance

### 2. Goals and Non-Goals
What are we trying to achieve? What are we explicitly NOT doing?

**Goals:**
- Primary user outcomes we're optimizing for
- Business metrics we expect to improve
- Scope boundaries

**Non-Goals:**
- Explicitly call out what's out of scope
- Prevents scope creep and manages expectations

### 3. Success Metrics
How will we measure if this solves the problem?
- Quantitative metrics (conversion rate, latency, retention, etc.)
- Baseline (current state)
- Target (what we're aiming for)
- Measurement method

### 4. User Stories
Reference the user stories using story_standards.md format.
- 2-5 primary stories that deliver the feature
- Link to story_id for full details
- Don't repeat story content here; just list IDs and titles

### 5. Technical Considerations
What technical decisions or constraints exist?
- Architecture impact (new services, database schema, etc.)
- Performance requirements
- Scalability considerations
- Integration points
- 2-4 sentences only; details in stories or design docs

### 6. Open Questions
What do we still need to figure out before building?
- Questions for the team
- Assumptions that need validation
- Design decisions pending
- List format, keep brief

## PRD Template

```markdown
# [Feature Title]

## Problem Statement
[2-3 sentences describing user pain point and why it matters]

## Goals and Non-Goals

### Goals
- [Primary user outcome]
- [Business metric to improve]

### Non-Goals
- [Explicitly out of scope]

## Success Metrics
- [Metric name]: [Baseline] → [Target]
- Example: "Search latency: 2.5s → <1.5s"

## User Stories
- STORY-2025-0001: User can search products by name
- STORY-2025-0002: User can filter results by category
- STORY-2025-0003: User can view search history

See story_standards.md for full story details and acceptance criteria.

## Technical Considerations
[2-4 sentences on architecture, performance, integration needs]

## Open Questions
- Should we implement search suggestions?
- Do we need real-time indexing or batch processing?
- How many historical search queries should we retain?
```

## When to Use This Standard

Use this PRD standard for:
- Major feature launches
- New product initiatives
- Cross-functional initiatives requiring alignment
- Strategic bets or experiments

## When to Skip
For small features or bugs:
- Create a story directly
- Skip the PRD; use story ACs for clarity

## Full PRD Generation

For comprehensive PRD generation with structured sections, market analysis, user research, and competitive analysis, use the **product-management:feature-spec** skill.

This standard is for the lightweight, story-focused PRD that drives development.
