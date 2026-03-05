# Story Writing Rules

When writing user stories, ALWAYS follow these conventions:

## Format
- YAML frontmatter with all fields from `${CLAUDE_PLUGIN_ROOT}/standards/frontmatter_schema.md`
- User story in "As a / I want / So that" format
- Acceptance criteria in GIVEN/WHEN/THEN format, numbered AC1, AC2, AC3...
- Edge cases numbered AC-E1, AC-E2, AC-E3...

## Required Edge Cases (minimum 5 per story)
- Empty state, loading state, error state, offline state, accessibility
- Mark 2-3 as [RECOMMENDED] for team review before dev

## Sizing
- Fibonacci: 1, 2, 3, 5, 8, 13
- Stories > 8pt are red flags — suggest splitting
- Stories > 13pt MUST be split before publishing

## Quality Gate
- Minimum 20/24 points to pass (see `${CLAUDE_PLUGIN_ROOT}/agents/reviewer_quality_gate_agent.md`)
- Auto-fail: missing Figma ref, < 3 ACs, < 5 edge cases, circular dependencies

## Components
- Check `product/context/ui_registry.json` before declaring any component as "new"
- Search Jira for existing components with similar names
- Use component IDs from the registry (CMP-XXX format)

## Dependencies
- Check `product/work_graph.json` for existing dependency chains
- No chains longer than 3 stories — flag for resolution
- Update work graph when publishing new stories

## Publishing
- NEVER save stories as local markdown files
- Draft in chat, then publish to Jira via `/thresh-publish`
- Preserve GIVEN/WHEN/THEN structure in Jira description
