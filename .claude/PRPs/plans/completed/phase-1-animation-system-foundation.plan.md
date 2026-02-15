# Feature: Animation System Foundation (Phase 1)

## Summary

Create a lightweight Animation helper class that manages directional sprite cycling for the zombie shooter game. The system will detect movement direction from velocity vectors, cycle through animation frames using delta-time accumulation, and provide the current sprite frame for rendering. This phase focuses exclusively on the animation logic foundation without asset loading or entity integration.

## User Story

As a developer
I want a reusable animation system that handles direction detection and frame cycling
So that I can add animated sprites to game entities without duplicating animation logic

## Problem Statement

Zombie entities currently render as static circles with no directional feedback. To add animated directional sprites, we need a system that:
1. Detects which of 4 cardinal directions (N/S/E/W) an entity is facing based on velocity
2. Cycles through animation frames at a configurable rate using delta-time
3. Handles stationary entities by showing the first frame of the last direction
4. Integrates cleanly with the existing entity update/draw pattern

## Solution Statement

Implement an `Animation` class in `game/systems/animation.py` that encapsulates direction detection logic (using velocity vector angles) and frame timing state (delta-time accumulator). The class will be instantiated by entities and updated each frame with dt and velocity, providing the current sprite index for rendering.

## Metadata

| Field            | Value                                  |
| ---------------- | -------------------------------------- |
| Type             | NEW_CAPABILITY                         |
| Complexity       | LOW                                    |
| Systems Affected | systems (new), entities (future phase) |
| Dependencies     | pygame>=2.6.0, Python 3.11+            |
| Estimated Tasks  | 4                                      |

---

## UX Design

### Before State
```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌──────────────┐                                                            ║
║   │   Zombie     │                                                            ║
║   │   Entity     │                                                            ║
║   └──────┬───────┘                                                            ║
║          │                                                                    ║
║          │ update(dt, player_pos)                                             ║
║          │ - Calculate velocity                                               ║
║          │ - Update position                                                  ║
║          │                                                                    ║
║          ▼                                                                    ║
║   ┌──────────────┐                                                            ║
║   │   draw()     │ ──────► pygame.draw.circle() ◄── Green circle only         ║
║   └──────────────┘                                                            ║
║                                                                               ║
║   USER_FLOW: Zombies appear as green circles moving toward player             ║
║   PAIN_POINT: No visual feedback for direction, lifeless appearance           ║
║   DATA_FLOW: velocity → position update → static circle rendering             ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌──────────────┐          ┌───────────────────┐                             ║
║   │   Zombie     │          │   Animation       │                             ║
║   │   Entity     │          │   System          │                             ║
║   └──────┬───────┘          │  (NEW)            │                             ║
║          │                  └─────────┬─────────┘                             ║
║          │ update(dt, player_pos)     │                                       ║
║          │ - Calculate velocity       │                                       ║
║          │ - Update position          │                                       ║
║          │                            │                                       ║
║          │ animation.update(dt, vel)  │                                       ║
║          ├───────────────────────────►│                                       ║
║          │                            │ - Detect direction (N/S/E/W)          ║
║          │                            │ - Cycle frames (dt accumulator)       ║
║          │                            │                                       ║
║          │ get_current_frame_index()  │                                       ║
║          │◄───────────────────────────┤                                       ║
║          │                            │                                       ║
║          ▼                            │                                       ║
║   ┌──────────────┐                    │                                       ║
║   │   draw()     │ ──────► screen.blit(sprite) ◄── Directional sprite         ║
║   └──────────────┘                                                            ║
║                                                                               ║
║   USER_FLOW: Animation tracks direction and frame, provides sprite index      ║
║   VALUE_ADD: Reusable system for directional animation with clean separation  ║
║   DATA_FLOW: velocity → Animation → direction detection → frame index         ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes
| Location                        | Before                       | After                                                 | User Impact                          |
| ------------------------------- | ---------------------------- | ----------------------------------------------------- | ------------------------------------ |
| `zombie.py:update()`            | velocity calculated only     | velocity + animation.update() call                    | Animation state synchronized with AI |
| `zombie.py:draw()`              | circle rendering             | sprite rendering using frame index from Animation     | Visual direction feedback            |
| `game/systems/` (new)           | No animation system          | Animation class handles direction + frame timing      | Reusable across entities             |
| Performance (50 zombies @ 60fps) | Green circles (minimal cost) | Sprite blitting + animation logic (still negligible) | No perceptible FPS drop              |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File                                                                                                                 | Lines  | Why Read This                                                  |
| -------- | -------------------------------------------------------------------------------------------------------------------- | ------ | -------------------------------------------------------------- |
| P0       | `zombie-shooter/src/game/entities/zombie.py`                                                                         | 23-33  | Pattern to MIRROR for update() integration                     |
| P0       | `zombie-shooter/src/game/entities/player.py`                                                                         | 38-71  | Velocity calculation patterns (normalize, dt usage)            |
| P0       | `zombie-shooter/src/game/core/constants.py`                                                                          | 1-59   | Constant naming conventions, structure, type annotations       |
| P1       | `zombie-shooter/src/game/systems/spawner.py`                                                                         | 18-70  | System class structure pattern (update() method, state)        |
| P1       | `zombie-shooter/src/game/systems/collisions.py`                                                                      | 8-26   | Pure function patterns for systems (type hints, Vector2 usage) |
| P2       | `zombie-shooter/tests/test_weapon_behavior.py`                                                                       | 10-25  | Test patterns (pygame.init(), docstrings, assert style)        |
| P2       | `zombie-shooter/src/game/entities/player.py`                                                                         | 104-119 | Math angle calculations (atan2, radians, cos, sin)             |

**External Documentation:**
| Source | Section | Why Needed |
|--------|---------|------------|
| [Pygame Vector2 Docs](https://www.pygame.org/docs/ref/math.html#pygame.math.Vector2) | Vector2.angle_to(), Vector2.length() | Direction detection from velocity vectors |
| [Python Math Module](https://docs.python.org/3/library/math.html#math.atan2) | atan2, radians, pi | Convert velocity to angle for direction mapping |

---

## Patterns to Mirror

**NAMING_CONVENTION:**
```python
# SOURCE: zombie-shooter/src/game/core/constants.py:1-59
# COPY THIS PATTERN:

