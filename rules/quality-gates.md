# Quality Gates

## Story Quality Gate (24-point rubric)
Stories must score 20/24 minimum before publishing to Jira.

### Scoring Dimensions (3 points each)
1. Frontmatter completeness — all required fields present and valid
2. AC quality — 5+ criteria in GIVEN/WHEN/THEN, specific and testable
3. Edge case coverage — all 12 mandatory categories addressed
4. Figma link — full URL with node-id, valid and accessible
5. Tag compliance — 4-6 meaningful tags from tag_vocabulary
6. Dependency accuracy — no circular deps, all references exist
7. Sizing reasonableness — justified Fibonacci estimate, fits 2-5 day window
8. Technical notes quality — API spec, security, performance, testing strategy

### Auto-Fail Conditions
- Missing Figma reference
- Fewer than 3 acceptance criteria
- Fewer than 5 edge cases
- Circular dependencies
- Points > 8 without split plan
- Title and description contradict

### Scoring Thresholds
- 20-24: PASS — ready for assignment
- 17-19: NEEDS_REVISION — fix and resubmit
- Below 17: REJECT — rewrite required

## Confidence Scoring
- Show confidence scores (Low/Medium/High) on ALL AI-generated recommendations
- Low: insufficient data, first-time pattern, < 3 data points
- Medium: some supporting data, 3-5 data points
- High: strong data support, 6+ data points, validated pattern
