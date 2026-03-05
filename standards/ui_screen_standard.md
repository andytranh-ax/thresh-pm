# UI Screen Standard

Framework for documenting and tracking user-facing screens and journeys across the product.

## Screen ID Format

All screens must have a unique identifier:
```
UX-XXX
```

Example: `UX-SEARCH-001`, `UX-CHECKOUT-CONFIRMATION`, `UX-ONBOARDING-EMAIL-VERIFY`

Format rules:
- Prefix: UX (constant)
- Separator: hyphen
- Description: Flow name + step indicator (1-2 words), UPPERCASE
- Numbering: Sequential within flow (SEARCH-001, SEARCH-002, etc.)
- Uniqueness: Must be globally unique

## Screen Registry Entry

Every user-facing screen must have a registry entry documenting:

### Required Fields

**screen_id** (required, string)
- Format: UX-XXX
- Example: UX-SEARCH-001
- Uniqueness: Must be unique

**name** (required, string)
- Human-readable screen name
- Example: "Search Results"
- Format: Title Case

**flow** (required, string)
- Which user journey does this screen belong to?
- Example: "Search and Discovery" or "Checkout"
- Maps to epic in stories

**position_in_flow** (required, enum or string)
- Position in journey: entry, step-1, step-2, step-N, confirmation, error
- Example: "entry" (if search results is entry point)
- Or: "step-3" (if 3rd step in checkout)

**description** (required, string, 1-2 sentences)
- What does this screen do? What is the user trying to accomplish?
- Example: "Displays search results with filters and pagination. User can refine search or select a product."

**components_used** (required, array of component IDs)
- All CMP-* IDs used on this screen
- Example: `[CMP-SEARCH-INPUT, CMP-RESULTS-LIST, CMP-FILTER-PANEL, CMP-PAGINATION]`
- Enables impact analysis when component changes

**interactions** (required, array)
- Key interactions user can perform on this screen
- Example: `[submit-search, filter-by-category, sort-results, view-product-detail, add-to-cart]`
- Helps understand user flows

**states** (required, array)
- All possible screen states: empty, loading, success, error, etc.
- Example: `[empty, loading, success, no-results, error]`
- Maps to AC edge cases

**responsive_breakpoints** (required, array)
- Which device sizes this screen supports
- Standard: `[mobile: 375px, tablet: 768px, desktop: 1440px]`
- Example: `[mobile, tablet, desktop]`

**figma_node_id** (required, string)
- Link to Figma screen
- Format: FILE_KEY or FILE_KEY/frame-id
- Example: `abc123xyz#1234:5678`
- Used to link design to stories

**stories_implementing** (required, array of story IDs)
- Stories that build or modify this screen
- Example: `[STORY-2025-0001, STORY-2025-0015, STORY-2025-0042]`
- Enables tracking of screen completion

**previous_screen** (optional, screen ID)
- Which screen comes before this in the flow
- Format: UX-XXX
- Example: `UX-SEARCH-FILTERS`
- Creates flow diagram

**next_screen** (optional, array of screen IDs)
- Which screens can come after this
- Format: array of UX-XXX
- Example: `[UX-PRODUCT-DETAIL, UX-SEARCH-001]`
- Creates flow diagram

**data_inputs** (optional, array)
- What data is passed to this screen?
- Example: `[search_query: string, filters: object, page: number]`
- Helps with API design

**data_outputs** (optional, array)
- What data/actions does this screen send out?
- Example: `[user_selection: product_id, filter_applied: string]`
- Helps with state management

**created_date** (required, ISO date)
- When screen was first documented
- Format: YYYY-MM-DD

**last_updated** (required, ISO date)
- Last modification date
- Format: YYYY-MM-DD

## Example Screen Entry

```yaml
screen_id: UX-SEARCH-001
name: Search Results
flow: Search and Discovery
position_in_flow: entry
description: |
  Displays search results with filters and sorting options. User can refine 
  search, filter by category/price, sort by relevance/price, and navigate 
  to product details.
components_used:
  - CMP-SEARCH-INPUT
  - CMP-RESULTS-LIST
  - CMP-FILTER-PANEL
  - CMP-PAGINATION
  - CMP-SORT-DROPDOWN
interactions:
  - submit-search
  - filter-by-category
  - filter-by-price
  - sort-results
  - view-product-detail
  - add-to-cart
  - page-navigation
states:
  - empty
  - loading
  - success
  - no-results
  - error
responsive_breakpoints:
  - mobile
  - tablet
  - desktop
figma_node_id: search-flow#component-results
stories_implementing:
  - STORY-2025-0001
  - STORY-2025-0015
  - STORY-2025-0042
previous_screen: null
next_screen:
  - UX-PRODUCT-001
  - UX-PRODUCT-002
data_inputs:
  - search_query: string
  - filters: { category: string, price_min: number, price_max: number }
  - sort: string (relevance|price|rating)
  - page: number
data_outputs:
  - selected_product: product_id
  - applied_filters: object
  - search_completed: boolean
created_date: 2025-01-15
last_updated: 2025-02-06
```

## Screen Lifecycle

### 1. Designed
- Screen mocked up in Figma
- Screen entry created in registry
- Screen ID assigned

### 2. Breakdown
- Identify all components used
- Map interactions
- Create acceptance criteria in stories

### 3. Built
- Stories implementing screen in progress
- Components being built or reused

### 4. Verified
- All stories completed
- Screen tested in QA
- Design matches Figma
- Responsive across breakpoints

### 5. Published
- Screen deployed to production
- Analytics tracking configured
- User feedback being gathered

## Connected Screens (Flow Mapping)

Use previous_screen and next_screen to create a visual flow:

```
UX-SEARCH-001 (Search Results)
    ↓
UX-PRODUCT-001 (Product Detail)
    ↓
UX-CART-001 (Shopping Cart)
    ↓
UX-CHECKOUT-001 (Checkout)
    ↓
UX-CHECKOUT-CONFIRMATION (Confirmation)
```

This helps:
- Understand user journey
- Identify missing screens
- Plan parallel development
- Calculate critical path

## Screen States and Edge Cases

Each screen should have corresponding edge case ACs in stories:

```yaml
states:
  - empty: No data to show (e.g., first-time user)
  - loading: API request in progress
  - success: Data loaded successfully
  - no-results: User searched but got 0 results
  - error: API error or system error
```

Each state should have:
- Figma mockup
- Acceptance criteria in stories
- QA test case

## Screen Update Checklist

Before updating a screen:
- [ ] Review all stories implementing this screen
- [ ] Update Figma design first
- [ ] Identify component changes (added, removed, modified)
- [ ] Update stories using modified components
- [ ] Update states list if adding new states
- [ ] Update responsive breakpoints if needed
- [ ] Update next/previous screen references
- [ ] Communicate changes to dependent screens
- [ ] Update last_updated date
