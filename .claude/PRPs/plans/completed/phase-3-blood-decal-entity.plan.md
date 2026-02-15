# Feature: Blood Decal Entity (Blood Pool Visual)

## Summary

Create a `BloodDecal` entity that renders a red blood pool at the position of killed zombies, persisting for 10 seconds with TTL countdown and alpha transparency. The entity uses the same TTL pattern as BloodParticle and DeadZombie but renders a simple ellipse/circle instead of sprites or particles, providing persistent visual evidence of combat underneath corpses.

## User Story

As a player
I want to see blood pools appear under dead zombies
So that I can see persistent visual evidence of combat and feel visceral satisfaction

## Problem Statement

Currently, there is no persistent blood visual under corpses. Blood particles fade quickly (0.8s) and corpses appear on clean ground, reducing the gore impact and making the battlefield feel sterile despite heavy combat.

## Solution Statement

Implement a `BloodDecal` entity that spawns at the position of killed zombies, draws a dark red ellipse with alpha transparency, persists for 10 seconds with TTL countdown, and auto-removes when lifetime expires. This uses the proven TTL pattern from BloodParticle/DeadZombie and simple pygame drawing instead of sprite loading.

## Metadata

| Field            | Value                                             |
| ---------------- | ------------------------------------------------- |
| Type             | NEW_CAPABILITY                                    |
| Complexity       | LOW                                               |
| Systems Affected | entities, core constants                          |
| Dependencies     | pygame (already in use)                           |
| Estimated Tasks  | 4                                                 |

---

## UX Design

### Before State
```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌─────────────┐         ┌─────────────┐         ┌─────────────┐            ║
║   │   Player    │ ──────► │   Shoots    │ ──────► │   Zombie    │            ║
║   │   Shoots    │         │   Zombie    │         │   Dies      │            ║
║   └─────────────┘         └─────────────┘         └─────────────┘            ║
║                                                           │                   ║
║                                                           ▼                   ║
║                                                  ┌─────────────┐              ║
║                                                  │  Corpse on  │              ║
║                                                  │ clean floor │              ║
║                                                  └─────────────┘              ║
║                                                                               ║
║   USER_FLOW: Kill zombie → corpse appears on clean ground                    ║
║   PAIN_POINT: No blood under corpse, less gore impact                        ║
║   DATA_FLOW: Zombie killed → corpse spawned (no blood decal)                 ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌─────────────┐         ┌─────────────┐         ┌─────────────┐            ║
║   │   Player    │ ──────► │   Shoots    │ ──────► │   Zombie    │            ║
║   │   Shoots    │         │   Zombie    │         │   Dies      │            ║
║   └─────────────┘         └─────────────┘         └─────────────┘            ║
║                                                           │                   ║
║                                                           ▼                   ║
║                                                  ┌─────────────┐              ║
║                                                  │ Blood Pool  │              ║
║                                                  │   (decal)   │              ║
║                                                  └─────────────┘              ║
║                                                           │                   ║
║                                                           ▼                   ║
║                                                  ┌─────────────┐              ║
║                                                  │  Corpse on  │              ║
║                                                  │  blood pool │              ║
║                                                  └─────────────┘              ║
║                                                                               ║
║   USER_FLOW: Kill zombie → blood pool + corpse appear → persist 10s          ║
║   VALUE_ADD: Blood under corpse, enhanced gore, combat evidence              ║
║   DATA_FLOW: Zombie killed → BloodDecal spawned → corpse spawned on top      ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location        | Before          | After              | User_Action | Impact                    |
| --------------- | --------------- | ------------------ | ----------- | ------------------------- |
| Play scene      | Corpse on clean ground | Corpse on blood pool | Kill zombie | Enhanced gore visual |
| Battlefield     | No blood pools | Red blood pools visible | Look around | Persistent combat evidence |
| 10 seconds later | N/A | Blood pool fades | Wait | Auto-cleanup |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `zombie-shooter/src/game/entities/blood_particle.py` | 1-83 | TTL pattern to MIRROR (just implemented in Phase 1) |
| P0 | `zombie-shooter/src/game/entities/dead_zombie.py` | 1-75 | Alternative TTL pattern example (just implemented in Phase 2) |
| P1 | `zombie-shooter/tests/test_blood_particle.py` | 1-92 | Test pattern to FOLLOW |
| P1 | `zombie-shooter/src/game/core/constants.py` | 1-68 | Constants file structure |

**External Documentation:**

| Source | Section | Why Needed |
|--------|---------|------------|
| [Pygame Docs - draw.ellipse](https://www.pygame.org/docs/ref/draw.html#pygame.draw.ellipse) | ellipse function | Drawing blood pool shape |
| [Pygame Docs - SRCALPHA](https://www.pygame.org/docs/ref/surface.html#pygame.SRCALPHA) | alpha transparency | Alpha blending for blood pool |

---

## Patterns to Mirror

**NAMING_CONVENTION:**
```python
# SOURCE: zombie-shooter/src/game/entities/blood_particle.py:1-10
# COPY THIS PATTERN:
"""Blood particle entity for gore effects."""

