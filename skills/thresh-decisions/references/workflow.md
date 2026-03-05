# /decisions — Weekly Decision Digest

Scans Jira comments and status changes for decisions that were made informally and should be formally captured.

## Step 1: Read Context

Read the CLAUDE.md for client info, Jira Cloud ID, and default project key. Read `${CLAUDE_PLUGIN_ROOT}/standards/intelligence_record_standard.md` for the decision record format.

## Step 2: Scan Jira Comments for Decision Language

Query Jira for issues with recent comments (last 7 days):

```
project = [DEFAULT_PROJECT] AND comment ~ "decided" OR comment ~ "agreed" OR comment ~ "approved" OR comment ~ "go with" OR comment ~ "let's do" OR comment ~ "final answer" AND updated >= -7d
```

For each result, read the comments using `getJiraIssue` with expand=renderedFields. Look for language indicating a decision was made:
- "We decided to..."
- "Approved by..."
- "Going with option..."
- "Agreed in standup..."
- "Final answer is..."
- Status transitions from "In Review" to "Approved" or "Done"

## Step 3: Cross-Reference Against Decision Log

Read all files in `product/context/decisions/`. Check if any of the decisions found in Step 2 are already captured. Only surface the ones that are NOT yet logged.

## Step 4: Present Candidates

For each uncaptured decision, present:
- **Source**: which Jira issue and comment
- **Decision**: what was decided (1 sentence)
- **Who decided**: names mentioned
- **Impact**: which stories or epics are affected
- **Confidence**: How confident are you this is a real decision vs. just discussion? (High/Medium/Low)

## Step 5: Capture Approved Decisions

For each decision the user confirms, create a decision record in `product/context/decisions/` following the intelligence record standard. Include:
- Decision ID (DEC-YYYYMMDD-NNN)
- Source reference (Jira issue key + comment)
- Decision statement
- Alternatives considered (if mentioned in comments)
- Impact scope

## Output Format

Present as a numbered list of decision candidates. Let the user approve/skip each one. Only write decision records for approved ones. At the end, summarize how many were captured.
