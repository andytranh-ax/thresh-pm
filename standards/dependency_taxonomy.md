# Dependency Taxonomy

Framework for modeling and managing dependencies between stories and work items.

## Dependency Types

### 1. Blocks (must complete first)
This story must finish before another story can start.

```yaml
blocks:
  - STORY-2025-0050  # STORY-2025-0050 is blocked by this story
```

- **Meaning**: This story completes a prerequisite
- **Impact**: Downstream stories cannot start until this finishes
- **Warning**: If blocked_by chain > 3, escalate for resolution

### 2. Blocked By (waiting on)
This story is waiting on one or more other stories.

```yaml
blocked_by:
  - STORY-2025-0001  # Cannot start until this completes
  - STORY-2025-0002  # Cannot start until this completes
```

- **Meaning**: This story has external dependencies
- **Impact**: Schedule risk; highlight in sprint planning
- **Rule**: Flag if > 3 blockers (sign of poor decomposition)

### 3. Relates To (parallel work)
Stories working on the same feature or screen but with no blocking relationship.

```yaml
related_stories:
  - STORY-2025-0015  # Parallel frontend work
  - STORY-2025-0016  # Parallel backend work
```

- **Meaning**: Stories can run in parallel
- **Impact**: Coordination needed; team alignment
- **Use case**: Same screen with frontend + backend work

### 4. Duplicate Of
This story is a duplicate and should be closed.

```yaml
related_stories:
  - STORY-2025-0001  # The canonical story; close this one
```

- **Meaning**: Another story already covers this work
- **Impact**: Close, redirect to canonical story
- **Rule**: Never have two active stories for the same work

## External Dependency Types

External dependencies: things outside the story system that block progress.

```yaml
dependencies:
  - api:search-endpoint           # Backend API must exist
  - database:user-profile-schema  # Database schema must be defined
  - component:product-card        # Existing reusable component
  - library:react-query           # Third-party library
  - service:payment-gateway       # Third-party service
  - infrastructure:cdn            # Infrastructure setup
  - configuration:api-keys        # Configuration or secrets
  - data-migration:legacy-users   # Data migration needed first
  - third-party:stripe            # Third-party integration
```

### Dependency Format
```
[type]:[identifier]
```

- **type**: api, database, component, library, infrastructure, service, configuration, data-migration, third-party
- **identifier**: Unique name or reference

## Dependency Rules

1. **No circular dependencies**: A story cannot directly or indirectly block itself
   - Story X blocks Story Y blocks Story Z → Story Z blocks Story X = INVALID

2. **No transitive chains > 3**: Avoid long chains of dependencies
   - Story A blocks B blocks C is acceptable
   - Story A blocks B blocks C blocks D blocks E = ESCALATE

3. **Flag for resolution if**: Any story has > 3 blockers or > 3 blocking relationships

4. **Auto-infer relationships**:
   - Same-screen stories (same ux_id) → relates_to
   - Sequential flow (previous_screen → next_screen) → blocks
   - Shared component → relates_to

## Dependency Graph Rules

The dependency graph should be:
- **Acyclic**: No circular dependencies allowed
- **Minimal**: Only direct dependencies listed; transitive deps inferred
- **Explicit**: All critical paths documented
- **Reviewable**: Visual representation in sprint planning

## Example Dependency Scenarios

### Scenario 1: Feature with Frontend + Backend
```yaml
# Story STORY-2025-0050 (Frontend)
story_id: STORY-2025-0050
title: Search form UI
category: Frontend
blocked_by:
  - STORY-2025-0051  # Wait on API implementation
related_stories:
  - STORY-2025-0051  # Working together

# Story STORY-2025-0051 (Backend)
story_id: STORY-2025-0051
title: Search API endpoint
category: Backend
blocks:
  - STORY-2025-0050  # Unblock frontend
related_stories:
  - STORY-2025-0050  # Working together
```

**Interpretation**: Backend (0051) must complete first, then frontend (0050) can start. Both are working on the same feature (related).

### Scenario 2: Dependent Feature Chain
```yaml
# Story 1
story_id: STORY-2025-0100
title: User authentication
blocks:
  - STORY-2025-0101

# Story 2
story_id: STORY-2025-0101
title: User profile page
blocks:
  - STORY-2025-0102
blocked_by:
  - STORY-2025-0100

# Story 3
story_id: STORY-2025-0102
title: User settings page
blocked_by:
  - STORY-2025-0101
```

**Flow**: Auth → Profile → Settings (dependency chain)

**Flag**: If adding a 4th story in chain, escalate for refactoring.

### Scenario 3: Parallel Work
```yaml
story_id: STORY-2025-0200
title: Checkout button styling
category: Frontend
related_stories:
  - STORY-2025-0201

story_id: STORY-2025-0201
title: Payment form validation
category: Frontend
related_stories:
  - STORY-2025-0200
```

**Interpretation**: Both stories work on checkout flow, can run in parallel, need coordination.

## Dependency Resolution Checklist

Before sprint planning:
- [ ] No circular dependencies (run cycle check)
- [ ] No chains longer than 3
- [ ] No story with > 3 blockers
- [ ] External dependencies are available or scheduled
- [ ] related_stories used correctly for parallel work
- [ ] blocks/blocked_by align in both directions
- [ ] blocked_by stories in same or earlier sprint