from __future__ import annotations

import pygame

from game.core.constants import BLOOD_PARTICLE_LIFETIME, BLOOD_PARTICLE_RADIUS


class BloodParticle:
    """Blood particle that sprays from zombie death."""
```

**TTL_PATTERN:**
```python
# SOURCE: zombie-shooter/src/game/entities/blood_particle.py:13-26
# COPY THIS PATTERN:
def __init__(self, pos: pygame.Vector2, velocity: pygame.Vector2) -> None:
    """Initialize blood particle.

    Args:
        pos: Starting position.
        velocity: Initial velocity vector.
    """
    self.pos = pos.copy()  # Copy to avoid reference issues
    self.vel = velocity
    self.lifetime = BLOOD_PARTICLE_LIFETIME  # Seconds
    self.max_lifetime = BLOOD_PARTICLE_LIFETIME
    self.radius = BLOOD_PARTICLE_RADIUS
    self.color = (180, 0, 0)  # Dark red
```

**UPDATE_METHOD_PATTERN:**
```python
# SOURCE: zombie-shooter/src/game/entities/dead_zombie.py:43-54
# COPY THIS PATTERN:
def update(self, dt: float) -> bool:
    """Update corpse lifetime.

    Args:
        dt: Delta time in seconds.

    Returns:
        True if corpse is still alive, False if should be removed.
    """
    self.lifetime -= dt  # Countdown
    return self.is_alive()
```

**IS_ALIVE_PATTERN:**
```python
# SOURCE: zombie-shooter/src/game/entities/dead_zombie.py:56-62
# COPY THIS PATTERN:
def is_alive(self) -> bool:
    """Check if corpse should still exist.

    Returns:
        True if lifetime > 0, False otherwise.
    """
    return self.lifetime > 0
```

**ALPHA_DRAWING_PATTERN:**
```python
# SOURCE: zombie-shooter/src/game/entities/blood_particle.py:57-82
# COPY THIS PATTERN:
def draw(self, screen: pygame.Surface) -> None:
    """Render blood particle with fade effect.

    Args:
        screen: Pygame surface to draw on.
    """
    # Create temporary surface for alpha blending
    temp_surface = pygame.Surface(
        (self.radius * 2, self.radius * 2), pygame.SRCALPHA
    )
    alpha = self.get_alpha()
    color_with_alpha = (*self.color, alpha)

    # Draw circle on temp surface
    pygame.draw.circle(
        temp_surface,
        color_with_alpha,
        (self.radius, self.radius),  # Center of temp surface
        self.radius,
    )

    # Blit temp surface to screen
    screen.blit(
        temp_surface,
        (int(self.pos.x) - self.radius, int(self.pos.y) - self.radius),
    )
```

**TEST_STRUCTURE:**
```python
# SOURCE: zombie-shooter/tests/test_blood_particle.py:13-27
# COPY THIS PATTERN:
def test_blood_particle_initialization() -> None:
    """Test that BloodParticle initializes with correct attributes."""
    pos = pygame.Vector2(100, 200)
    vel = pygame.Vector2(50, -30)

    particle = BloodParticle(pos, vel)

    assert particle.pos.x == 100
    assert particle.pos.y == 200
    assert particle.vel.x == 50
    assert particle.vel.y == -30
    assert particle.lifetime > 0
    assert particle.radius == 3
    assert particle.is_alive() is True