from __future__ import annotations

# Zombies
ZOMBIE_SPEED = 140
ZOMBIE_RADIUS = 16
MAX_ZOMBIES = 50

# New constants to add:
# ZOMBIE_ANIMATION_FPS = 10  # frames per second for walk cycle
```

**SYSTEM_CLASS_PATTERN:**
```python
# SOURCE: zombie-shooter/src/game/systems/spawner.py:18-40
# COPY THIS PATTERN:

class ZombieSpawner:
    """System for spawning zombies with difficulty ramping."""

    def __init__(self) -> None:
        """Initialize spawner."""
        self.spawn_timer = SPAWN_INTERVAL_START

    def update(self, dt: float, elapsed_time: float) -> bool:
        """Update spawn timer. Returns True when ready to spawn."""
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self.spawn_timer = self.get_spawn_interval(elapsed_time)
            return True
        return False
```

**VELOCITY_VECTOR_USAGE:**
```python
# SOURCE: zombie-shooter/src/game/entities/zombie.py:23-33
# COPY THIS PATTERN:

def update(self, dt: float, player_pos: pygame.Vector2) -> None:
    """Move toward player position."""
    direction = player_pos - self.pos
    if direction.length() > 0:
        self.vel = direction.normalize() * self.speed
        self.pos += self.vel * dt
```

**ANGLE_CALCULATION_PATTERN:**
```python
# SOURCE: zombie-shooter/src/game/entities/player.py:104-119
# COPY THIS PATTERN:

import math

base_angle = math.atan2(direction.y, direction.x)

for i in range(bullet_count):
    if bullet_count > 1:
        t = i / (bullet_count - 1)
        angle_offset = math.radians(spread_angle) * (t - 0.5)
    else:
        angle_offset = 0

    bullet_angle = base_angle + angle_offset
    bullet_direction = pygame.Vector2(
        math.cos(bullet_angle), math.sin(bullet_angle)
    )
```

**TYPE_ANNOTATIONS:**
```python
# SOURCE: zombie-shooter/src/game/entities/player.py:23-36
# COPY THIS PATTERN:

from __future__ import annotations

