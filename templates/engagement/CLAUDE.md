# Thresh Product OS — Client Engagement

> Boot file for a Thresh consulting engagement. Keep this under 80 lines.
> Standards, conventions, and routing rules live in `.claude/rules/`.

## Client Information

- **Client**: [CLIENT NAME]
- **Engagement**: [ENGAGEMENT NAME]
- **Status**: active
- **Start Date**: [YYYY-MM-DD]

## Setup

On first interaction in a new session:
1. Read `.claude/rules/` — these load automatically in Claude Code; in Cowork, read them manually
2. Read `memory/sessions/` — find the most recent file for "previously on..." context
3. Read `jira_config.json` for Jira connection details
4. If any `[PLACEHOLDER]` values remain in this file, run `/thresh-setup` to configure

## Jira

- **Config**: All Jira settings are in `jira_config.json` (cloud ID, project keys, custom fields)
- **Live queries**: Always query current sprint live via JQL
- **Historical data**: Read from `product/metrics/*.json` (updated nightly by scheduled ingest)

## Source of Truth

| Data | Source | Local? |
|------|--------|--------|
| Stories & Epics | Jira (live query) | NO — draft in chat, publish to Jira |
| Sprint Status | Jira (live query) | NO |
| Documents | Google Drive | NO — search, don't copy |
| Designs | Figma | NO — reference via MCP |
| Context summaries | `product/context/*.json` | YES — populated by /ingest |
| Dependency graph | `product/work_graph.json` | YES — maintained by /ingest + /publish |
| Metrics & trends | `product/metrics/*.json` | YES — updated by scheduled tasks |
| Customer data | `product/customer_data/` | YES — populated by /thresh-synthesize |
| Feedback triage | `product/customer_data/feedback_triage.json` | YES — populated by /thresh-feedback |
| Opportunity tree | `product/opportunity_tree.json` | YES — populated by /thresh-opportunities |
| Prioritization | `product/prioritization.json` | YES — populated by /thresh-prioritize |
| Decisions | `product/context/decisions/` | YES |

## Key Rules

1. **Never create local markdown files for stories.** Draft in chat, publish to Jira.
2. **Never store document copies locally.** Search Google Drive.
3. **Always query Jira live** for current sprint data.
4. **Read JSON files** for historical metrics — they're more precise than markdown.
5. **Write session summaries** to `memory/sessions/` at end of every session.

## Workflows

| Workflow | Skill | What It Does |
|----------|-------|-------------|
| **Discovery & Synthesis** | | |
| Synthesize | `/thresh-synthesize` | Mass customer data ingestion → pain points → features |
| Interview | `/thresh-interview` | Prepare interview scripts + process transcripts |
| Feedback | `/thresh-feedback` | Bulk triage of feature requests, tickets, reviews |
| Opportunities | `/thresh-opportunities` | Build evidence-backed Opportunity Solution Trees |
| Prioritize | `/thresh-prioritize` | Evidence-based feature prioritization (RICE, ICE, etc.) |
| **Execution & Delivery** | | |
| Ingest | `/thresh-ingest` | Pull context from Jira/Figma/Drive into local files |
| Briefing | `/thresh-briefing` | Morning intelligence report |
| Decompose | `/thresh-decompose` | Break Figma designs into sized, linked stories |
| Refine | `/thresh-refine` | Facilitate refinement sessions |
| Publish | `/thresh-publish` | Push stories/epics to Jira with linking |
| Decisions | `/thresh-decisions` | Capture informal decisions |
| Team Health | `/thresh-team-health` | Developer profiles and assignment recs |
| Forecast | `/thresh-forecast` | Sprint completion predictions |
| Risk | `/thresh-risk` | Per-story risk scoring |
| Reconcile | `/thresh-reconcile` | Reconcile roadmap against backlog |

## Required Connectors

| Connector | Required? | Purpose |
|-----------|-----------|---------|
| Atlassian | YES | Jira read/write |
| Google Drive | Recommended | Document search (or upload files directly) |
| Figma | If designs | Design file access |
| Slack | Recommended | Team communication |
