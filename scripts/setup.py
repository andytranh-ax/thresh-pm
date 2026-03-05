#!/usr/bin/env python3
"""
Thresh PM — One-touch engagement scaffolding.

Usage:
    python3 setup.py --client "Acme Corp" --engagement "Mobile App Redesign" --jira-project "ACME" --jira-cloud-id "abc123"

Or interactive:
    python3 setup.py
"""

import argparse
import json
import os
import sys
from datetime import date, datetime
from pathlib import Path


def create_dir(base: Path, rel: str):
    (base / rel).mkdir(parents=True, exist_ok=True)


def write_json(path: Path, data: dict):
    path.write_text(json.dumps(data, indent=2) + "\n")


def write_md(path: Path, content: str):
    path.write_text(content)


def scaffold(base: Path, client: str, engagement: str, jira_project: str, jira_cloud_id: str):
    """Create the full engagement directory structure with all data templates."""
    today = date.today().isoformat()

    # --- Directories ---
    dirs = [
        ".claude/rules",
        "memory/sessions",
        "product/context/decisions",
        "product/metrics",
        "product/customer_data/raw/interviews",
        "product/customer_data/raw/surveys",
        "product/customer_data/raw/tickets",
        "product/customer_data/raw/nps",
        "product/customer_data/raw/reviews",
        "product/customer_data/raw/analytics",
        "product/customer_data/processed",
        "product/customer_data/intermediate",
        "product/roadmap",
        "deliverables",
    ]
    for d in dirs:
        create_dir(base, d)

    # --- CLAUDE.md ---
    plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
    template_path = Path(plugin_root) / "templates" / "engagement" / "CLAUDE.md" if plugin_root else None

    if template_path and template_path.exists():
        claude_md = template_path.read_text()
    else:
        # Inline template fallback
        claude_md = """# Thresh Product OS — Client Engagement

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

## Jira

- **Config**: All Jira settings are in `jira_config.json`
- **Live queries**: Always query current sprint live via JQL
- **Historical data**: Read from `product/metrics/*.json`

## Key Rules

1. **Never create local markdown files for stories.** Draft in chat, publish to Jira.
2. **Never store document copies locally.** Search Google Drive.
3. **Always query Jira live** for current sprint data.
4. **Read JSON files** for historical metrics.
5. **Write session summaries** to `memory/sessions/` at end of every session.
"""

    claude_md = claude_md.replace("[CLIENT NAME]", client)
    claude_md = claude_md.replace("[ENGAGEMENT NAME]", engagement)
    claude_md = claude_md.replace("[YYYY-MM-DD]", today)
    write_md(base / "CLAUDE.md", claude_md)

    # --- jira_config.json ---
    write_json(base / "jira_config.json", {
        "schema_version": "1.0",
        "cloud_id": jira_cloud_id,
        "instance_url": f"https://{client.lower().replace(' ', '-')}.atlassian.net",
        "projects": [jira_project],
        "custom_fields": {
            "story_points": "customfield_10016",
            "sprint": "customfield_10020",
            "epic_link": "customfield_10014",
            "acceptance_criteria": "customfield_10035"
        },
        "workflows": {
            "story": ["To Do", "In Progress", "In Review", "Done"],
            "bug": ["Open", "In Progress", "Fixed", "Verified", "Closed"]
        },
        "issue_types": {
            "story": "Story",
            "bug": "Bug",
            "task": "Task",
            "epic": "Epic",
            "subtask": "Sub-task"
        }
    })

    # --- Empty JSON data templates ---
    write_json(base / "product/work_graph.json", {
        "schema_version": "1.0", "last_updated": None,
        "nodes": {}, "edges": [],
        "component_index": {}, "critical_path": [], "unblocked_stories": []
    })

    write_json(base / "product/metrics/velocity.json", {
        "schema_version": "1.0", "last_updated": None,
        "sprints": [], "rolling_avg_velocity": None,
        "forecast_next_sprint": {"low": None, "mid": None, "high": None},
        "trend": None
    })

    write_json(base / "product/metrics/team_profiles.json", {
        "schema_version": "1.0", "last_updated": None,
        "developers": [], "bus_factor_risks": []
    })

    write_json(base / "product/metrics/estimation_accuracy.json", {
        "schema_version": "1.0", "last_updated": None, "entries": []
    })

    write_json(base / "product/context/.ingest_state.json", {
        "schema_version": "1.0", "last_updated": None,
        "last_ingest": None, "mode": None,
        "sources_used": [], "jira_issues_scanned": 0,
        "drive_docs_processed": [], "figma_files_processed": [],
        "data_files_profiled": [], "change_log": []
    })

    # --- Dual-format context files ---
    context_files = {
        "glossary": {"schema_version": "1.0", "last_updated": None, "entries": []},
        "stakeholders": {"schema_version": "1.0", "last_updated": None, "entries": []},
        "technical_atlas": {"schema_version": "1.0", "last_updated": None, "services": [], "integrations": []},
        "ui_registry": {"schema_version": "1.0", "last_updated": None, "entries": []},
        "data_catalog": {"schema_version": "1.0", "last_updated": None, "sources": []},
    }

    for name, data in context_files.items():
        write_json(base / f"product/context/{name}.json", data)
        write_md(base / f"product/context/{name}.md",
                 f"# {name.replace('_', ' ').title()}\n\n> Populated by /thresh-ingest. See {name}.json for structured data.\n\n(empty — run /thresh-ingest to populate)\n")

    write_md(base / "product/context/discovery_summary.md",
             "# Discovery Summary\n\n> High-level engagement summary.\n\n(empty — populated during discovery phase)\n")

    # --- Memory ---
    write_md(base / "memory/MEMORY.md",
             f"# Thresh Auto-Memory — {client}\n\n> Claude updates this file across sessions. First 200 lines are loaded on startup.\n\n## Engagement Started\n- {today}\n\n## Key Decisions\n\n(none yet)\n\n## Important Context\n\n(none yet)\n")

    write_md(base / "memory/sessions/.session-template.md",
             """# Session Summary — [DATE]

## Context
What was the focus of this session?

## Decisions Made
-

## Questions Left Open
-

## Actions Taken
-

## Next Session Should
-
""")

    # --- Copy rules from plugin if available ---
    if plugin_root:
        rules_src = Path(plugin_root) / "rules"
        rules_dst = base / ".claude" / "rules"
        if rules_src.exists():
            for rule_file in rules_src.glob("*.md"):
                dst = rules_dst / rule_file.name
                if not dst.exists():
                    dst.write_text(rule_file.read_text())

    # --- .gitignore ---
    write_md(base / ".gitignore", """# OS
.DS_Store
__pycache__/
*.pyc

# PM-specific (per-person)
memory/MEMORY.md

# Temporary
product/customer_data/intermediate/
*.tmp

# Sensitive
.env
""")

    print(f"""
✅ Thresh engagement initialized!

   Client:     {client}
   Engagement: {engagement}
   Jira:       {jira_project} ({jira_cloud_id})
   Location:   {base.resolve()}

📋 Next steps:
   1. Review jira_config.json — update custom_fields to match your Jira instance
   2. Run /thresh-ingest to pull initial context from Jira
   3. Drop customer research files into product/customer_data/raw/
   4. Run /thresh-synthesize to process customer data
""")


def main():
    parser = argparse.ArgumentParser(description="Thresh PM — Initialize a new engagement")
    parser.add_argument("--client", help="Client name (e.g., 'Acme Corp')")
    parser.add_argument("--engagement", help="Engagement name (e.g., 'Mobile App Redesign')")
    parser.add_argument("--jira-project", help="Jira project key (e.g., 'ACME')")
    parser.add_argument("--jira-cloud-id", help="Jira cloud ID")
    parser.add_argument("--dir", default=".", help="Directory to scaffold in (default: current)")
    args = parser.parse_args()

    # Interactive fallback
    client = args.client or input("Client name: ").strip()
    engagement = args.engagement or input("Engagement name: ").strip()
    jira_project = args.jira_project or input("Jira project key: ").strip()
    jira_cloud_id = args.jira_cloud_id or input("Jira cloud ID (or 'skip'): ").strip()

    if not client or not engagement or not jira_project:
        print("Error: client, engagement, and jira-project are required.")
        sys.exit(1)

    if jira_cloud_id == "skip":
        jira_cloud_id = "CONFIGURE_ME"

    base = Path(args.dir).resolve()
    scaffold(base, client, engagement, jira_project, jira_cloud_id)


if __name__ == "__main__":
    main()
