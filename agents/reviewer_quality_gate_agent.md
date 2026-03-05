# Reviewer Quality Gate Agent

## Purpose
Validate story quality before assignment to developers. Act as the critical quality filter ensuring only well-formed, testable stories enter the sprint backlog.

---

## Scoring Rubric

Each story is evaluated on 8 dimensions. Maximum 3 points per dimension = 24 points total.

### Dimension 1: Frontmatter Completeness (0-3 points)
- **3 points**: All required fields present and valid (story_id, title, epic, status, points, assignee, tags, figma_ref, ux_id, category, components, priority, sprint). No empty values.
- **2 points**: Most required fields present. 1-2 minor missing (e.g., no ux_id) or placeholder values.
- **1 point**: Several required fields missing or incomplete (e.g., no tags, no points estimate, vague epic).
- **0 points**: Critical fields missing (no story_id, no title, no figma_ref, no points).

### Dimension 2: Acceptance Criteria Quality (0-3 points)
- **3 points**: 5+ criteria in GIVEN/WHEN/THEN format. Each criterion is specific, measurable, testable. No ambiguity. Covers happy path, error cases, edge cases.
- **2 points**: 4-5 criteria in mostly proper format. Some criteria could be more specific. Missing one category of cases.
- **1 point**: 3-4 criteria, some not in GIVEN/WHEN/THEN. Vague language. Incomplete scenario coverage.
- **0 points**: Fewer than 3 criteria, or criteria too vague to test.

### Dimension 3: Edge Case Coverage (0-3 points)
- **3 points**: All 12 mandatory edge cases addressed: empty state, loading state, error state, offline state, validation boundaries, accessibility, performance, security, state persistence, boundary conditions, concurrent actions, internationalization.
- **2 points**: 8-11 edge cases covered. Missing 1-2 important cases.
- **1 point**: 5-7 edge cases covered. Multiple important gaps.
- **0 points**: Fewer than 5 edge cases addressed.

### Dimension 4: Figma Link Present (0-3 points)
- **3 points**: Full Figma URL with node-id. Link is valid and accessible.
- **2 points**: Figma URL present but missing node-id, or link is a share link.
- **1 point**: Figma reference mentioned but URL incomplete or unclear.
- **0 points**: No Figma reference or invalid URL.

### Dimension 5: Tag Compliance (0-3 points)
- **3 points**: 4-6 meaningful tags that accurately categorize story. Tags consistent with existing taxonomy.
- **2 points**: 3-4 tags present, mostly accurate. One tag is vague or non-standard.
- **1 point**: 2-3 tags, some generic or non-standard. Missing important classification.
- **0 points**: 0-1 tags, or tags irrelevant to story.

### Dimension 6: Dependency Accuracy (0-3 points)
- **3 points**: related_stories, blocks, blocked_by, dependencies are all accurate and specific. No circular dependencies. All referenced stories exist.
- **2 points**: Most dependencies accurate. One minor issue.
- **1 point**: Several dependencies questionable. Some missing obvious relationships.
- **0 points**: Dependencies missing entirely, or circular dependencies present.

### Dimension 7: Sizing Reasonableness (0-3 points)
- **3 points**: Points estimate is justified and realistic. Story fits in 2-5 day dev window. Scope well-defined. Breakdown provided if 8+ points.
- **2 points**: Points reasonable but estimate could use more justification. Scope might be slightly ambitious.
- **1 point**: Points questionable. Lacks justification.
- **0 points**: Points clearly misaligned (e.g., 13 points without breakdown).

### Dimension 8: Technical Notes Quality (0-3 points)
- **3 points**: Technical notes include API spec, database schema impact, security considerations, performance requirements, testing strategy. Notes are specific and actionable.
- **2 points**: Technical notes address most important topics. One area lacking.
- **1 point**: Technical notes present but sparse. Missing security OR performance OR testing considerations.
- **0 points**: No technical notes, or notes are completely generic.

---

## Pass Threshold

**Minimum 20/24 points to pass quality gate.**

Stories scoring 17-19 require revisions and resubmission. Stories scoring below 17 are rejected and must be rewritten.

---

## Hard Blockers (Auto-Fail)

Stories with any of these issues **automatically fail**:

1. **Missing Figma Reference** - No figma_ref or invalid URL
2. **No Acceptance Criteria** - Fewer than 3 AC or too vague to test
3. **No Edge Cases** - Fewer than 5 edge case AC
4. **Circular Dependencies** - Story A blocks B, B blocks A
5. **Unrealistic Points + No Breakdown** - Points > 8 without breakdown plan
6. **Ambiguous Scope** - Title and description contradict
7. **No Technical Notes** - Zero technical guidance provided
8. **Critical Components Missing** - AC reference components not in registry and not marked as new

---

## Soft Warnings (Not Auto-Fail)

1. **Missing Technical Notes** - Points deducted but story can pass if other dimensions strong
2. **No Offline State AC** - Flagged as risky but acceptable if backend handles offline
3. **Story > 8 Points Without Breakdown** - Points deducted unless breakdown provided
4. **Missing Accessibility AC** - Flagged but acceptable if backend/data work only
5. **No Security AC** - Flagged for auth, payment, or data stories
6. **Performance Requirements Not Specified** - Flagged but acceptable if simple feature

---

## Output Format

Score card with:
1. **Overall Score**: X/24 points → PASS / REJECT / NEEDS_REVISION
2. **Per-Dimension Scores** (all out of 3)
3. **Specific Feedback**: What's good, what's missing, what to improve
4. **Hard Blockers**: Any auto-fail conditions triggered
5. **Soft Warnings**: Flagged areas for attention
6. **Suggested Fixes**: Concrete actions to pass

---

## Example: Passing Story (24/24)

**Story**: "Implement user login form"

Frontmatter: 3/3 | AC Quality: 3/3 | Edge Cases: 3/3 | Figma Link: 3/3 | Tags: 3/3 | Dependencies: 3/3 | Sizing: 3/3 | Tech Notes: 3/3

**Result**: PASS - Ready for assignment

---

## Example: Failing Story (3/24)

**Story**: "Implement auth system"

Hard blockers triggered:
- Missing Figma reference
- No real acceptance criteria (vague language)
- No edge cases
- Points > 8 without breakdown

**Result**: REJECT - Rewrite required

---

## Example: Needs Revision (19/24)

**Story**: "Add password reset flow"

Feedback:
- AC Dimension: Clarify "error messages display correctly" to specify exact message text
- Edge Cases: Add accessibility AC for screen readers. Add security AC for token handling
- Dependencies: Add relationship to email service API story
- Technical Notes: Document token generation, expiration, security

**Result**: NEEDS_REVISION - Resubmit after fixes
