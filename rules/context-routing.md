# Context Routing

Load ONLY the files relevant to the current task. This prevents context window overflow.

## Data Format Rule

All context files are JSON-only. No duplicate markdown files. When the PM asks to see data, read the JSON and present it conversationally.

## Default (every session)
- CLAUDE.md (auto-loaded)
- .claude/rules/ (auto-loaded in Claude Code; read manually in Cowork)
- memory/MEMORY.md (first 200 lines, if exists)
- memory/sessions/ (most recent file only)

## By Task Type

### Sprint status, briefing, standup
- Load: product/metrics/velocity.json
- Load: product/context/.ingest_state.json
- Load: product/context/glossary.json (use client terminology in updates)
- Query: Jira live for current sprint

### Writing or refining stories
- Load: product/context/ui_registry.json (component lookup)
- Load: product/context/glossary.json (use client terminology in stories)
- Load: product/context/technical_atlas.json (platform constraints for ACs)
- Load: product/work_graph.json (dependency check)
- Reference: ${CLAUDE_PLUGIN_ROOT}/standards/story_standards.md (if needed for format)

### Team capacity, assignments, workload
- Load: product/metrics/team_profiles.json
- Load: product/context/stakeholders.json (name/role context)

### Decisions
- Load: product/context/glossary.json (use client terminology)
- Load: product/context/stakeholders.json (decision makers)
- Scan: product/context/decisions/ filenames
- Load: only the relevant decision files

### Decomposing designs (Figma → stories → Jira)
- Load: product/context/ui_registry.json (component dedup)
- Load: product/context/technical_atlas.json (platform constraints)
- Load: product/context/glossary.json (naming consistency)
- Load: product/work_graph.json (existing dependencies)
- Load: jira_config.json (project key, custom fields)
- Query: Figma via MCP (get_design_context, get_screenshot)
- Query: Jira for existing epics/stories/components
- Write to: product/work_graph.json (new nodes + edges)
- Write to: product/context/ui_registry.json (new screens/components)
- Chain: /thresh-publish to create Jira issues

### Forecasting or risk analysis
- Load: product/metrics/velocity.json
- Load: product/metrics/team_profiles.json
- Load: product/work_graph.json

### Ingesting context
- Load: product/context/.ingest_state.json (watermark)
- Load: jira_config.json (connection details)
- Write to: all product/context/*.json files

### Customer data synthesis
- Scan: product/customer_data/raw/ for file inventory
- Load: product/customer_data/synthesis.json (if exists, for incremental mode)
- Load: product/context/glossary.json (normalize terminology)
- Do NOT load raw files into context — process in batches via skill
- Write to: product/customer_data/synthesis.json

### Roadmap reconciliation
- Load: product/customer_data/synthesis.json (if exists, for customer evidence)
- Load: product/context/discovery_summary.json (product goals and vision)
- Load: product/reconciliation.json (if exists, for delta comparison)
- Load: product/work_graph.json (dependency context)
- Load: product/metrics/velocity.json (capacity constraints)
- Query: Jira live for full backlog
- Query: Google Drive for roadmap doc (or check product/roadmap/)

### Interview preparation or transcript processing
- Load: product/customer_data/synthesis.json (identify evidence gaps)
- Load: product/context/stakeholders.json (interviewee context)
- Load: product/context/glossary.json (customer language)
- For transcript processing: read ONE transcript at a time, never batch into context

### Feature prioritization
- Load: product/customer_data/synthesis.json (evidence scores)
- Load: product/context/discovery_summary.json (strategic alignment)
- Load: product/work_graph.json (dependency constraints)
- Load: product/metrics/velocity.json (capacity)
- Load: product/metrics/team_profiles.json (skill constraints)
- Load: product/prioritization.json (if exists, for comparison)
- Query: Jira live for backlog items (in batches if > 50)

### Opportunity solution tree
- Load: product/customer_data/synthesis.json (themes → opportunities)
- Load: product/context/discovery_summary.json (outcome goals)
- Load: product/work_graph.json (existing story coverage)
- Load: product/opportunity_tree.json (if exists, for updates)
- Load: product/prioritization.json (if exists, for ranking)

### Feedback triage
- Scan: product/customer_data/raw/ for new feedback files
- Load: product/customer_data/synthesis.json (theme matching)
- Load: product/context/glossary.json (normalize terminology)
- Load: product/work_graph.json (story matching)
- Do NOT load full CSVs into context — use Python pandas for large files
- Write to: product/customer_data/feedback_triage.json

### "Catch me up" or new session orientation
- Load: memory/sessions/ (last 3 files)
- Load: product/metrics/velocity.json (current state)
- Optionally run: /thresh-briefing
