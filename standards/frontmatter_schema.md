# Frontmatter Schema

Complete YAML schema for story frontmatter. All fields are documented with type, requirement level, description, and examples.

## Field Reference

### Identification

**story_id** (required, string)
- Format: STORY-YYYY-NNNN or EPIC-YYYY-NNNN
- Description: Unique identifier for the story, typically auto-generated
- Example: `STORY-2025-0001`
- Validation: Must be unique across all stories

**title** (required, string, max 100 chars)
- Description: Concise title describing what the story delivers
- Example: `User can search products by name`
- Validation: Should be action-oriented, not generic

### Organization

**epic** (required, string)
- Description: Parent epic or initiative this story belongs to
- Example: `Search and Discovery` or `Checkout Flow`
- Validation: Must match an existing epic in the system

**category** (required, string, enum)
- Options: Frontend, Backend, Full-stack, Design, Data, Infrastructure
- Description: Primary technical category for this story
- Example: `Frontend`
- Validation: Must be one of the listed options

**components[]** (optional, array of strings)
- Description: UI or code components touched by this story
- Example: `[CMP-SEARCH-INPUT, CMP-RESULTS-LIST]`
- Format: Component IDs from ui_component_standard.md
- Validation: Each ID must match an existing component

**tags[]** (required, array of strings, 1-5 items)
- Description: Controlled vocabulary tags for classification
- Example: `[domain:frontend, type:feature, priority:high, platform:web]`
- Rules: Must include minimum 1 domain tag + 1 type tag (see tag_vocabulary.md)
- Validation: All tags must exist in tag_vocabulary.md

### Status and Lifecycle

**status** (required, string, enum)
- Options: Draft, Ready, In Progress, Done, Blocked
- Description: Current stage of the story
- Default: Draft
- Rules:
  - Draft: Incomplete, not ready for sprint
  - Ready: Approved, has ACs and design, ready to assign
  - In Progress: Actively being worked on
  - Done: Completed and merged
  - Blocked: Waiting on external dependency
- Validation: Transitions must follow workflow rules

**story_type** (required, string, enum)
- Options: feature, bugfix, refactor, chore, spike, tech-debt
- Description: Type of work this story represents
- Example: `feature`
- Validation: Must be one of the listed options

**priority** (required, string, enum)
- Options: Critical, High, Medium, Low
- Description: Business priority relative to other stories
- Rules:
  - Critical: Blocks launches or major features; 4h response time
  - High: Significant feature or bug; 1 day response time
  - Medium: Nice-to-have features; 3 days response time
  - Low: Polish, tech debt; next sprint
- Validation: Usually set during refinement

**sprint** (optional, string)
- Format: Sprint-NN or "Backlog"
- Description: Which sprint this story is assigned to
- Example: `Sprint-25`
- Validation: Must match an active sprint or "Backlog"

### Sizing and Effort

**points** (required, integer, Fibonacci)
- Options: 1, 2, 3, 5, 8, 13
- Description: Story size estimate
- Rules:
  - 1pt = 15 min, 2pt = 2 hours, 3pt = 1 day
  - 5pt = 2-3 days, 8pt = consider split, 13pt = must split
- Validation: Must be Fibonacci number; stories >8 are red flags
- Note: Required before "Ready" status

**risk_level** (optional, string, enum)
- Options: Low, Medium, High
- Description: Implementation complexity or risk
- Example: `Low`
- Validation: Set during estimation if complexity is high

### Assignments

**assignee** (optional, string)
- Format: email@company.com
- Description: Developer or team member assigned to work on this story
- Example: `alice@company.com`
- Rules: Only set when story moves to "In Progress"
- Validation: Must be a valid team member email

**decided_by** (optional, string)
- Format: email@company.com
- Description: Team member who made final decision (for decision records)
- Example: `pm@company.com`
- Validation: Used in intelligence_record_standard.md

### Design and UX

