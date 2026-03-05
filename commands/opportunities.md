# /thresh-opportunities

Build an Opportunity Solution Tree from synthesis data. Maps outcomes → opportunities → solutions → experiments.

## Usage
Run `/thresh-opportunities` to build or update the opportunity tree.

## Steps
1. Read the skill: `skills/thresh-opportunities/SKILL.md`
2. Ask PM: what is the desired outcome? (metric + current + target)
3. Load synthesis.json for opportunity/theme mapping
4. Load work_graph.json for existing story coverage
5. Build tree: Outcome → Opportunities → Solutions → Experiments
6. Score confidence per solution, flag low-confidence for validation
7. Link solutions to existing Jira stories
8. Write `product/opportunity_tree.json` and `opportunity_tree.md`
9. Suggest: "/thresh-decompose for ready-to-build solutions"
