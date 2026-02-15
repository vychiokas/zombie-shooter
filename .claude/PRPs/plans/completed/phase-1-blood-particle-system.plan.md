# Feature: Blood Particle System

## Summary

Implementing a lightweight blood particle system for zombie death visual feedback. When zombies are killed, 8 small red particles will spray outward from the impact point, move with velocity-based physics, and fade out over 0.8 seconds. This provides immediate visceral visual feedback for kills, following the proven DOOM-style gore pattern. The system uses custom lightweight particles (no external libraries) with position + velocity + lifetime tracking, integrated into the existing entity lifecycle pattern.

## User Story

As a player
I want to see blood particles spray when I kill a zombie
So that I feel visceral satisfaction and visual confirmation that my shot connected

## Problem Statement

Zombie deaths currently provide zero visual feedback - zombies vanish instantly with no particle effects, splash, or indication of impact. This creates an unsatisfying experience lacking the visceral "game juice" expected from a gore-focused zombie shooter. The blood particle system solves this by adding immediate, dynamic visual feedback at the moment of kill.

## Solution Statement

Create a `BloodParticle` entity class following the existing entity pattern (Bullet, Pickup, Zombie). Particles spawn at zombie death position with random outward velocities, update position using delta-time physics (`pos += vel * dt`), decrement lifetime, and fade alpha over time. Particles are managed in a list (`self.blood_particles`) in PlayScene, updated each frame, and auto-removed when lifetime expires. This leverages the existing entity lifecycle without introducing new architectural patterns.

## Metadata

| Field            | Value                                             |
| ---------------- | ------------------------------------------------- |
| Type             | NEW_CAPABILITY                                    |
| Complexity       | LOW                                               |
| Systems Affected | entities (new BloodParticle), scenes (PlayScene integration), constants |
| Dependencies     | pygame 2.6.1 (already present)                    |
| Estimated Tasks  | 5                                                 |

---

## UX Design

### Before State
```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   Player shoots zombie                                                        ║
║   ┌─────────┐        ┌──────────┐        ┌────────────┐                      ║
║   │ Bullet  │ ─────► │  Zombie  │ ─────► │   VANISH   │                      ║
║   │ hits    │        │ collision│        │ (instant)  │                      ║
║   └─────────┘        └──────────┘        └────────────┘                      ║
║                                                                               ║
║   USER_FLOW:                                                                  ║
║   1. Player fires bullet                                                      ║
║   2. Bullet collides with zombie                                              ║
║   3. Zombie instantly disappears (removed from list)                          ║
║   4. No visual feedback, feels cheap                                          ║
║                                                                               ║
║   PAIN_POINT: Zero visual feedback, no particle splash, feels unrewarding    ║
║                                                                               ║
║   DATA_FLOW:                                                                  ║
║   collision detected → zombie removed from self.zombies → screen updates      ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   Player shoots zombie                                                        ║
║   ┌─────────┐      ┌──────────┐      ┌────────────────┐                      ║
║   │ Bullet  │ ───► │  Zombie  │ ───► │  BLOOD SPLASH  │ ◄─ NEW!              ║
║   │ hits    │      │ collision│      │  (8 particles) │                      ║
║   └─────────┘      └──────────┘      └────────────────┘                      ║
║                                             │                                 ║
║                                             ▼                                 ║
║                                      ┌──────────────┐                         ║
║                                      │  Particles:  │                         ║
║                                      │  - Fly out   │                         ║
║                                      │  - Fade      │                         ║
║                                      │  - Removed   │                         ║
║                                      │  (0.8s TTL)  │                         ║
║                                      └──────────────┘                         ║
║                                                                               ║
║   USER_FLOW:                                                                  ║
║   1. Player fires bullet                                                      ║
║   2. Bullet collides with zombie                                              ║
║   3. **8 blood particles spawn** at zombie position                           ║
║   4. **Particles spray outward** with random velocities                       ║
║   5. **Particles fade** over 0.8 seconds                                      ║
║   6. Zombie removed (will show corpse in Phase 2)                             ║
║   7. Visual satisfaction from blood spray                                     ║
║                                                                               ║
║   VALUE_ADD: Visceral visual feedback, satisfying kill confirmation          ║
║                                                                               ║
║   DATA_FLOW:                                                                  ║
║   collision → spawn_blood_splash(pos) → create 8 BloodParticle objects →     ║
║   add to self.blood_particles → update each frame (move, fade) →             ║
║   remove when ttl <= 0 → render with alpha fade                              ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| PlayScene collision handler (play.py:135-151) | Zombie removed instantly | Zombie removed + blood particles spawned | Player sees blood spray on kill |
| Screen rendering | Zombie vanishes with no effect | Blood particles visible flying outward, fading | Visceral visual feedback |
| Kill moment | No visual reward | Red particle splash with motion | Satisfying "game juice" effect |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `/Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/src/game/entities/bullet.py` | 1-60 | Pattern to MIRROR exactly - shows entity init, update(dt) returning bool, physics, TTL |
| P0 | `/Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/src/game/entities/pickup.py` | 1-70 | TTL countdown pattern, is_alive() method, simple draw() |
| P1 | `/Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/src/game/scenes/play.py` | 135-151, 173-189 | Integration point - where to spawn particles and draw them |
| P1 | `/Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/src/game/core/constants.py` | all | Where to add new constants (BLOOD_PARTICLE_*) |
| P2 | `/Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/tests/test_pickup.py` | all | Test pattern to FOLLOW - TTL tests, initialization tests |

**External Documentation:**

| Source | Section | Why Needed |
|--------|---------|------------|
| [Pygame 2.6 docs - draw.circle](https://www.pygame.org/docs/ref/draw.html#pygame.draw.circle) | circle drawing | Drawing particles with color |
| [Pygame 2.6 docs - Surface alpha](https://www.pygame.org/docs/ref/surface.html#pygame.Surface.set_alpha) | alpha blending | Fade effect over time |

---

## Patterns to Mirror

**ENTITY_INITIALIZATION:**
```python
# SOURCE: /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/src/game/entities/bullet.py:14-19
# COPY THIS PATTERN:
def __init__(self, pos: pygame.Vector2, direction: pygame.Vector2) -> None:
    """Initialize bullet."""
    self.pos = pos.copy()  # IMPORTANT: copy() to avoid reference issues
    self.vel = direction.normalize() * BULLET_SPEED
    self.radius = BULLET_RADIUS
    self.ttl = BULLET_TTL
