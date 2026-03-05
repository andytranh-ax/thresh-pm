---
name: thresh-publish
description: Validates stories have Figma links and dependency mappings, then creates issues in Jira with full story content and linked relationships. Trigger with "publish", "publish to jira", "push stories", "sync to jira", "create jira issues", or "push to jira".
---

# thresh-publish

Publishes local stories to Jira with complete content fidelity and proper dependency linking. Validates Figma links and relationship mappings before creating issues.

## Quick Steps

1. Validate all stories have figma_ref (block if missing)
2. Identify story relationships (relates_to, blocks, is_blocked_by)
3. Confirm dependency summary with user
4. Populate local frontmatter with relationship metadata
5. Use createJiraIssue to create each issue with full story content
6. Preserve GIVEN/WHEN/THEN structure and all technical notes
7. Create issue links for all dependencies
8. Calculate and display impact radius for each story
9. Confirm with user before final publish
10. Report completion with issue keys

For the full step-by-step workflow, read `references/workflow.md`.
