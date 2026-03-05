# UI Component Standard

Framework for documenting and tracking reusable UI components across the design system.

## Component ID Format

All components must have a unique identifier:
```
CMP-XXX
```

Example: `CMP-SEARCH-INPUT`, `CMP-BUTTON-PRIMARY`, `CMP-CARD-PRODUCT`

Format rules:
- Prefix: CMP (constant)
- Separator: hyphen
- Description: 1-3 words, UPPERCASE, descriptive noun + optional modifier
- Uniqueness: Must be globally unique

## Component Registry Entry

Every component must have a registry entry documenting:

### Required Fields

**component_id** (required, string)
- Format: CMP-XXX
- Example: CMP-SEARCH-INPUT
- Uniqueness: Must be unique

**name** (required, string)
- Display name of the component
- Example: "Search Input"
- Format: Title Case

**description** (required, string, 1-2 sentences)
- What is this component? What problem does it solve?
- Example: "Text input field for search queries. Handles autocomplete and query validation."

**status** (required, enum)
- Options: Proposed, Development, Production, Deprecated
- Proposed: Design under review
- Development: Being built
- Production: Stable and in use
- Deprecated: No longer use; being replaced

**variants** (required, array of strings)
- Different variations of the component
- Example: `[default, compact, outline, ghost]`
- Include size variants, style variants, etc.

**states** (required, array of strings)
- All possible visual states
- Standard states: default, hover, active, disabled, loading, error, focus
- Example: `[default, hover, active, disabled, loading, error, focus]`

**props_inputs** (required, object)
- List of props/inputs the component accepts
- Format:
  ```yaml
  props_inputs:
    label:
      type: string
      description: Label text displayed above input
      required: true
      example: "Search products"
    placeholder:
      type: string
      description: Placeholder text when empty
      required: false
      example: "e.g., blue shoes"
    disabled:
      type: boolean
      description: If true, input is disabled
      required: false
      default: false
  ```

**accessibility** (required, array)
- Accessibility features and requirements
- Example:
  ```yaml
  accessibility:
    - "ARIA label on input field"
    - "Focus indicator visible"
    - "Error messages linked via aria-describedby"
    - "Color contrast ratio 4.5:1 WCAG AA"
  ```

**figma_node_id** (required, string)
- Link to Figma component
- Format: FILE_KEY or FILE_KEY/component-id
- Example: `abc123xyz#1234:5678`
- Used to link design to implementation

**stories_using** (required, array of story IDs)
- All stories that use this component
- Example: `[STORY-2025-0001, STORY-2025-0005]`
- Enables impact analysis when component changes

**existing_or_new** (required, enum)
- Existing: Component already built and in production
- New: Being created as part of this story/initiative
- Example: `Existing`
- Helps track design system debt

**created_date** (required, ISO date)
- When component was first documented
- Format: YYYY-MM-DD
- Example: `2025-02-06`

**last_updated** (required, ISO date)
- Last modification date
- Format: YYYY-MM-DD
- Auto-updated when component changes

**maintainer** (optional, email)
- Team member responsible for this component
- Format: email@company.com
- Used for getting approvals or asking questions

## Example Component Entry

```yaml
component_id: CMP-SEARCH-INPUT
name: Search Input
description: |
  Text input field for search queries. Handles autocomplete suggestions, 
  query validation, and search submission.
status: Production
variants:
  - default
  - compact
outline:
states:
  - default
  - hover
  - active
  - disabled
  - loading
  - error
  - focus
props_inputs:
  label:
    type: string
    description: Label text
    required: true
    example: "Search products"
  placeholder:
    type: string
    description: Placeholder text
    required: false
    example: "e.g., blue shoes"
  value:
    type: string
    description: Current input value
    required: false
  onChange:
    type: function
    description: Callback when input value changes
    required: true
  onSubmit:
    type: function
    description: Callback when user submits search
    required: true
  disabled:
    type: boolean
    description: If true, input is disabled
    required: false
    default: false
  error:
    type: string
    description: Error message to display
    required: false
    example: "Please enter a valid search query"
  suggestions:
    type: array
    description: Array of autocomplete suggestions
    required: false
    example: ["blue shoes", "red shoes"]
accessibility:
  - ARIA label on input field required
  - Focus indicator visible (3px outline)
  - Error messages linked via aria-describedby
  - Color contrast 4.5:1 WCAG AA minimum
  - Keyboard navigation: Tab to focus, Enter to submit, Escape to clear
  - Screen reader announcements for suggestions
figma_node_id: search-design#component-search-input
stories_using:
  - STORY-2025-0001
  - STORY-2025-0015
  - STORY-2025-0042
existing_or_new: Existing
created_date: 2024-12-01
last_updated: 2025-02-06
maintainer: design@company.com
```

## Component Lifecycle

### 1. Proposed
- Design created in Figma
- Component entry created in registry
- Component ID assigned
- Status: Proposed

### 2. Development
- Developer creates component
- Props/inputs documented
- Variants and states implemented
- Status: Development
- Linked to stories using it

### 3. Production
- Component tested and working
- Accessibility verified
- Design matches Figma
- Status: Production
- Added to design system documentation

### 4. Deprecated
- Component being replaced by newer component
- Status: Deprecated
- Document replacement component
- Migrate stories to new component

## Component Update Checklist

Before updating a component:
- [ ] Review all stories using this component (stories_using list)
- [ ] Identify impact radius (how many places affected)
- [ ] Update Figma design first
- [ ] Update all stories using component
- [ ] Communicate changes to dependent teams
- [ ] Update props/inputs documentation
- [ ] Update variants list if adding new variants
- [ ] Update accessibility checklist if applicable
- [ ] Update last_updated date

## Using Components in Stories

When a story uses a component:
1. Add component_id to story frontmatter `components:` list
2. Component already exists → reference it by CMP-ID
3. Creating new component as part of this story → create CMP-ID entry, mark as "New"
4. Modify existing component → add story to component's `stories_using` list
