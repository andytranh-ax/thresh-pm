# /ingest — Client Discovery & Context Population

Pull from Jira, Figma, Google Drive, and data files to populate context files. Smart about re-runs — only pulls new or changed data after the first run.

## How It Works

```
First run:   Pull everything → Populate all context files → Save watermark
Re-runs:     Pull only changes since last watermark → Merge into existing files
```

---

## Step 1: Check Ingest State

Read `product/context/.ingest_state.json` to determine if this is a first run or a re-run.

**If the file doesn't exist** → First run. Pull everything. Set `mode = full`.
**If the file exists** → Re-run. Read the `last_ingest` date and set `mode = incremental`.

```
Agent: [First run detected — I'll do a full discovery across all sources.]
-- or --
Agent: [Last ingest was 2026-01-15. I'll pull only changes since then.]
```

---

## Step 2: Check Connected Sources

```
Agent: Checking sources...
       ✅ Jira — Connected (Cloud ID: [from CLAUDE.md])
       ✅ Figma — Connected ([X] files configured)
       ✅ Google Drive — Connected
       ❌ [Any source not connected — skip gracefully]
```

---

## Step 3: Pull from Jira

**Full mode:** Query all issues to build initial context.
**Incremental mode:** Query only issues updated since last ingest.

### Full Mode Queries

| Context File | JQL | What to Extract |
|-------------|-----|----------------|
| glossary.json | `project = [KEY] ORDER BY created ASC` | Domain terms, acronyms, business rule language from summaries and descriptions |
| technical_atlas.json | `project = [KEY] AND (labels in (api, backend, frontend, infrastructure) OR summary ~ "API" OR summary ~ "integration")` | API names, systems, tech stack references |
| stakeholders.json | `project = [KEY] AND updated >= -30d` | Unique assignees and reporters |
| ui_registry.json | `project = [KEY] AND (labels in (design, ui, ux) OR summary ~ "screen" OR summary ~ "page" OR summary ~ "component")` | Screen names, component refs, flow names |

### Incremental Mode Queries

Same queries but add `AND updated >= "[LAST_INGEST_DATE]"` to each one. Only extract NEW terms, people, or components not already in the context files.

```
Agent: [Incremental] Checking Jira for changes since [LAST_INGEST_DATE]...
       Found [X] updated issues. Extracting new context...
       • 3 new terms added to glossary
       • 1 new stakeholder added
       • 0 new screens (no UI changes)
```

---

## Step 4: Pull from Figma

**Full mode:** Read all configured Figma files — extract screens, components, flows, and text.
**Incremental mode:** Read Figma files and compare against existing ui_registry.json. Only add screens/components that aren't already listed.

| Context File | What to Extract |
|-------------|----------------|
| ui_registry.json | Screen names from top-level frames, component names, page→flow mapping, Figma node IDs |
| glossary.json | Recurring terms from text layers, button labels, feature names not already in glossary |

---

## Step 5: Pull from Google Drive

Search Google Drive for client documents. Documents stay in Drive — Claude reads them on demand.

**Full mode:** Search broadly.
```
google_drive_search: "[CLIENT NAME] PRD"
google_drive_search: "[CLIENT NAME] SOW"
google_drive_search: "[CLIENT NAME] requirements"
google_drive_search: "[CLIENT NAME] spec"
```

**Incremental mode:** Search for recently modified documents only.
```
google_drive_search with order_by: "modifiedTime desc"
```
Compare results against the document list in `.ingest_state.json`. Only fetch and process documents not previously ingested.

For each document found, extract into context files:

| Extract Into | What to Look For |
|-------------|-----------------|
| glossary.json | Domain terms, acronyms, business rules |
| technical_atlas.json | Tech stack, APIs, architecture, integration points |
| stakeholders.json | Names, roles, communication preferences |
| discovery_summary.json | Scope, goals, constraints, timeline, success metrics |
| ui_registry.json | Screen names, flows, component references |

---

## Step 6: Profile Data Files (if any)

**Full mode:** Profile all Excel/CSV files found in the mounted folder.
**Incremental mode:** Only profile files not already in `data_catalog.json`.

For each new data file:
- Use the `explore-data` skill to profile it (sheets, columns, row counts, data types)
- Write a one-line entry into `product/context/data_catalog.json`

For deeper data setup, suggest running the `data-context-extractor` skill.

---

## Step 7: Write Context Files

**CRITICAL: Merge, don't overwrite.**

- If a context file already has content, ADD new entries without removing existing ones
- If a term/person/screen already exists, UPDATE it only if the new data is more complete
- Flag conflicts: "glossary.json already defines 'MVNO' differently — which is correct?"

---

## Step 8: Update Ingest State

Write `product/context/.ingest_state.json`:

```json
{
  "last_ingest": "[ISO DATE]",
  "mode": "full | incremental",
  "sources_used": ["jira", "figma", "drive", "data"],
  "jira_issues_scanned": 0,
  "drive_docs_processed": [],
  "figma_files_processed": [],
  "data_files_profiled": [],
  "change_log": [
    { "date": "[ISO DATE]", "mode": "full", "summary": "Added [X] terms, [Y] stakeholders, [Z] screens" }
  ]
}
```

---

## Step 9: Present Findings

```
Agent: 📊 Ingest Complete! [Full / Incremental since LAST_DATE]

       Changes:
       • glossary.json — [X] new terms
       • technical_atlas.json — [X] new systems/APIs
       • stakeholders.json — [X] new people
       • ui_registry.json — [X] new screens, [Y] components
       • data_catalog.json — [X] new datasets profiled
       • discovery_summary.json — [Updated / No changes]

       ❓ Want to:
       ├── [A] Review a specific context file
       ├── [B] Start /decompose on Figma designs
       ├── [C] Save and stop
       └── [D] Re-run as full ingest (ignores watermark)
```

---

## Rules

> **NEVER auto-create stories.** Summarize findings first and ask permission.

> **Merge, don't overwrite.** Every re-run adds to existing context — never deletes.

> **Flag conflicts.** If new data contradicts existing context, ask the user.

> **Option D exists.** If the user says "re-run everything" or "full ingest", ignore the watermark and do a full scan.
