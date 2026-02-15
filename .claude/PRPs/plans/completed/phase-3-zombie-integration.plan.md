# Feature: Phase 3 - Zombie Integration

## Summary

Replace circle rendering with animated sprites for zombie entities. Integrate Animation system (Phase 1) and asset loader (Phase 2) into Zombie class by adding an Animation instance, calling animation.update() during zombie update, and blitting sprites instead of drawing circles. Zombies will display 4-direction walk cycle animations that match their velocity vector.

## User Story

As a player/developer
I want to see zombies as animated sprites that face their movement direction
So that the game feels more alive, polished, and visually engaging

## Problem Statement

Zombies currently render as static green circles with no directional or animation feedback. Players cannot intuitively understand zombie behavior through visual cues. The game feels placeholder-like and unpolished. This phase integrates the Animation system (Phase 1) and sprite assets (Phase 2) to transform zombies into visually engaging animated entities.

## Solution Statement

Modify the Zombie entity to use the Animation system for directional sprite rendering. Load zombie sprites once at module level (shared across all instances), create an Animation instance per zombie, update animation state based on velocity, and blit the current frame sprite instead of drawing a circle. The Animation system handles direction detection and frame cycling, while the Zombie class focuses on movement and rendering integration.

## Metadata

| Field            | Value                                             |
| ---------------- | ------------------------------------------------- |
| Type             | ENHANCEMENT |
| Complexity       | LOW-MEDIUM |
| Systems Affected | Zombie entity, potentially entity tests |
| Dependencies     | pygame 2.6.0, Animation system (Phase 1), Asset loader (Phase 2) |
| Estimated Tasks  | 5 |

---

## UX Design

### Before State
```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│   Zombie     │         │   Zombie     │         │   Screen     │
│  Entity      │         │   update()   │         │   Render     │
│              │         │              │         │              │
│ pos: (x,y)   │ ──────► │ vel: (dx,dy) │ ──────► │   [green     │
│ radius: 16   │         │              │         │    circle]   │
│ speed: 140   │         │ moves toward │         │              │
└──────────────┘         │   player     │         │  No visual   │
                         └──────────────┘         │  direction   │
                                                  └──────────────┘

DATA FLOW: spawn_pos → Zombie(pos) → update(dt, player_pos) → draw(circle)
PAIN: No visual direction, feels placeholder-like, no animation feedback
```

### After State
```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│   Zombie     │         │   Zombie     │         │   Screen     │
│  Entity      │         │   update()   │         │   Render     │
│              │         │              │         │              │
│ pos: (x,y)   │         │ vel: (dx,dy) │         │   [zombie    │
│ animation    │ ──────► │              │ ──────► │    sprite]   │
│ sprites{}    │         │ animation.   │         │   facing     │
└──────────────┘         │ update(dt,v) │         │   direction  │
      │                  └──────────────┘         └──────────────┘
      ▼                           │
┌──────────────┐                 ▼
│  Animation   │         ┌──────────────┐
│   System     │◄────────│ get_current_ │
│              │         │   frame()    │
│ direction    │         │              │
│ frame_index  │         │ Returns      │
│ frame_timer  │         │ pygame.      │
└──────────────┘         │ Surface      │
      │                  └──────────────┘
      ▼
┌──────────────┐
│ Sprite Dict  │  ◄── loaded from load_zombie_sprites()
│              │
│ "down": [f0, f1, f2]
│ "up":   [f0, f1, f2]
│ "left": [f0, f1, f2]
│ "right":[f0, f1, f2]
└──────────────┘

DATA FLOW:
  load_zombie_sprites() → sprites_dict (cached)
    ↓
  Zombie.__init__(pos) → Animation(fps=10, frames=3)
    ↓
  update(dt, player_pos) → animation.update(dt, self.vel)
    ↓
  draw(screen) → animation.get_current_frame() → sprites[dir][frame]
    ↓
  screen.blit(sprite, centered_on_pos)

VALUE: Visual direction feedback, smooth walk cycle, polished feel
```