```

---

## Files to Change

| File                                      | Action | Justification                            |
| ----------------------------------------- | ------ | ---------------------------------------- |
| `zombie-shooter/src/game/core/constants.py` | UPDATE | Add BLOOD_POOL_SIZE constant |
| `zombie-shooter/src/game/entities/blood_decal.py` | CREATE | BloodDecal entity class |
| `zombie-shooter/tests/test_blood_decal.py` | CREATE | Unit tests for BloodDecal |

---

## NOT Building (Scope Limits)

Explicit exclusions to prevent scope creep:

- **PlayScene integration**: Deferred to Phase 4 (Gore Integration) - this phase only creates the entity class
- **Variable blood pool sizes**: Fixed size for all kills, no randomization
- **Blood pool animation**: Static ellipse, no spreading or dripping animation
- **Blood pool stacking**: Multiple pools can overlap, no special handling
- **Collision detection**: Blood pools are purely visual, no physics
- **Alpha fade over time**: Constant alpha (with optional light fade), not gradual fade like particles

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: UPDATE `zombie-shooter/src/game/core/constants.py`

- **ACTION**: ADD blood pool size constant after corpse persistence constant
- **IMPLEMENT**: `BLOOD_POOL_SIZE = 28  # Pixel diameter of blood pool`
- **MIRROR**: `zombie-shooter/src/game/core/constants.py:60-62` (gore effects section)
- **PLACEMENT**: After line 62 (CORPSE_PERSISTENCE), before spawning constants
- **GOTCHA**: Use int literal (28 not 28.0) for size constant
- **VALIDATE**: `cd zombie-shooter && .venv/bin/ruff check src/game/core/constants.py`

### Task 2: CREATE `zombie-shooter/src/game/entities/blood_decal.py`

- **ACTION**: CREATE BloodDecal entity class
- **IMPLEMENT**:
  - Module docstring
  - Import statements (pygame, constants)
  - `BloodDecal` class with:
    - `__init__(pos: pygame.Vector2)` - copy position, set lifetime, size, color
    - `update(dt: float) -> bool` - countdown TTL, return is_alive()
    - `is_alive() -> bool` - check lifetime > 0
    - `draw(screen: pygame.Surface)` - draw red ellipse with alpha
- **MIRROR**:
  - TTL pattern: `zombie-shooter/src/game/entities/dead_zombie.py:36-62`
  - Alpha drawing: `zombie-shooter/src/game/entities/blood_particle.py:57-82`
- **IMPORTS**:
  ```python
  from __future__ import annotations

  import pygame

  from game.core.constants import BLOOD_POOL_SIZE, CORPSE_PERSISTENCE
  ```
- **DRAWING**: Use `pygame.draw.ellipse()` on temporary SRCALPHA surface, with slight alpha (200 for semi-transparency)
- **GOTCHA**:
  - Use `pos.copy()` to avoid reference bugs
  - Blood pool should be slightly transparent (alpha ~200, not 255) for layering
  - Use CORPSE_PERSISTENCE for lifetime to match corpse duration
- **VALIDATE**: `cd zombie-shooter && .venv/bin/ruff check src/game/entities/blood_decal.py && .venv/bin/ruff format src/game/entities/blood_decal.py`

### Task 3: CREATE `zombie-shooter/tests/test_blood_decal.py`

