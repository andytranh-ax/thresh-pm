# /thresh-prioritize

Prioritize features or backlog items using customer evidence, dependency data, and capacity constraints.

## Usage
Run `/thresh-prioritize` to rank items using a selected framework.

## Steps
1. Read the skill: `skills/thresh-prioritize/SKILL.md`
2. Collect items to prioritize (ask PM: synthesis features? Jira backlog? custom list?)
3. Ask PM: which framework? (RICE, ICE, Value/Complexity, Weighted, MoSCoW)
4. Load synthesis.json, work_graph.json, velocity.json, team_profiles.json
5. Enrich each item with evidence, dependency, and capacity data
6. Score and rank
7. Write `product/prioritization.json` and `prioritization.md`
8. Suggest: "/thresh-decompose for top items" or "/thresh-publish to update Jira priorities"