```

**UPDATE_WITH_PHYSICS:**
```python
# SOURCE: /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/src/game/entities/bullet.py:21-26
# COPY THIS PATTERN:
def update(self, dt: float) -> bool:
    """Update bullet position and lifetime. Returns True if alive."""
    self.pos += self.vel * dt  # Physics: position += velocity * delta_time
    self.ttl -= dt              # Decrement time-to-live
    return self.is_alive()      # Return alive status
```

**IS_ALIVE_PATTERN:**
```python
# SOURCE: /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/src/game/entities/bullet.py:28-32
# COPY THIS PATTERN:
def is_alive(self) -> bool:
    """Check if bullet should still exist."""
    # Check both TTL and bounds
    if self.ttl <= 0:
        return False
    # Could also check if off-screen
    return True
```

**DRAW_SIMPLE_CIRCLE:**
```python
# SOURCE: /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/src/game/entities/bullet.py:57-59
# COPY THIS PATTERN:
def draw(self, screen: pygame.Surface) -> None:
    """Render bullet."""
    pygame.draw.circle(
        screen, (255, 255, 0),  # Color as RGB tuple
        (int(self.pos.x), int(self.pos.y)),  # Convert to int
        self.radius
    )
```

**TYPE_HINTS:**
```python
# SOURCE: /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/src/game/entities/bullet.py:1-3
# COPY THIS PATTERN:
"""Bullet entity for zombie shooter."""

from __future__ import annotations  # ALWAYS include this

import pygame

from game.core.constants import BULLET_RADIUS, BULLET_SPEED, BULLET_TTL
```

**CONSTANTS_DEFINITION:**
```python
# SOURCE: /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/src/game/core/constants.py:16-20
# COPY THIS PATTERN:
# Bullets
BULLET_SPEED = 700
BULLET_RADIUS = 4
BULLET_TTL = 1.5  # time to live in seconds
SHOOT_COOLDOWN = 0.15
```

**SCENE_ENTITY_LIST_MANAGEMENT:**
```python
# SOURCE: /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/src/game/scenes/play.py:100-102
# COPY THIS PATTERN:
# Update bullets and filter out dead ones
self.bullets = [b for b in self.bullets if b.update(dt)]

