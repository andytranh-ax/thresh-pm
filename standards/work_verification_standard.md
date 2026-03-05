# Work Verification Standard

Quality assurance and verification processes to ensure stories are correct, complete, and ready for production.

## Developer Self-Check

Before submitting code for review, developer must verify:

### Acceptance Criteria Coverage

- [ ] Implemented all functional ACs (AC1, AC2, AC3...)
- [ ] Implemented all edge case ACs (AC-E1, AC-E2, AC-E3...)
- [ ] Each AC has at least one test case (unit, integration, or e2e)
- [ ] Test cases pass locally
- [ ] Implementation matches AC description exactly

**Example:**
```
Story STORY-2025-0001 has:
AC1: Search input accepts text ✓ (tested)
AC2: Search executes on submit ✓ (tested)
AC3: Results display correctly ✓ (tested)
AC4: Pagination works ✓ (tested)
AC-E1: Empty state [RECOMMENDED] ✓ (tested)
AC-E2: No results state ✓ (tested)
AC-E3: Loading state ✓ (tested)
AC-E4: API error state [RECOMMENDED] ✓ (tested)
```

### Edge Case Coverage

- [ ] Empty state: Tested component with no data
- [ ] Loading state: Network latency > 300ms shows spinner
- [ ] Error state: API 500 error shows error message
- [ ] Offline state: No network shows offline message or cached data
- [ ] Boundary: Very long input, special characters, max values
- [ ] Accessibility: Keyboard navigation, screen reader, color contrast
- [ ] Performance: Meets performance targets in ACs

### Code Quality

- [ ] No lint warnings or errors (eslint, prettier, etc.)
- [ ] No console.log, debugger, or test code left in
- [ ] No commented-out code
- [ ] Code follows team style guide and patterns
- [ ] Variable and function names are clear and descriptive
- [ ] Complex logic has comments explaining intent
- [ ] DRY: No repeated code blocks (refactored)
- [ ] No hard-coded values (use constants or config)

### Design Fidelity

- [ ] UI matches Figma design exactly
- [ ] Colors use design tokens (not hard-coded hex)
- [ ] Typography matches design (font size, weight, line height)
- [ ] Spacing matches design (margins, padding)
- [ ] Responsive behavior matches breakpoints
- [ ] Hover/active states match design
- [ ] Transitions and animations match design
- [ ] Dark mode (if applicable) matches design

### Testing

- [ ] All tests passing locally
- [ ] Test coverage > 80% for modified code
- [ ] Tests cover happy path and edge cases
- [ ] Tests are not brittle or flaky
- [ ] Tests have clear, descriptive names
- [ ] Integration tests verify API interactions

### Performance

- [ ] Meets performance targets in ACs
- [ ] No unnecessary re-renders (React)
- [ ] No N+1 queries (database)
- [ ] Bundle size impact analyzed (if frontend)
- [ ] Lighthouse score acceptable
- [ ] No memory leaks

## Peer Review Checklist

Code reviewer verifies:

### Code Quality

- [ ] Code is readable and understandable
- [ ] Logic is correct and well-structured
- [ ] No obvious bugs or edge cases missed
- [ ] Error handling is appropriate
- [ ] Performance is acceptable
- [ ] Security vulnerabilities addressed (no SQL injection, XSS, etc.)
- [ ] Code follows team patterns and conventions
- [ ] Tests are comprehensive and passing

### AC Alignment

- [ ] Implementation matches all ACs
- [ ] Edge cases from AC-E1, AC-E2... are handled
- [ ] No scope creep (only what ACs specify)
- [ ] ACs are properly tested

### Design Review

- [ ] Visual appearance matches Figma
- [ ] Responsive behavior correct
- [ ] Accessibility checklist passed
- [ ] No visual regressions detected

### Testing Review

- [ ] Test cases cover all ACs
- [ ] Edge cases tested
- [ ] Integration tests verify API behavior
- [ ] Test coverage acceptable
- [ ] Tests are maintainable

### Architecture Review

