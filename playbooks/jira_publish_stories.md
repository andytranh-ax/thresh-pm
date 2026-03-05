# Playbook: Jira Publish Stories

End-to-end process for publishing stories from Thresh into Jira, ensuring proper validation and traceability.

## Prerequisites

- All stories have complete YAML frontmatter
- All ACs follow GIVEN/WHEN/THEN format
- Figma references are valid for Frontend/Design stories
- Dependencies are mapped and no circular deps exist
- Points assigned using Fibonacci scale
- Story status is "Ready"

## Step-by-Step Process

### Step 1: Validate Story Completeness (5 minutes)

Before publishing, verify the story has everything required:

```
For each story:
✓ story_id exists and is unique
✓ Title is action-oriented ("User can X")
✓ Epic is set and exists
✓ Points are Fibonacci (1, 2, 3, 5, 8, 13)
✓ Tags include 1+ domain + 1+ type (see tag_vocabulary.md)
✓ Category is set
✓ priority is set
✓ story_type is set
✓ Acceptance criteria are complete (AC1+, AC-E1+)
✓ All ACs follow GIVEN/WHEN/THEN format
✓ figma_ref populated (for Frontend/Design stories)
✓ components list complete
✓ dependencies documented
✓ ux_id linked (for Frontend/Design stories)
```

**Blocking issues:**
- Missing required fields → return to author
- Points > 8 → request split before publishing
- Circular dependencies detected → escalate

### Step 2: Check Figma Links (2 minutes)

Validate all Figma references are correct and accessible:

```
For each Frontend/Design story:
✓ Figma URL is valid format
✓ URL opens and is accessible
✓ node-id points to correct screen/component
✓ Design is complete (not just a wireframe)
✓ Design matches story description
```

**Issues found:**
- Figma file not shared → request access
- Node ID invalid → update with correct ID
- Design incomplete → return to design team

### Step 3: Verify Dependencies (3 minutes)

Confirm all dependencies are available or properly tracked:

```
For each story's dependencies:
✓ All blocked_by stories exist in system
✓ No circular dependencies (check dep graph)
✓ No transitive chains > 3 stories
✓ External dependencies (api:X, database:Y) documented
✓ Related stories are marked correctly

If blocked_by stories exist:
  → confirm they're in earlier sprint
  → add to "Risk" section if missing dates
```

**Red flags:**
- Circular dependency found → escalate, cannot publish
- blocked_by chain > 3 → escalate for decomposition
- Blocking story not scheduled → adjust sprint plan

### Step 4: Confirm with Stakeholders (5 minutes)

Get final approval before publishing:

```
Send message to #product-team:
"Ready to publish these stories:
- STORY-2025-0001: User can search products
- STORY-2025-0015: User can filter results
- STORY-2025-0042: User can share results

Any objections or changes needed?"

Wait for approval or concerns.
If concerns:
  → address issues
  → return to Step 1
```

### Step 5: Create Jira Issues (10 minutes)

For each story, create a Jira issue:

```bash
for each story:
  1. Go to Jira project
  2. Click "Create Issue"
  3. Fill in fields:
     - Summary: Use story title
     - Issue Type: Task (or Bug if story_type: bugfix)
     - Assignee: If story has assignee field, pre-fill (else leave unassigned)
     - Description: Paste story frontmatter + full story text
     - Labels: Add all tags
     - Due Date: If sprint assigned, set sprint end date
     - Components: Link to affected Jira components (if any)
     - Links: Link to related stories
  4. Click Create
  5. Copy generated Jira issue key (e.g., "JIRA-5423")
  6. Update story_id to match: JIRA-5423 → STORY-2025-0001 mapping
```

### Step 6: Link Stories (5 minutes)

Connect related stories and create dependency graph:

```
For each story, in Jira:
  → Link blocked_by stories: Issue Link → "is blocked by"
  → Link blocks stories: Issue Link → "blocks"
  → Link related_stories: Issue Link → "relates to"
  → Add comments with story ACs for reference
```

**Jira link types:**
- "blocks" / "is blocked by": Hard dependency
- "relates to": Soft dependency (parallel work)
- "duplicates" / "is duplicated by": Same work

### Step 7: Verify in Jira (2 minutes)

Check that all data synced correctly:

```
For each story in Jira:
✓ Summary matches title
✓ Description shows full story text
✓ Labels include all tags
✓ Links point to correct related stories
✓ Sprint is assigned (if applicable)
✓ No formatting issues
```

Issues found:
- Description truncated → manually fix
- Links broken → re-create
- Labels missing → add manually

### Step 8: Sprint Assignment (2 minutes)

If not already assigned, add to sprint:

```
For each story:
  → Click "Sprint" field
  → Select correct sprint
  → If no sprint: leave in "Backlog"
  → If future sprint: use "Backlog" until sprint planning
```

### Step 9: Communicate Completion (2 minutes)

Notify team that stories are published:

```
Post to #engineering:
"Published 3 stories to Jira (Sprint 25):
- JIRA-5423: User can search products
- JIRA-5424: User can filter results
- JIRA-5425: User can share results

Ready for assignment and work to begin."
```

## Post-Publication Checklist

After all stories are published:

- [ ] All stories have Jira issue keys
- [ ] All links established in Jira
- [ ] Sprint board updated
- [ ] No orphaned stories in Thresh
- [ ] Team notified
- [ ] Blocked stories identified and highlighted
- [ ] Figma links accessible to entire team

## Common Issues and Resolutions

**"Story points > 8"**
- Solution: Split into smaller stories before publishing
- Example: 13pt epic broken into 3pt + 5pt + 5pt

**"Missing Figma link"**
- Solution: Return to author, request design completion
- Blocking: Cannot publish Frontend story without Figma ref

**"Circular dependency detected"**
- Solution: Escalate, modify dependency relationships
- Example: A blocks B blocks C blocks A → resolve before publishing

**"Blocked story scheduled before blocker"**
- Solution: Adjust sprint assignments in sprint planning
- Example: If Story-5 blocked by Story-3, Story-3 must be earlier sprint

## Success Criteria

Playbook complete when:
- All stories published to Jira
- All frontmatter fields synced
- All dependencies linked
- All stories assigned to sprint
- Team notified and ready to work
- No blocking issues remaining
