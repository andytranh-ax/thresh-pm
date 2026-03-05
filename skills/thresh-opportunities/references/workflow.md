# Opportunity Solution Tree Workflow

1. PM defines desired outcome (metric + current + target)
2. Load synthesis.json for opportunity/theme mapping
3. Load work_graph.json for existing story coverage
4. Build tree: Outcome → Opportunities (themes) → Solutions (features) → Experiments
5. Score confidence per solution using evidence counts
6. Flag low-confidence solutions for validation experiments
7. Link solutions to existing Jira stories where possible
8. Output to product/opportunity_tree.json + .md
9. Suggest: /thresh-decompose for ready-to-build solutions

## Chaining
- /thresh-synthesize → /thresh-opportunities → /thresh-decompose
- /thresh-opportunities → /thresh-prioritize (rank solutions)