# Draw all bullets
for bullet in self.bullets:
    bullet.draw(screen)
```

**TEST_INITIALIZATION:**
```python
# SOURCE: /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/tests/test_pickup.py:13-24
# COPY THIS PATTERN:
def test_pickup_initialization() -> None:
    """Test that Pickup initializes with correct attributes."""
    pos = pygame.Vector2(100, 200)
    weapon_type = "shotgun"

    pickup = Pickup(pos, weapon_type)

    assert pickup.pos.x == 100
    assert pickup.pos.y == 200
    assert pickup.weapon_type == "shotgun"
    assert pickup.radius == 20
    assert pickup.ttl > 0
```

**TEST_TTL_COUNTDOWN:**
```python
# SOURCE: /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/tests/test_pickup.py:27-37
# COPY THIS PATTERN:
def test_pickup_update_decreases_ttl() -> None:
    """Test that update() decreases TTL."""
    pickup = Pickup(pygame.Vector2(0, 0), "smg")
    initial_ttl = pickup.ttl

    is_alive = pickup.update(1.0)  # 1 second elapsed

    assert pickup.ttl == initial_ttl - 1.0
    assert is_alive is True
```

---

## Files to Change

| File | Action | Justification |
|------|--------|---------------|
| `zombie-shooter/src/game/entities/blood_particle.py` | CREATE | New entity class for blood particles |
| `zombie-shooter/src/game/core/constants.py` | UPDATE | Add blood particle constants (BLOOD_PARTICLE_COUNT, etc.) |
| `zombie-shooter/tests/test_blood_particle.py` | CREATE | Unit tests for BloodParticle class |
| `zombie-shooter/src/game/scenes/play.py` | UPDATE | Spawn particles on zombie death, manage particle list, draw particles |

---

## NOT Building (Scope Limits)

Explicit exclusions to prevent scope creep:

- **Dead zombie corpses** - Phase 2 responsibility, not this phase
- **Blood pool decals** - Phase 3 responsibility
- **Particle gravity** - Simple linear motion only for MVP
- **Variable particle sizes** - All particles same size for simplicity
- **Particle collision with walls** - Particles pass through everything
- **Sound effects** - Visual only, no audio
- **Screen shake** - No camera effects
- **Weapon-specific particle counts** - Always 8 particles regardless of weapon

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: ADD blood particle constants to `constants.py`

- **ACTION**: UPDATE `/Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/src/game/core/constants.py`
- **IMPLEMENT**: Add blood particle section after zombie constants (after line 53)
- **MIRROR**: `/Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/src/game/core/constants.py:16-20` - bullet constants pattern
- **CODE**:
  ```python
  # Blood particles
  BLOOD_PARTICLE_COUNT = 8  # Particles spawned per death
  BLOOD_PARTICLE_SPEED = 150  # Initial velocity magnitude (pixels/sec)
  BLOOD_PARTICLE_LIFETIME = 0.8  # Seconds before particle fades out
  BLOOD_PARTICLE_RADIUS = 3  # Pixel radius of particle
  ```
- **GOTCHA**: Place these constants in the "Blood particles" section AFTER zombies, BEFORE spawning section
- **VALIDATE**: `cd zombie-shooter && ruff check src/game/core/constants.py` - no errors

### Task 2: CREATE `blood_particle.py` entity class

- **ACTION**: CREATE `/Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/src/game/entities/blood_particle.py`
- **IMPLEMENT**: BloodParticle class with __init__, update, is_alive, draw, get_alpha methods
- **MIRROR**: `/Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/src/game/entities/bullet.py:1-60` - entity pattern with TTL
- **CODE**:
  ```python
  """Blood particle entity for gore effects."""

  from __future__ import annotations

  import pygame

  from game.core.constants import (
      BLOOD_PARTICLE_LIFETIME,
      BLOOD_PARTICLE_RADIUS,
      HEIGHT,
      WIDTH,
  )


  class BloodParticle:
      """Blood particle that sprays from zombie death."""

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

      def is_alive(self) -> bool:
          """Check if particle should still exist.

          Returns:
              True if lifetime > 0, False otherwise.
          """
          return self.lifetime > 0

      def get_alpha(self) -> int:
          """Calculate alpha transparency based on remaining lifetime.

          Returns:
              Alpha value (0-255), fades from 255 to 0.
          """
          ratio = self.lifetime / self.max_lifetime
          return int(255 * ratio)

      def draw(self, screen: pygame.Surface) -> None:
          """Render blood particle with fade effect.

          Args:
              screen: Pygame surface to draw on.
          """
          # Create temporary surface for alpha blending
          temp_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
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
- **TYPES**: All methods typed with `-> bool`, `-> int`, `-> None`
- **GOTCHA**: Must use `pos.copy()` to avoid reference bugs, use `pygame.SRCALPHA` for alpha blending
- **VALIDATE**: `cd zombie-shooter && ruff check src/game/entities/blood_particle.py && ruff format src/game/entities/blood_particle.py` - no errors

