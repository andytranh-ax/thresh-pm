# Story Standards

The canonical story format for Thresh-managed product development. All user stories must follow this structure to ensure clarity, testability, and consistent implementation across teams.

## Frontmatter Schema

Every story begins with YAML frontmatter (see `frontmatter_schema.md` for complete field definitions):

```yaml
story_id: STORY-2025-0001
title: User can search products by name
epic: Search and Discovery
status: Ready
points: 3
assignee: alice@company.com
created: 2025-02-06
updated: 2025-02-06
tags:
  - domain:frontend
  - domain:api
  - type:feature
  - priority:high
  - platform:web
figma_ref: https://figma.com/design/XXX?node-id=1234:5678
related_stories:
  - STORY-2025-0002
blocks: []
blocked_by: []
dependencies:
  - api:search-endpoint
category: Frontend
components:
  - CMP-SEARCH-INPUT
  - CMP-RESULTS-LIST
story_type: feature
priority: High
sprint: Sprint-25
risk_level: Low
ux_id: UX-SEARCH-001
```

## Story Body Format

### 1. Summary (2-3 sentences)
Clear, concise description of what this story delivers and why it matters.

**Example:** 
"Users need to quickly find products by entering search terms. Currently, users must browse categories manually, causing friction and increasing time-to-purchase. This story implements the search UI and integrates with the search API."

### 2. User Story
Use the standard format:

```
As a [user type]
I want [capability/feature]
So that [business value/user benefit]
```

**Example:**
```
As a shopper
I want to search for products by name, brand, or category
So that I can quickly find what I'm looking for without browsing all categories
```

### 3. Acceptance Criteria (AC)

Format: GIVEN/WHEN/THEN with explicit numbering. Each AC tests one behavior.

**Functional Criteria (AC1, AC2, AC3...):**
```
AC1: Search input accepts user text
GIVEN the search page is loaded
WHEN the user types "blue shoes" in the search input
THEN the input displays the text and is cleared after submission

AC2: Search executes on submit
GIVEN the user has entered "blue shoes" in the search input
WHEN the user presses Enter or clicks the Search button
THEN the page calls GET /api/search?q=blue+shoes with the query
AND results load within 2 seconds

AC3: Results display correctly
GIVEN the search API returned results for "blue shoes"
WHEN the search completes
THEN the results list displays 1-20 products per page
AND each product shows: image, name, price, rating
AND results are sorted by relevance

AC4: Pagination works
GIVEN search results span multiple pages
WHEN the user clicks "Next Page" or page number
THEN the URL updates with ?page=N
AND new results load without page reload
```

**Edge Case Criteria (AC-E1, AC-E2, AC-E3...):**
```
AC-E1: Empty search state [RECOMMENDED]
GIVEN the search page loads
WHEN no search has been performed yet
THEN a helpful empty state displays: "Search for products to get started"
AND a few featured products or recent searches appear

AC-E2: No results state
GIVEN the user searched for "xyzabc123"
WHEN the API returns 0 results
THEN the page displays "No products found for 'xyzabc123'"
AND suggests: "Try different keywords" or "Browse all products"
AND shows related search suggestions

AC-E3: Loading state
GIVEN the user submitted a search
WHEN the API is processing (latency > 300ms)
THEN a loading spinner appears in the results area
AND the search button is disabled to prevent duplicate submissions

AC-E4: API error state [RECOMMENDED]
GIVEN the search API returns 500 error
WHEN the user submitted a search
THEN the page displays "Something went wrong. Please try again."
AND shows a retry button
AND logs the error with request ID for debugging

AC-E5: Offline state
GIVEN the user is offline (no network connection)
WHEN the user attempts to search
THEN the input is disabled or shows "Check your connection"
AND cached previous results are displayed if available

AC-E6: Boundary: very long search query
GIVEN the user types a 500-character search string
WHEN submitted
THEN the input truncates at 255 characters
AND the search still executes

AC-E7: Accessibility
GIVEN a user with a screen reader
WHEN navigating the search form
THEN all inputs have proper labels and ARIA attributes
AND results have semantic HTML structure (article, heading hierarchy)
AND keyboard navigation works (Tab, Enter, Arrow keys)

AC-E8: Performance
GIVEN typical network conditions (3G)
WHEN the user submits a search
THEN results fully load in ≤ 2 seconds
AND time-to-interactive for the page is ≤ 3 seconds
```

## Edge Case Categories

Edge cases should cover:
- **Empty state**: Page/component loaded but no data yet
- **Loading state**: Network request in flight (>300ms)
- **Error state**: API, validation, or network errors
- **Offline state**: No connectivity; use cache if available
- **Boundary conditions**: Max lengths, special characters, extreme values
- **Accessibility**: Screen readers, keyboard nav, color contrast, ARIA
- **Performance**: Slow networks, large data sets, resource constraints

Mark edge cases as `[RECOMMENDED]` if the team should review before dev starts (usually 2-3 per story).

## Components and Dependencies

