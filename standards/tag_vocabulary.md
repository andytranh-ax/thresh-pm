# Tag Vocabulary

Controlled vocabulary for story tagging. All tags must conform to this list to enable consistent filtering, reporting, and analysis.

## Tag Format

All tags use `category:value` format (lowercase, colon-separated):
```
domain:frontend
type:feature
priority:high
platform:ios
```

## Domain Tags (Required: minimum 1)

Describes the technical area of the story.

```
domain:ui              # User interface, visual components
domain:api             # REST APIs, backend endpoints
domain:backend         # Server logic, databases, services
domain:frontend        # Client-side code, JavaScript, React
domain:infrastructure  # DevOps, deployment, CI/CD
domain:auth            # Authentication, authorization, security
domain:payments        # Payment processing, billing
domain:mobile          # Mobile-specific logic or features
domain:web             # Web platform specific
domain:performance     # Optimization, speed, efficiency
domain:security        # Security features, data protection
domain:data            # Data pipelines, analytics, warehousing
domain:search          # Search functionality, indexing
domain:notifications   # Push, email, in-app notifications
domain:onboarding      # User signup, first-time experience
domain:checkout        # Purchase flow, cart, order processing
domain:settings        # User preferences, account management
```

## Type Tags (Required: minimum 1)

Describes the kind of work.

```
type:feature           # New user-facing feature
type:bugfix            # Bug fix, defect resolution
type:refactor          # Code cleanup, restructuring (no behavior change)
type:chore             # Routine maintenance, infrastructure
type:spike             # Research, exploration, proof-of-concept
type:tech-debt         # Addressing technical debt
```

## Priority Tags (Recommended)

Business and time-sensitivity priority.

```
priority:critical      # Blocks launch, system down, security issue
priority:high          # Core feature, significant impact
priority:medium        # Nice-to-have, can wait a sprint
priority:low           # Polish, technical debt, backlog
```

## Platform Tags (Optional)

Target platform for the work.

```
platform:ios           # Apple iOS (iPhone, iPad)
platform:android       # Android devices
platform:web           # Web browser (desktop/mobile)
platform:responsive    # Responsive design across breakpoints
platform:desktop       # Desktop-specific
platform:mobile        # Mobile-specific (iOS + Android)
```

## Theme/Team Tags (Optional)

For larger initiatives or team-specific work.

```
theme:q1-2025          # Quarterly initiative
theme:migration        # Data or system migration
theme:redesign         # UI redesign effort
```

## Tag Rules

1. **Minimum coverage**: Every story must have:
   - At least 1 domain tag
   - At least 1 type tag
   - Recommended: at least 1 priority tag

2. **Maximum tags**: Maximum 5 tags per story (enforces clarity)

3. **Consistency**: Use only tags from this vocabulary; no custom tags

4. **Automation**: Tags enable:
   - Filtering by area (e.g., "all frontend stories")
   - Risk reporting (e.g., "all high priority security work")
   - Sprint planning (e.g., "all tech debt in backlog")
   - Burn-down charts by category

## Example Tagging

### Search Feature Story
```yaml
tags:
  - domain:frontend
  - domain:api
  - type:feature
  - priority:high
  - platform:web
```
(5 tags: domain x2, type x1, priority x1, platform x1)

### Bug Fix Story
```yaml
tags:
  - domain:auth
  - type:bugfix
  - priority:critical
```
(3 tags: domain x1, type x1, priority x1)

### Refactoring Story
```yaml
tags:
  - domain:backend
  - type:refactor
  - priority:low
```
(3 tags: domain x1, type x1, priority x1)

## Tag Updates and Extensions

If a new tag is needed:
1. Propose addition to this vocabulary document
2. Get PM/team agreement
3. Update documentation here
4. Migrate any affected stories
5. Add to automation rules (if applicable)

Do not create ad-hoc tags.
