# Jira Conventions

## Configuration
- All Jira settings are in `jira_config.json` at the repo root
- Read cloud_id, project keys, and custom field mappings from this file
- NEVER hardcode Jira IDs — always reference the config

## JQL Patterns

### Current sprint stories
```
project = {KEY} AND sprint in openSprints() ORDER BY priority DESC
```

### Stories updated since last ingest
```
project = {KEY} AND updated >= "{WATERMARK_DATE}" ORDER BY updated DESC
```

### Defects in last 7 days
```
project = {KEY} AND issuetype = Bug AND created >= -7d ORDER BY priority DESC
```

### Stories by assignee
```
project = {KEY} AND assignee = "{JIRA_USERNAME}" AND sprint in openSprints()
```

### Cross-project query
```
project in ({KEY1}, {KEY2}) AND sprint in openSprints()
```

## Query Strategy
- **Current sprint status**: Always query Jira LIVE (never rely on cached data)
- **Historical metrics**: Read from `product/metrics/*.json` (updated nightly)
- **Cross-project analysis**: Read from JSON cache (too large for live context)
- **Paginate large results**: Use maxResults=50, extract to JSON, then analyze

## Creating Issues
- Default to primary delivery board (first project in jira_config.json)
- Use issue type mappings from jira_config.json
- Always include: summary, description (with ACs), story points, labels, priority
- Create issue links for dependencies after all issues are created

## Field Mapping
- Story points, sprint, and epic link fields vary by Jira instance
- Always read custom field IDs from `jira_config.json.custom_fields`
- NEVER assume field names — they differ per client
