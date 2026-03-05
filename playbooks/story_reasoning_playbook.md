# Playbook: Story Reasoning

Mental framework for working through a story during development. Use this to ensure complete understanding before coding.

## When to Use

Use this checklist when:
- Moving story to "In Progress"
- Starting implementation
- During code review
- When stuck or confused

Time: 10-15 minutes before writing code.

## Story Reasoning Framework

### 1. Read and Understand ACs (5 minutes)

```
Goal: Understand exactly what needs to be built

Steps:
[ ] Read title: What does this story deliver?
[ ] Read summary: Why are we building this?
[ ] Read user story: Who uses this and why?
[ ] Read each functional AC (AC1, AC2...)
    For each AC:
    - What is the scenario? (GIVEN)
    - What action happens? (WHEN)
    - What should result? (THEN)
[ ] Read each edge case AC (AC-E1, AC-E2...)
    Same questions as above

Ask yourself:
- Do I understand what success looks like?
- Are there any ambiguous ACs?
- Do I need to clarify any ACs with PM?
```

### 2. Identify Edge Cases (3 minutes)

```
Review the AC-E* cases to understand:

[ ] Empty state: What if there's no data?
[ ] Loading state: Show spinner if latency > 300ms?
[ ] Error state: What if API fails?
[ ] Offline: What if no network?
[ ] Boundary: Max length, special characters?
[ ] Accessibility: Keyboard nav, screen reader?
[ ] Performance: Latency targets?

For each edge case:
- How will it look in the UI?
- How will it behave?
- Do I understand how to test it?
```

### 3. Verify Dependencies (2 minutes)

```
Check: Does this story have dependencies?

[ ] Read blocked_by field
    If dependencies exist:
    - Are they already done?
    - Do I have access to the API/component?
    - Do I need to wait for something?

[ ] Read dependencies field (external)
    - api:search-endpoint - do I have API docs?
    - component:product-card - is it built?
    - database:product-schema - does it exist?
    
If dependencies not ready:
→ Cannot start, escalate to PM
If ready:
→ Get access/credentials, proceed
```

### 4. Identify Risks (2 minutes)

```
Ask yourself:

[ ] Is there anything confusing in the story?
    If yes: ask PM/design for clarification

[ ] Are there multiple ways to implement?
    If yes: document your chosen approach, run by reviewer

[ ] Are there performance targets?
    If yes: understand the metrics, plan for testing

[ ] Are there accessibility requirements?
    If yes: plan keyboard nav, screen reader testing

[ ] Does this touch security-sensitive code?
    If yes: involve security review, plan for scrutiny

Red flags (stop and ask):
- "I'm not sure what AC3 means"
- "There are multiple valid interpretations"
- "The performance target seems impossible"
- "I don't have access to the API"
```

### 5. Estimate Effort (1 minute)

```
Review the points and your understanding:

Story is 3 points → expect 1 day
Story is 5 points → expect 2-3 days
Story is 8 points → RED FLAG (should be split)

Does your understanding match the points?
[ ] Yes, points make sense
[ ] No, seems too big: ask to split
[ ] No, seems too small: double-check I understand fully
```

## Development Checklist

Before writing code:

```
[ ] All ACs understood (no ambiguity)
[ ] All edge cases identified
[ ] Dependencies satisfied (API ready, components available)
[ ] Risk areas identified
[ ] Effort estimate reasonable
[ ] Testing strategy clear:
    - How will I test AC1?
    - How will I test AC-E1?
    - Unit tests? Integration? E2E?
```

## During Development

Keep referencing ACs:

```
For each AC:
[ ] Write test case first (TDD)
[ ] Implement code to pass test
[ ] Verify test passes
[ ] Move to next AC

For each edge case AC:
[ ] Plan UI state/message
[ ] Implement edge case handling
[ ] Test edge case scenarios
[ ] Verify matches design
```

## Before Code Review

Self-review against ACs:

```
[ ] AC1 implemented and tested: ✓ or ✗
[ ] AC2 implemented and tested: ✓ or ✗
[ ] AC3 implemented and tested: ✓ or ✗
[ ] AC4 implemented and tested: ✓ or ✗
[ ] AC-E1 implemented and tested: ✓ or ✗
[ ] AC-E2 implemented and tested: ✓ or ✗
[ ] AC-E3 implemented and tested: ✓ or ✓
[ ] AC-E4 implemented and tested: ✓ or ✗

Any ✗ → finish before submitting for review
```

## When Stuck

If confused during development:

```
1. Re-read the AC that's confusing
   - Is the AC unclear?
   - Do I misunderstand?

2. Check the design (figma_ref)
   - Does design show what should happen?
   - Does it match the AC?

3. Review technical notes
   - Are there implementation hints?

4. Ask for clarification
   - Message PM or designer
   - Quote the specific AC
   - Ask "Does this AC mean...?"

5. Document your interpretation
   - Leave comment in code
   - Link to Slack discussion
   - Reference clarifying message
```

## Example: Working Through a Story

```
Story: STORY-2025-0042 - User can share search results

Read ACs:
- AC1: Share button appears on results page ✓
- AC2: Click share opens modal ✓
- AC3: Modal shows link to share ✓
- AC4: Link copied to clipboard ✓
- AC-E1: Offline state - show "Check connection" ✓
- AC-E2: Error state - show "Something wrong" ✓
- AC-E3: Accessibility - keyboard nav ✓

Identify Edge Cases:
[ ] Empty state: N/A (share only on results page)
[ ] Loading: Share button disabled while loading results
[ ] Error: Show error if share API fails
[ ] Offline: Link can't be generated without connection
[x] Boundary: URL max 2048 chars - may need shortener
[ ] A11y: ARIA labels, keyboard navigation
[ ] Performance: Share action should be instant

Dependencies:
[ ] blocked_by: STORY-2025-0001 (search feature) ✓ Done
[ ] api:share-endpoint - API docs available ✓
[ ] component:share-modal - already built ✓

Risks:
[ ] URL shortener latency: Plan for timeout
[ ] A11y: Modal needs ARIA role="dialog"
[ ] Clipboard API: Not supported in old browsers - plan fallback

Testing Strategy:
1. Unit tests: Share action generates correct URL
2. Integration tests: Modal appears on click
3. E2E tests: Share flow end-to-end
4. Edge case: Test offline state
5. A11y: Screen reader, keyboard nav
6. Manual: Test in Chrome, Firefox, Safari, Edge

Ready to code: ✓ Yes
```
