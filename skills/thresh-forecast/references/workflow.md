# Forecast Workflow

1. Load `product/metrics/velocity.json`
2. Query Jira for current sprint status
3. Load `product/work_graph.json` for blocked items
4. Load `product/metrics/team_profiles.json` for capacity
5. Calculate three-point estimate (P10/P50/P90)
6. Adjust for blocked items and capacity
7. Present sprint health card