### Task 3: CREATE `test_blood_particle.py` unit tests

- **ACTION**: CREATE `/Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/tests/test_blood_particle.py`
- **IMPLEMENT**: Tests for initialization, update physics, TTL countdown, is_alive, alpha fade, draw
- **MIRROR**: `/Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/tests/test_pickup.py:1-100` - TTL test pattern
- **CODE**:
  ```python
  """Tests for blood particle entity."""

  from __future__ import annotations

  import pygame

  from game.entities.blood_particle import BloodParticle

  # Initialize pygame once for all tests
  pygame.init()


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


  def test_blood_particle_update_moves_position() -> None:
      """Test that update() moves particle based on velocity."""
      particle = BloodParticle(pygame.Vector2(0, 0), pygame.Vector2(100, 0))

      particle.update(0.1)  # 0.1 seconds

      assert particle.pos.x == 10  # 100 * 0.1
      assert particle.pos.y == 0


  def test_blood_particle_update_decreases_lifetime() -> None:
      """Test that update() decreases lifetime."""
      particle = BloodParticle(pygame.Vector2(0, 0), pygame.Vector2(0, 0))
      initial_lifetime = particle.lifetime

      is_alive = particle.update(0.2)

      assert particle.lifetime == initial_lifetime - 0.2
      assert is_alive is True


  def test_blood_particle_dies_when_lifetime_expires() -> None:
      """Test that particle becomes not alive when lifetime <= 0."""
      particle = BloodParticle(pygame.Vector2(0, 0), pygame.Vector2(0, 0))
      particle.lifetime = 0.1

      is_alive = particle.update(0.5)  # Exceed lifetime

      assert particle.lifetime <= 0
      assert is_alive is False


  def test_blood_particle_alpha_fades_over_time() -> None:
      """Test that alpha decreases as lifetime decreases."""
      particle = BloodParticle(pygame.Vector2(0, 0), pygame.Vector2(0, 0))

      alpha_start = particle.get_alpha()
      particle.update(0.4)  # Half of 0.8s lifetime
      alpha_mid = particle.get_alpha()
      particle.update(0.35)  # Near end
      alpha_end = particle.get_alpha()

      assert alpha_start == 255  # Full opacity
      assert 100 < alpha_mid < 150  # Mid-fade
      assert alpha_end < 50  # Nearly transparent


  def test_blood_particle_draw_no_error() -> None:
      """Test that draw() executes without errors."""
      particle = BloodParticle(pygame.Vector2(100, 100), pygame.Vector2(0, 0))
      screen = pygame.Surface((800, 600))

      particle.draw(screen)  # Should not raise exception


  def test_blood_particle_pos_copy_independence() -> None:
      """Test that particle pos is independent of source pos."""
      source_pos = pygame.Vector2(50, 50)
      particle = BloodParticle(source_pos, pygame.Vector2(0, 0))

      source_pos.x = 999

      assert particle.pos.x == 50  # Should not change
  ```
- **PATTERN**: Use `pygame.init()` at module level, assert exact values for deterministic tests
- **VALIDATE**: `cd zombie-shooter && PYTHONPATH=src pytest tests/test_blood_particle.py -v` - all tests pass

### Task 4: UPDATE `play.py` to spawn particles on zombie death

- **ACTION**: UPDATE `/Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/src/game/scenes/play.py`
- **IMPLEMENT**:
  1. Import BloodParticle and constants
  2. Add `self.blood_particles: list[BloodParticle] = []` in __init__
  3. Add `spawn_blood_splash(pos)` helper method
  4. Call spawn in collision handler (line 135-151)
  5. Update particles in update() method