### Interaction Changes
| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| `zombie.py:35-44` | Green circle rendered | Animated sprite with direction | Zombies visually indicate movement direction |
| Zombie movement | No visual feedback | Sprite faces up/down/left/right | Player can anticipate zombie behavior |
| Stationary zombies | Same circle | First frame of walk cycle | Direction history preserved when stopped |
| Walk animation | No animation | 3-frame walk cycle at 10 FPS | Visual "life" and polish |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `zombie-shooter/src/game/entities/zombie.py` | 1-44 | Current Zombie implementation - MUST PRESERVE collision logic |
| P0 | `zombie-shooter/src/game/systems/animation.py` | 17-91 | Animation API to integrate - constructor, update(), get methods |
| P0 | `zombie-shooter/src/game/assets/loader.py` | 74-118 | Asset loading API - load_zombie_sprites() return structure |
| P1 | `zombie-shooter/src/game/entities/player.py` | 1-36 | Entity pattern for imports and __init__() structure |
| P1 | `zombie-shooter/src/game/core/constants.py` | 47-53 | Zombie constants including ZOMBIE_ANIMATION_FPS, ZOMBIE_FRAME_COUNT, ZOMBIE_SPRITE_SIZE |
| P2 | `zombie-shooter/tests/test_animation.py` | 1-100 | Test pattern for animation integration |
| P2 | `zombie-shooter/tests/test_collisions.py` | 1-50 | Test pattern for entity collision verification |

