# Feature: Phase 5 - Spitter Zombie Variant

## Summary

Implement the Spitter zombie variant - a slow-moving (100 px/s), ranged attacker that shoots acid projectiles at the player from distance (400px range). This variant forces players to prioritize threats, breaks pure melee kiting patterns, and adds strategic depth by requiring players to dodge incoming projectiles while managing other zombies. The implementation follows the established Bullet entity pattern but creates distinct green acid projectiles that damage the player on contact.

## User Story

As a player
I want to face zombies that attack from range with visible projectiles
So that I must adapt my strategy to prioritize distant threats and practice dodging mechanics instead of only kiting in circles

## Problem Statement

Current gameplay allows players to kite zombies indefinitely using simple circular movement patterns. All zombies are melee-only, creating predictable, one-dimensional combat. Players can survive entire 60-second sessions without changing tactics. This becomes repetitive and doesn't leverage the full tactical potential of the weapon system.

**Testable Success**: Green spitter zombies spawn during gameplay, stay at distance (300-400px from player), shoot visible acid projectiles at 1.5s intervals, and player takes damage when hit by acid (5 HP per projectile).

## Solution Statement

Create a ranged zombie variant using the existing Bullet entity pattern as a foundation. Spitters spawn with weight-based probability (10% after enabling), maintain distance from the player, and fire acid projectiles on a cooldown timer. The acid projectiles use the same collision system as bullets but check player collision instead of zombie collision. Visual distinction comes from green-tinted sprites and yellow-green acid projectile rendering.

## Metadata

| Field            | Value                                                  |
| ---------------- | ------------------------------------------------------ |
| Type             | NEW_CAPABILITY                                         |
| Complexity       | MEDIUM                                                 |
| Systems Affected | entities, scenes, systems/collisions, core/constants   |
| Dependencies     | pygame>=2.6.0, Python 3.11+                            |
| Estimated Tasks  | 8                                                      |

---

## UX Design

