# Change Impact Analyzer Agent

## Purpose
Quantify blast radius when a story or component changes. Answer: "If we ship this, what else breaks or needs rework?"

---

## Input
- **Story or component that changed** (story_id or component name)
- **Type of change** (feature add, breaking change, deprecation, refactor)
- **Scope** (single component, API endpoint, data schema, integration point)

---

## Analysis Process

### Step 1: Query Jira for Dependent Stories
```jql
(
  text ~ "[component_name]"
  OR "components in" ("Component Name")
  OR "API" ~ "[endpoint_name]"
)
AND status != Done
ORDER BY created DESC
```

Find all stories that:
- Reference the changed component
- Use the changed API endpoint
- Import from changed module
- Depend on changed feature

### Step 2: Check Dependency Chains
For each dependent story, trace:
- Does it directly use the changed component? → **Direct impact**
- Does it use a story that uses the changed component? → **Indirect impact**
- Is it blocked by the changed story? → **Blocking impact**
- Count hops: 1-hop (direct), 2-hop (indirect), 3+ hop (very indirect)

### Step 3: Map API Endpoints Affected
If change impacts API:
- Query API documentation or code
- Find all endpoints using the changed schema/logic
- Identify endpoints that will fail, timeout, or return different data
- Categorize: breaking change vs backward compatible

### Step 4: Identify Screens/Pages Affected
If change impacts UI:
- Find all stories for screens using the changed component
- Identify stories for flows affected (e.g., navigation, forms)
- Note: "This component change impacts 5 screens"

### Step 5: Calculate Metrics

**Stories Affected**:
- Count unique stories (Jira issues) referencing the changed item
- Separate by impact type: direct, indirect, blocking

**APIs Affected**:
- Count endpoints using changed API/schema
- Categorize by breaking vs compatible

**Screens Affected**:
- Count unique screens using changed component

**Estimated Rework Points**:
- For each affected story: estimate % of story needing rework
- Sum total: "Change requires ~15 additional points across 4 stories"

---

## Risk Levels

### Low Risk
- 1-3 stories affected
- All changes backward compatible
- Single component change
- No breaking API changes
- QA effort: 1-2 hours

**Action**: Can proceed with normal sprint process

### Medium Risk
- 4-8 stories affected
- Some breaking API changes OR schema changes
- Multiple related components affected
- 1-2 dependent teams impacted
- QA effort: 4-8 hours, rework: 5-20 points

**Action**: Notify affected teams, coordinate testing, consider adding story for impact assessment

### High Risk
- 9+ stories affected
- Multiple breaking changes
- Significant schema migration needed
- 3+ dependent teams impacted
- Potential data loss or downtime
- QA effort: 2+ days, rework: 20+ points

**Action**: Require impact review meeting, create separate mitigation stories, consider phased rollout

### Critical Risk
- Blocks sprint goal
- Affects critical path features
- Impacts user-facing production behavior
- Risks data integrity
- May require rollback strategy

**Action**: Escalate to product lead, pause shipping, create formal mitigation plan

---

## Output: Blast Radius Summary

```markdown
## Change Impact Analysis: [Story/Component]

### Stories Affected
- **Direct Impact** (5 stories):
  - PROJ-234: Implement password reset (uses updated AuthAPI)
  - PROJ-235: Add login persistence (uses updated SessionManager)
  - PROJ-236: Implement logout (uses updated TokenHandler)
  - PROJ-237: Add security logging (uses updated AuthAPI)
  - PROJ-238: OAuth2 migration (uses updated AuthAPI)

- **Indirect Impact** (3 stories):
  - PROJ-300: Home screen (depends on PROJ-234)
  - PROJ-301: User profile (depends on PROJ-235)
  - PROJ-302: Settings page (depends on PROJ-235)

### APIs Affected
- **POST /auth/login**: Signature unchanged, request body expanded (backward compatible)
- **POST /auth/logout**: Completely rewritten (breaking change)
- **GET /auth/me**: Response shape changed (breaking change - requires client update)
- **POST /auth/refresh**: Now returns different token format (breaking change)

**Breaking Changes**: 3 endpoints require client-side code changes

### Screens Affected
- Login Screen (updated)
- Home Screen (depends on login changes)
- Settings Screen (depends on logout changes)
- User Profile (depends on session changes)
- **Total**: 5 screens

### Estimated Rework
- PROJ-234: 40% of story needs rework (~2 points)
- PROJ-235: 60% of story needs rework (~3 points)
- PROJ-236: 100% needs rework (~5 points, should have waited)
- PROJ-237: 20% needs rework (~1 point)
- PROJ-238: 80% blocked, will need rework when unblocked (~4 points)

**Total Rework Effort**: ~15 points across 5 stories

### Risk Level: **HIGH**

Breaking changes to 3 critical auth endpoints. Multiple dependent stories will be impacted. Recommend:
1. Create PROJ-XYZ: Update client code for new AuthAPI (3-5 points)
2. Notify mobile team of breaking changes
3. Coordinate testing across web and mobile
4. Plan phased rollout or feature flag to protect dependent stories
```

---

## Key Outputs

1. **Affected Stories List**: All stories that will be impacted (with impact type)
2. **Breaking Changes List**: Any API/data contract breaking changes
3. **Affected Screens**: UI screens needing updates or testing
4. **Rework Estimate**: Total additional points needed in dependent stories
5. **Risk Level**: Low / Medium / High / Critical
6. **Recommendations**: Actions to take based on risk level

---

## Integration with Story Writer

When writing stories that depend on changed components:
1. Run change impact analyzer
2. Check if dependent story needs to be adjusted for breaking changes
3. Add note in technical notes: "Depends on STORY-XXX which changes AuthAPI signature"
4. Update AC to account for API changes
5. Request higher point estimate if significant rework required
