# Feature: Dead Zombie Entity (Corpse Persistence)

## Summary

Create a `DeadZombie` entity that persists for 10 seconds after a zombie is killed, providing visual feedback of combat and creating a more satisfying gore experience. The entity combines TTL (time-to-live) pattern from BloodParticle/Pickup with sprite rendering from Zombie, displaying a static fallen zombie sprite that auto-removes after its lifetime expires.

## User Story

As a player
I want to see zombie corpses remain on the battlefield for a short time after I kill them
So that I can see the result of my actions and feel the impact of combat

## Problem Statement

Currently, zombies instantly disappear when killed, making combat feel less impactful and providing no visual record of the player's actions. This reduces satisfaction and makes it harder to visually track which areas have seen heavy combat.

## Solution Statement

Implement a `DeadZombie` entity that spawns at the position of a killed zombie, displays a static sprite (rotated 90° for fallen effect), persists for 10 seconds with TTL countdown, and auto-removes when lifetime expires. This uses proven patterns from existing codebase: TTL from BloodParticle/Pickup, sprite rendering from Zombie, and PlayScene integration following bullet/pickup patterns.

## Metadata

| Field            | Value                                             |
| ---------------- | ------------------------------------------------- |
| Type             | NEW_CAPABILITY                                    |
| Complexity       | LOW                                               |
| Systems Affected | entities, scenes, core constants                  |
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
║   │   Shoots    │         │   Zombie    │         │   Vanishes  │            ║
║   └─────────────┘         └─────────────┘         └─────────────┘            ║
║                                                           │                   ║
║                                                           ▼                   ║
║                                                    [INSTANT REMOVAL]          ║
║                                                    (no visual trace)          ║
║                                                                               ║
║   USER_FLOW: Kill zombie → instant disappearance → no feedback               ║
║   PAIN_POINT: Combat feels weightless, can't see battle history              ║
║   DATA_FLOW: Zombie removed from list immediately on bullet collision        ║
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
║                                                  │ DeadZombie  │              ║
║                                                  │  (corpse)   │              ║
║                                                  │ 10s persist │              ║
║                                                  └─────────────┘              ║
║                                                           │                   ║
║                                                           ▼                   ║
║                                                   [FADE AFTER 10s]            ║
║                                                                               ║
║   USER_FLOW: Kill zombie → corpse appears → persists 10s → fades away        ║
║   VALUE_ADD: Visual combat feedback, battlefield "history", satisfaction     ║
║   DATA_FLOW: Zombie removed → DeadZombie spawned → TTL countdown → removal   ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location        | Before          | After       | User_Action | Impact        |
| --------------- | --------------- | ----------- | ----------- | ------------- |
| Play scene      | Zombie vanishes | Corpse appears | Kill zombie | Visual feedback |
| Battlefield     | No combat trace | Corpses visible | Look around | See battle history |
| 10 seconds later | N/A | Corpse fades | Wait | Auto-cleanup |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `zombie-shooter/src/game/entities/blood_particle.py` | 1-83 | TTL pattern to MIRROR (just implemented in Phase 1) |
| P0 | `zombie-shooter/src/game/entities/pickup.py` | 1-78 | Alternative TTL pattern example |
| P0 | `zombie-shooter/src/game/entities/zombie.py` | 1-97 | Sprite rendering pattern to MIRROR |
| P1 | `zombie-shooter/tests/test_blood_particle.py` | 1-92 | Test pattern to FOLLOW (just created in Phase 1) |
| P1 | `zombie-shooter/src/game/core/constants.py` | 1-52 | Constants file structure |

**External Documentation:**

