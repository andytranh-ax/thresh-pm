# Playbook: UX to Story Translation

Step-by-step process for converting Figma designs into product stories with full acceptance criteria.

## Overview

Convert a complete UX flow in Figma into a set of well-defined stories that can be handed to engineering.

## Prerequisites

- Figma file with complete flows and screens
- Screen naming convention consistent
- Components identified and named
- States and interactions documented
- Design signed off and ready for build

## Step-by-Step Process

### Step 1: Receive Figma Designs (1 minute)

Start with:
- Valid Figma file link
- File access granted to team
- Design complete (not wireframes)
- Design has clear naming (e.g., "Search Results", "Product Detail")

### Step 2: Inventory All Screens (5 minutes)

List every user-facing screen in the design:

```
Example:
1. UX-ONBOARDING-001: Welcome Screen
2. UX-ONBOARDING-002: Email Signup
3. UX-ONBOARDING-003: Email Verification
4. UX-SEARCH-001: Search Results
5. UX-SEARCH-FILTERS: Filter Panel
6. UX-PRODUCT-001: Product Detail
7. UX-CART-001: Shopping Cart
8. UX-CHECKOUT-001: Checkout Form
9. UX-CHECKOUT-002: Payment Info
10. UX-CHECKOUT-CONFIRMATION: Order Confirmation
```

Document in spreadsheet:
- Screen ID (UX-XXX)
- Screen name (human-readable)
- Flow it belongs to (e.g., "Checkout")
- Position in flow (entry, step-1, step-2, confirmation, error)

### Step 3: Analyze Each Screen (15 minutes)

For each screen, document:

```yaml
screen_id: UX-SEARCH-001
name: Search Results
flow: Search and Discovery
components:
  - CMP-SEARCH-INPUT
  - CMP-RESULTS-LIST
  - CMP-FILTER-PANEL
  - CMP-PAGINATION
interactions:
  - submit-search
  - filter-by-category
  - sort-results
  - go-to-product-detail
states:
  - empty (before any search)
  - loading (network latency)
  - success (results found)
  - no-results (zero results)
  - error (API error)
responsive_breakpoints:
  - mobile
  - tablet
  - desktop
data_inputs:
  - search_query: string
  - filters: object
  - sort: string
data_outputs:
  - selected_product: product_id
  - applied_filters: object
```

### Step 4: Detect All Components (10 minutes)

For each unique UI element, create a component ID:

```
Identify:
- Input fields: CMP-SEARCH-INPUT, CMP-EMAIL-INPUT
- Buttons: CMP-BUTTON-PRIMARY, CMP-BUTTON-SECONDARY
- Cards: CMP-PRODUCT-CARD, CMP-FILTER-CARD
- Panels: CMP-FILTER-PANEL, CMP-SORT-PANEL
- Lists: CMP-RESULTS-LIST, CMP-PRODUCT-GALLERY
- Navigation: CMP-PAGINATION, CMP-TAB-NAVIGATION
- Modals: CMP-SHARE-MODAL, CMP-FILTER-MODAL

For each component, note:
- Where it appears (which screens)
- Variants (sizes, styles)
- States (hover, active, disabled, error, loading)
```

Create component registry entries (see ui_component_standard.md).

### Step 5: Infer Journey Flow (5 minutes)

Map how screens connect:

```
Entry Point:
  └─ UX-SEARCH-001 (Search Results)
      ├─ Next: UX-PRODUCT-001 (Product Detail)
      │   └─ Next: UX-CART-001 (Shopping Cart)
      │       └─ Next: UX-CHECKOUT-001 (Checkout)
      ├─ Filter: UX-SEARCH-FILTERS (Filter Panel)
      └─ Sort: [same screen, dropdown]

User can:
- Enter search query and see results
- Filter results (opens filter panel)
- Click product to view details
- Add product to cart
- Proceed to checkout
- Confirm order
```

### Step 6: Generate Stories (30 minutes)

For each significant interaction or feature, create a story:

**Story 1: Search functionality**
```yaml
story_id: STORY-2025-0001
title: User can search products by name
epic: Search and Discovery
components:
  - CMP-SEARCH-INPUT
  - CMP-RESULTS-LIST
acceptance_criteria:
  AC1: Search input accepts text → GIVEN page loads WHEN user types THEN text appears
  AC2: Search executes → GIVEN text entered WHEN user hits Enter THEN API called
  AC3: Results display → GIVEN API returns results WHEN page loads THEN results shown
  AC-E1: Empty state → GIVEN no search WHEN page loads THEN "Search to get started" shown
  AC-E2: No results → GIVEN search returns 0 WHEN loading completes THEN "No results" shown
  AC-E3: Loading → GIVEN user searching WHEN latency > 300ms THEN spinner shown
figma_ref: https://figma.com/design/XXX?node-id=search:001
ux_id: UX-SEARCH-001
```

