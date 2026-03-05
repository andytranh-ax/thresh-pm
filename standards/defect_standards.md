# Defect Standards

Framework for identifying, tracking, and managing bugs. All defects must follow this standard to ensure proper categorization and accountability.

## Defect as Story Type

Defects are tracked as stories with `story_type: bugfix` and additional metadata.

## Severity Classification

All defects must be classified by severity, which determines SLA and response priority.

### Critical (Severity: Critical)
- **Definition**: System is completely down or unusable; data loss possible; security breach
- **Example**: Checkout page crashes on all browsers; users can view others' private data
- **SLA Response**: 4 hours
- **SLA Resolution**: 1 day
- **Escalation**: Immediate notification to leadership

### High (Severity: High)
- **Definition**: Major feature is broken or significantly degraded; workaround difficult
- **Example**: Search returns no results for any query; login fails for 25% of users
- **SLA Response**: 4 hours
- **SLA Resolution**: 1 day

### Medium (Severity: Medium)
- **Definition**: Feature works but with degraded experience; workaround available
- **Example**: Search results take 10 seconds to load; checkout flow has missing validation
- **SLA Response**: 1 business day
- **SLA Resolution**: 3 business days

### Low (Severity: Low)
- **Definition**: Cosmetic issue or minor inconvenience; no functional impact
- **Example**: Typo in button label; incorrect color on secondary button
- **SLA Response**: 1 sprint
- **SLA Resolution**: Next available sprint

## Frontmatter Requirements

All defect stories must include:

```yaml
story_type: bugfix
severity: [Critical, High, Medium, Low]
affected_component: [component ID that has the bug]
reproduction_steps: [clear steps to reproduce]
root_cause: [only after investigation; initially "Under investigation"]
linked_story: [STORY-ID that introduced this bug]
```

### Linked Story

The `linked_story` field tracks which original story introduced the bug. This:
- Creates accountability (links defect to the developer who wrote the code)
- Enables analysis of defect patterns by developer or team
- Informs code review and testing improvements
- Tracks technical debt and quality trends

**Example:**
```yaml
story_id: STORY-2025-0105
title: Search results not loading for special characters
story_type: bugfix
severity: High
affected_component: CMP-RESULTS-LIST
linked_story: STORY-2025-0001  # Original search feature story
```

## Story Fields for Defects

### Title
Start with action verb that describes the fix:
- Good: "Fix search results not loading for special characters"
- Bad: "Search broken"

### Acceptance Criteria
Use GIVEN/WHEN/THEN format to describe the fix:

```
AC1: Search results load for queries with special characters
GIVEN the user enters "shoes & boots" in search
WHEN they submit the search
THEN results display (not error or blank page)

AC-E1: Edge case - ampersand handling
GIVEN the user enters query with &
WHEN the API processes the query
THEN the ampersand is properly escaped in the URL
```

### Reproduction Steps
Clear, step-by-step instructions to reproduce the bug:

```
Reproduction Steps:
1. Go to search page
2. Enter "blue & green shoes"
3. Press Enter
4. Observe: Results page is blank
5. Expected: Results list shows matching products
```

### Root Cause
Document what caused the bug (fill in during investigation):

```
Root Cause:
The search API URL-encodes the query but the & character is being 
double-encoded, causing the API to interpret it as a query parameter 
separator instead of literal text. Fixed by using encodeURIComponent 
on individual query parameters.
```

## Defect Lifecycle

### 1. Reported
- Defect comes in (support ticket, QA finding, user report)
- Severity is assigned (based on impact)
- Status: Draft

### 2. Triaged
- Confirmed that bug is reproducible
- Root cause identified or under investigation
- Assigned to developer or marked as blocked
- Status: Ready

### 3. In Progress
- Developer starts work
- linked_story field populated
- Status: In Progress

### 4. Verification
- Developer marks complete
- QA verifies fix resolves the issue
- Regression testing performed
- Status: Done (once verified)

### 5. Closed
- Story closed
- Metrics recorded (severity, time-to-fix, cause)

## Defect Metrics

Track the following to improve quality:

- **Mean Time to Detection**: How quickly bugs found after deployment
- **Mean Time to Resolution**: By severity level
- **Defect Escape Rate**: Bugs not caught before production (indicator of test coverage)
- **Defects per Story**: Helps identify developers needing mentorship
- **Severity Distribution**: Track critical vs cosmetic bugs
- **Root Cause Analysis**: Most common causes (missing ACs, skipped edge cases, etc.)

## Example Defect Story

```yaml
---
story_id: STORY-2025-0105
title: Fix search results not loading for special characters
epic: Search and Discovery
status: In Progress
points: 3
assignee: bob@company.com
created: 2025-02-05
updated: 2025-02-06
tags:
  - domain:frontend
  - type:bugfix
  - priority:high
  - platform:web
figma_ref: null
story_type: bugfix
severity: High
affected_component: CMP-RESULTS-LIST
reproduction_steps: |
  1. Go to search page
  2. Enter "blue & green shoes"
  3. Press Enter
  4. Observe: Results page is blank or shows error
  5. Expected: Results list shows matching products
root_cause: "URL encoding issue: ampersand being double-encoded in API URL. Fixed by applying encodeURIComponent correctly."
linked_story: STORY-2025-0001
category: Frontend
components:
  - CMP-SEARCH-INPUT
  - CMP-RESULTS-LIST
priority: High
sprint: Sprint-25
risk_level: Low
ux_id: UX-SEARCH-001
related_stories: []
blocks: []
blocked_by: []
dependencies: []
---

# Fix search results not loading for special characters

## Summary
Users searching for queries with special characters (& % $ etc) see blank results or errors. This was introduced in the original search feature when query parameters were not properly URL-encoded. This fix applies correct URL encoding to handle all special characters.

## Reproduction Steps
1. Go to search page
2. Enter "blue & green shoes"
3. Press Enter
4. Bug: Results page is blank or shows error
5. Expected: Results list shows matching products

## Root Cause
The search API URL-encodes queries, but the ampersand was being double-encoded, causing the API to parse it as a parameter separator instead of literal text. This was caused by not using encodeURIComponent on the query string before building the API URL.

## Acceptance Criteria

AC1: Special characters in search work
GIVEN the user enters "shoes & boots"
WHEN they submit the search
THEN results load and display matching products

AC2: Various special characters handled
GIVEN the user enters queries with: & % $ # @ ! etc.
WHEN they search
THEN each special character is properly encoded
AND results load correctly

AC3: URL encoding verified
GIVEN a query "blue & green"
WHEN the API request is made
THEN the URL shows: ?q=blue%20%26%20green (correct single encoding)

AC-E1: Edge case - consecutive special chars
GIVEN the user enters "shoes & boots & socks"
WHEN they search
THEN multiple ampersands are all properly encoded

## Linked Story
STORY-2025-0001: User can search products by name (original search feature)
```

## Defect Prevention

To reduce defect rates:

1. **Complete ACs**: Every story should have 2-3 edge case ACs covering special characters, empty inputs, boundary conditions
2. **Test edge cases**: QA should test ACs before story is marked Done
3. **Code review focus**: Reviewers should specifically check for input validation and encoding
4. **Learn from defects**: After closure, review root cause to prevent similar bugs
