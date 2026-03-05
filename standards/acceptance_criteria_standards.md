# Acceptance Criteria Standards

## GIVEN/WHEN/THEN Format

The standard format for all acceptance criteria:

```
GIVEN [initial context/state]
WHEN [user action or system event]
THEN [observable result]
AND [additional assertions]
```

- **GIVEN**: Describes the precondition, setup, or current state
- **WHEN**: Describes the action, input, or trigger
- **THEN**: Describes the expected outcome or result
- **AND**: Chains additional assertions to the THEN clause

### Example:

```
AC1: User receives confirmation after purchase
GIVEN the user has items in the shopping cart
WHEN the user clicks "Complete Purchase" with valid payment details
THEN a success page displays with order number XYZ
AND the order confirmation email is sent within 2 minutes
AND the user is redirected to the account orders page
```

## Acceptance Criteria Rules

1. **One behavior per AC**: Each AC should test exactly one feature, not multiple scenarios
2. **Specific and measurable**: Use concrete values, not vague language
   - Good: "results load within 2 seconds"
   - Bad: "results load quickly"
3. **Testable**: Can be verified by QA, automation, or product review
4. **No implementation details**: Describe the what, not the how
   - Good: "form validation displays an error message"
   - Bad: "use React state to validate form fields"
5. **Observable**: The result must be visible or provable

## Acceptance Criteria Types

### Happy Path
The main, expected flow with valid inputs and normal conditions.
```
AC1: User creates account with email
GIVEN the signup form is loaded
WHEN the user enters valid email and password
THEN the account is created and the user is logged in
```

### Validation
Input validation and constraint checking.
```
AC2: Email validation prevents invalid addresses
GIVEN the signup form is displayed
WHEN the user enters "notanemail"
THEN an error message displays: "Please enter a valid email"
AND the submit button remains disabled
```

### Error Handling
System or API errors and recovery.
```
AC3: API failure shows user-friendly message
GIVEN the create account API returns a 500 error
WHEN the user attempts to sign up
THEN the page displays "Something went wrong. Please try again."
AND a retry button is available
```

### Edge Case
Boundary conditions, empty states, extreme values.
```
AC-E1: Very long password is accepted
GIVEN the password field has a 128-character limit
WHEN the user enters a 128-character password
THEN the form accepts it and allows submission
```

### Performance
Response time and resource constraints.
```
AC4: Results page loads within SLA
GIVEN typical network conditions (3G)
WHEN the user navigates to results page
THEN the page is interactive within 3 seconds
```

### Accessibility
Screen readers, keyboard navigation, color contrast.
```
AC-E2: Form is keyboard navigable
GIVEN a user navigating with keyboard only
WHEN tabbing through the signup form
THEN focus moves through all inputs, buttons, and links in logical order
AND visible focus indicators appear around active elements
```

## Examples: Good vs Bad

### Good AC
```
AC1: Search results are filtered by category
GIVEN the search results page is displayed
WHEN the user selects "Electronics" in the category filter
THEN only products in the Electronics category appear
AND the category filter shows a checkmark next to "Electronics"
AND the URL updates to include ?category=electronics
```

**Why this is good:**
- One clear behavior (category filtering)
- Measurable outcome (visible filter state, URL change)
- Testable without implementation knowledge
- Complete description of what should happen

### Bad AC
```
AC1: The filter works
GIVEN the results page is open
WHEN the user uses the filter
THEN it filters correctly
```

**Why this is bad:**
- Vague: "the filter works" is not measurable
- No specifics: which filter? which category?
- Incomplete: doesn't describe all observable changes
- Untestable: "correctly" is subjective

## Numbering Scheme

- **Functional ACs**: AC1, AC2, AC3... (main user-facing behaviors)
- **Edge Case ACs**: AC-E1, AC-E2, AC-E3... (error states, boundaries, accessibility, performance)

This makes it easy to distinguish happy path from edge cases in reviews and test coverage reports.

## Acceptance Criteria Checklist

Before marking a story as "Ready":
- [ ] Each AC tests exactly one behavior
- [ ] All AC have GIVEN/WHEN/THEN format
- [ ] Criteria are specific, not vague ("within 2 seconds" not "quickly")
- [ ] Criteria are testable by QA or automation
- [ ] No implementation details in the ACs
- [ ] Edge case ACs marked [RECOMMENDED] for team review
- [ ] At least 2-3 edge case ACs per story of complexity 3pts or higher
- [ ] Success conditions are observable (UI changes, API calls, data state)
