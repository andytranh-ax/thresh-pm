# Thresh PM — Product OS Plugin

Agentic PM operating system for consulting engagements. Built for Claude Cowork and Claude Code.

**[Read the full User Guide →](https://andytranh-ax.github.io/thresh-pm/)**

## Install

### Cowork (Desktop App)
1. Open **Customize** → **Browse plugins** → **Personal** tab
2. Click **+** → **Add marketplace from GitHub**
3. Enter: `andytranh-ax/thresh-pm`
4. Click **Sync**, then install from the card

### Claude Code (CLI)
```bash
claude plugin marketplace add andytranh-ax/thresh-pm
claude plugin install thresh-pm@thresh-pm
```

## What's Included

### 15 Skills

**Discovery & Synthesis**
| Skill | Purpose |
|-------|---------|
| `/thresh-synthesize` | Mass customer data ingestion → pain points → themes → feature candidates |
| `/thresh-interview` | Prepare targeted interview scripts + process transcripts into structured signals |
| `/thresh-feedback` | Bulk triage of feature requests, support tickets, NPS, reviews |
| `/thresh-opportunities` | Build Opportunity Solution Trees backed by real evidence data |
| `/thresh-prioritize` | Evidence-based feature prioritization (RICE, ICE, Value/Complexity, MoSCoW) |

**Execution & Delivery**
| Skill | Purpose |
|-------|---------|
| `/thresh-ingest` | Pull context from Jira, Figma, Drive into structured local files |
| `/thresh-briefing` | Morning intelligence report — sprint status, blockers, decisions needed |
| `/thresh-decompose` | Break Figma designs into sized, dependency-linked stories |
| `/thresh-refine` | Facilitate refinement sessions with quality scoring |
| `/thresh-publish` | Push stories to Jira with field mapping |
| `/thresh-decisions` | Capture informal decisions from meetings/Slack |
| `/thresh-team-health` | Developer profiles, assignment recommendations, bus factor |
| `/thresh-forecast` | Sprint completion predictions using velocity + work graph |
| `/thresh-risk` | Per-story risk scoring across 4 dimensions |
| `/thresh-reconcile` | Roadmap vs backlog reconciliation — gaps, orphans, capacity |

### 17 Commands
`/thresh-setup` · `/thresh-ingest` · `/thresh-briefing` · `/thresh-decompose` · `/thresh-refine` · `/thresh-publish` · `/thresh-publish-to-jira` · `/thresh-decisions` · `/thresh-team-health` · `/thresh-forecast` · `/thresh-risk` · `/thresh-synthesize` · `/thresh-reconcile` · `/thresh-interview` · `/thresh-prioritize` · `/thresh-opportunities` · `/thresh-feedback`

### 7 Agents
Story writer · Quality gate reviewer · Change impact analyzer · Product drift detector · Decision candidate detector · Offboard intelligence synthesizer · Untrusted text scanner

### Supporting Infrastructure
- 11 JSON schemas for data validation
- 5 modular rule files (auto-loaded in Claude Code)
- 12 standards documents
- 9 playbooks
- 2 Python linters

## The Pipeline

Thresh skills chain together into a full discovery-to-delivery pipeline:

```
Customer Data → /thresh-feedback → /thresh-synthesize → /thresh-opportunities
                                          ↓
                                  /thresh-prioritize → /thresh-reconcile
                                          ↓                    ↓
                                  /thresh-decompose    Roadmap alignment
                                          ↓
                                  /thresh-refine → /thresh-publish → Jira
                                                          ↓
                              /thresh-briefing ← /thresh-ingest ← Jira
```

## Quick Start

1. Install the plugin
2. Run `/thresh-setup` to initialize a new engagement
3. Run `/thresh-ingest` to pull initial context from Jira
4. Drop customer research files into `product/customer_data/raw/`
5. Run `/thresh-feedback` to triage incoming feedback
6. Run `/thresh-synthesize` to extract pain points and feature candidates
7. Run `/thresh-opportunities` to build an evidence-backed opportunity tree
8. Run `/thresh-prioritize` to rank features using real data
9. Run `/thresh-reconcile` to compare against the backlog
10. Run `/thresh-decompose` to turn top features into stories

## Works With

- **phuryn/pm-skills** — Use their strategy frameworks (SWOT, business model, pricing, PESTLE) alongside Thresh's data pipeline. Thresh handles structured data; phuryn handles thinking frameworks.
- **Atlassian connector** — Required for Jira integration
- **Google Drive connector** — Optional, for searching client docs without copying locally
- **Figma connector** — Optional, for design decomposition
- **Slack connector** — Optional, for feedback and decision capture

## Engagement Template

Run `/thresh-setup` to scaffold the per-client directory structure:

```
CLAUDE.md                          ← Boot file (auto-configured)
jira_config.json                   ← Jira connection details
memory/
  MEMORY.md                        ← Auto-memory (Claude updates across sessions)
  sessions/                        ← Session summaries
product/
  work_graph.json                  ← Dependency graph
  reconciliation.json              ← Roadmap vs backlog
  opportunity_tree.json            ← OST linked to evidence
  prioritization.json              ← Ranked feature list
  context/                         ← Structured context (md + json pairs)
  metrics/                         ← Velocity, team profiles, estimation accuracy
  customer_data/
    raw/                           ← Drop customer research files here
      interviews/                  ← Interview transcripts
      surveys/                     ← Survey exports
      tickets/                     ← Support ticket exports
      nps/                         ← NPS/CSAT data
      reviews/                     ← App store reviews
      analytics/                   ← Analytics summaries
    processed/                     ← Structured extractions per source
    synthesis.json                 ← Master synthesis: themes, pain points, features
    feedback_triage.json           ← Latest triage report
  roadmap/                         ← Roadmap source docs
deliverables/                      ← Reports and outputs
```

## Why Thresh Instead of Generic PM Skills?

Generic PM skills (like phuryn's) give you frameworks as standalone exercises — you run a prioritization, get markdown output, and it's done. Thresh is different:

1. **Structured data pipeline** — Everything writes to JSON with schemas. Your synthesis feeds your prioritization feeds your roadmap reconciliation feeds your story decomposition.
2. **Jira-native** — Stories aren't markdown files. They're Jira issues with real sprints, real assignments, real velocity data.
3. **Evidence chain** — Every story traces back through: solution → opportunity → theme → customer quote. No "we built this because someone said so."
4. **Incremental** — Synthesis, feedback, and reconciliation all support incremental updates. Process new data without restarting from scratch.
5. **Context-managed** — Rules tell Claude exactly which files to load per task. No context window overflow on large engagements.