List all UI components used by this story:
```yaml
components:
  - CMP-SEARCH-INPUT
  - CMP-RESULTS-LIST
  - CMP-PAGINATION
```

List all external dependencies:
```yaml
dependencies:
  - api:search-endpoint  # Must be deployed first
  - component:product-card  # Existing component
```

## Technical Notes

Optional section for implementation guidance (not requirements):

**Example:**
- Consider caching search results in IndexedDB for quick recall
- Use debounce (300ms) on input to reduce API calls
- Implement result prefetching on page navigation
- Monitor search latency in analytics

## Story Sizing Guide

Fibonacci scale; consider complexity, uncertainty, and test coverage:

- **1pt** (Trivial): Typo fix, simple CSS tweak, small copy change. Estimate: 15 min.
- **2pt** (Small): Single UI component, simple validation, straightforward API integration. Estimate: 2 hours.
- **3pt** (Medium): Multi-component feature, basic error handling, moderate API work. Estimate: 1 day.
- **5pt** (Large): Complex feature, multiple edge cases, significant state management. Estimate: 2-3 days.
- **8pt** (Very Large): Cross-team feature, multiple dependencies, extensive testing needed. **Consider splitting.**
- **13pt** (Epic): Major feature, multiple stories, week+ of work. **Must split into smaller stories.**

## Example: Complete Well-Written Story

```markdown
---
story_id: STORY-2025-0015
title: User can filter search results by price range
epic: Search and Discovery
status: Ready
points: 5
assignee: bob@company.com
created: 2025-02-01
updated: 2025-02-06
tags:
  - domain:frontend
  - domain:api
  - type:feature
  - priority:medium
  - platform:web
figma_ref: https://figma.com/design/search-flow?node-id=42:103
related_stories:
  - STORY-2025-0001
blocks: []
blocked_by:
  - STORY-2025-0001
dependencies:
  - api:search-filters
category: Frontend
components:
  - CMP-FILTER-PANEL
  - CMP-PRICE-SLIDER
story_type: feature
priority: Medium
sprint: Sprint-25
risk_level: Low
ux_id: UX-SEARCH-002
---

# User can filter search results by price range

## Summary

Users want to narrow search results to their budget. Currently, the search shows all products at any price. This story adds a price range slider in the filter panel, allowing users to set min/max price and instantly see filtered results.

## User Story

As a budget-conscious shopper
I want to filter products by price range
So that I can focus on items within my budget

## Acceptance Criteria

AC1: Price filter appears in filter panel
GIVEN search results are displayed
WHEN the filter panel loads
THEN the "Price" filter section appears with a min/max slider
AND current price range (e.g., "$0 - $10,000") is displayed

AC2: User can set price range
GIVEN the price filter is visible
WHEN the user adjusts the min slider to $50 and max slider to $500
THEN the input fields update to show $50 and $500
AND the results instantly filter to show only items in $50-$500 range

AC3: Results update on slider change
GIVEN the user is dragging the price slider
WHEN they release the slider
THEN the filtered results load within 500ms
AND products outside the range are removed from display

AC4: Filter persists in URL
GIVEN the user has set price range $100-$300
WHEN they refresh the page or share the URL
THEN the price filter is preserved
AND results load with the same price filter applied

AC-E1: Empty state with filter applied
GIVEN the user sets price range $5,000-$6,000
WHEN there are no products in that range
THEN "No products found in $5,000-$6,000 range" displays
AND a button to "Clear filters" or "Adjust range" appears

AC-E2: Boundary: invalid range
GIVEN the user attempts to set min price > max price
WHEN they interact with the sliders
THEN the system prevents invalid state
AND displays a helpful message: "Min price cannot exceed max price"

AC-E3: Loading state during filter
GIVEN the user adjusts the price slider
WHEN the results are loading
THEN a loading spinner appears over the results list
AND the filter controls remain interactive

AC-E4: Accessibility [RECOMMENDED]
GIVEN a user on a keyboard or screen reader
WHEN interacting with the price filter
THEN slider inputs are keyboard accessible (arrow keys)
AND aria-labels describe the current range: "Price range: $50 to $500"
AND screen readers announce range updates

AC-E5: Performance on large result sets
GIVEN 10,000+ products match the search
WHEN the user adjusts the price filter
THEN results update in ≤ 1 second
AND no layout shift or jank occurs

## Technical Notes

- Use React.lazy for filter panel if not on initial load
- Debounce slider input changes (200ms) to reduce filter API calls
- Cache filter options (common price ranges) in localStorage
- Log filter usage to analytics to understand user preferences
- Consider offering "Quick filters" like "$0-50", "$50-100" for common ranges
```

## Key Principles

1. **Specificity**: Every AC must be testable and measurable.
2. **Completeness**: Edge cases should be reviewed before development starts.
3. **Clarity**: User story and ACs written in plain language, no jargon.
4. **Traceability**: Story links to design, dependencies, and related work.
5. **Sizing discipline**: Stories > 8pts are red flags; consider splitting.