### Before State
```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌─────────────┐                                                             ║
║   │   Player    │ ◄───── all zombies walk directly toward player              ║
║   │  (center)   │                                                             ║
║   └─────────────┘                                                             ║
║         ▲                                                                     ║
║         │                                                                     ║
║    ┌────┴────┐                                                                ║
║    │ Normal  │ (walks toward)                                                 ║
║    │ Zombie  │                                                                ║
║    └─────────┘                                                                ║
║         │                                                                     ║
║    ┌────▼────┐                                                                ║
║    │ Runner  │ (runs toward - 2x speed)                                       ║
║    │ Zombie  │                                                                ║
║    └─────────┘                                                                ║
║                                                                               ║
║   USER_FLOW: Player circles around, shoots zombies as they approach           ║
║   PAIN_POINT: All threats are melee only - same kiting strategy works always  ║
║   DATA_FLOW: Player → Move → Zombies chase → Player shoots → Repeat           ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌─────────────┐          ~~~~~~~~~~~~~~~~►                                  ║
║   │   Player    │ ◄~~~~~~~ Acid Projectile (green)                            ║
║   │  (center)   │                                                             ║
║   └─────────────┘                                                             ║
║         ▲                     ▲                                               ║
║         │                     │                                               ║
║    ┌────┴────┐           ┌────────┐                                           ║
║    │ Normal  │           │Spitter │ (green, stays at 300-400px distance)      ║
║    │ Zombie  │           │ Zombie │ (shoots acid every 1.5 seconds)           ║
║    └─────────┘           └────────┘                                           ║
║                               │                                               ║
║                          [Attack Range Check]                                 ║
║                          [Cooldown Timer: 1.5s]                               ║
║                          [Fire Acid Projectile]                               ║
║                                                                               ║
║   USER_FLOW:                                                                  ║
║   1. Spitter spawns → moves slowly toward player                              ║
║   2. When within 400px → stops advancing, starts shooting                     ║
║   3. Player sees green acid projectile flying toward them                     ║
║   4. Player must: dodge projectile OR kill spitter OR tank damage (5 HP)      ║
║   5. Forces tactical decisions: "Do I focus spitter or nearby melee zombies?" ║
║                                                                               ║
║   VALUE_ADD:                                                                  ║
║   - Breaks pure melee kiting patterns                                         ║
║   - Forces target prioritization (spitter vs melee threats)                   ║
║   - Adds dodging challenge with visible projectiles                           ║
║   - Creates tactical depth: kill spitter first vs tank damage                 ║
║                                                                               ║
║   DATA_FLOW:                                                                  ║
║   Spitter.update() → Check range → Check cooldown → Create AcidProjectile →   ║
║   PlayScene collects projectiles → Update projectiles → Check player          ║
║   collision → Apply damage → Remove projectile                                ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location                   | Before                      | After                                       | User Impact                                            |
| -------------------------- | --------------------------- | ------------------------------------------- | ------------------------------------------------------ |
| Zombie spawning            | Normal/Runner variants only | Spitters spawn at 10% rate                  | Player sees green zombies appearing                    |
| Spitter behavior (300-400px) | N/A                        | Spitter slows, shoots acid projectiles      | Player must dodge visible green projectiles            |
| Player HP                  | Only melee damage           | Melee + ranged acid damage (5 HP per hit)   | Player takes damage from distance, must prioritize     |
| Tactical decisions         | Simple kiting               | Must choose: focus spitter or melee threats | Gameplay becomes more strategic and dynamic            |
| Visual feedback            | Yellow bullets only         | Green acid projectiles visible              | Clear visual distinction between player/enemy attacks  |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File                                                                                                            | Lines    | Why Read This                                                     |
| -------- | --------------------------------------------------------------------------------------------------------------- | -------- | ----------------------------------------------------------------- |
| P0       | `/zombie-shooter/src/game/entities/bullet.py`                                                                   | 1-59     | Pattern to MIRROR for AcidProjectile - exact structure            |
| P0       | `/zombie-shooter/src/game/entities/zombie.py`                                                                   | 37-75    | How to add variant-specific behavior in update() method           |
| P0       | `/zombie-shooter/src/game/scenes/play.py`                                                                       | 44-57    | Entity list initialization pattern                                |
| P0       | `/zombie-shooter/src/game/scenes/play.py`                                                                       | 122-157  | Entity update loop pattern with list filtering                    |
| P0       | `/zombie-shooter/src/game/scenes/play.py`                                                                       | 172-196  | Collision handling pattern with index-based removal               |
| P1       | `/zombie-shooter/src/game/systems/collisions.py`                                                                | 8-68     | Collision detection functions to extend                           |
| P1       | `/zombie-shooter/src/game/core/constants.py`                                                                    | 1-106    | Constants structure and naming conventions                        |
| P2       | `/zombie-shooter/tests/test_collisions.py`                                                                      | all      | Test pattern for collision functions                              |
| P2       | `/zombie-shooter/tests/test_zombie_integration.py`                                                              | all      | Test pattern for zombie variant features                          |

**External Documentation:**
| Source | Section | Why Needed |
|--------|---------|------------|
| [Pygame Docs v2.6](https://www.pygame.org/docs/ref/draw.html#pygame.draw.circle) | draw.circle | Rendering acid projectiles |
| [Pygame Docs v2.6](https://www.pygame.org/docs/ref/math.html#pygame.math.Vector2) | Vector2 | Distance calculations for attack range |

---

## Patterns to Mirror

**PROJECTILE ENTITY STRUCTURE:**
```python
# SOURCE: /zombie-shooter/src/game/entities/bullet.py:13-23
# COPY THIS PATTERN FOR AcidProjectile:
class Bullet:
    """Bullet entity with directional movement and TTL."""

    def __init__(self, pos: pygame.Vector2, direction: pygame.Vector2) -> None:
        """Initialize bullet."""
        self.pos = pos.copy()  # Copy to avoid reference issues
        self.vel = direction.normalize() * BULLET_SPEED
        self.radius = BULLET_RADIUS
        self.ttl = BULLET_TTL
```

**PROJECTILE UPDATE METHOD:**
```python
# SOURCE: /zombie-shooter/src/game/entities/bullet.py:25-36
# COPY THIS PATTERN:
def update(self, dt: float) -> bool:
    """Update bullet position and TTL. Returns True if alive, False if should be removed."""
    self.pos += self.vel * dt
    self.ttl -= dt
    return self.is_alive()
```

**PROJECTILE LIFECYCLE CHECK:**
```python
# SOURCE: /zombie-shooter/src/game/entities/bullet.py:38-48
# COPY THIS PATTERN:
def is_alive(self) -> bool:
    """Check if bullet should be removed."""
    if self.ttl <= 0:
        return False
    if self.pos.x < 0 or self.pos.x > WIDTH:
        return False
    return not (self.pos.y < 0 or self.pos.y > HEIGHT)
```

**PROJECTILE DRAW METHOD:**
```python
# SOURCE: /zombie-shooter/src/game/entities/bullet.py:50-59
# COPY THIS PATTERN BUT CHANGE COLOR:
def draw(self, screen: pygame.Surface) -> None:
    """Draw bullet as yellow circle."""
    pygame.draw.circle(
        screen, (255, 255, 0), (int(self.pos.x), int(self.pos.y)), self.radius
    )