- [ ] No unnecessary complexity
- [ ] Follows established patterns
- [ ] Reuses components/utilities appropriately
- [ ] No dependency issues
- [ ] Scalability considered

### Approval Criteria

```markdown
## Code Review Checklist

- [ ] All ACs implemented and tested
- [ ] Code quality: no lint errors, clear naming, good structure
- [ ] Design matches Figma exactly
- [ ] Test coverage > 80%
- [ ] No accessibility issues
- [ ] Performance acceptable
- [ ] Documentation updated (if needed)
- [ ] No merge conflicts

**Approved** ✓ or **Needs Changes** (specify below)
```

## QA Verification Checklist

QA verifies functionality and design:

### Functional Testing

- [ ] All functional ACs work correctly (AC1, AC2, AC3...)
- [ ] Happy path flows as expected
- [ ] All edge case ACs work (AC-E1, AC-E2...)
- [ ] No regressions in related features
- [ ] Cross-browser testing (Chrome, Firefox, Safari, Edge)
- [ ] Mobile testing (iOS and Android)
- [ ] Network latency tested (slow 3G simulated)

### Edge Case Testing

- [ ] Empty state displays correctly
- [ ] Loading state spinner appears and disappears
- [ ] Error states display error messages
- [ ] Offline state handled gracefully
- [ ] Boundary conditions: max length, special characters, very large numbers
- [ ] Validation error messages clear and helpful

### Accessibility Testing

- [ ] Keyboard navigation works (Tab, Shift+Tab, Enter, Escape, Arrow keys)
- [ ] Screen reader announces all content (NVDA, JAWS, VoiceOver)
- [ ] Color contrast WCAG AA (4.5:1 normal text, 3:1 large text)
- [ ] Focus indicators visible
- [ ] ARIA labels present
- [ ] Form labels associated with inputs
- [ ] No keyboard traps

### Performance Testing

- [ ] Page load time acceptable (< 3 seconds)
- [ ] Interactions responsive (< 300ms)
- [ ] No jank or layout shift
- [ ] Lighthouse score green (or acceptable)
- [ ] Memory usage stable (no leaks)

### Design Verification

- [ ] UI matches Figma pixel-perfect
- [ ] Colors correct (use color picker)
- [ ] Typography correct (font, size, weight, line height)
- [ ] Spacing correct (compare with design specs)
- [ ] Hover states match design
- [ ] Active states match design
- [ ] Disabled states match design
- [ ] Loading states match design

### Test Report Template

```markdown
## Test Report: STORY-2025-0001

### Functional Testing
- [x] AC1: Search input accepts text ✓
- [x] AC2: Search executes on submit ✓
- [x] AC3: Results display correctly ✓
- [x] AC4: Pagination works ✓
- [x] AC-E1: Empty state ✓
- [x] AC-E2: No results ✓
- [x] AC-E3: Loading state ✓
- [x] AC-E4: API error ✓

### Cross-Browser Testing
- [x] Chrome: ✓
- [x] Firefox: ✓
- [x] Safari: ✓
- [x] Edge: ✓

### Mobile Testing
- [x] iOS: ✓
- [x] Android: ✓

### Accessibility
- [x] Keyboard nav: ✓
- [x] Screen reader: ✓
- [x] Color contrast: ✓

### Design Verification
- [x] Matches Figma: ✓
- [x] Spacing correct: ✓
- [x] Typography correct: ✓

### Status: APPROVED ✓
```

## Product Sign-Off

Product Manager verifies:

- [ ] Feature matches product vision
- [ ] All ACs satisfied
- [ ] Design correct and approved
- [ ] No regressions or side effects
- [ ] Performance acceptable
- [ ] Ready for production deployment

## Sign-Off Chain

```
Developer ──[Self-Check]──> Code Reviewer
                ↓
             Code Review ──[Approved]──> QA
                ↓
             QA Testing ──[Approved]──> Product
                ↓
             Product Sign-Off ──[Approved]──> Ready to Merge
```

All checks must pass in sequence before merging to main branch.
