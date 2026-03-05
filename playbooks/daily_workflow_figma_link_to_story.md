# Playbook: Daily Workflow - Figma Link to Story

Quick 10-minute daily check to catch newly designed screens and flag them for story creation.

## When to Run

Run once per day, ideally:
- First thing in morning
- After design team standup
- Before sprint planning

## Step-by-Step (10 minutes)

### Step 1: Check Figma for Changes (2 minutes)

```
Open main Figma file:
1. Go to Figma design file
2. Look at "Last Updated" timestamp
3. Check if modified since yesterday
4. If no changes: done, check back tomorrow

If changes found:
  → Continue to Step 2
```

### Step 2: Diff Against UI Registry (3 minutes)

```
Compare Figma screens with existing ui_registry.md:

For each screen in Figma:
  → Look up in ui_registry (search by flow name)
  → Is there a matching UX-* entry?

If screen exists:
  → Mark as "checked"
  → Continue

If screen is NEW:
  → Note screen name and flow
  → Continue to Step 3
```

### Step 3: Flag Unlinked Screens (2 minutes)

```
For each NEW screen found:

Create a task:
- Screen name: [name from Figma]
- Flow: [which journey: Search, Checkout, etc.]
- Status: Needs Story Creation
- Assigned to: Product Manager

Example:
[ ] New Screen: "Search Results"
    Flow: Search and Discovery
    Status: Needs UX-SEARCH-001 entry
    Action: Create story STORY-2025-001
```

### Step 4: Suggest Stories (3 minutes)

```
For each flagged screen, suggest a story:

"I found a new screen in Figma: 'Search Results'

Suggested story:
- Story ID: STORY-2025-0001
- Title: User can search products by name
- Components: CMP-SEARCH-INPUT, CMP-RESULTS-LIST
- ACs: (basic outline)
  AC1: Search input accepts text
  AC2: Search executes on submit
  AC-E1: Empty state
  AC-E2: No results state

Please review and create if ready."

Include:
- Link to Figma screen
- Suggested story title
- Component list
- Basic AC outline
```

## Quick Reference

**New Screen Workflow:**
1. Figma has new screen
2. Not in ui_registry
3. Flag for story creation
4. Suggest story template
5. PM reviews and creates
6. Add to sprint
7. Next day, mark as linked

**Workflow complete when:**
- All Figma screens linked to ui_registry entries
- All screens have corresponding stories
- No orphaned designs

## Output

Daily report (if changes found):

```
Figma Link to Story - Daily Check

Date: 2025-02-07
File: Main Product Design

New Screens Found: 2
- "Search Results" (Search and Discovery) → Suggest STORY-2025-0001
- "Product Detail" (Product Discovery) → Suggest STORY-2025-0002

Already Linked: 15
- UX-SEARCH-001: STORY-2025-0001 ✓
- UX-PRODUCT-001: STORY-2025-0003 ✓
[...]

Next Actions:
- PM: Review suggested stories
- Designer: Verify screen naming conventions
- Engineer: No action needed

Status: 2 stories pending review
```

## No Changes Day

If no Figma changes:

```
Figma Link to Story - Daily Check

Date: 2025-02-07
File: Main Product Design

No changes since 2025-02-06.
All 15 screens linked to stories.

Status: ✓ Complete
```
