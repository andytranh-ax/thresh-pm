# /thresh-setup

Full guided setup for a new Thresh engagement. Handles connectors, engagement scaffolding, context seeding, and first ingest.

## Overview
This is the ONE command a PM runs when starting a new client engagement. It walks them through everything — connecting tools, creating the folder structure, seeding context (glossary, stakeholders, product vision, designs, customer data), configuring Jira, and pulling initial data. The PM should be able to go from "just installed the plugin" to "productive first session" in one sitting.

## Phase 1: Connectors

Before creating any files, ensure the PM has the required connectors enabled. Check each one and guide them through setup if missing.

### Required: Atlassian (Jira)
1. Check if the Atlassian connector is available by attempting a simple Jira query
2. If NOT connected:
   - Tell the PM: "I need access to Jira. Let me help you connect it."
   - In Cowork: Guide them to Customize → Connectors → Atlassian → Connect
   - In Claude Code: Guide them to install the Atlassian MCP server
   - Wait for confirmation before proceeding
3. If connected: Confirm "✓ Jira connected" and move on

### Recommended: Google Drive
1. Ask: "Do you have client documents in Google Drive you'd like me to search? (roadmaps, PRDs, meeting notes)"
2. If yes and NOT connected:
   - Tell the PM: "Let me help you connect Google Drive so I can search for docs."
   - In Cowork: Guide them to Customize → Connectors → Google Drive → Connect
   - In Claude Code: Guide them to install the Google Drive MCP server
3. If connected: Confirm "✓ Google Drive connected"
4. If no: Skip — the PM can upload docs directly or place them in the engagement folder

### Optional: Figma
1. Ask: "Will this engagement involve Figma designs?"
2. If yes and NOT connected:
   - Guide them to Customize → Connectors → Figma → Connect
3. If no: Skip, note in CLAUDE.md that Figma is not in use

### Optional: Slack
1. Ask: "Do you want me to be able to pull context from Slack?"
2. If yes and NOT connected:
   - Guide them to Customize → Connectors → Slack → Connect
3. If no: Skip

### Connector Summary
After checking all connectors, confirm:
```
✓ Jira — connected
✓ Google Drive — connected (or ○ skipped)
○ Figma — skipped (not needed)
○ Slack — skipped
```

## Phase 2: Engagement Info

Ask the PM 3-4 questions. Use a natural conversational flow, not a form:

1. **"What's the client name?"** (e.g., "Acme Corp")
2. **"What's the engagement called?"** (e.g., "Mobile App Redesign")
3. **"What's the Jira project key?"** (e.g., "ACME")
   - If unsure, query Jira to list available projects and let them pick
4. **"Any other Jira project keys I should know about?"** (some engagements span multiple projects)

### Auto-detect from Jira
Once we have the project key, query Jira to auto-detect:
- Cloud ID (from the connection)
- Instance URL
- Available issue types
- Custom field IDs for story points, sprint, epic link (query an existing issue and inspect fields)
- Workflow statuses (query project workflow scheme)

This eliminates the "verify jira_config.json" friction — we populate it with real values, not guesses.

## Phase 3: Create Engagement Structure

Create all directories and files in the current folder. Adapt based on what we learned in Phase 1-2:

### Directories
```
.claude/rules/
memory/sessions/
product/context/decisions/
product/metrics/
product/customer_data/raw/interviews/
product/customer_data/raw/surveys/
product/customer_data/raw/tickets/
product/customer_data/raw/nps/
product/customer_data/raw/reviews/
product/customer_data/raw/analytics/
product/customer_data/processed/
product/customer_data/intermediate/
product/roadmap/
deliverables/
```

### CLAUDE.md
Generate from the template in the plugin, filling in:
- Client name, engagement name, start date
- Remove Figma rows from Source of Truth table if Figma is not connected
- Remove Slack from Required Connectors if not connected
- Add any additional Jira project keys

### jira_config.json
Populate with REAL values auto-detected from Jira:
```json
{
  "schema_version": "1.0",
  "cloud_id": "<auto-detected>",
  "instance_url": "<auto-detected>",
  "projects": ["<selected-key>", "<any-additional-keys>"],
  "custom_fields": {
    "story_points": "<auto-detected field ID>",
    "sprint": "<auto-detected field ID>",
    "epic_link": "<auto-detected field ID>",
    "acceptance_criteria": "<auto-detected or null>"
  },
  "workflows": {
    "story": ["<auto-detected statuses>"],
    "bug": ["<auto-detected statuses>"]
  },
  "issue_types": "<auto-detected>"
}
```

### .claude/rules/
Copy all 5 rule files from the plugin:
- story-writing.md
- jira-conventions.md
- quality-gates.md
- context-routing.md
- client-overrides.md

### Empty Data Templates
Create all JSON templates with `"last_updated": null` and empty arrays:
- `product/work_graph.json`
- `product/metrics/velocity.json`
- `product/metrics/team_profiles.json`
- `product/metrics/estimation_accuracy.json`
- `product/context/.ingest_state.json`

### Context Files (JSON-only)
Create empty JSON templates for each:
- `product/context/glossary.json`
- `product/context/stakeholders.json`
- `product/context/technical_atlas.json`
- `product/context/ui_registry.json`
- `product/context/data_catalog.json`
- `product/context/discovery_summary.json`

### Memory
- `memory/MEMORY.md` — auto-memory file with engagement start date
- `memory/sessions/.session-template.md` — template for session summaries

### Other
- `.gitignore` — exclude .DS_Store, __pycache__, MEMORY.md, intermediate/, .env

## Phase 4: Seed Context

The empty context files are useless without initial content. Before pulling Jira data, ask the PM to seed the engagement with what they already know. This is the difference between a cold start and a productive first day.