# For acid: use (100, 255, 100) for green color
```

**ZOMBIE UPDATE WITH VARIANT BEHAVIOR:**
```python
# SOURCE: /zombie-shooter/src/game/entities/zombie.py:62-75
# EXTEND THIS PATTERN WITH SPITTER CHECK:
def update(self, dt: float, player_pos: pygame.Vector2) -> None:
    """Move toward player position."""
    direction = player_pos - self.pos
    if direction.length() > 0:
        self.vel = direction.normalize() * self.speed
        self.pos += self.vel * dt
    else:
        self.vel = pygame.Vector2(0, 0)

    # Update animation based on current velocity
    self.animation.update(dt, self.vel)

    # ADD SPITTER ATTACK LOGIC HERE:
    # if self.variant == "spitter":
    #     self.attack_cooldown -= dt
    #     distance = (player_pos - self.pos).length()
    #     if distance <= SPITTER_ATTACK_RANGE and self.attack_cooldown <= 0:
    #         # Fire projectile logic
```

**ENTITY LIST UPDATE PATTERN:**
```python
# SOURCE: /zombie-shooter/src/game/scenes/play.py:123-132
# COPY THIS PATTERN FOR ACID PROJECTILES:
# Update bullets and remove dead ones
self.bullets = [b for b in self.bullets if b.update(dt)]

# Update blood particles
self.blood_particles = [p for p in self.blood_particles if p.update(dt)]

# FOR ACID PROJECTILES:
# self.acid_projectiles = [p for p in self.acid_projectiles if p.update(dt)]
```

**COLLISION DETECTION FUNCTION:**
```python
# SOURCE: /zombie-shooter/src/game/systems/collisions.py:51-68
# COPY THIS PATTERN FOR ACID-PLAYER COLLISION:
def check_player_zombie_collisions(
    player_pos: pygame.Vector2, player_radius: float, zombies: list
) -> list[int]:
    """Check player-zombie collisions."""
    colliding = []
    for z_idx, zombie in enumerate(zombies):
        if check_collision_circle(player_pos, player_radius, zombie.pos, zombie.radius):
            colliding.append(z_idx)
    return colliding

# FOR ACID PROJECTILES - RENAME AND ADAPT:
# def check_acid_projectile_player_collisions(
#     player_pos: pygame.Vector2, player_radius: float, projectiles: list
# ) -> list[int]:
```

**COLLISION HANDLING WITH DAMAGE:**
```python
# SOURCE: /zombie-shooter/src/game/scenes/play.py:199-204
# COPY THIS PATTERN FOR ACID DAMAGE:
colliding_zombies = check_player_zombie_collisions(
    self.player.pos, self.player.radius, self.zombies
)
if colliding_zombies:
    damage = CONTACT_DPS * dt * len(colliding_zombies)
    self.player.hp -= damage  # Direct HP subtraction

# FOR ACID PROJECTILES:
# acid_hits = check_acid_projectile_player_collisions(
#     self.player.pos, self.player.radius, self.acid_projectiles
# )
# projectiles_to_remove = set()
# for p_idx in acid_hits:
#     self.player.hp -= ACID_PROJECTILE_DAMAGE
#     projectiles_to_remove.add(p_idx)
```

**TEST STRUCTURE:**
```python
# SOURCE: /zombie-shooter/tests/test_collisions.py:42-52
# COPY THIS PATTERN FOR ACID COLLISION TESTS:
def test_check_bullet_zombie_collisions_no_hits() -> None:
    """Test when bullets and zombies don't collide."""
    bullet = Bullet(pygame.Vector2(0, 0), pygame.Vector2(1, 0))
    zombie = Zombie(pygame.Vector2(100, 100))
    collisions = check_bullet_zombie_collisions([bullet], [zombie])
    assert collisions == []