- **MIRROR**: `/Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/src/game/scenes/play.py:100-102` - bullet list management
- **CHANGES**:

  **Import addition** (after line 10):
  ```python
  from game.entities.blood_particle import BloodParticle
  from game.core.constants import BLOOD_PARTICLE_COUNT, BLOOD_PARTICLE_SPEED
  ```

  **__init__ addition** (after line 40, after `self.pickups = []`):
  ```python
  self.blood_particles: list[BloodParticle] = []
  ```

  **New helper method** (add after handle_input method, around line 90):
  ```python
  def spawn_blood_splash(self, pos: pygame.Vector2) -> None:
      """Spawn blood particles at position with random outward velocities.

      Args:
          pos: Position to spawn particles from.
      """
      import random
      import math

      for _ in range(BLOOD_PARTICLE_COUNT):
          # Random angle (0 to 2π)
          angle = random.uniform(0, 2 * math.pi)
          # Random speed variation (75% to 125% of base speed)
          speed = BLOOD_PARTICLE_SPEED * random.uniform(0.75, 1.25)

          # Convert angle to velocity vector
          vel = pygame.Vector2(
              math.cos(angle) * speed,
              math.sin(angle) * speed
          )

          self.blood_particles.append(BloodParticle(pos, vel))
  ```

  **Collision handler update** (modify lines 135-151):
  ```python
  # Bullet-zombie collisions
  bullet_zombie_hits = check_bullet_zombie_collisions(self.bullets, self.zombies)

  # Remove hit bullets and zombies (reverse order to avoid index issues)
  bullets_to_remove = set()
  zombies_to_remove = set()
  for b_idx, z_idx in bullet_zombie_hits:
      zombie = self.zombies[z_idx]  # NEW: Get zombie before removal
      self.spawn_blood_splash(zombie.pos)  # NEW: Spawn blood particles
      bullets_to_remove.add(b_idx)
      zombies_to_remove.add(z_idx)
      self.kills += 1

  self.bullets = [
      b for i, b in enumerate(self.bullets) if i not in bullets_to_remove
  ]
  self.zombies = [
      z for i, z in enumerate(self.zombies) if i not in zombies_to_remove
  ]
  ```

  **Update method addition** (after bullet update, around line 105):
  ```python
  # Update blood particles
  self.blood_particles = [p for p in self.blood_particles if p.update(dt)]
  ```

- **GOTCHA**: Must get `zombie.pos` BEFORE removing zombie from list, otherwise index invalid
- **VALIDATE**: `cd zombie-shooter && ruff check src/game/scenes/play.py` - no errors

### Task 5: UPDATE `play.py` to draw blood particles

- **ACTION**: UPDATE `/Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/src/game/scenes/play.py`
- **IMPLEMENT**: Add particle drawing in draw() method AFTER pickups, BEFORE HUD (so particles on top)
- **MIRROR**: `/Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/src/game/scenes/play.py:173-189` - entity draw loop
- **CHANGE** (add after pickup drawing, around line 187):
  ```python
  # Draw pickups
  for pickup in self.pickups:
      pickup.draw(screen)

  # Draw blood particles (NEW - on top of everything except HUD)
  for particle in self.blood_particles:
      particle.draw(screen)

  # HUD text (drawn last, on top)
  ```
- **GOTCHA**: Particles drawn LAST (except HUD) so they appear on top for visibility
- **VALIDATE**: `cd zombie-shooter && ruff check src/game/scenes/play.py && ruff format src/game/scenes/play.py` - no errors

---

## Testing Strategy

### Unit Tests to Write

| Test File | Test Cases | Validates |
|-----------|------------|-----------|
| `tests/test_blood_particle.py` | initialization, physics update, TTL countdown, death, alpha fade, draw | BloodParticle entity |

### Edge Cases Checklist

