# Prioritize Workflow

1. Collect items to prioritize (synthesis features, Jira backlog, or PM-provided list)
2. Load synthesis.json, work_graph.json, velocity.json, team_profiles.json
3. PM selects framework (RICE, ICE, Value/Complexity, Weighted, MoSCoW)
4. Enrich each item with evidence scores, dependency data, capacity constraints
5. Score and rank
6. Output to product/prioritization.json + .md
7. Suggest: /thresh-decompose for top items, /thresh-publish to update Jira priorities

## Chaining
- /thresh-synthesize → /thresh-prioritize → /thresh-decompose → /thresh-publish
- /thresh-reconcile → /thresh-prioritize (re-rank with roadmap alignment data)