# FOR ACID PROJECTILES:
# def test_check_acid_projectile_player_collisions_no_hits() -> None:
#     """Test when acid projectiles and player don't collide."""
#     projectile = AcidProjectile(pygame.Vector2(0, 0), pygame.Vector2(1, 0))
#     player_pos = pygame.Vector2(100, 100)
#     collisions = check_acid_projectile_player_collisions(
#         player_pos, PLAYER_RADIUS, [projectile]
#     )
#     assert collisions == []
```

---

## Files to Change

| File                                                                         | Action | Justification                                                    |
| ---------------------------------------------------------------------------- | ------ | ---------------------------------------------------------------- |
| `zombie-shooter/src/game/entities/acid_projectile.py`                        | CREATE | New entity for spitter acid attacks                              |
| `zombie-shooter/src/game/entities/__init__.py`                               | UPDATE | Export AcidProjectile class                                      |
| `zombie-shooter/src/game/entities/zombie.py`                                 | UPDATE | Add attack_cooldown, firing logic for spitter variant            |
| `zombie-shooter/src/game/core/constants.py`                                  | UPDATE | Add acid projectile constants, spitter attack constants          |
| `zombie-shooter/src/game/systems/collisions.py`                              | UPDATE | Add check_acid_projectile_player_collisions()                    |
| `zombie-shooter/src/game/scenes/play.py`                                     | UPDATE | Add acid_projectiles list, update loop, collision handling, draw |
| `zombie-shooter/src/assets/zombies/spitter/walk_down.png`                    | CREATE | Green-tinted spitter sprite (down direction)                     |
| `zombie-shooter/src/assets/zombies/spitter/walk_up.png`                      | CREATE | Green-tinted spitter sprite (up direction)                       |
| `zombie-shooter/src/assets/zombies/spitter/walk_left.png`                    | CREATE | Green-tinted spitter sprite (left direction)                     |
| `zombie-shooter/src/assets/zombies/spitter/walk_right.png`                   | CREATE | Green-tinted spitter sprite (right direction)                    |
| `zombie-shooter/tests/test_acid_projectile.py`                               | CREATE | Unit tests for AcidProjectile entity                             |
| `zombie-shooter/tests/test_spitter_variant.py`                               | CREATE | Integration tests for spitter zombie behavior                    |

---

## NOT Building (Scope Limits)

Explicit exclusions to prevent scope creep:

- **Trail effects for acid projectiles** - Simple circle rendering only (can add in Phase 6 polish)
- **Acid pool area effects** - No lingering damage zones after projectile expires
- **Different acid colors per spitter** - All spitters use same green color
- **Spitter aiming prediction** - Projectiles fire directly at current player position (no lead targeting)
- **Spitter retreat behavior** - Spitters don't actively flee when player approaches (just slow movement)
- **Sound effects** - Visual distinction only (no unique audio for acid or spitter)
- **Spitter animation variants** - Uses same 4-direction walk cycle as other zombies
- **Chain reactions** - Acid hitting other zombies doesn't trigger effects
- **Acid visual effects on player** - No screen tint or particle effects when hit by acid

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: CREATE `zombie-shooter/src/game/core/constants.py` (update)

- **ACTION**: ADD acid projectile and spitter attack constants
- **IMPLEMENT**: Add constants after BULLET section (around line 20):
  ```python
  # Acid Projectiles (Spitter variant)
  ACID_PROJECTILE_SPEED = 300  # Slower than bullets (700)
  ACID_PROJECTILE_RADIUS = 8  # Larger than bullets (4)
  ACID_PROJECTILE_TTL = 2.5  # Longer lifetime than bullets (1.5)
  ACID_PROJECTILE_DAMAGE = 5  # Damage per hit

  # Spitter variant attack
  SPITTER_ATTACK_COOLDOWN = 1.5  # Seconds between attacks
  SPITTER_ATTACK_RANGE = 400  # Pixels - when to start attacking
  ```
- **MIRROR**: Follow existing constant structure (line 15-20: BULLET_SPEED, BULLET_RADIUS, BULLET_TTL)
- **GOTCHA**: Keep constants grouped logically - add acid constants right after bullet constants, before weapons
- **VALIDATE**:
  ```bash
  /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/.venv/bin/python -m ruff check zombie-shooter/src/
  ```

### Task 2: CREATE `zombie-shooter/src/game/entities/acid_projectile.py`

- **ACTION**: CREATE acid projectile entity class
- **IMPLEMENT**: Copy Bullet structure exactly, modify for acid:
  ```python
  """Acid projectile entity for spitter zombie attacks."""

  from __future__ import annotations

  import pygame

  from game.core.constants import (
      ACID_PROJECTILE_DAMAGE,
      ACID_PROJECTILE_RADIUS,
      ACID_PROJECTILE_SPEED,
      ACID_PROJECTILE_TTL,
      HEIGHT,
      WIDTH,
  )


  class AcidProjectile:
      """Acid projectile entity with directional movement and TTL."""

      def __init__(self, pos: pygame.Vector2, direction: pygame.Vector2) -> None:
          """Initialize acid projectile.

          Args:
              pos: Starting position as Vector2.
              direction: Direction vector (will be normalized).
          """
          self.pos = pos.copy()  # Copy to avoid reference issues
          self.vel = direction.normalize() * ACID_PROJECTILE_SPEED
          self.radius = ACID_PROJECTILE_RADIUS
          self.ttl = ACID_PROJECTILE_TTL
          self.damage = ACID_PROJECTILE_DAMAGE

      def update(self, dt: float) -> bool:
          """Update projectile position and TTL.

          Args:
              dt: Delta time in seconds.

          Returns:
              True if projectile should remain in list, False if should be removed.
          """
          self.pos += self.vel * dt
          self.ttl -= dt
          return self.is_alive()

      def is_alive(self) -> bool:
          """Check if projectile should be removed.

          Returns:
              True if projectile is still active, False if expired or off-screen.
          """
          if self.ttl <= 0:
              return False
          if self.pos.x < 0 or self.pos.x > WIDTH:
              return False
          return not (self.pos.y < 0 or self.pos.y > HEIGHT)

      def draw(self, screen: pygame.Surface) -> None:
          """Draw acid projectile as green circle.

          Args:
              screen: Pygame surface to draw on.
          """
          pygame.draw.circle(
              screen, (100, 255, 100), (int(self.pos.x), int(self.pos.y)), self.radius
          )
  ```
- **MIRROR**: `/zombie-shooter/src/game/entities/bullet.py:1-59` - exact structure
- **IMPORTS**: Import constants, pygame, Vector2 pattern
- **GOTCHA**: Use `pos.copy()` not `pos` to avoid reference issues
- **VALIDATE**:
  ```bash
  /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/.venv/bin/python -m ruff check zombie-shooter/src/game/entities/acid_projectile.py
  ```

### Task 3: UPDATE `zombie-shooter/src/game/entities/__init__.py`

- **ACTION**: EXPORT AcidProjectile class
- **IMPLEMENT**: Add to existing exports:
  ```python
  from game.entities.acid_projectile import AcidProjectile

  __all__ = [
      # ... existing exports ...
      "AcidProjectile",
  ]
  ```
- **MIRROR**: Follow existing export pattern in the file
- **VALIDATE**:
  ```bash
  /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/.venv/bin/python -c "from game.entities import AcidProjectile; print('Import OK')"
  ```

### Task 4: UPDATE `zombie-shooter/src/game/entities/zombie.py`

- **ACTION**: ADD spitter attack behavior to Zombie class
- **IMPLEMENT**:
  1. Add attack_cooldown to `__init__` (after line 57):
     ```python
     # Attack cooldown for spitter variant
     self.attack_cooldown = 0.0
     self.pending_projectiles: list[tuple[pygame.Vector2, pygame.Vector2]] = []
     ```
  2. Add attack logic at end of `update()` method (after line 75):
     ```python
     # Spitter variant attack behavior
     if self.variant == "spitter":
         from game.core.constants import SPITTER_ATTACK_COOLDOWN, SPITTER_ATTACK_RANGE

         self.attack_cooldown -= dt
         distance = (player_pos - self.pos).length()

         # Attack if in range and cooldown ready
         if distance <= SPITTER_ATTACK_RANGE and self.attack_cooldown <= 0:
             # Calculate direction to player
             attack_direction = (player_pos - self.pos).normalize()
             # Store projectile data for PlayScene to collect
             self.pending_projectiles.append((self.pos.copy(), attack_direction))
             self.attack_cooldown = SPITTER_ATTACK_COOLDOWN
     ```
- **MIRROR**: `/zombie-shooter/src/game/entities/zombie.py:62-75` - extend update() method
- **IMPORTS**: Import SPITTER_ATTACK_COOLDOWN, SPITTER_ATTACK_RANGE inside method (avoid circular imports)
- **GOTCHA**: Use `self.pos.copy()` when storing position to avoid reference issues
- **VALIDATE**:
  ```bash
  /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/.venv/bin/python -m ruff check zombie-shooter/src/game/entities/zombie.py
  ```

### Task 5: UPDATE `zombie-shooter/src/game/systems/collisions.py`

- **ACTION**: ADD acid projectile-player collision detection function
- **IMPLEMENT**: Add after `check_player_zombie_collisions()` (after line 68):
  ```python
  def check_acid_projectile_player_collisions(
      player_pos: pygame.Vector2, player_radius: float, projectiles: list
  ) -> list[int]:
      """Check player-acid projectile collisions.

      Args:
          player_pos: Player position as Vector2.
          player_radius: Player collision radius.
          projectiles: List of AcidProjectile instances.

      Returns:
          List of projectile indices that collided with player.
      """
      colliding = []
      for p_idx, projectile in enumerate(projectiles):
          if check_collision_circle(
              player_pos, player_radius, projectile.pos, projectile.radius
          ):
              colliding.append(p_idx)
      return colliding
  ```
- **MIRROR**: `/zombie-shooter/src/game/systems/collisions.py:51-68` - check_player_zombie_collisions pattern
- **PATTERN**: Return list of indices, not objects (allows index-based removal)
- **VALIDATE**:
  ```bash
  /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/.venv/bin/python -m ruff check zombie-shooter/src/game/systems/collisions.py
  ```

### Task 6: UPDATE `zombie-shooter/src/game/scenes/play.py`

- **ACTION**: INTEGRATE acid projectiles into play scene (update, collision, draw)
- **IMPLEMENT**:
  1. Add import (after line 8):
     ```python
     from game.entities.acid_projectile import AcidProjectile
     from game.systems.collisions import check_acid_projectile_player_collisions
     ```
  2. Add list to `__init__` (after line 57):
     ```python
     self.acid_projectiles: list[AcidProjectile] = []
     ```
  3. Add update loop (after zombies update, around line 143):
     ```python
     # Collect acid projectiles from spitter zombies
     for zombie in self.zombies:
         if zombie.variant == "spitter" and zombie.pending_projectiles:
             for pos, direction in zombie.pending_projectiles:
                 self.acid_projectiles.append(AcidProjectile(pos, direction))
             zombie.pending_projectiles.clear()

     # Update acid projectiles and remove dead ones
     self.acid_projectiles = [p for p in self.acid_projectiles if p.update(dt)]
     ```
  4. Add collision handling (after player-zombie collision, around line 206):
     ```python
     # Acid projectile-player collisions
     acid_hits = check_acid_projectile_player_collisions(
         self.player.pos, self.player.radius, self.acid_projectiles
     )
     projectiles_to_remove = set()
     for p_idx in acid_hits:
         projectile = self.acid_projectiles[p_idx]
         self.player.hp -= projectile.damage
         projectiles_to_remove.add(p_idx)

     self.acid_projectiles = [
         p for i, p in enumerate(self.acid_projectiles) if i not in projectiles_to_remove
     ]
     ```
  5. Add drawing (after pickups, before blood particles, around line 256):
     ```python
     # Draw acid projectiles
     for projectile in self.acid_projectiles:
         projectile.draw(screen)
     ```
- **MIRROR**:
  - `/zombie-shooter/src/game/scenes/play.py:123-157` - update loop pattern
  - `/zombie-shooter/src/game/scenes/play.py:172-196` - collision handling pattern
  - `/zombie-shooter/src/game/scenes/play.py:212-268` - draw pattern
- **GOTCHA**: Draw acid projectiles BEFORE blood particles (layer order matters)
- **VALIDATE**:
  ```bash
  /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/.venv/bin/python -m ruff check zombie-shooter/src/game/scenes/play.py
  ```

### Task 7: CREATE spitter zombie sprites

- **ACTION**: CREATE green-tinted sprite assets for spitter variant
- **IMPLEMENT**: Create Python script to generate green-tinted sprites:
  ```python
  """Generate green-tinted spitter zombie sprites."""
  from pathlib import Path
  import pygame

  pygame.init()
  pygame.display.set_mode((1, 1))  # Minimal display for image processing

  script_dir = Path(__file__).resolve().parent
  assets_dir = script_dir / "src/assets/zombies"
  spitter_dir = script_dir / "src/assets/zombies/spitter"
  spitter_dir.mkdir(parents=True, exist_ok=True)

  directions = ["walk_down", "walk_up", "walk_left", "walk_right"]

  for direction in directions:
      original_path = assets_dir / f"{direction}.png"
      original = pygame.image.load(str(original_path))

      # Create green-tinted version
      tinted = original.copy()
      green_overlay = pygame.Surface(original.get_size()).convert_alpha()
      green_overlay.fill((80, 255, 120, 0))  # Green tint
      tinted.blit(green_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

      # Save
      output_path = spitter_dir / f"{direction}.png"
      pygame.image.save(tinted, str(output_path))
      print(f"Created {output_path}")

  print("Spitter sprites created successfully!")
  ```
- **RUN**:
  ```bash
  /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/.venv/bin/python zombie-shooter/create_spitter_sprites.py
  ```
- **MIRROR**: Phase 2 runner sprite generation pattern (color tinting with BLEND_RGBA_ADD)
- **VALIDATE**: Check files exist:
  ```bash
  ls -la zombie-shooter/src/assets/zombies/spitter/
  ```

### Task 8: CREATE `zombie-shooter/tests/test_acid_projectile.py`

- **ACTION**: CREATE unit tests for AcidProjectile entity
- **IMPLEMENT**:
  ```python
  """Tests for acid projectile entity."""

  from __future__ import annotations

  import pygame
  from game.core.constants import (
      ACID_PROJECTILE_DAMAGE,
      ACID_PROJECTILE_RADIUS,
      ACID_PROJECTILE_SPEED,
      ACID_PROJECTILE_TTL,
  )
  from game.entities.acid_projectile import AcidProjectile

  pygame.init()


  def test_acid_projectile_initialization() -> None:
      """Test that acid projectile initializes with correct attributes."""
      pos = pygame.Vector2(100, 100)
      direction = pygame.Vector2(1, 0)
      projectile = AcidProjectile(pos, direction)

      assert projectile.pos.x == 100
      assert projectile.pos.y == 100
      assert projectile.radius == ACID_PROJECTILE_RADIUS
      assert projectile.ttl == ACID_PROJECTILE_TTL
      assert projectile.damage == ACID_PROJECTILE_DAMAGE


  def test_acid_projectile_position_copy() -> None:
      """Test that acid projectile copies position (no reference issues)."""
      pos = pygame.Vector2(100, 100)
      direction = pygame.Vector2(1, 0)
      projectile = AcidProjectile(pos, direction)

      pos.x = 200  # Modify original
      assert projectile.pos.x == 100  # Projectile position unchanged


  def test_acid_projectile_update_moves_position() -> None:
      """Test that acid projectile moves based on velocity."""
      projectile = AcidProjectile(pygame.Vector2(100, 100), pygame.Vector2(1, 0))
      initial_x = projectile.pos.x

      projectile.update(0.1)

      assert projectile.pos.x > initial_x
      assert projectile.pos.x == pytest.approx(initial_x + ACID_PROJECTILE_SPEED * 0.1, abs=0.1)


  def test_acid_projectile_update_decreases_ttl() -> None:
      """Test that acid projectile TTL decreases over time."""
      projectile = AcidProjectile(pygame.Vector2(100, 100), pygame.Vector2(1, 0))
      initial_ttl = projectile.ttl

      projectile.update(0.5)

      assert projectile.ttl < initial_ttl
      assert projectile.ttl == pytest.approx(initial_ttl - 0.5, abs=0.01)


  def test_acid_projectile_dies_when_ttl_expires() -> None:
      """Test that acid projectile is removed after TTL expires."""
      projectile = AcidProjectile(pygame.Vector2(100, 100), pygame.Vector2(1, 0))

      is_alive = projectile.update(ACID_PROJECTILE_TTL + 0.5)

      assert is_alive is False


  def test_acid_projectile_dies_off_screen() -> None:
      """Test that acid projectile is removed when off-screen."""
      projectile = AcidProjectile(pygame.Vector2(100, 100), pygame.Vector2(-1, 0))

      # Move far off screen
      for _ in range(100):
          projectile.update(0.1)

      assert projectile.is_alive() is False


  def test_acid_projectile_draw_no_error() -> None:
      """Test that acid projectile draws without error."""
      projectile = AcidProjectile(pygame.Vector2(100, 100), pygame.Vector2(1, 0))
      screen = pygame.Surface((800, 600))

      projectile.draw(screen)  # Should not raise
  ```
- **MIRROR**: `/zombie-shooter/tests/test_collisions.py` - test structure and patterns
- **IMPORTS**: Import pytest for approx assertions if needed
- **VALIDATE**:
  ```bash
  export PYTHONPATH="zombie-shooter/src" && /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/.venv/bin/python -m pytest zombie-shooter/tests/test_acid_projectile.py -v
  ```

---

## Testing Strategy

### Unit Tests to Write

| Test File                                              | Test Cases                                                 | Validates                           |
| ------------------------------------------------------ | ---------------------------------------------------------- | ----------------------------------- |
| `tests/test_acid_projectile.py`                        | init, movement, TTL expiry, off-screen removal, draw       | AcidProjectile entity behavior      |
| `tests/test_spitter_variant.py`                        | cooldown, range check, projectile spawning, damage        | Spitter zombie attack behavior      |
| `tests/test_collisions.py` (extend)                    | acid-player collision detection                            | Collision system extension          |

### Edge Cases Checklist

- [ ] Acid projectile spawns at spitter position (not player position)
- [ ] Attack cooldown prevents spam (1.5s minimum between attacks)
- [ ] Spitter doesn't attack when player is beyond range (400px)
- [ ] Acid projectiles removed when player is hit
- [ ] Acid projectiles removed when off-screen
- [ ] Acid projectiles removed when TTL expires
- [ ] Player HP reduces correctly on acid hit (5 damage)
- [ ] Multiple acid projectiles can hit player simultaneously
- [ ] Spitter attack works while moving
- [ ] Dead spitter doesn't fire projectiles
- [ ] Pending projectiles cleared each frame

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
/Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/.venv/bin/python -m ruff check zombie-shooter/src/
```

**EXPECT**: Exit 0, no errors or warnings

### Level 2: UNIT_TESTS

```bash
export PYTHONPATH="zombie-shooter/src" && /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/.venv/bin/python -m pytest zombie-shooter/tests/ -v
```

**EXPECT**: All tests pass, including new acid projectile and spitter tests

### Level 3: FULL_SUITE

```bash
export PYTHONPATH="zombie-shooter/src" && /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/.venv/bin/python -m pytest zombie-shooter/tests/ && /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/.venv/bin/python -m ruff check zombie-shooter/src/
```

**EXPECT**: All tests pass, linting passes, exit 0

### Level 4: ENABLE_SPITTER_SPAWNING

After all tests pass, enable spitter variant:

```bash
# Edit constants.py - change spitter weight from 0 to 1.0 (10% spawn rate)
```

**EXPECT**: Spitter zombies spawn in gameplay

### Level 5: MANUAL_VALIDATION

1. **Start game**: Run `python zombie-shooter/src/game/main.py`
2. **Verify spitter spawning**: Wait 10-15 seconds, look for green zombies
3. **Verify attack behavior**:
   - Green zombie approaches but stops at distance
   - Green acid projectiles fire toward player
   - Projectiles are visible and distinct from yellow bullets
4. **Verify damage**: Watch player HP bar - should decrease when hit by acid
5. **Verify tactical challenge**: Spitters force target prioritization decisions
6. **Check performance**: Game maintains 60 FPS with spitters active

---

## Acceptance Criteria

- [ ] All specified functionality implemented per user story
- [ ] Level 1-3 validation commands pass with exit 0
- [ ] Unit tests cover acid projectile lifecycle, spitter attack behavior
- [ ] Code mirrors existing patterns exactly (Bullet entity, collision system)
- [ ] No regressions in existing tests (94/94 still pass)
- [ ] Spitter sprites created and loaded correctly (green-tinted, 4 directions)
- [ ] Spitter zombies spawn at 10% rate when enabled (weight=1.0)
- [ ] Acid projectiles visible, distinct from player bullets (green vs yellow)
- [ ] Player takes damage from acid projectiles (5 HP per hit)
- [ ] Spitter maintains distance and attacks from range (300-400px)
- [ ] Attack cooldown prevents spam (1.5s between attacks)
- [ ] Performance stable (60 FPS with multiple spitters)

---

## Completion Checklist

- [ ] Task 1: Constants added (ACID_PROJECTILE_*, SPITTER_ATTACK_*)
- [ ] Task 2: AcidProjectile entity created
- [ ] Task 3: AcidProjectile exported from entities module
- [ ] Task 4: Zombie.update() extended with spitter attack logic
- [ ] Task 5: Collision function added (check_acid_projectile_player_collisions)
- [ ] Task 6: PlayScene integrated (list, update, collision, draw)
- [ ] Task 7: Spitter sprites created (green-tinted, 4 directions)
- [ ] Task 8: Unit tests written and passing
- [ ] Level 1: Linting passes (ruff check)
- [ ] Level 2: Unit tests pass (pytest)
- [ ] Level 3: Full suite passes (tests + lint)
- [ ] Level 4: Spitter weight enabled (weight=1.0)
- [ ] Level 5: Manual validation passed (gameplay testing)
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk                                       | Likelihood | Impact | Mitigation                                                                                 |
| ------------------------------------------ | ---------- | ------ | ------------------------------------------------------------------------------------------ |
| Projectile spam degrades performance       | LOW        | MEDIUM | Use TTL (2.5s), limit spawn rate (1.5s cooldown), tested at 50 zombies                    |
| Spitters too easy/hard to kill             | MEDIUM     | MEDIUM | Use same HP as normal zombies (1 shot), tune weight in Phase 6 if needed                  |
| Attack range feels unbalanced              | MEDIUM     | MEDIUM | Start at 400px, can adjust in Phase 6 based on playtesting                                |
| Acid projectiles hard to see/dodge         | MEDIUM     | HIGH   | Use distinct green color (100, 255, 100), larger radius (8px vs 4px), slower speed (300)  |
| Spitter doesn't maintain distance          | LOW        | MEDIUM | No retreat behavior - just slow speed (100 vs 140 normal), attack from current position   |
| Circular import issues                     | LOW        | LOW    | Import constants inside methods if needed, follow existing patterns                        |
| Pending projectiles not cleared            | LOW        | HIGH   | Clear `pending_projectiles` list after collecting in PlayScene                             |

---

## Notes

**Design Decisions:**

1. **Projectile Collection Pattern**: Zombies don't create projectiles directly - they store pending projectiles that PlayScene collects. This avoids circular imports (Zombie → AcidProjectile → constants → Zombie) and keeps entity creation centralized in PlayScene.

2. **Attack Range vs Movement**: Spitters don't actively maintain distance - they just move slowly (100 px/s) and attack when in range (400px). This is simpler than flee behavior and creates natural spacing.

3. **Color Choice**: Green (100, 255, 100) provides high contrast against yellow bullets (255, 255, 0) and gray background (40, 40, 40). Easy to distinguish at a glance.

4. **Damage Tuning**: 5 HP per projectile means:
   - 20 hits to kill player (100 HP / 5 damage)
   - At 1.5s cooldown = 30 seconds of constant hits
   - With player dodging, about 5-10 hits in 60s session is reasonable

5. **Spawn Weight**: Start at 10% (weight=1.0) after Phase 5, tune in Phase 6 based on playtesting. May adjust to 8% (0.8) or 12% (1.2) if needed.

**Future Enhancements (Phase 6):**
- Visual trail effect for acid projectiles
- Hit feedback (screen flash when hit by acid)
- Spitter warning indicator (color change before attack)
- Sound effects for acid firing and impact
- Particle burst on acid impact

**Phase 5 → Phase 6 Transition:**
After Phase 5 complete, Phase 4 (Exploder) will still be pending (depends on Phase 3 Tank completion). Phase 6 (polish) requires all variants complete. Recommended next step: implement Phase 3 (Tank) in parallel worktree, then Phase 4, then Phase 6.