| Source | Section | Why Needed |
|--------|---------|------------|
| [Pygame Docs - Surface.blit](https://www.pygame.org/docs/ref/surface.html#pygame.Surface.blit) | blit method | Understanding sprite rendering |
| [Pygame Docs - transform.rotate](https://www.pygame.org/docs/ref/transform.html#pygame.transform.rotate) | rotate function | 90° rotation for fallen effect |

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
# SOURCE: zombie-shooter/src/game/entities/blood_particle.py:27-38
# COPY THIS PATTERN:
def update(self, dt: float) -> bool:
    """Update particle position and lifetime.

    Args:
        dt: Delta time in seconds.

    Returns:
        True if particle is still alive, False if should be removed.
    """
    self.pos += self.vel * dt  # Physics update
    self.lifetime -= dt  # Countdown
    return self.is_alive()
```

**IS_ALIVE_PATTERN:**
```python
# SOURCE: zombie-shooter/src/game/entities/blood_particle.py:40-46
# COPY THIS PATTERN:
def is_alive(self) -> bool:
    """Check if particle should still exist.

    Returns:
        True if lifetime > 0, False otherwise.
    """
    return self.lifetime > 0
```

**SPRITE_RENDERING_PATTERN:**
```python
# SOURCE: zombie-shooter/src/game/entities/zombie.py:72-86
# COPY THIS PATTERN:
def draw(self, screen: pygame.Surface) -> None:
    """Render zombie sprite.

    Args:
        screen: Pygame surface to draw on.
    """
    # Get direction index (0=right, 1=down, 2=left, 3=up)
    direction_idx = self.get_direction_index()

    # Get sprite for current direction and frame
    sprite = self.sprites[direction_idx][self.current_frame]

    # Center sprite on position
    rect = sprite.get_rect(center=(int(self.pos.x), int(self.pos.y)))
    screen.blit(sprite, rect)
```

**MODULE_LEVEL_SPRITE_CACHING:**
```python
# SOURCE: zombie-shooter/src/game/entities/zombie.py:12-33
# COPY THIS PATTERN:
# Load zombie sprites once at module level (cached across instances)
def _load_zombie_sprites() -> list[list[pygame.Surface]]:
    """Load zombie sprites for all directions.

    Returns:
        2D list: [direction][frame] of surfaces.
    """
    # ... sprite loading logic ...
    return sprites


# Cache sprites at module level
_ZOMBIE_SPRITES = _load_zombie_sprites()
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
| `zombie-shooter/src/game/core/constants.py` | UPDATE | Add CORPSE_PERSISTENCE constant |
| `zombie-shooter/src/game/entities/dead_zombie.py` | CREATE | DeadZombie entity class |
| `zombie-shooter/tests/test_dead_zombie.py` | CREATE | Unit tests for DeadZombie |

---

## NOT Building (Scope Limits)

Explicit exclusions to prevent scope creep:

- **PlayScene integration**: Deferred to Phase 4 (Gore Integration) - this phase only creates the entity class
- **Corpse collision**: Dead zombies are purely visual, no physics/collision
- **Animation**: Static sprite only (no fade animation, rotation happens once on creation)
- **Blood decals**: Separate entity in Phase 3
- **Corpse variants**: Single fallen zombie sprite, no randomization

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: UPDATE `zombie-shooter/src/game/core/constants.py`

- **ACTION**: ADD corpse persistence constant after blood particle constants
- **IMPLEMENT**: `CORPSE_PERSISTENCE = 10.0  # Seconds dead zombie remains visible`
- **MIRROR**: `zombie-shooter/src/game/core/constants.py:45-48` (blood particle constants section)
- **PLACEMENT**: After line 48 (BLOOD_PARTICLE_RADIUS), before zombie movement constants
- **GOTCHA**: Use float literal (10.0 not 10) for consistency with other time constants
- **VALIDATE**: `cd zombie-shooter && .venv/bin/ruff check src/game/core/constants.py`

### Task 2: CREATE `zombie-shooter/src/game/entities/dead_zombie.py`

- **ACTION**: CREATE DeadZombie entity class
- **IMPLEMENT**:
  - Module docstring
  - Import statements (pygame, constants, zombie sprites)
  - `_load_dead_zombie_sprite()` function - load and rotate zombie sprite 90° clockwise
  - Module-level sprite cache: `_DEAD_ZOMBIE_SPRITE`
  - `DeadZombie` class with:
    - `__init__(pos: pygame.Vector2)` - copy position, set lifetime
    - `update(dt: float) -> bool` - countdown TTL, return is_alive()
    - `is_alive() -> bool` - check lifetime > 0
    - `draw(screen: pygame.Surface)` - blit rotated sprite
- **MIRROR**:
  - TTL pattern: `zombie-shooter/src/game/entities/blood_particle.py:13-46`
  - Sprite rendering: `zombie-shooter/src/game/entities/zombie.py:72-86`
  - Module caching: `zombie-shooter/src/game/entities/zombie.py:12-33`
- **IMPORTS**:
  ```python
  from __future__ import annotations

  import pygame

  from game.core.constants import CORPSE_PERSISTENCE
  from game.entities.zombie import _ZOMBIE_SPRITES
  ```
- **SPRITE_ROTATION**: Use `pygame.transform.rotate(sprite, -90)` for 90° clockwise rotation
- **GOTCHA**:
  - Use `pos.copy()` to avoid reference bugs
  - Zombie sprites are 2D list `[direction][frame]` - use `_ZOMBIE_SPRITES[1][0]` (down direction, first frame) as base
  - Negative angle for clockwise rotation (-90, not 90)
- **VALIDATE**: `cd zombie-shooter && .venv/bin/ruff check src/game/entities/dead_zombie.py && .venv/bin/ruff format src/game/entities/dead_zombie.py && .venv/bin/mypy src/game/entities/dead_zombie.py`

### Task 3: CREATE `zombie-shooter/tests/test_dead_zombie.py`

- **ACTION**: CREATE unit tests for DeadZombie
- **IMPLEMENT**: Test cases for:
  - Initialization (position, lifetime, is_alive)
  - Update decreases lifetime
  - Update returns True when alive
  - Particle dies when lifetime expires (update returns False)
  - Draw executes without error (smoke test)
  - Position copy independence (source pos change doesn't affect entity)
- **MIRROR**: `zombie-shooter/tests/test_blood_particle.py:1-92` (all test patterns)
- **IMPORTS**:
  ```python
  from __future__ import annotations

  import pygame

  from game.entities.dead_zombie import DeadZombie

  # Initialize pygame once for all tests
  pygame.init()
  ```
- **TEST_COUNT**: 6 tests minimum (matching BloodParticle coverage pattern)
- **GOTCHA**: Initialize pygame before any entity creation (sprites need pygame.display initialized)
- **VALIDATE**: `cd zombie-shooter && PYTHONPATH=src .venv/bin/pytest tests/test_dead_zombie.py -v`

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
  - Pytest: All tests pass (including 6 new dead_zombie tests)

---

## Testing Strategy

### Unit Tests to Write

| Test File                                | Test Cases (6 total)                 | Validates      |
| ---------------------------------------- | ------------------------------------ | -------------- |
| `zombie-shooter/tests/test_dead_zombie.py` | - Initialization with correct attributes | Constructor |
|                                          | - Update decreases lifetime | TTL countdown |
|                                          | - Update returns True when alive | Return value logic |
|                                          | - Entity dies when lifetime expires | Death condition |
|                                          | - Draw executes without error | Rendering |
|                                          | - Position copy independence | Reference safety |

### Edge Cases Checklist

- [ ] Lifetime exactly 0.0 (boundary case)
- [ ] Negative lifetime after large dt (should still die)
- [ ] Draw before sprite loaded (handled by module cache)
- [ ] Position mutation after creation (should not affect entity)
- [ ] Multiple DeadZombie instances share sprite cache (memory efficiency)

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
PYTHONPATH=src .venv/bin/pytest tests/test_dead_zombie.py -v
```

**EXPECT**: 6 tests pass, coverage adequate

### Level 3: FULL_SUITE

```bash
cd zombie-shooter
PYTHONPATH=src .venv/bin/pytest -v
```

**EXPECT**: All tests pass (existing + 6 new = ~75 total)

### Level 4: DATABASE_VALIDATION

N/A - no database changes

### Level 5: BROWSER_VALIDATION

N/A - no UI integration yet (deferred to Phase 4)

### Level 6: MANUAL_VALIDATION

Not applicable until Phase 4 integration - entity class only, not wired into game loop yet.

---

## Acceptance Criteria

- [ ] `CORPSE_PERSISTENCE` constant added to constants.py
- [ ] `DeadZombie` class created with TTL pattern
- [ ] DeadZombie uses rotated zombie sprite (90° clockwise)
- [ ] DeadZombie.update() returns bool (True=alive, False=remove)
- [ ] DeadZombie.is_alive() checks lifetime > 0
- [ ] DeadZombie.draw() renders sprite at position
- [ ] Module-level sprite caching implemented
- [ ] Unit tests cover initialization, TTL, draw, position copy
- [ ] Level 1-3 validation passes
- [ ] Code mirrors existing patterns (TTL from BloodParticle, sprite from Zombie)
- [ ] No regressions in existing tests
- [ ] All type hints present and correct

---

## Completion Checklist

- [ ] Task 1: Constants updated
- [ ] Task 2: DeadZombie class created
- [ ] Task 3: Unit tests created
- [ ] Task 4: Full validation passed
- [ ] Level 1: Static analysis passes
- [ ] Level 2: Unit tests pass (6 new tests)
- [ ] Level 3: Full test suite passes
- [ ] All acceptance criteria met
- [ ] Implementation report created
- [ ] PRD Phase 2 status updated to complete

---

## Risks and Mitigations

| Risk               | Likelihood   | Impact       | Mitigation                              |
| ------------------ | ------------ | ------------ | --------------------------------------- |
| Sprite loading overhead | LOW | LOW | Module-level caching prevents repeated loads |
| Rotated sprite quality | LOW | LOW | pygame.transform.rotate preserves quality at 90° |
| Memory with many corpses | LOW | LOW | 10s TTL ensures max ~50 corpses (5 kills/sec) |
| Position reference bugs | LOW | MEDIUM | Use pos.copy() pattern from BloodParticle |

---

## Notes

**Design Decision - Static Sprite**: DeadZombie uses a single rotated sprite (no animation) for simplicity and performance. The 90° rotation creates a "fallen" effect that clearly distinguishes corpses from live zombies.

**Design Decision - No Collision**: Dead zombies are purely visual - they do not block movement or bullets. This prevents gameplay disruption while maintaining visual feedback.

**Design Decision - 10 Second Persistence**: Balances visual feedback (see recent combat) with screen clutter (automatic cleanup). Long enough to appreciate, short enough to not overwhelm.

**Integration Deferred**: PlayScene integration is intentionally deferred to Phase 4 (Gore Integration) to keep this phase focused and independently testable. The entity class is complete and ready to use, but spawning logic will be added when wiring all gore systems together.

**Sprite Reuse**: DeadZombie reuses the Zombie entity's sprite system rather than loading separate assets. This maintains visual consistency and reduces asset duplication.

**Future Enhancement Opportunities** (out of scope for now):
- Multiple corpse orientations (random rotation angles)
- Blood pool decal integration (Phase 3)
- Fade-out animation in final 2 seconds
- Corpse variants (different death poses)
