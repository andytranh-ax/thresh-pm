---
name: thresh-ingest
description: Pull context from Jira, Figma, Drive into local JSON files. Smart re-runs detect deltas since last sync. Trigger with "ingest", "pull context", "sync sources", "import from jira", "discovery".
---

# thresh-ingest

Populates `product/context/` and `product/metrics/` from live data sources.
First run does full discovery. Re-runs pull only changes since watermark.

## Prerequisites
- Jira connected (verify: `getAccessibleAtlassianResources`)
- `jira_config.json` has cloud_id and project keys
- `product/context/` directory exists

## Quick Steps

1. Read `product/context/.ingest_state.json` — if missing, this is a full run
2. Read `jira_config.json` for connection details
3. Query each connected source (Jira, Figma, Drive) with appropriate scope
4. For each context file, write `.json` — structured data matching schema in `${CLAUDE_PLUGIN_ROOT}/schemas/`
5. Rebuild `product/work_graph.json` from Jira issue links
6. Update `product/metrics/velocity.json` from sprint history
7. Update `product/metrics/team_profiles.json` from assignee data
8. Write `.ingest_state.json` with new watermark
9. Write session summary to `memory/sessions/`
10. Present findings with next-step options

## JSON-Only Rule

All context files are JSON-only. Claude presents data conversationally when the PM asks. No duplicate markdown files.

| File | JSON Schema | Key Fields |
|------|------------|------------|
| glossary.json | (freeform) | terms, definitions, sources |
| technical_atlas.json | (freeform) | systems, APIs, integrations |
| stakeholders.json | (freeform) | names, roles, jira_usernames |
| ui_registry.json | ui_registry.schema.json | screens, components, figma_node_ids |
| .ingest_state.json | ingest_state.schema.json | watermark, sources, change_log |

## Large Backlog Mode (100+ stories)

When the Jira project has 100+ issues, standard ingestion will overflow context. Use batch mode:

### Detection
After the first JQL count query (`project = [KEY]`), if total > 100 issues:
```
"This project has [N] issues. I'll process them in batches of 50 to avoid context overflow."
```

### Batch Processing
1. **Query in pages**: Use `startAt` and `maxResults=50` in JQL pagination
2. **Per batch**: Extract context signals (glossary terms, stakeholders, components) and write to intermediate file `product/customer_data/intermediate/ingest_batch_[N].json`
3. **Work graph assembly**: After all batches, read intermediates and assemble `product/work_graph.json` — process edges per epic group, not all at once
4. **Progressive updates**: Update `.ingest_state.json` after each batch with `batches_completed` count, so interrupted runs can resume

### Batch Work Graph Strategy
For 500+ stories, building the full dependency graph in one pass is impossible. Instead:
1. First pass: Create all nodes (story key, title, type, status, points, assignee)
2. Second pass: Query issue links in batches of 50, add edges
3. Third pass: Calculate critical_path and unblocked_stories from the assembled graph
4. Write work_graph.json once at the end from the assembled intermediates

### Memory Rules
- Never hold more than 50 raw Jira responses in context at once
- Write intermediate results after each batch, then clear from context
- For very large projects (1000+), offer to scope: "Want me to ingest everything, or focus on active sprints + recent 90 days?"

## On Error
- If Jira fails: skip Jira, continue other sources, report failure
- If a context file is locked: write to `.ingest_pending.json`, merge next run
- If a batch fails: log the batch number, skip to next, retry failed batch at end

## Rules
- **Merge, don't overwrite** — add new entries without removing existing ones
- **Flag conflicts** — if new data contradicts existing context, ask the user
- **Never auto-create stories** — summarize findings first, ask permission

For detailed step-by-step: `references/workflow.md`
