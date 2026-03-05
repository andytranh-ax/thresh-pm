# Protocol of Verification

Quality gates and verification checkpoints throughout the story lifecycle. Ensures stories are properly validated before development, review, and publication.

## Pre-Development Gate

Before a story moves to "In Progress", verify:

**Story Completeness**
- [ ] YAML frontmatter is complete and valid
- [ ] Title is action-oriented ("User can X" not "Implement X")
- [ ] Acceptance criteria follow GIVEN/WHEN/THEN format
- [ ] All AC are specific and measurable (no vague language)
- [ ] At least one AC describes happy path success
- [ ] At least 2-3 edge case ACs (AC-E1, AC-E2, etc.)
- [ ] Edge case ACs cover: empty state, error state, boundary conditions, accessibility (if applicable), performance (if applicable)
- [ ] ACs are marked [RECOMMENDED] where appropriate for team review

**Design Validation**
- [ ] figma_ref link is valid and points to correct screen/component
- [ ] Figma design is complete and matches story description
- [ ] ux_id is linked (for Frontend/Design stories)
- [ ] Design is signed off by design lead

**Dependencies Mapped**
- [ ] No circular dependencies
- [ ] blocked_by stories are scheduled before this story
- [ ] external dependencies are available or tracked
- [ ] related_stories are correctly identified (parallel work)
- [ ] All dependencies documented in story

**Points Assigned**
- [ ] Story has Fibonacci point estimate (1, 2, 3, 5, 8, 13)
- [ ] Story > 8pts is marked for splitting
- [ ] Estimate discussed in team estimation session

**Components Listed**
- [ ] All UI components are listed and exist
- [ ] All backend/API components are listed
- [ ] Component IDs follow naming convention (CMP-XXX)

**Metadata Complete**
- [ ] Tags include at least 1 domain + 1 type tag
- [ ] Priority is set (Critical, High, Medium, Low)
- [ ] Category is set (Frontend, Backend, Full-stack, Design, Data, Infrastructure)
- [ ] story_type is set (feature, bugfix, refactor, chore, spike, tech-debt)
- [ ] Sprint is assigned (or "Backlog" if future sprint)

**Sign-Off**
- [ ] Product Manager has reviewed and approved
- [ ] Design Lead has reviewed (for Design/Frontend stories)
- [ ] Tech Lead has reviewed dependencies (for Backend/Infrastructure stories)

## Pre-Review Gate (Before QA/Code Review)

Before code review and QA, verify:

**Acceptance Criteria Coverage**
- [ ] All functional ACs have automated test cases (unit, integration, or e2e)
- [ ] All edge case ACs have corresponding test cases
- [ ] Test coverage report shows coverage for all AC
- [ ] QA has test plan matching each AC

**Edge Cases Tested**
- [ ] Empty state scenarios tested
- [ ] Error scenarios tested (API errors, validation errors, etc.)
- [ ] Boundary conditions tested (max length, special characters, etc.)
- [ ] Offline/loading states tested (if applicable)
- [ ] Accessibility tested (keyboard nav, screen reader, color contrast)
- [ ] Performance tested against targets (if applicable)

**Code Quality**
- [ ] No lint warnings or errors (eslint, prettier, etc.)
- [ ] No console errors or warnings
- [ ] Code follows team style guide
- [ ] Comments added for non-obvious logic
- [ ] No debug code left in (console.log, debugger, etc.)

**Design Fidelity**
- [ ] Implementation matches Figma design exactly
- [ ] Colors, spacing, typography match design tokens
- [ ] Responsive behavior matches design breakpoints
- [ ] Interactions match design (hover states, transitions, etc.)

**Documentation**
- [ ] Code comments explain complex logic
- [ ] API changes documented (if backend)
- [ ] Database schema changes documented (if applicable)
- [ ] Setup or deployment instructions updated (if needed)

## Pre-Publish Gate (Before Merging to Main)

Before publishing (merging to main branch), verify:

**Final Validation**
- [ ] All ACs have passed QA
- [ ] All test cases passing (unit, integration, e2e, visual regression)
- [ ] Code review approved
- [ ] Design review approved
- [ ] No merge conflicts
- [ ] Main branch is green (all CI checks passing)

**Figma Reference Validated**
- [ ] Figma node ID in figma_ref is correct and still valid
- [ ] Figma design matches implemented feature
- [ ] Figma link is accessible to team

**Dependency Graph Checked**
- [ ] No new circular dependencies introduced
- [ ] All blocked_by dependencies have been completed
- [ ] Related stories have been notified of changes
- [ ] Impact radius calculated (how many other stories/systems affected)

**Impact Radius Calculated**
- [ ] Identified all downstream stories that depend on this
- [ ] Identified all components or systems that depend on this
- [ ] Documented any breaking changes
- [ ] Communicated changes to dependent teams (if cross-team)

**Release Notes**
- [ ] Story added to release notes (if customer-facing)
- [ ] Change description is clear and non-technical
- [ ] Any deprecations or breaking changes called out
- [ ] Links to documentation (if applicable)

## Post-Publish Gate (After Merging)

After story is merged, verify:

**Jira Issue Created**
- [ ] Jira ticket exists with story_id as key
- [ ] All frontmatter fields synced to Jira
- [ ] Story status updated to "Done"
- [ ] Merge commit linked in Jira

**Links Established**
- [ ] linked_story populated (for bugfixes)
- [ ] related_stories linked in both directions
- [ ] Figma reference linked in Jira
- [ ] Pull request linked in Jira

**Sprint Assignment**
- [ ] Story assigned to correct sprint
- [ ] Sprint board updated
- [ ] Burndown chart reflects completion
- [ ] Metrics captured (velocity, cycle time, etc.)

**Notifications Sent**
- [ ] QA team notified of completion (if verification needed)
- [ ] Product team notified (if stakeholder communication needed)
- [ ] Dependent teams notified (if cross-team impact)

**Monitoring Setup**
- [ ] Error tracking configured (Sentry, etc.)
- [ ] Performance monitoring configured (if applicable)
- [ ] Analytics tracking verified (if applicable)
- [ ] Alerting setup for critical issues

## Verification Checklist Template

Use this checklist in code review comments:

```markdown
## Pre-Review Checklist

- [ ] All ACs have test cases
- [ ] Edge cases covered
- [ ] No lint errors
- [ ] Design matches Figma
- [ ] Accessible (keyboard, screen reader)
- [ ] Performance acceptable

## Pre-Merge Checklist

- [ ] All tests passing
- [ ] Code review approved
- [ ] Design review approved
- [ ] Figma reference validated
- [ ] Dependencies resolved
- [ ] Release notes updated

## Post-Merge Checklist

- [ ] Jira issue created
- [ ] Story status updated
- [ ] Related stories linked
- [ ] Sprint updated
- [ ] Team notified
```

## Common Verification Failures

### Failed Pre-Development Gate
- Story sent back for complete ACs
- Story lacks design reference
- Circular dependencies detected → must resolve before starting

### Failed Pre-Review Gate
- Test cases missing → development paused until tests written
- Design doesn't match → rework required
- Lint errors → must be fixed

### Failed Pre-Publish Gate
- Test failures → must debug and fix
- Merge conflicts → resolve conflicts
- Breaking changes not documented → must update
- Performance targets not met → must optimize

## Who Verifies

- **Pre-Development**: Product Manager, Design Lead, Tech Lead
- **Pre-Review**: Developer, QA
- **Pre-Publish**: Code Reviewer, QA Lead, Design Reviewer
- **Post-Publish**: QA, Product Manager, DevOps (for deployment)