**External Documentation:**
| Source | Section | Why Needed |
|--------|---------|------------|
| [Pygame Docs - Surface.blit](https://www.pygame.org/docs/ref/surface.html#pygame.Surface.blit) | blit() method | Sprite rendering syntax |
| [Pygame Docs - Rect](https://www.pygame.org/docs/ref/rect.html#pygame.Rect.center) | get_rect(center=...) | Centering sprite on position |

---

## Patterns to Mirror

**IMPORT_PATTERN:**
```python
// SOURCE: zombie-shooter/src/game/entities/player.py:1-17
// COPY THIS PATTERN:
from __future__ import annotations

import pygame

from game.core.constants import (
    ZOMBIE_ANIMATION_FPS,
    ZOMBIE_FRAME_COUNT,
    ZOMBIE_RADIUS,
    ZOMBIE_SPEED,
    ZOMBIE_SPRITE_SIZE,
)
from game.systems.animation import Animation
from game.assets.loader import load_zombie_sprites
```

**CLASS_VARIABLE_PATTERN:**
```python
// SOURCE: Similar to asset loading cache pattern
// COPY THIS PATTERN:
# Module-level sprite loading (shared across all instances)
_zombie_sprites: dict[str, list[pygame.Surface]] | None = None

def _load_sprites() -> dict[str, list[pygame.Surface]]:
    """Load zombie sprites once and cache."""
    global _zombie_sprites
    if _zombie_sprites is None:
        _zombie_sprites = load_zombie_sprites(
            sprite_size=ZOMBIE_SPRITE_SIZE,
            frame_count=ZOMBIE_FRAME_COUNT
        )
    return _zombie_sprites
```

**INIT_PATTERN:**
```python
// SOURCE: zombie-shooter/src/game/entities/zombie.py:13-21
// EXTEND THIS PATTERN:
def __init__(self, pos: pygame.Vector2) -> None:
    """Initialize zombie.

    Args:
        pos: Starting position as Vector2.
    """
    self.pos = pos
    self.vel = pygame.Vector2(0, 0)  # Add this - needed for animation
    self.radius = ZOMBIE_RADIUS
    self.speed = ZOMBIE_SPEED

    # NEW: Load sprites and create animation
    self.sprites = _load_sprites()
    self.animation = Animation(
        frame_count=ZOMBIE_FRAME_COUNT,
        fps=ZOMBIE_ANIMATION_FPS
    )
```

**UPDATE_PATTERN:**
```python
// SOURCE: zombie-shooter/src/game/entities/zombie.py:23-33
// EXTEND THIS PATTERN:
def update(self, dt: float, player_pos: pygame.Vector2) -> None:
    """Move toward player position.

    Args:
        dt: Delta time in seconds.
        player_pos: Target player position to move toward.
    """
    direction = player_pos - self.pos
    if direction.length() > 0:
        self.vel = direction.normalize() * self.speed
        self.pos += self.vel * dt
    else:
        self.vel = pygame.Vector2(0, 0)  # Add this for stationary state

    # NEW: Update animation based on velocity
    self.animation.update(dt, self.vel)
```

**DRAW_PATTERN:**
```python
// SOURCE: zombie-shooter/src/game/entities/zombie.py:35-44
// REPLACE THIS WITH:
def draw(self, screen: pygame.Surface) -> None:
    """Draw zombie to screen.

    Args:
        screen: Pygame surface to draw on.
    """
    # Get current animation frame
    direction = self.animation.get_current_direction()
    frame_index = self.animation.get_current_frame_index()
    sprite = self.sprites[direction][frame_index]

    # Center sprite on zombie position
    sprite_rect = sprite.get_rect(center=(int(self.pos.x), int(self.pos.y)))
    screen.blit(sprite, sprite_rect)
```

**TEST_STRUCTURE:**
```python
// SOURCE: zombie-shooter/tests/test_animation.py:1-25
// COPY THIS PATTERN:
from __future__ import annotations

import pygame
from game.entities.zombie import Zombie

# Initialize pygame once for all tests
pygame.init()

def test_zombie_has_animation_instance() -> None:
    """Test that zombie initializes with Animation instance."""
    zombie = Zombie(pygame.Vector2(100, 100))
    assert hasattr(zombie, 'animation')
    assert zombie.animation is not None

def test_zombie_renders_sprite_not_circle() -> None:
    """Test that zombie uses sprite rendering (manual verification)."""
    zombie = Zombie(pygame.Vector2(100, 100))
    # Create dummy surface
    screen = pygame.Surface((800, 600))
    # Should not raise error
    zombie.draw(screen)
```

---

## Files to Change

| File                             | Action | Justification                            |
| -------------------------------- | ------ | ---------------------------------------- |
| `zombie-shooter/src/game/entities/zombie.py` | UPDATE | Add animation integration - imports, class variable, __init__, update, draw |
| `zombie-shooter/tests/test_zombie.py` | CREATE/UPDATE | Add tests for animation integration |

---

## NOT Building (Scope Limits)

Explicit exclusions to prevent scope creep:

- **Player animations** - Out of scope, player remains circle (PRD Phase scope)
- **Death animations** - Zombies disappear instantly on kill (no fade/death sequence)
- **Attack animations** - No special animation for damage states
- **8-direction sprites** - Using 4-direction only (PRD decision)
- **Animation blending/smoothing** - Instant direction changes (PRD decision)
- **Dynamic asset loading** - Sprites loaded once at import, not on-demand
- **Sprite-based collision** - Keep existing radius-based collision (sprite is visual only)

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: UPDATE `zombie-shooter/src/game/entities/zombie.py` - Add imports

- **ACTION**: Add animation and asset loader imports to zombie.py
- **IMPLEMENT**:
  ```python
  from game.systems.animation import Animation
  from game.assets.loader import load_zombie_sprites
  from game.core.constants import (
      ZOMBIE_ANIMATION_FPS,
      ZOMBIE_FRAME_COUNT,
      ZOMBIE_RADIUS,
      ZOMBIE_SPEED,
      ZOMBIE_SPRITE_SIZE,
  )
  ```
- **MIRROR**: `zombie-shooter/src/game/entities/player.py:1-17` - import pattern
- **LOCATION**: Insert after existing imports, before class definition
- **GOTCHA**: Import from `game.systems.animation` not `game.animation` (systems subdirectory)
- **VALIDATE**: `cd zombie-shooter && ruff check src/game/entities/zombie.py` - no import errors

### Task 2: UPDATE `zombie-shooter/src/game/entities/zombie.py` - Add module-level sprite loading

- **ACTION**: Add module-level sprite loading function before Zombie class
- **IMPLEMENT**:
  ```python
  # Module-level sprite loading (shared across all instances)
  _zombie_sprites: dict[str, list[pygame.Surface]] | None = None


  def _load_sprites() -> dict[str, list[pygame.Surface]]:
      """Load zombie sprites once and cache at module level.

      Returns:
          Dictionary mapping direction to list of sprite frames.
      """
      global _zombie_sprites
      if _zombie_sprites is None:
          _zombie_sprites = load_zombie_sprites(
              sprite_size=ZOMBIE_SPRITE_SIZE,
              frame_count=ZOMBIE_FRAME_COUNT
          )
      return _zombie_sprites
  ```
- **MIRROR**: Asset caching pattern from `zombie-shooter/src/game/assets/loader.py:96-99`
- **LOCATION**: After imports, before `class Zombie:`
- **GOTCHA**: Use `global` keyword to modify module-level variable
- **VALIDATE**: `cd zombie-shooter && ruff check src/game/entities/zombie.py && mypy src/game/entities/zombie.py` - type hints correct

### Task 3: UPDATE `zombie-shooter/src/game/entities/zombie.py` - Modify __init__() to create Animation

- **ACTION**: Add `self.vel`, `self.sprites`, `self.animation` attributes to __init__()
- **IMPLEMENT**:
  ```python
  def __init__(self, pos: pygame.Vector2) -> None:
      """Initialize zombie.

      Args:
          pos: Starting position as Vector2.
      """
      self.pos = pos
      self.vel = pygame.Vector2(0, 0)  # Initialize velocity for animation
      self.radius = ZOMBIE_RADIUS
      self.speed = ZOMBIE_SPEED

      # Load sprites and create animation instance
      self.sprites = _load_sprites()
      self.animation = Animation(
          frame_count=ZOMBIE_FRAME_COUNT,
          fps=ZOMBIE_ANIMATION_FPS
      )
  ```
- **MIRROR**: `zombie-shooter/src/game/entities/zombie.py:13-21` - extend existing __init__()
- **LOCATION**: Replace lines 13-21 in zombie.py
- **GOTCHA**: Must initialize `self.vel` to Vector2(0,0) for animation.update() to work correctly
- **VALIDATE**: `cd zombie-shooter && python -c "import pygame; pygame.init(); from game.entities.zombie import Zombie; z = Zombie(pygame.Vector2(100, 100)); print('✓ Zombie instantiation works')"` - no errors

### Task 4: UPDATE `zombie-shooter/src/game/entities/zombie.py` - Modify update() to call animation.update()

- **ACTION**: Add animation.update() call at end of update() method, handle zero velocity case
- **IMPLEMENT**:
  ```python
  def update(self, dt: float, player_pos: pygame.Vector2) -> None:
      """Move toward player position.

      Args:
          dt: Delta time in seconds.
          player_pos: Target player position to move toward.
      """
      direction = player_pos - self.pos
      if direction.length() > 0:
          self.vel = direction.normalize() * self.speed
          self.pos += self.vel * dt
      else:
          self.vel = pygame.Vector2(0, 0)  # Explicitly set zero velocity when stationary

      # Update animation based on current velocity
      self.animation.update(dt, self.vel)
  ```
- **MIRROR**: `zombie-shooter/src/game/entities/zombie.py:23-33` - extend existing update()
- **LOCATION**: Replace lines 23-33 in zombie.py
- **GOTCHA**: Animation needs velocity even when stationary - set to Vector2(0,0) explicitly in else branch
- **VALIDATE**: `cd zombie-shooter && python -c "import pygame; pygame.init(); from game.entities.zombie import Zombie; z = Zombie(pygame.Vector2(100, 100)); z.update(0.016, pygame.Vector2(200, 200)); print('✓ Zombie update with animation works')"` - no errors

### Task 5: UPDATE `zombie-shooter/src/game/entities/zombie.py` - Replace draw() circle with sprite blit

- **ACTION**: Replace pygame.draw.circle() with sprite rendering
- **IMPLEMENT**:
  ```python
  def draw(self, screen: pygame.Surface) -> None:
      """Draw zombie to screen.

      Args:
          screen: Pygame surface to draw on.
      """
      # Get current animation frame
      direction = self.animation.get_current_direction()
      frame_index = self.animation.get_current_frame_index()
      sprite = self.sprites[direction][frame_index]

      # Center sprite on zombie position
      sprite_rect = sprite.get_rect(center=(int(self.pos.x), int(self.pos.y)))
      screen.blit(sprite, sprite_rect)
  ```
- **MIRROR**: Pygame blit pattern from pygame documentation
- **LOCATION**: Replace lines 35-44 in zombie.py
- **GOTCHA**: Use `get_rect(center=...)` to center sprite on position (not top-left)
- **VALIDATE**: `cd zombie-shooter && python -m game.main` - run game, verify zombies render as sprites (manual verification)

---

## Testing Strategy

### Unit Tests to Write

| Test File                                | Test Cases                 | Validates      |
| ---------------------------------------- | -------------------------- | -------------- |
| `zombie-shooter/tests/test_zombie_integration.py` | test_zombie_has_animation_instance | Animation attribute exists |
| | test_zombie_has_sprites_loaded | Sprites loaded correctly |
| | test_zombie_animation_updates_on_movement | Animation.update() called |
| | test_zombie_renders_without_error | draw() doesn't raise exceptions |
| | test_zombie_collision_unchanged | Collision still uses pos/radius |

### Edge Cases Checklist

- [ ] Zero velocity - animation shows frame 0 of current direction
- [ ] Direction changes - animation switches immediately to new direction
- [ ] Stationary zombie - still renders sprite (not blank)
- [ ] Multiple zombies - all animate independently
- [ ] Collision detection - still works with radius (not sprite bounds)
- [ ] Performance - 50 zombies at 60 FPS with no degradation

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
cd zombie-shooter && ruff check src/game/entities/zombie.py && ruff format src/game/entities/zombie.py
```

**EXPECT**: Exit 0, no errors or warnings

### Level 2: TYPE_CHECK

```bash
cd zombie-shooter && mypy src/game/entities/zombie.py
```

**EXPECT**: Exit 0, no type errors

### Level 3: UNIT_TESTS

```bash
cd zombie-shooter && pytest tests/test_zombie_integration.py -v
```

**EXPECT**: All tests pass

### Level 4: FULL_TEST_SUITE

```bash
cd zombie-shooter && pytest -q
```

**EXPECT**: All existing tests still pass (no regressions)

### Level 5: COLLISION_VALIDATION

```bash
cd zombie-shooter && pytest tests/test_collisions.py -v -k zombie
```

**EXPECT**: Collision tests pass (radius-based collision unchanged)

### Level 6: MANUAL_GAMEPLAY_VALIDATION

```bash
cd zombie-shooter && python -m game.main
```

**Manual checks:**
1. Zombies spawn as animated sprites (not circles)
2. Zombies face direction of movement (up/down/left/right)
3. Walk cycle animates smoothly (3 frames looping)
4. Direction changes update sprite instantly
5. Stationary zombies show first frame of last direction
6. Performance: 60 FPS maintained with 50 zombies
7. Collision detection still works (shoot zombies)

---

## Acceptance Criteria

- [ ] Zombie entity has `animation` and `sprites` attributes
- [ ] Zombies render as sprites instead of circles
- [ ] Sprites face direction of movement (4 cardinal directions)
- [ ] Walk cycle animates at 10 FPS (3 frames per direction)
- [ ] Stationary zombies show first frame of current direction
- [ ] Level 1-5 validation commands pass with exit 0
- [ ] Manual gameplay validation confirms visual behavior matches PRD
- [ ] Code mirrors existing patterns (imports, docstrings, type hints)
- [ ] No regressions in collision detection or game logic
- [ ] Performance: 60 FPS maintained with 50 zombies

---

## Completion Checklist

- [ ] Task 1: Imports added
- [ ] Task 2: Module-level sprite loading added
- [ ] Task 3: __init__() modified with Animation instance
- [ ] Task 4: update() calls animation.update()
- [ ] Task 5: draw() renders sprite instead of circle
- [ ] Level 1: Static analysis passes (ruff check + format)
- [ ] Level 2: Type check passes (mypy)
- [ ] Level 3: Unit tests pass (pytest test_zombie_integration.py)
- [ ] Level 4: Full test suite passes (pytest -q)
- [ ] Level 5: Collision tests pass (test_collisions.py)
- [ ] Level 6: Manual gameplay validation completed
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk               | Likelihood | Impact | Mitigation                              |
| ------------------ | ---------- | ------ | --------------------------------------- |
| Sprite rendering slower than circles | LOW | MEDIUM | Blitting is optimized in pygame, 50 sprites negligible; validate with FPS counter |
| Animation timing drift at variable FPS | LOW | LOW | Animation uses dt accumulator (already tested in Phase 1) |
| Direction changes create visual stutter | MEDIUM | LOW | Instant direction change acceptable per PRD; can be playtested later |
| Collision detection breaks | LOW | HIGH | Keep existing pos/radius collision system; sprite is visual only |
| Sprites not found at runtime | LOW | MEDIUM | Asset loader has FileNotFoundError handling with clear messages |
| Multiple zombies share animation state | LOW | MEDIUM | Each zombie has independent Animation instance (frame timers separate) |

---

## Notes

**Design decisions:**
- **Module-level sprite loading**: Sprites loaded once and cached, shared across all zombie instances for performance
- **Independent animation timing**: Each zombie has its own Animation instance so frame timers are independent
- **Collision unchanged**: Keep existing radius-based collision detection; sprite rendering is purely visual
- **Zero velocity handling**: Explicitly set `self.vel = Vector2(0,0)` in update() else branch for animation stationary state

**Integration with existing systems:**
- Animation system (Phase 1) provides direction detection and frame cycling
- Asset loader (Phase 2) provides sprite loading and caching
- Collision system unchanged (uses pos/radius, not sprite bounds)
- PlayScene unchanged (still calls zombie.update() and zombie.draw())

**Future extensibility:**
- Death animations could follow same pattern (add death Animation instance)
- Attack animations could be triggered conditionally in draw()
- Other entities (player, pickups) could use same Animation integration pattern

**Performance considerations:**
- Sprites loaded once at module level (amortized cost)
- Blitting 50 sprites per frame is negligible (pygame.Surface.blit is optimized)
- Animation overhead: ~50 dt accumulations + modulo operations (microseconds)
- Memory: 4 directions × 3 frames × 32×32 pixels × 4 bytes/pixel = ~49KB per zombie type (shared)

---

*Generated: 2026-01-28*
*Phase: 3 of 4 - Zombie Integration*
*Dependencies: Phase 1 (Animation system) ✅, Phase 2 (Asset loading) ✅*