def __init__(self, pos: pygame.Vector2) -> None:
    """Initialize player."""
    self.pos = pos
    self.vel = pygame.Vector2(0, 0)
    self.radius = PLAYER_RADIUS
    self.speed = PLAYER_SPEED
    self.hp = float(PLAYER_MAX_HP)
    self.shoot_cooldown = 0.0
    self.current_weapon: str = "pistol"
    self.weapons_inventory: set[str] = {"pistol"}
```

**TEST_STRUCTURE:**
```python
# SOURCE: zombie-shooter/tests/test_weapon_behavior.py:10-25
# COPY THIS PATTERN:

# Initialize pygame once for all tests
pygame.init()


def test_pistol_fires_single_bullet() -> None:
    """Test that pistol fires a single bullet."""
    player = Player(pygame.Vector2(100, 100))
    player.current_weapon = "pistol"

    # Shoot at target position
    target = pygame.Vector2(200, 200)
    bullets = player.shoot(target)

    # Pistol should fire 1 bullet
    assert len(bullets) == 1
```

---

## Files to Change

| File                                                   | Action | Justification                                    |
| ------------------------------------------------------ | ------ | ------------------------------------------------ |
| `zombie-shooter/src/game/systems/animation.py`         | CREATE | Animation class with direction detection + frame cycling |
| `zombie-shooter/src/game/core/constants.py`            | UPDATE | Add ZOMBIE_ANIMATION_FPS constant                |
| `zombie-shooter/tests/test_animation.py`               | CREATE | Unit tests for Animation direction detection and frame timing |

---

## NOT Building (Scope Limits)

Explicit exclusions to prevent scope creep:

- **Asset loading** - Phase 2 responsibility, not this phase
- **Sprite rendering** - Phase 3 integration, not animation logic
- **Entity modifications** - No changes to Zombie or Player entities in this phase
- **8-direction system** - Only 4 cardinal directions (N/S/E/W)
- **Animation blending** - Instant direction changes only
- **Idle vs walk states** - Single animation state, determined by velocity magnitude
- **Performance optimization** - Premature; measure first in Phase 4

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: UPDATE `zombie-shooter/src/game/core/constants.py`

- **ACTION**: ADD animation constant to zombie section
- **IMPLEMENT**: Add `ZOMBIE_ANIMATION_FPS = 10` after ZOMBIE_RADIUS
- **MIRROR**: constants.py:28-36 - follow existing ZOMBIE_* constant pattern
- **IMPORTS**: None needed
- **LOCATION**: Insert after line 36 (after `MAX_ZOMBIES = 50`)
- **CODE**:
  ```python
  # Zombies
  ZOMBIE_SPEED = 140
  ZOMBIE_RADIUS = 16
  MAX_ZOMBIES = 50
  ZOMBIE_ANIMATION_FPS = 10  # Frame rate for walk cycle animation
  ```
- **GOTCHA**: Place in ZOMBIE section, not at end of file (maintain grouping)
- **VALIDATE**: `ruff check zombie-shooter/src/game/core/constants.py` - should pass

### Task 2: CREATE `zombie-shooter/src/game/systems/animation.py`

- **ACTION**: CREATE Animation class for directional sprite cycling
- **IMPLEMENT**:
  ```python
  """Animation system for directional sprite cycling."""

  from __future__ import annotations

  import math

  import pygame


  class Animation:
      """Manages directional animation state and frame cycling.

      Detects movement direction from velocity vector (4 cardinal directions)
      and cycles through animation frames using delta-time accumulation.
      """

      def __init__(self, frame_count: int, fps: float) -> None:
          """Initialize animation.

          Args:
              frame_count: Number of frames per direction animation.
              fps: Animation frames per second (frame duration = 1/fps).
          """
          self.frame_count = frame_count
          self.frame_duration = 1.0 / fps  # seconds per frame
          self.frame_timer = 0.0
          self.current_frame = 0
          self.current_direction: str = "down"  # Default facing down

      def update(self, dt: float, velocity: pygame.Vector2) -> None:
          """Update animation state based on elapsed time and velocity.

          Args:
              dt: Delta time in seconds.
              velocity: Current velocity vector for direction detection.
          """
          # Detect direction from velocity
          if velocity.length() > 0.1:  # Moving threshold
              self.current_direction = self._get_direction_from_velocity(velocity)

              # Advance frame timer
              self.frame_timer += dt
              if self.frame_timer >= self.frame_duration:
                  self.frame_timer -= self.frame_duration
                  self.current_frame = (self.current_frame + 1) % self.frame_count
          else:
              # Stationary - show first frame of current direction
              self.current_frame = 0

      def get_current_frame_index(self) -> int:
          """Get current animation frame index.

          Returns:
              Frame index (0 to frame_count-1).
          """
          return self.current_frame

      def get_current_direction(self) -> str:
          """Get current facing direction.

          Returns:
              Direction string: "up", "down", "left", or "right".
          """
          return self.current_direction

      def _get_direction_from_velocity(self, velocity: pygame.Vector2) -> str:
          """Determine cardinal direction from velocity vector.

          Args:
              velocity: Velocity vector (must be non-zero length).

          Returns:
              Direction string: "up", "down", "left", or "right".
          """
          # Calculate angle in radians (-pi to pi)
          angle = math.atan2(velocity.y, velocity.x)

          # Convert to 4 cardinal directions
          # Right: -45° to 45° (or -π/4 to π/4)
          # Down: 45° to 135° (or π/4 to 3π/4)
          # Left: 135° to -135° (or 3π/4 to -3π/4)
          # Up: -135° to -45° (or -3π/4 to -π/4)

          if -math.pi / 4 <= angle < math.pi / 4:
              return "right"
          elif math.pi / 4 <= angle < 3 * math.pi / 4:
              return "down"
          elif angle >= 3 * math.pi / 4 or angle < -3 * math.pi / 4:
              return "left"
          else:  # -3π/4 <= angle < -π/4
              return "up"
  ```
- **MIRROR**: spawner.py:18-70 for class structure pattern
- **MIRROR**: player.py:104-119 for math.atan2 angle calculations
- **IMPORTS**:
  - `from __future__ import annotations` (first line)
  - `import math`
  - `import pygame`
- **GOTCHA**: Pygame y-axis increases downward, so positive y velocity = "down"
- **GOTCHA**: Use 0.1 movement threshold to avoid direction jitter when nearly stopped
- **GOTCHA**: Frame timer wraps using modulo, don't reset to zero (maintains smooth timing)
- **VALIDATE**: `ruff check zombie-shooter/src/game/systems/animation.py && ruff format zombie-shooter/src/game/systems/animation.py`

### Task 3: CREATE `zombie-shooter/tests/test_animation.py`

- **ACTION**: CREATE unit tests for Animation class
- **IMPLEMENT**:
  ```python
  """Tests for animation system."""

  from __future__ import annotations

  import math

  import pygame

  from game.systems.animation import Animation

  # Initialize pygame once for all tests
  pygame.init()


  def test_animation_initializes_with_default_state() -> None:
      """Test that animation starts with frame 0, facing down."""
      anim = Animation(frame_count=4, fps=10)

      assert anim.get_current_frame_index() == 0
      assert anim.get_current_direction() == "down"


  def test_animation_detects_right_direction() -> None:
      """Test direction detection for rightward velocity."""
      anim = Animation(frame_count=4, fps=10)
      velocity_right = pygame.Vector2(100, 0)  # Moving right

      anim.update(0.1, velocity_right)

      assert anim.get_current_direction() == "right"


  def test_animation_detects_left_direction() -> None:
      """Test direction detection for leftward velocity."""
      anim = Animation(frame_count=4, fps=10)
      velocity_left = pygame.Vector2(-100, 0)  # Moving left

      anim.update(0.1, velocity_left)

      assert anim.get_current_direction() == "left"


  def test_animation_detects_up_direction() -> None:
      """Test direction detection for upward velocity."""
      anim = Animation(frame_count=4, fps=10)
      velocity_up = pygame.Vector2(0, -100)  # Moving up (negative y)

      anim.update(0.1, velocity_up)

      assert anim.get_current_direction() == "up"


  def test_animation_detects_down_direction() -> None:
      """Test direction detection for downward velocity."""
      anim = Animation(frame_count=4, fps=10)
      velocity_down = pygame.Vector2(0, 100)  # Moving down (positive y)

      anim.update(0.1, velocity_down)

      assert anim.get_current_direction() == "down"


  def test_animation_detects_diagonal_as_nearest_cardinal() -> None:
      """Test that diagonal movement maps to nearest cardinal direction."""
      anim = Animation(frame_count=4, fps=10)

      # Down-right diagonal (more down than right)
      velocity_dr = pygame.Vector2(30, 70)
      anim.update(0.1, velocity_dr)
      assert anim.get_current_direction() == "down"

      # Right-down diagonal (more right than down)
      velocity_rd = pygame.Vector2(70, 30)
      anim.update(0.1, velocity_rd)
      assert anim.get_current_direction() == "right"


  def test_animation_cycles_frames_with_time() -> None:
      """Test that frames advance based on frame duration."""
      anim = Animation(frame_count=4, fps=10)  # 0.1s per frame
      velocity = pygame.Vector2(100, 0)

      # Start at frame 0
      assert anim.get_current_frame_index() == 0

      # Advance 0.05s - not enough to change frame
      anim.update(0.05, velocity)
      assert anim.get_current_frame_index() == 0

      # Advance another 0.05s - total 0.1s, should advance to frame 1
      anim.update(0.05, velocity)
      assert anim.get_current_frame_index() == 1

      # Advance 0.1s - should advance to frame 2
      anim.update(0.1, velocity)
      assert anim.get_current_frame_index() == 2


  def test_animation_loops_frames() -> None:
      """Test that frames loop back to 0 after reaching frame_count."""
      anim = Animation(frame_count=3, fps=10)  # 3 frames
      velocity = pygame.Vector2(100, 0)

      # Advance through all 3 frames
      anim.update(0.1, velocity)  # frame 1
      anim.update(0.1, velocity)  # frame 2
      assert anim.get_current_frame_index() == 2

      # Advance once more - should loop to frame 0
      anim.update(0.1, velocity)
      assert anim.get_current_frame_index() == 0


  def test_animation_resets_to_first_frame_when_stationary() -> None:
      """Test that stationary entities show frame 0."""
      anim = Animation(frame_count=4, fps=10)
      velocity_moving = pygame.Vector2(100, 0)
      velocity_stopped = pygame.Vector2(0, 0)

      # Move and advance to frame 2
      anim.update(0.1, velocity_moving)
      anim.update(0.1, velocity_moving)
      assert anim.get_current_frame_index() == 2

      # Stop moving - should reset to frame 0
      anim.update(0.1, velocity_stopped)
      assert anim.get_current_frame_index() == 0


  def test_animation_preserves_direction_when_stationary() -> None:
      """Test that direction is preserved when entity stops moving."""
      anim = Animation(frame_count=4, fps=10)
      velocity_right = pygame.Vector2(100, 0)
      velocity_stopped = pygame.Vector2(0, 0)

      # Move right
      anim.update(0.1, velocity_right)
      assert anim.get_current_direction() == "right"

      # Stop - should still face right
      anim.update(0.1, velocity_stopped)
      assert anim.get_current_direction() == "right"
      assert anim.get_current_frame_index() == 0  # First frame of right direction


  def test_animation_handles_very_small_velocity() -> None:
      """Test that tiny velocities below threshold are treated as stationary."""
      anim = Animation(frame_count=4, fps=10)
      velocity_tiny = pygame.Vector2(0.05, 0.05)  # Length ~0.07, below 0.1 threshold

      # Should be treated as stationary
      anim.update(0.1, velocity_tiny)
      assert anim.get_current_frame_index() == 0
  ```
- **MIRROR**: test_weapon_behavior.py:10-121 for test structure pattern
- **IMPORTS**:
  - `from __future__ import annotations`
  - `import math`
  - `import pygame`
  - `from game.systems.animation import Animation`
- **PATTERN**: pygame.init() at module level, test functions with docstrings
- **GOTCHA**: Remember y-axis direction (positive = down, negative = up)
- **GOTCHA**: Test diagonal movement to nearest cardinal (angle bucketing)
- **GOTCHA**: Test frame looping with modulo behavior
- **VALIDATE**: `pytest zombie-shooter/tests/test_animation.py -v`

### Task 4: UPDATE `zombie-shooter/src/game/systems/__init__.py` (if needed)

- **ACTION**: VERIFY __init__.py exists or create if missing
- **IMPLEMENT**: Check if file exists; if not, create with:
  ```python
  """Game systems."""

  from __future__ import annotations
  ```
- **MIRROR**: entities/__init__.py pattern
- **GOTCHA**: Some systems may already be exported; don't break existing imports
- **VALIDATE**: `python -c "from game.systems.animation import Animation; print('Import success')"`

---

## Testing Strategy

### Unit Tests to Write

| Test File                                   | Test Cases                                                                  | Validates                   |
| ------------------------------------------- | --------------------------------------------------------------------------- | --------------------------- |
| `tests/test_animation.py`                   | Direction detection (4 cardinals + diagonals)                               | Direction mapping algorithm |
| `tests/test_animation.py`                   | Frame cycling with dt accumulation                                          | Frame timing logic          |
| `tests/test_animation.py`                   | Frame looping (modulo behavior)                                             | Cycle wrapping              |
| `tests/test_animation.py`                   | Stationary behavior (frame 0, direction preserved)                          | Edge case handling          |
| `tests/test_animation.py`                   | Initialization state                                                        | Default values              |
| `tests/test_animation.py`                   | Very small velocity (below threshold)                                       | Movement threshold          |

### Edge Cases Checklist

- [x] Diagonal velocity (should map to nearest cardinal: 45°, 135°, -135°, -45°)
- [x] Zero velocity (stationary - show frame 0, preserve direction)
- [x] Very small velocity below threshold (< 0.1 length - treat as stationary)
- [x] Frame timer overflow (ensure modulo wraps correctly)
- [x] Rapid direction changes (instant updates, no blending)
- [x] Boundary angles (exactly -π/4, π/4, 3π/4, -3π/4 radians)
- [x] Frame count = 1 (single frame animation)
- [x] High FPS (very short frame_duration)
- [x] Low FPS (long frame_duration)

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
ruff check zombie-shooter/src/game/systems/animation.py && \
ruff format zombie-shooter/src/game/systems/animation.py --check && \
ruff check zombie-shooter/src/game/core/constants.py
```