- [x] Particle dies when lifetime <= 0
- [x] Particle position independent from source position (pos.copy())
- [x] Alpha fades smoothly from 255 to 0
- [x] Particles move with velocity * dt (frame-rate independent)
- [x] Draw doesn't crash with invalid positions
- [x] Multiple particles spawn independently
- [x] Particles removed from list when dead (no memory leak)

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
cd zombie-shooter
ruff check src/ tests/
ruff format src/ tests/
```

**EXPECT**: Exit 0, no errors or warnings

### Level 2: UNIT_TESTS

```bash
cd zombie-shooter
PYTHONPATH=src pytest tests/test_blood_particle.py -v
```

**EXPECT**: All 8 tests pass

### Level 3: FULL_SUITE

```bash
cd zombie-shooter
PYTHONPATH=src pytest -v
ruff check src/ tests/
```

**EXPECT**: All tests pass (including existing tests - no regressions)

### Level 4: MANUAL_VALIDATION

**Steps:**
1. Launch game: `cd zombie-shooter && PYTHONPATH=src python -m game.main`
2. Shoot zombies (click on them)
3. Verify blood particle spray appears at death point
4. Verify particles fly outward in random directions
5. Verify particles fade out over ~0.8 seconds
6. Kill 10+ zombies rapidly - verify no performance degradation
7. Confirm game maintains 60 FPS with particles active

**EXPECT**:
- Red particles spray from zombie death position
- Particles move smoothly and fade naturally
- No stuttering or FPS drops
- Particles disappear after fading

---

## Acceptance Criteria

- [x] `BloodParticle` class created with proper type hints
- [x] Particles spawn on zombie death (8 per death)
- [x] Particles have random outward velocities
- [x] Particles move with delta-time physics
- [x] Particles fade alpha over 0.8 seconds
- [x] Particles auto-remove when dead
- [x] Blood particle constants added to constants.py
- [x] Unit tests pass (100% coverage of BloodParticle)
- [x] No regressions in existing tests
- [x] Code follows existing patterns (Bullet/Pickup entity style)
- [x] Static analysis passes (ruff check)
- [x] Manual testing confirms visual effect works

---

## Completion Checklist

- [ ] Task 1: Constants added to constants.py
- [ ] Task 2: BloodParticle class created
- [ ] Task 3: Unit tests written and passing
- [ ] Task 4: PlayScene spawn integration complete
- [ ] Task 5: PlayScene draw integration complete
- [ ] Level 1: Static analysis passes
- [ ] Level 2: Unit tests pass
- [ ] Level 3: Full test suite passes
- [ ] Level 4: Manual validation confirms blood splash works
- [ ] All acceptance criteria met
- [ ] No performance degradation (60 FPS maintained)

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Too many particles cause FPS drop | Low | Medium | Particles fade quickly (0.8s), max 50 zombies × 8 = 400 particles briefly |
| Alpha blending expensive | Low | Low | Pygame handles SRCALPHA efficiently, small temp surfaces |
| Particles not visible on dark background | Medium | Low | Use bright red (180, 0, 0), particles rendered on top |
| Random velocity looks too uniform | Low | Low | Speed variation (75%-125%) and full 360° angle spread |
| Memory leak from particles not removed | Very Low | High | update() returns bool, list comprehension filters dead particles |
| pos reference bug | Low | Medium | Always use pos.copy() in __init__, tested in unit test |

---

## Notes

**Design decisions:**
- **8 particles per death**: Balance visual impact without overwhelming screen
- **0.8 second lifetime**: Long enough to see, short enough to not clutter
- **150 px/sec speed**: Fast spray feel without going off-screen instantly
- **Dark red (180,0,0)**: Clearly visible on gray background, blood-like
- **Radius 3**: Small enough to feel like spray, large enough to be visible
- **Random velocity variation**: ±25% speed, 360° angle for organic feel
- **Alpha fade**: Smooth fade from 255→0 using lifetime ratio
- **Temporary surface for alpha**: Standard pygame pattern for per-pixel alpha

**Trade-offs:**
- Custom particle system vs library: Chose custom for simplicity, no external deps
- Linear motion vs gravity: Chose linear for MVP simplicity (gravity deferred)
- Fixed size vs variable: Chose fixed for consistent visual, simpler code

**Future considerations (Phase 4/5):**
- Add particle velocity randomness (currently uniform spread)
- Add gravity for more realistic arc motion
- Add particle size variation for visual depth
- Limit max particles if performance degrades (unlikely)

**Integration with Phase 2 (Dead Zombie):**
- Phase 2 will add dead zombie corpse at same position
- Particles will spray from corpse position
- Rendering order: blood decals → corpses → live zombies → particles (particles on top)

---

*Generated: 2026-02-02*
*PRD Source: `.claude/PRPs/prds/003_zombie-gore-death-effects.prd.md`*
*Phase: 1 of 5 - Blood Particle System*