**Story 2: Filter functionality**
```yaml
story_id: STORY-2025-0002
title: User can filter search results by category
epic: Search and Discovery
components:
  - CMP-FILTER-PANEL
blocked_by:
  - STORY-2025-0001
acceptance_criteria:
  AC1: Filter panel appears → GIVEN results shown WHEN filter clicked THEN panel opens
  AC2: Select filter → GIVEN panel open WHEN user clicks category THEN results filtered
  AC-E1: Loading → GIVEN filter applied WHEN results loading THEN spinner in panel
figma_ref: https://figma.com/design/XXX?node-id=search-filter:001
ux_id: UX-SEARCH-001
```

**Story 3: Product detail**
```yaml
story_id: STORY-2025-0003
title: User can view product details
epic: Product Discovery
components:
  - CMP-PRODUCT-DETAIL
  - CMP-PRODUCT-IMAGES
  - CMP-ADD-TO-CART-BUTTON
blocked_by:
  - STORY-2025-0001
acceptance_criteria:
  AC1: Product page loads → GIVEN user clicks product WHEN page navigates THEN details shown
  AC2: Images display → GIVEN page loaded WHEN user scrolls THEN all images visible
  AC3: Add to cart → GIVEN details shown WHEN user clicks "Add" THEN item added to cart
  AC-E1: Out of stock → GIVEN product unavailable WHEN page loads THEN "Out of stock" shown
figma_ref: https://figma.com/design/XXX?node-id=product:detail
ux_id: UX-PRODUCT-001
```

### Step 7: Validate Against Design (10 minutes)

Ensure stories match the design:

```
For each story:
✓ ACs match what Figma shows
✓ Components listed are visible in design
✓ Interactions documented in AC match design interactions
✓ States (empty, loading, error) have mockups in Figma
✓ Responsive variants documented if shown in design
✓ Design is accessible (color contrast, spacing, typography)
```

Mismatches → update stories or request design revision.

### Step 8: Link Components and Screens (5 minutes)

Create cross-references:

```
Update component entries:
- CMP-SEARCH-INPUT: used in STORY-2025-0001, STORY-2025-0042
- CMP-RESULTS-LIST: used in STORY-2025-0001, STORY-2025-0002

Update screen entries:
- UX-SEARCH-001: built by STORY-2025-0001, STORY-2025-0002
- UX-PRODUCT-001: built by STORY-2025-0003
```

This creates impact analysis capability.

### Step 9: Assign Points (5 minutes)

Estimate effort for each story:

```
STORY-2025-0001 (Search UI + API call): 3pts (1 day)
STORY-2025-0002 (Filter panel + filtering): 5pts (2-3 days) [blocked by Story-1]
STORY-2025-0003 (Product detail page): 5pts (2-3 days) [blocked by Story-1]
STORY-2025-0004 (Add to cart): 2pts (2 hours) [blocked by Story-3]
STORY-2025-0005 (Shopping cart view): 3pts (1 day)
STORY-2025-0006 (Checkout form): 5pts (2-3 days) [blocked by Story-5]
STORY-2025-0007 (Payment processing): 8pts [SPLIT THIS - too big]
  → STORY-2025-0007a: Payment form (3pts)
  → STORY-2025-0007b: Payment submission (5pts)
```

Flag stories > 8pts for splitting.

### Step 10: Publish (5 minutes)

See jira_publish_stories.md playbook for publishing to Jira.

## Validation Checklist

Before marking complete:
- [ ] All screens inventoried with UX-* IDs
- [ ] All components identified with CMP-* IDs
- [ ] All significant interactions captured in stories
- [ ] Stories follow story_standards.md format
- [ ] All ACs follow GIVEN/WHEN/THEN format
- [ ] Edge cases documented (empty, loading, error states)
- [ ] Dependencies mapped (no orphaned stories)
- [ ] Points assigned (no stories > 8pts)
- [ ] Figma references valid
- [ ] Design matches stories (no discrepancies)
- [ ] Team reviewed stories
- [ ] Ready for engineering work

## Success Criteria

Process complete when:
- Design fully translated to stories
- Each story has complete ACs
- All edge cases captured
- Dependencies clear
- Points estimated
- Ready for sprint planning