Present this as a single conversational prompt — NOT a form:

```
Now let's give me some context so I'm useful from day one.
Share whatever you have — you can paste text, upload files, or point me to Drive docs.

1. GLOSSARY — Any client-specific terms, acronyms, or jargon I should know?
   (e.g., "CRV = Credit Risk Verification", "The Vault = their legacy system")

2. STAKEHOLDERS — Who are the key people? Names, roles, Jira usernames if you know them.
   (e.g., "Sarah Chen — Engineering Lead — schen@acme — jira: sarah.chen")

3. PRODUCT CONTEXT — Do you have a product vision doc, PRD, one-pager, or brief?
   Upload it, paste a Drive link, or just describe the product in a few sentences.

4. TECHNICAL LANDSCAPE — Any key systems, APIs, or integrations I should know about?
   (e.g., "They run a React Native app, Rails API, PostgreSQL, Stripe for payments")

5. EXISTING DESIGNS — Are there Figma files, wireframes, or mockups already?
   Paste Figma URLs so I can reference them during decomposition later.

6. CUSTOMER RESEARCH — Do you have interview transcripts, survey results, NPS data,
   support ticket exports, or feedback board dumps? Drop them in or tell me where they are.

Skip anything you don't have yet — we can fill gaps later.
```

### Processing Each Input

For each category the PM provides:

**Glossary**: Write terms to `product/context/glossary.json` + `.md`. Use the structured format:
```json
{ "terms": [{ "term": "CRV", "definition": "Credit Risk Verification", "source": "PM during setup" }] }
```

**Stakeholders**: Write to `product/context/stakeholders.json` + `.md`. Include name, role, email, Jira username, and any notes the PM shares about working style or decision authority.

**Product context**: If the PM uploads a doc or pastes a Drive link:
- Read/fetch the document
- Extract key information (vision, goals, target users, success metrics)
- Write a structured summary to `product/context/discovery_summary.json` + `.md`
- Do NOT copy the full document locally — summarize and reference the source

**Technical landscape**: Write to `product/context/technical_atlas.json` + `.md`. Capture systems, languages, APIs, third-party services, and any known constraints.

**Existing designs**: If Figma URLs are provided:
- Add entries to `product/context/ui_registry.json` with status "existing"
- Note these for future /thresh-decompose runs

**Customer research**: If the PM has files:
- Guide them to drop files into the appropriate `product/customer_data/raw/` subfolder
- Note that they should run `/thresh-feedback` and then `/thresh-synthesize` after setup completes
- If they paste a Drive folder link, search it and catalog what's there

### Adaptation Rules
- If the PM dumps a wall of text: parse it, categorize it across the right files, confirm what you captured
- If the PM says "I'll add that later": skip gracefully, note the gap in the session summary
- If the PM uploads a doc: read it and extract context rather than asking them to summarize it
- If the PM gives partial info: write what you have, mark gaps with `[TODO]` placeholders
- Don't block on completeness — some context is better than none

## Phase 5: First Data Pull

After context seeding, offer to run the first ingest immediately:

1. "Want me to pull your current Jira state now? This will populate your velocity data and work graph."
2. If yes: Run a quick count query first — `project = [KEY]` to get total issues
3. If total ≤ 100: Run `/thresh-ingest` immediately (standard mode)
4. If total > 100: Warn and offer options:
   ```
   This project has [N] stories in Jira. I have two options:

   [A] Full import — I'll pull everything in batches of 50. This will take a few minutes
       but gives you a complete work graph with all dependencies.

   [B] Active only — I'll pull the current sprint + last 90 days of activity.
       Faster, and covers what's actively being worked on. We can backfill later.
   ```
5. For option A: Run `/thresh-ingest` which will auto-detect large backlog and use batch mode
6. For option B: Run `/thresh-ingest` with a JQL scope filter (will be passed as context)
7. If they have customer data files already dropped in: "I see files in customer_data/raw/. Want me to run /thresh-feedback and /thresh-synthesize now?"

## Phase 6: Confirmation

Summarize what was created and seeded:
```
✅ Engagement ready: [Client Name] — [Engagement Name]

Structure:
  • CLAUDE.md — configured for [Client]
  • jira_config.json — connected to [PROJECT] on [instance].atlassian.net
  • 5 rule files in .claude/rules/
  • Data templates: work graph, velocity, team profiles

Connectors:
  ✓ Jira — [PROJECT] connected
  [✓/○] Google Drive — [status]
  [✓/○] Figma — [status]
  [✓/○] Slack — [status]

Context seeded:
  [✓/○] Glossary — [N terms captured / not yet provided]
  [✓/○] Stakeholders — [N people captured / not yet provided]
  [✓/○] Product context — [summarized from doc / not yet provided]
  [✓/○] Technical atlas — [captured / not yet provided]
  [✓/○] Existing designs — [N Figma refs captured / none yet]
  [✓/○] Customer data — [N files ready to process / none yet]

Next steps:
  • /thresh-ingest — pull current sprint and backlog data
  • /thresh-briefing — get your first morning briefing
  • /thresh-synthesize — process customer data (if files were dropped in)
  • Fill any [TODO] gaps in context files as info becomes available
```

## Error Handling
- If Jira auto-detection fails for custom fields: create jira_config.json with nulls and tell the PM which fields need manual configuration
- If a connector can't be enabled: note it as a blocker and proceed with what's available
- If the folder already has a CLAUDE.md: ask "This folder already has an engagement. Reset it or set up alongside?"

## Adaptation
This command should feel like a conversation, not a checklist. If the PM says "we're not using Jira for this one" — skip all Jira steps and create a lighter setup. If they say "we just need customer data synthesis" — skip Jira and focus on the customer_data/ structure. The skill adapts to what the PM actually needs.
