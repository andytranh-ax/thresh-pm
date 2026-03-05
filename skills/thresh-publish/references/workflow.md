# Publish Stories to Jira Workflow

This workflow ensures stories have accurate dependency mappings before syncing with Jira.

## Pre-Publish Checklist

Before publishing ANY stories to Jira, validate the following:

### 0. Validate Figma Links (REQUIRED)

> [!CAUTION]
> **Stories CANNOT be published to Jira without Figma links.**
> This is a hard requirement — no exceptions.

Before publishing, check each story for `figma_ref` in frontmatter:

If ANY story is missing a Figma link:

```
Agent: ⚠️ BLOCKED: The following stories are missing Figma links:

       ❌ UX-001-device-grid-plp.md — figma_ref: null
       ❌ UX-002-iphone-pdp.md — figma_ref: null

       Please provide Figma links for each screen:

       1. UX-001 Device Grid (PLP) — Figma link?
       2. UX-002 iPhone 16 Pro PDP — Figma link?

       (Paste links or type "skip" to add later — but publish will remain blocked)
```

**After receiving links**, update each story file:

```yaml
figma_ref: "https://www.figma.com/file/xxx/Project?node-id=123-456"
```

Then re-validate before proceeding.

---

### 1. Identify Story Relationships

For stories generated from the same screen/feature:

| Relationship | When to Use | Jira Link Type |
|--------------|-------------|----------------|
| **Relates to** | Default for stories from same screen/feature | `relates to` |
| **Blocks / Is blocked by** | Component must be complete before wiring story can start | `blocks` |
| **Depends on** | Sequential work order required | `is blocked by` |

### 2. Confirm with User

Before each publish, present the dependency summary:

```
Agent: I'm about to publish 6 stories from the Credit Verification screen.

Proposed relationships:
- FGAT-30 through FGAT-35 → All "relates to" each other (same screen)
- No blocking dependencies detected

Do you want to:
1. Proceed with these relationships
2. Add specific blocking dependencies (e.g., "Card Form blocks Form Actions")
3. Skip dependency linking
```

### 3. Populate Local Frontmatter First

Before publishing, ensure each story file has:

```yaml
---
figma_ref: "https://www.figma.com/..."  # REQUIRED
related_story_refs: [STORY-015-01, STORY-015-02, ...]  # Same screen/feature
blocks: []  # Stories this one blocks
blocked_by: []  # Stories blocking this one
---
```

### 4. Create Issues in Jira via MCP

Use Jira MCP to create issues:

- Call `createJiraIssue` with the story details
- Reference your `cloudId` and `projectKey` from CLAUDE.md
- Include full story content in the description field

**Required Fields:**
- `summary`: Story title
- `description`: Full story content with ACs, technical notes, error states
- `issueTypeName`: "Story"
- `projectKey`: Your project key (from CLAUDE.md)
- Additional fields as needed (assignee, labels, etc.)

### 5. Content Fidelity (STRICT)

When creating the Jira issue `description` field:
- **Exact Copy**: Copy/Paste the ENTIRE content of the markdown file (Story, Visual Source, ACs, Tech Notes, Error States).
- **No Summarization**: Do NOT summarize, shorten, or rephrase the Acceptance Criteria.
- **Formatting**: Preserve GIVEN/WHEN/THEN structure as paragraphs or lists in Jira.
- **Completeness**: If the local file has technical notes or error scenarios, they MUST appear in Jira.

### 6. Impact Radius Mapping

Before final publish, calculate and display the blast radius:

1. **Extract Dependencies:**
   - From `component_refs`: Which components does this story touch?
   - From `api_refs`: Which APIs are called?
   - From `related_story_refs`: Which stories are linked?

2. **Display Summary:**
   ```
   Impact Radius for STORY-016-02:
   - Components: CartService, PaymentGateway, InventorySync (3)
   - APIs: POST /api/cart/add, GET /api/products (2)
   - Related Stories: FGAT-36, FGAT-38, FGAT-39 (3)

   Total blast radius: 8 touch points
   ```

3. **User Confirms:** "Proceed with publish? (Y/n)"

## Default Behaviors

1. **Same screen/feature** → Auto-link as "relates to"
2. **Component vs Wiring** → Ask user if component blocks wiring
3. **Sequential flow** → Ask user to confirm order dependencies
4. **Cross-screen** → No auto-linking; user must specify

## Rules

> [!IMPORTANT]
> Before EVERY Jira publish:
> 1. Show proposed dependency relationships
> 2. Show impact radius
> 3. Ask user to confirm or modify
> 4. Only then create issues via Jira MCP

## Jira MCP Integration

This workflow uses Jira MCP tools directly:

- **createJiraIssue**: Create new stories/epics
- **editJiraIssue**: Update existing issues
- **getJiraIssue**: Retrieve issue details
- **transitionJiraIssue**: Move issues between statuses
- **searchJiraIssuesUsingJql**: Find existing issues before duplicating

See your `CLAUDE.md` for cloudId and projectKey configuration.