**ux_id** (optional, string)
- Format: UX-XXX
- Description: Linked UX screen or journey ID from ui_screen_standard.md
- Example: `UX-SEARCH-001`
- Rules: Required for all Frontend or Design stories
- Validation: Must match existing screen ID

**figma_ref** (optional, URL)
- Description: Link to Figma design file and node ID
- Format: `https://figma.com/design/FILE_KEY?node-id=X:Y`
- Example: `https://figma.com/design/abc123?node-id=1234:5678`
- Rules: Required for Frontend and Design stories
- Validation: URL must be valid and accessible

### Dependencies and Relationships

**related_stories[]** (optional, array of story IDs)
- Description: Stories working on the same feature (parallel work)
- Example: `[STORY-2025-0002, STORY-2025-0005]`
- Relationship type: relates_to (no blocking, just related)

**blocks[]** (optional, array of story IDs)
- Description: Stories that must wait for this story to complete
- Example: `[STORY-2025-0018]`
- Relationship type: blocks (this story must finish first)
- Rules: No circular dependencies allowed

**blocked_by[]** (optional, array of story IDs)
- Description: Stories that must complete before this one starts
- Example: `[STORY-2025-0001]`
- Relationship type: blocked_by (must wait on these)
- Rules: No chains longer than 3 stories; flag for resolution

**dependencies[]** (optional, array of strings)
- Description: External dependencies: APIs, databases, libraries, services
- Format: `[type:identifier]` e.g., `api:search-endpoint`, `database:product-schema`
- Types: api, database, component, library, infrastructure, service, configuration, data-migration, third-party
- Example: `[api:search-endpoint, component:product-card]`
- Rules: All dependencies must be documented and tracked

### Timestamps

**created** (required, ISO date)
- Format: YYYY-MM-DD
- Description: Story creation date
- Example: `2025-02-06`
- Auto-set by system

**updated** (required, ISO date)
- Format: YYYY-MM-DD
- Description: Last update date
- Example: `2025-02-06`
- Auto-updated by system

## Validation Rules

### Before "Ready" Status
- [ ] story_id is unique
- [ ] title is action-oriented
- [ ] epic exists
- [ ] category is set
- [ ] tags include 1+ domain and 1+ type (see tag_vocabulary.md)
- [ ] points are Fibonacci
- [ ] story_type is set
- [ ] priority is set
- [ ] figma_ref populated (for Frontend/Design stories)
- [ ] Acceptance criteria written and numbered
- [ ] Edge cases defined (AC-E1, AC-E2, AC-E3)
- [ ] components list is complete
- [ ] dependencies documented
- [ ] ux_id linked (for Frontend/Design stories)

### Before Assignment ("In Progress")
- [ ] All ACs have test cases in QA system
- [ ] All dependencies are resolved or marked as blocked_by
- [ ] blocked_by stories are visible in sprint planning
- [ ] No circular dependencies

### Before Closure ("Done")
- [ ] All ACs verified in QA
- [ ] All edge cases tested
- [ ] Design matches Figma reference
- [ ] Tests cover all AC + edge cases
- [ ] Code review approved
- [ ] No lint warnings or errors

## Example Frontmatter

```yaml
story_id: STORY-2025-0042
title: User can share search results via link
epic: Search and Discovery
status: Ready
points: 3
assignee: null
created: 2025-02-01
updated: 2025-02-06
tags:
  - domain:frontend
  - domain:api
  - type:feature
  - priority:high
  - platform:web
figma_ref: https://figma.com/design/search?node-id=98:765
related_stories:
  - STORY-2025-0001
blocks: []
blocked_by: []
dependencies:
  - api:search-filters
  - component:share-modal
category: Frontend
components:
  - CMP-SHARE-BUTTON
  - CMP-SHARE-MODAL
story_type: feature
priority: High
sprint: Sprint-25
risk_level: Low
ux_id: UX-SEARCH-003
```
