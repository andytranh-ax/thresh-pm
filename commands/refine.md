# /refine — Refinement Facilitation Mode

When user invokes `/refine`, facilitate a structured refinement session.

## Modes

| Command | Purpose |
|---------|---------|
| `/refine prep` | Pre-refinement: select stories, flag not-ready |
| `/refine start` | During: walk through ACs, capture decisions |
| `/refine end` | Post: sync to Jira, transition to Ready for Dev |

---

## /refine prep — Pre-Refinement

```
┌─────────────────────────────────────────────────────────────┐
│  📋 REFINEMENT PREP — Sprint [#]                             │
├─────────────────────────────────────────────────────────────┤
│  👥 TEAM CAPACITY                                            │
│  • @[Name] ([Level]): [X] pts, [Domain] expert               │
│  • Total: [X] pts                                            │
├─────────────────────────────────────────────────────────────┤
│  🎯 STORIES FOR REFINEMENT                                   │
│                                                             │
│  | # | Story | Pts | Best Fit | Status |                    │
│  |---|-------|-----|----------|--------|                    │
│  | 1 | [KEY] | [X] | @[Name]  | ✅ Ready |                   │
│  | 2 | [KEY] | [X] | @[Name]  | ⚠️ Missing ACs |             │
│  | 3 | [KEY] | [X] | @[Name]  | ❌ Blocked |                 │
├─────────────────────────────────────────────────────────────┤
│  ⚠️ [KEY] is NOT ready — missing error states.              │
│     → Run `/draft-spec [KEY]` before refinement.            │
├─────────────────────────────────────────────────────────────┤
│  📅 AGENDA (Est. [X] min)                                    │
│  1. [KEY] ([X] min) — [Complexity note]                     │
│  2. [KEY] ([X] min) — [Complexity note]                     │
│  3. Buffer ([X] min) — Open questions                       │
└─────────────────────────────────────────────────────────────┘

Reply: `/refine start` to begin facilitated walkthrough
```

---

## Pre-Refinement Hook: Rule Validation

> **Before starting AC walkthrough, check for applicable business rules.**

**Trigger:** After `/refine prep`, before `/refine start`

**Steps:**
1. Extract product/feature keywords from story summary
2. Query catalog rules: search `product/context/external/catalog/` for matches
3. For each matching rule, check if ACs cover the error state
4. If missing, surface as suggestion

**Output:**
```
📋 RULE CHECK for [KEY]

Detected product: "Ultimate TV"

| Rule | Condition | Status |
|------|-----------|--------|
| RULE-001 | internet_tier < Pro | ⚠️ Missing AC |
| RULE-004 | region = Rural | ⚠️ Missing AC |

Suggested ACs:
• AC-ERROR: GIVEN user has Basic Internet, WHEN selecting Ultimate TV, THEN show error
  └─ Source: RULE-001 (sample_rules.csv, row 2)

Reply: `/add-ac 1` to add suggested AC, or `/skip-rules` to continue
```

**Provenance format:**
```
Source: [RULE-ID] ([filename], row [N])
```

---

## /refine start — During Refinement

```
┌─────────────────────────────────────────────────────────────┐
│  📖 STORY [#] of [total]: [KEY] — [Summary]                  │
│  Assignee: @[Name] | Points: [X] | Risk: [Level]            │
├─────────────────────────────────────────────────────────────┤
│  💡 FUNCTIONAL INTENT                                        │
│  "[User story statement]"                                   │
│                                                             │
│  [Brief explanation of business value and context]          │
├─────────────────────────────────────────────────────────────┤
│  📋 ACCEPTANCE CRITERIA WALKTHROUGH                          │
│                                                             │
│  ▶ AC[#]: [Title]                                            │
│    GIVEN [context]                                          │
│    WHEN [action]                                            │
│    THEN [outcome]                                           │
│                                                             │
│    🗣️ Discussion Prompt:                                    │
│    "[Clarifying question if ambiguity detected]"           │
├─────────────────────────────────────────────────────────────┤
│  Progress: [▓▓▓░░░░░░░] [#]/[total] stories | AC [#]/[total]│
└─────────────────────────────────────────────────────────────┘
```

### Commands During Refinement

| Command | Action |
|---------|--------|
| `/next-ac` | Move to next Acceptance Criteria |
| `/skip-ac` | Skip AC (log as "Needs follow-up") |
| `/question "[text]"` | Log open question |
| `/decision "[text]"` | Log decision made |
| `/assign @[name]` | Change assignee |
| `/points [N]` | Update story points |
| `/next-story` | Move to next story |
| `/pause` | Pause refinement (resume later) |
| `/end` | End refinement, generate summary |

---

## /refine end — Post-Refinement

```
┌─────────────────────────────────────────────────────────────┐
│  ✅ REFINEMENT COMPLETE — Sprint [#]                         │
├─────────────────────────────────────────────────────────────┤
│  📊 SUMMARY                                                  │
│  • Stories refined: [X]                                      │
│  • Total points committed: [X]                               │
│  • Open questions: [X]                                       │
│  • Decisions logged: [X]                                     │
├─────────────────────────────────────────────────────────────┤
│  📋 DECISIONS CAPTURED                                       │
│  • [KEY] AC[#]: [Decision text]                             │
│  • [KEY]: [Scope change or assignment]                      │
├─────────────────────────────────────────────────────────────┤
│  ❓ OPEN QUESTIONS (needs follow-up)                         │
│  • [KEY] AC[#]: "[Question]"                                │
│    → Assigned to @[Name] to clarify                         │
├─────────────────────────────────────────────────────────────┤
│  📤 SYNC TO JIRA                                             │
│                                                             │
│  | Story | Updates | Status Change |                        │
│  |-------|---------|---------------|                        │
│  | [KEY] | +[X] decisions | Draft → Ready for Dev |         │
│  | [KEY] | Scope reduced | Draft → Ready for Dev |          │
│  | [KEY] | Has blocker | Draft → Blocked ⚠️ |                │
│                                                             │
│  Reply: `/sync-jira` to push all updates                    │
└─────────────────────────────────────────────────────────────┘
```

### Sync to Jira

When user confirms `/sync-jira`:

1. Use `editJiraIssue` to update story descriptions with decisions captured
2. Use `transitionJiraIssue` to move stories to appropriate status:
   - All ACs reviewed, no blockers → "Ready for Dev"
   - Has open questions → "Ready for Dev" with comment
   - Has blocker → "Blocked"
3. Reference your `cloudId` and `projectKey` from CLAUDE.md

## Status Transition Logic

| Condition | Jira Transition |
|-----------|-----------------|
| All ACs reviewed, no blockers | `Draft → Ready for Dev` |
| Has open questions (non-blocking) | `Draft → Ready for Dev` + comment |
| Has blocker (missing design, dependency) | `Draft → Blocked` |
| Skipped during refinement | No change (stays `Draft`) |

## Trigger

User types: `/refine`, `/refine prep`, `/refine start`, or `/refine end`

## Setup Required

Ensure `CLAUDE.md` is configured with:
- `cloudId`: Your Jira cloud ID
- `projectKey`: Your project key

This enables Jira MCP integration for syncing refinement results.