- **ACTION**: CREATE unit tests for BloodDecal
- **IMPLEMENT**: Test cases for:
  - Initialization (position, lifetime, size, is_alive)
  - Update decreases lifetime
  - Update returns True when alive
  - Decal dies when lifetime expires (update returns False)
  - Draw executes without error (smoke test)
  - Position copy independence (source pos change doesn't affect entity)
- **MIRROR**: `zombie-shooter/tests/test_blood_particle.py:1-92` (all test patterns)
- **IMPORTS**:
  ```python
  from __future__ import annotations

  import pygame

  from game.entities.blood_decal import BloodDecal

  # Initialize pygame once for all tests
  pygame.init()
  ```
- **TEST_COUNT**: 6 tests minimum (matching BloodParticle/DeadZombie coverage pattern)
- **GOTCHA**: Initialize pygame before any entity creation (drawing requires pygame initialized)
- **VALIDATE**: `cd zombie-shooter && PYTHONPATH=src .venv/bin/pytest tests/test_blood_decal.py -v`

### Task 4: RUN full validation suite

- **ACTION**: Run all validation levels
- **IMPLEMENT**: Execute Level 1-3 validation commands
- **VALIDATE**:
  ```bash
  cd zombie-shooter
  .venv/bin/ruff check .
  .venv/bin/ruff format .
  PYTHONPATH=src .venv/bin/pytest -v
  ```
- **EXPECT**:
  - Ruff check: Exit 0, no errors
  - Ruff format: No changes needed
  - Pytest: All tests pass (including 6 new blood_decal tests)

---

## Testing Strategy

### Unit Tests to Write

| Test File                                | Test Cases (6 total)                 | Validates      |
| ---------------------------------------- | ------------------------------------ | -------------- |
| `zombie-shooter/tests/test_blood_decal.py` | - Initialization with correct attributes | Constructor |
|                                          | - Update decreases lifetime | TTL countdown |
|                                          | - Update returns True when alive | Return value logic |
|                                          | - Entity dies when lifetime expires | Death condition |
|                                          | - Draw executes without error | Rendering |
|                                          | - Position copy independence | Reference safety |

### Edge Cases Checklist

- [ ] Lifetime exactly 0.0 (boundary case)
- [ ] Negative lifetime after large dt (should still die)
- [ ] Draw before pygame initialized (handled by test setup)
- [ ] Position mutation after creation (should not affect entity)
- [ ] Multiple BloodDecal instances can overlap (no special handling needed)

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
cd zombie-shooter
.venv/bin/ruff check .
.venv/bin/ruff format .
```

**EXPECT**: Exit 0, no errors or warnings

### Level 2: UNIT_TESTS

```bash
cd zombie-shooter
PYTHONPATH=src .venv/bin/pytest tests/test_blood_decal.py -v
```

**EXPECT**: 6 tests pass, coverage adequate

### Level 3: FULL_SUITE

```bash
cd zombie-shooter
PYTHONPATH=src .venv/bin/pytest -v
```

**EXPECT**: All tests pass (existing + 6 new = ~81 total)

### Level 4: DATABASE_VALIDATION

N/A - no database changes

### Level 5: BROWSER_VALIDATION

N/A - no UI integration yet (deferred to Phase 4)

### Level 6: MANUAL_VALIDATION

Not applicable until Phase 4 integration - entity class only, not wired into game loop yet.

---

## Acceptance Criteria

- [ ] `BLOOD_POOL_SIZE` constant added to constants.py
- [ ] `BloodDecal` class created with TTL pattern
- [ ] BloodDecal draws red ellipse with alpha transparency
- [ ] BloodDecal.update() returns bool (True=alive, False=remove)
- [ ] BloodDecal.is_alive() checks lifetime > 0
- [ ] BloodDecal.draw() renders ellipse at position
- [ ] Unit tests cover initialization, TTL, draw, position copy
- [ ] Level 1-3 validation passes
- [ ] Code mirrors existing patterns (TTL from BloodParticle/DeadZombie)
- [ ] No regressions in existing tests
- [ ] All type hints present and correct

---

## Completion Checklist

- [ ] Task 1: Constants updated
- [ ] Task 2: BloodDecal class created
- [ ] Task 3: Unit tests created
- [ ] Task 4: Full validation passed
- [ ] Level 1: Static analysis passes
- [ ] Level 2: Unit tests pass (6 new tests)
- [ ] Level 3: Full test suite passes
- [ ] All acceptance criteria met
- [ ] Implementation report created
- [ ] PRD Phase 3 status updated to complete

---

## Risks and Mitigations

| Risk               | Likelihood   | Impact       | Mitigation                              |
| ------------------ | ------------ | ------------ | --------------------------------------- |
| Blood pools overlap poorly | LOW | LOW | Alpha transparency ensures layering looks acceptable |
| Drawing overhead | LOW | LOW | Simple ellipse draw is very fast, max ~50 pools |
| Memory with many pools | LOW | LOW | 10s TTL ensures max ~50 pools (5 kills/sec) |
| Position reference bugs | LOW | MEDIUM | Use pos.copy() pattern from BloodParticle |

---

## Notes

**Design Decision - Simple Ellipse**: BloodDecal uses `pygame.draw.ellipse()` instead of loading sprite assets. This keeps implementation simple and matches the "programmer art" approach for MVP.

**Design Decision - Semi-Transparent**: Blood pools use alpha ~200 (not 255) for slight transparency. This allows multiple pools to stack/layer without looking completely opaque, and lets the background show through slightly.

**Design Decision - Fixed Size**: All blood pools are the same size (BLOOD_POOL_SIZE constant). This simplifies implementation and maintains consistency. Variable sizes could be added later.

**Design Decision - Same Lifetime as Corpse**: Blood pools use CORPSE_PERSISTENCE (10 seconds) instead of a separate constant. This ensures blood pools and corpses disappear together, keeping the cleanup synchronized.

**Integration Deferred**: PlayScene integration is intentionally deferred to Phase 4 (Gore Integration) to keep this phase focused and independently testable. The entity class is complete and ready to use, but spawning logic will be added when wiring all gore systems together.

**Rendering Order**: Blood decals should be drawn FIRST (underneath everything) so corpses appear on top of them. This will be handled in Phase 4 integration.

**Future Enhancement Opportunities** (out of scope for now):
- Variable blood pool sizes based on weapon/overkill
- Blood pool spreading animation
- Multiple blood pool shapes (circular, splatter patterns)
- Gradual alpha fade in final 2 seconds
- Blood pool stacking limit (remove oldest if >100)