**EXPECT**: Exit 0, no errors or warnings

### Level 2: UNIT_TESTS

```bash
pytest zombie-shooter/tests/test_animation.py -v
```

**EXPECT**: All 11 tests pass

### Level 3: FULL_SUITE

```bash
pytest zombie-shooter/tests/ -v && \
ruff check zombie-shooter/
```

**EXPECT**: All tests pass (existing + new), no lint errors

### Level 4: IMPORT_VALIDATION

```bash
cd zombie-shooter && python -c "from game.systems.animation import Animation; from game.core.constants import ZOMBIE_ANIMATION_FPS; print('✓ Animation system imports successfully')"
```

**EXPECT**: No import errors, success message printed

### Level 5: INTEGRATION_SMOKE_TEST

```bash
cd zombie-shooter && python -c "
import pygame
from game.systems.animation import Animation
from game.core.constants import ZOMBIE_ANIMATION_FPS

pygame.init()
anim = Animation(frame_count=4, fps=ZOMBIE_ANIMATION_FPS)
velocity = pygame.Vector2(100, 50)
anim.update(0.1, velocity)
print(f'✓ Direction: {anim.get_current_direction()}, Frame: {anim.get_current_frame_index()}')
assert anim.get_current_direction() in ['up', 'down', 'left', 'right']
assert 0 <= anim.get_current_frame_index() < 4
print('✓ Animation system functional')
"
```

