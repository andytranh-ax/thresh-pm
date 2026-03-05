# Risk Scoring Workflow

1. Identify target (single story or full sprint)
2. Load `product/work_graph.json` for dependency analysis
3. Load `product/metrics/team_profiles.json` for assignment analysis
4. Load `product/metrics/velocity.json` for pattern analysis
5. Query Jira for story details (points, components, status)
6. Score each dimension (0-3): dependency, complexity, assignment, pattern
7. Calculate total risk score and classify (green/yellow/red/black)
8. Present risk card with recommendations