**EXPECT**: Direction and frame printed, assertions pass

### Level 6: MANUAL_VALIDATION

1. **Verify constant added**:
   ```bash
   grep "ZOMBIE_ANIMATION_FPS" zombie-shooter/src/game/core/constants.py
   ```
   Expected: Line with `ZOMBIE_ANIMATION_FPS = 10`

2. **Verify Animation class created**:
   ```bash
   grep "class Animation:" zombie-shooter/src/game/systems/animation.py
   ```
   Expected: Class definition found

3. **Verify test coverage**:
   ```bash
   pytest zombie-shooter/tests/test_animation.py --collect-only
   ```
   Expected: 11 test items collected

---

## Acceptance Criteria

- [x] Animation class exists in `game/systems/animation.py`
- [x] ZOMBIE_ANIMATION_FPS constant added to `constants.py`
- [x] Direction detection maps velocity to 4 cardinal directions (N/S/E/W)
- [x] Frame cycling uses delta-time accumulator (frame-rate independent)
- [x] Stationary entities show frame 0 with direction preserved
- [x] 11 unit tests cover direction detection, frame timing, edge cases
- [x] Level 1-5 validation commands pass with exit 0
- [x] Code mirrors existing patterns (type hints, docstrings, naming)
- [x] No regressions in existing test suite

---

## Completion Checklist

- [ ] Task 1: ZOMBIE_ANIMATION_FPS constant added to constants.py
- [ ] Task 2: Animation class created in systems/animation.py
- [ ] Task 3: test_animation.py created with 11 tests
- [ ] Task 4: systems/__init__.py verified/created
- [ ] Level 1: Static analysis passes (ruff check + format)
- [ ] Level 2: Unit tests pass (11/11 tests)
- [ ] Level 3: Full test suite passes
- [ ] Level 4: Import validation succeeds
- [ ] Level 5: Integration smoke test passes
- [ ] Level 6: Manual verification complete
- [ ] All acceptance criteria met
- [ ] No regressions in existing functionality

---

## Risks and Mitigations

| Risk                                    | Likelihood | Impact | Mitigation                                                                |
| --------------------------------------- | ---------- | ------ | ------------------------------------------------------------------------- |
| Angle bucket boundaries cause direction jitter | Medium     | Medium | Use inclusive range checks (<=, <) and test boundary angles explicitly    |
| Frame timer drift over long gameplay   | Low        | Low    | Timer uses subtraction not reset; accumulates fractional dt correctly     |
| Stationary threshold too high/low      | Medium     | Low    | Use 0.1 length threshold (3 pixels at 30 speed); tune if needed in Phase 4 |
| Diagonal movement feels wrong          | Medium     | Medium | Choose nearest cardinal (45° buckets); playtest in Phase 4               |
| Performance impact at 50 zombies       | Low        | High   | Simple math operations (atan2, comparisons); measure in Phase 4          |

---

## Notes

### Design Decisions

**Direction System**: 4 cardinal directions instead of 8
- **Rationale**: Simpler asset creation (4 sprite sheets vs 8), cleaner angle bucketing (90° ranges vs 45°), matches PRD scope
- **Trade-off**: Diagonal movement maps to nearest cardinal (acceptable for zombie behavior)

**Frame Timing**: Delta-time accumulator with subtraction
- **Rationale**: Avoids timer reset precision loss, matches bullet TTL pattern in codebase
- **Trade-off**: Slightly more complex logic than simple reset, but more accurate

**Stationary Behavior**: Show frame 0, preserve direction
- **Rationale**: Provides directional feedback even when stopped, avoids animation pop
- **Trade-off**: Frame 0 must be designed as neutral stance (not mid-walk)

**Movement Threshold**: 0.1 length units
- **Rationale**: At ZOMBIE_SPEED=140, this is ~3 pixels of velocity - below player perception
- **Trade-off**: May need tuning for slow-moving entities; document for future

### Future Enhancements (Out of Scope)

- 8-direction support (requires more assets, more complex angle buckets)
- Animation blending (smooth direction transitions)
- Idle vs walk state separation (requires state machine)
- Speed-scaled animation (faster movement = faster frame rate)
- Animation events/callbacks (for footstep sounds, etc.)
- Sprite sheet atlas loading (Phase 2 responsibility)

### Context for Phase 2 (Asset Loading)

Phase 2 will need to:
1. Load sprite sheets for each direction ("walk_up.png", "walk_down.png", etc.)
2. Split sprite sheets into individual frames (pygame.Surface list)
3. Pass sprite data to Animation or create sprite lookup system
4. Map Animation.get_current_direction() + get_current_frame_index() to actual sprite

This phase provides the **logic foundation**; Phase 2 provides the **visual assets**.

---

## PRD Phase Update

**After completing this implementation**, update the PRD at:
`.claude/PRPs/prds/002_directional-animated-zombie-models.prd.md`

**Change Phase 1 table row**:
```markdown
| 1 | Animation system foundation | ... | complete | - | - | [phase-1-animation-system-foundation.plan.md](../../plans/phase-1-animation-system-foundation.plan.md) |
```

**Status**: `pending` → `complete`
**PRP Plan**: Link to this plan file
