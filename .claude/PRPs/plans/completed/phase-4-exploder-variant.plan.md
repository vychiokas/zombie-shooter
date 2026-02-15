# Feature: Phase 4 - Exploder Zombie Variant

## Summary

Implement the Exploder zombie variant - a normal-speed (140 px/s) enemy that explodes on death, dealing AOE damage to both the player (10 HP if within 80px) and nearby zombies (1 HP each). Creates tactical depth through risk/reward decisions (kill near self = damage, kill near horde = crowd clear) and emergent chain reactions (exploding Exploders trigger more explosions). Orange/yellow-tinted sprites provide clear visual distinction.

## User Story

As a player
I want to encounter explosive zombies that damage nearby enemies on death
So that I can make strategic decisions about kill timing and positioning for tactical advantage

## Problem Statement

Players have no tactical decisions around enemy death timing. All zombies simply die when killed with no consequence or opportunity cost. Combat lacks emergent gameplay and strategic positioning decisions. There's no risk/reward trade-off or chain reaction mechanics.

**Testable Success**: Orange Exploder zombies spawn, move at 140 px/s, die in 1 hit, explode on death dealing 10 HP to player if within 80px radius, 1 HP to zombies within radius, create visible explosion effect, and enable chain reactions.

## Solution Statement

Exploder variant leverages the existing HP system (Phase 1) and death detection (PlayScene line 197). When `zombie.hp <= 0` AND `zombie.variant == "exploder"`, trigger AOE explosion logic that: (1) finds all entities within 80px using existing `check_collision_circle()`, (2) applies damage to player and nearby zombies, (3) spawns explosion particle effect (more particles than normal death), (4) checks if damaged zombies die to trigger chain reactions.

## Metadata

| Field            | Value                                    |
| ---------------- | ---------------------------------------- |
| Type             | NEW_CAPABILITY                           |
| Complexity       | MEDIUM                                   |
| Systems Affected | constants, assets, PlayScene, collisions |
| Dependencies     | pygame>=2.6.0, Python 3.11+              |
| Estimated Tasks  | 5 (core) + 1 (optional warning visual)   |

---

## UX Design

### Before State
```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌─────────────┐                                                             ║
║   │   Player    │ shoots → zombie dies (no consequence)                       ║
║   │  (center)   │                                                             ║
║   └─────────────┘                                                             ║
║         ▲                                                                     ║
║         │                                                                     ║
║    ┌────┴────┐                                                                ║
║    │ Normal  │ HP=1, dies instantly                                           ║
║    │ Zombie  │                                                                ║
║    └─────────┘                                                                ║
║         │                                                                     ║
║    ┌────▼────┐                                                                ║
║    │ Runner  │ HP=1, dies instantly (fast)                                    ║
║    │ Zombie  │                                                                ║
║    └─────────┘                                                                ║
║                                                                               ║
║   USER_FLOW: See zombie → shoot → zombie dies → spawn gore → continue         ║
║   PAIN_POINT: No tactical decisions around death timing or positioning        ║
║   DATA_FLOW: Bullet hits zombie → HP-=1 → HP<=0 → spawn gore → remove zombie  ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌─────────────┐                                                             ║
║   │   Player    │ shoots Exploder → explosion damages player!                 ║
║   │  (nearby)   │ HP: 100 → 90 (took explosion damage)                        ║
║   └─────────────┘                                                             ║
║         ▲                                                                     ║
║         │ 50px away                                                           ║
║    ┌────┴────────┐                                                            ║
║    │  EXPLODER   │ HP=1, explodes on death (80px AOE)                         ║
║    │  (Orange)   │                                                            ║
║    └─────────────┘                                                            ║
║         │ ◄── Shot 1: HP=1→0 (dies, triggers explosion)                       ║
║         │                                                                     ║
║         ├───► Explosion Effect: 16 particles burst outward (300px/s)          ║
║         ├───► Player damaged: -10 HP (within 80px radius)                     ║
║         └───► Nearby zombies damaged: -1 HP each (within 80px radius)         ║
║                                                                               ║
║   ┌──────────────────────── CHAIN REACTION ──────────────────────┐            ║
║   │                                                               │            ║
║   │  Exploder #1 dies → explosion damages Exploder #2            │            ║
║   │  Exploder #2 HP: 1→0 → triggers explosion #2                 │            ║
║   │  Explosion #2 damages Normal Zombie + Exploder #3            │            ║
║   │  Exploder #3 HP: 1→0 → triggers explosion #3                 │            ║
║   │  Chain continues until no more Exploders in blast radius     │            ║
║   │                                                               │            ║
║   └───────────────────────────────────────────────────────────────┘            ║
║                                                                               ║
║   USER_FLOW:                                                                  ║
║   1. Orange Exploder spawns → moves toward player                             ║
║   2. Player shoots → Exploder dies                                            ║
║   3. Explosion effect plays (large particle burst)                            ║
║   4. Player takes damage if too close (-10 HP)                                ║
║   5. Nearby zombies damaged (-1 HP, may die and chain react)                  ║
║                                                                               ║
║   TACTICAL DECISIONS:                                                         ║
║   - "Should I kill this Exploder now or wait until more zombies cluster?"     ║
║   - "Am I too close? Will I take explosion damage?"                           ║
║   - "Can I trigger a chain reaction to clear this horde?"                     ║
║   - "Should I prioritize Exploders or let them cluster first?"                ║
║                                                                               ║
║   VALUE_ADD:                                                                  ║
║   - Risk/reward positioning (kill close = damage, kill far = safe clear)      ║
║   - Emergent chain reactions (Exploders trigger Exploders)                    ║
║   - Strategic kill timing (wait for clusters vs instant kill)                 ║
║   - Crowd control tool (use explosions to thin hordes)                        ║
║                                                                               ║
║   DATA_FLOW:                                                                  ║
║   Bullet hits Exploder → HP-=1 → HP<=0 → check variant=="exploder"            ║
║   → apply_explosion(pos, 80px radius)                                         ║
║   → check all zombies within radius → reduce HP by 1                          ║
║   → check if damaged zombies HP<=0 → recursive chain reaction                 ║
║   → check player within radius → reduce player HP by 10                       ║
║   → spawn explosion particles (16, faster, shorter lifetime)                  ║
║   → spawn normal gore (corpse, blood pool, blood particles)                   ║
║   → remove Exploder zombie                                                    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location              | Before                     | After                                         | User Impact                                      |
| --------------------- | -------------------------- | --------------------------------------------- | ------------------------------------------------ |
| Zombie spawning       | Normal/Runner/Tank/Spitter | Exploders spawn at 10% rate                   | Player sees slow orange zombies                  |
| Zombie death          | Dies, spawns gore          | Exploder dies, spawns gore + **explosion**    | Visual burst, AOE damage                         |
| Player positioning    | No death consequence       | Explosion damages player if within 80px       | Must maintain safe distance from Exploders       |
| Zombie clustering     | No benefit to spacing      | Explosions damage nearby zombies              | Strategic kill timing for crowd control          |
| Chain reactions       | N/A                        | Exploder deaths can trigger more Exploders    | Emergent cascading explosions                    |
| Tactical decision     | Simple kill priority       | "Kill now or wait for cluster?"               | Risk/reward timing decisions                     |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `zombie-shooter/src/game/scenes/play.py` | 186-209 | Death detection logic - WHERE to inject explosion code |
| P0 | `zombie-shooter/src/game/systems/collisions.py` | 8-26 | Circle collision function - HOW to find zombies in radius |
| P0 | `zombie-shooter/src/game/scenes/play.py` | 82-99 | Particle spawn pattern - HOW to create explosion effect |
| P1 | `zombie-shooter/src/game/core/constants.py` | 66-97 | ZOMBIE_VARIANTS structure - exploder already defined |
| P1 | `zombie-shooter/tests/test_tank_variant.py` | all | Test pattern to copy for Exploder tests |
| P2 | `zombie-shooter/src/game/entities/blood_particle.py` | all | Particle entity structure (optional: custom explosion particles) |

**External Documentation:**
| Source | Section | Why Needed |
|--------|---------|------------|
| [Pygame v2.6 Surface Docs](https://www.pygame.org/docs/ref/surface.html) | BLEND_RGBA_ADD | Sprite tinting for orange/yellow color |
| [Pygame Collision Best Practices](https://github.com/Rabbid76/PyGameExamplesAndAnswers/blob/master/documentation/pygame/pygame_collision_and_intesection.md) | Distance squared | AOE radius checks (already implemented) |

---

## Patterns to Mirror

**DEATH DETECTION PATTERN:**
```python
# SOURCE: zombie-shooter/src/game/scenes/play.py:186-209
# INJECT EXPLOSION LOGIC HERE:

# Bullet-zombie collisions
bullet_zombie_hits = check_bullet_zombie_collisions(self.bullets, self.zombies)

zombies_to_remove = set()
for b_idx, z_idx in bullet_zombie_hits:
    zombie = self.zombies[z_idx]
    zombie.hp -= 1
    bullets_to_remove.add(b_idx)

    # Death check - INJECT EXPLOSION LOGIC HERE
    if zombie.hp <= 0:
        # Check if exploder variant
        if zombie.variant == "exploder":
            self.apply_explosion(zombie.pos)  # <-- NEW METHOD

        # Standard death handling
        self.spawn_blood_splash(zombie.pos)
        self.blood_decals.append(BloodDecal(zombie.pos))
        self.dead_zombies.append(DeadZombie(zombie.pos))
        zombies_to_remove.add(z_idx)
        self.kills += 1
```

**CIRCLE COLLISION PATTERN (for AOE):**
```python
# SOURCE: zombie-shooter/src/game/systems/collisions.py:8-26
# REUSE THIS FOR EXPLOSION RADIUS:

def check_collision_circle(
    pos1: pygame.Vector2, r1: float, pos2: pygame.Vector2, r2: float
) -> bool:
    """Check if two circles overlap using distance squared (no sqrt).

    Returns True if circles overlap, False otherwise.
    """
    dx = pos2.x - pos1.x
    dy = pos2.y - pos1.y
    distance_squared = dx * dx + dy * dy
    radius_sum = r1 + r2
    return distance_squared <= radius_sum * radius_sum
```

**PARTICLE SPAWN PATTERN:**
```python
# SOURCE: zombie-shooter/src/game/scenes/play.py:82-99
# COPY THIS FOR EXPLOSION EFFECT (modify counts/speed):

def spawn_blood_splash(self, pos: pygame.Vector2) -> None:
    """Spawn blood particles at position with random outward velocities."""
    import math

    for _ in range(BLOOD_PARTICLE_COUNT):  # 8 for blood, 16 for explosion
        # Random angle (0 to 2π)
        angle = random.uniform(0, 2 * math.pi)
        # Random speed variation
        speed = BLOOD_PARTICLE_SPEED * random.uniform(0.75, 1.25)

        # Convert angle to velocity vector
        vel = pygame.Vector2(math.cos(angle) * speed, math.sin(angle) * speed)

        self.blood_particles.append(BloodParticle(pos, vel))
```

**DAMAGE APPLICATION PATTERN:**
```python
# SOURCE: zombie-shooter/src/game/scenes/play.py:211-233
# COPY THIS PATTERN FOR EXPLOSION DAMAGE:

# Acid projectile-player collisions (for reference)
acid_hits = check_acid_projectile_player_collisions(
    self.player.pos, self.player.radius, self.acid_projectiles
)
for p_idx in acid_hits:
    projectile = self.acid_projectiles[p_idx]
    self.player.hp -= projectile.damage  # <-- DAMAGE APPLICATION

# For explosion damage to zombies:
# for zombie in self.zombies:
#     if check_collision_circle(explosion_pos, 80, zombie.pos, zombie.radius):
#         zombie.hp -= EXPLODER_EXPLOSION_DAMAGE_TO_ZOMBIES
```

**SPRITE TINTING PATTERN:**
```python
# SOURCE: Phase 2 Runner implementation, Phase 3 Tank implementation
# COPY THIS PATTERN FOR ORANGE/YELLOW TINT:

import pygame

pygame.init()
pygame.display.set_mode((1, 1))

original = pygame.image.load("src/assets/zombies/walk_down.png")
tinted = original.copy()

# Orange overlay for Exploder
orange_overlay = pygame.Surface(original.get_size()).convert_alpha()
orange_overlay.fill((255, 140, 0, 0))  # Orange tint
tinted.blit(orange_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

# Yellow highlight for extra visibility
yellow_overlay = pygame.Surface(original.get_size()).convert_alpha()
yellow_overlay.fill((200, 180, 0, 0))  # Yellow tint
tinted.blit(yellow_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

pygame.image.save(tinted, "src/assets/zombies/exploder/walk_down.png")
```

**TEST STRUCTURE:**
```python
# SOURCE: zombie-shooter/tests/test_tank_variant.py
# COPY THIS STRUCTURE FOR EXPLODER TESTS:

def test_exploder_variant_has_correct_stats() -> None:
    """Test that exploder zombie initializes with correct variant stats."""
    exploder = Zombie(pygame.Vector2(100, 100), variant="exploder")

    assert exploder.variant == "exploder"
    assert exploder.hp == 1
    assert exploder.speed == 140
    assert exploder.radius == 16


def test_exploder_explosion_damages_nearby_zombies() -> None:
    """Test that explosion damages nearby zombies within radius."""
    game = MagicMock()
    scene = PlayScene(game)

    exploder = Zombie(pygame.Vector2(100, 100), variant="exploder")
    nearby = Zombie(pygame.Vector2(150, 100))  # 50px away (within 80px)
    far = Zombie(pygame.Vector2(300, 100))  # 200px away (outside 80px)

    scene.zombies.extend([exploder, nearby, far])

    # Kill exploder
    from game.entities.bullet import Bullet
    bullet = Bullet(pygame.Vector2(98, 98), pygame.Vector2(1, 0))
    scene.bullets.append(bullet)
    scene.update(0.01)

    # Check damage application
    assert nearby.hp < 1  # Was damaged
    assert far.hp == 1    # Untouched
```

---

## Files to Change

| File | Action | Justification |
|------|--------|---------------|
| `zombie-shooter/src/game/core/constants.py` | UPDATE | Add explosion constants, enable exploder weight |
| `zombie-shooter/src/game/scenes/play.py` | UPDATE | Add explosion logic to death handler, create apply_explosion method |
| `zombie-shooter/src/assets/zombies/exploder/walk_down.png` | CREATE | Exploder sprite (down direction) |
| `zombie-shooter/src/assets/zombies/exploder/walk_up.png` | CREATE | Exploder sprite (up direction) |
| `zombie-shooter/src/assets/zombies/exploder/walk_left.png` | CREATE | Exploder sprite (left direction) |
| `zombie-shooter/src/assets/zombies/exploder/walk_right.png` | CREATE | Exploder sprite (right direction) |
| `zombie-shooter/tests/test_exploder_variant.py` | CREATE | Unit tests for Exploder variant and explosion mechanics |

---

## NOT Building (Scope Limits)

Explicit exclusions to prevent scope creep:

- **Warning visual (pulse before explosion)** - Optional Phase 4 enhancement, not core requirement
- **Different explosion particle colors** - Explosion reuses blood particle system (red), not custom orange particles
- **Explosion sound effects** - Visual distinction only per PRD
- **Explosion screen shake** - No camera effects
- **Explosion damage variance** - Fixed damage (10 to player, 1 to zombies)
- **Explosion radius scaling** - Always 80px, no time-based or HP-based scaling
- **Exploder self-destruct timer** - Only explodes on death, not automatic detonation
- **Player explosive damage to Exploders** - No special interaction, bullets deal normal damage
- **Explosion damage to pickups/items** - Only affects player and zombies
- **Different blood colors for Exploder** - Uses standard red blood like all variants

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: UPDATE `zombie-shooter/src/game/core/constants.py`

- **ACTION**: ADD explosion constants and ENABLE exploder spawning
- **IMPLEMENT**:
  ```python
  # Add after line 30 (after SPITTER_ATTACK_RANGE):

  # Exploder variant explosion
  EXPLODER_EXPLOSION_RADIUS = 80  # Pixels - AOE damage radius
  EXPLODER_EXPLOSION_DAMAGE_TO_ZOMBIES = 1  # HP damage per nearby zombie
  EXPLODER_EXPLOSION_DAMAGE_TO_PLAYER = 10  # HP damage if player in radius
  EXPLODER_PARTICLE_COUNT = 16  # More particles than normal death (vs 8)
  EXPLODER_PARTICLE_SPEED = 300  # Faster particles than blood (vs 150)
  EXPLODER_PARTICLE_LIFETIME = 0.5  # Shorter for dramatic effect (vs 0.8)

  # Update exploder weight (line 89):
  "exploder": {
      "speed": 140,  # Normal speed
      "hp": 1,
      "radius": 16,
      "weight": 1.0,  # 10% spawn rate (enabled in Phase 4)
  },
  ```
- **MIRROR**: ZOMBIE_VARIANTS structure lines 66-97, acid projectile constants lines 22-30
- **LOCATION**: Lines 31-37 (new constants), line 89 (weight change)
- **GOTCHA**: Keep constants together by category (explosion constants grouped)
- **VALIDATE**:
  ```bash
  /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/.venv/bin/python -m ruff check zombie-shooter/src/game/core/constants.py
  ```

### Task 2: CREATE `zombie-shooter/src/game/scenes/play.py` - Add explosion method

- **ACTION**: ADD apply_explosion method to PlayScene class
- **IMPLEMENT** (add after `spawn_blood_splash` method, around line 100):
  ```python
  def apply_explosion(self, explosion_pos: pygame.Vector2) -> None:
      """Apply AOE explosion damage to player and zombies.

      Handles:
      1. Damage to player if within radius (10 HP)
      2. Damage to nearby zombies (1 HP each)
      3. Chain reaction handling (newly killed Exploders trigger recursively)
      4. Enhanced particle effect (more/faster than normal death)

      Args:
          explosion_pos: Center of explosion (dead Exploder position).
      """
      from game.core.constants import (
          EXPLODER_EXPLOSION_RADIUS,
          EXPLODER_EXPLOSION_DAMAGE_TO_PLAYER,
          EXPLODER_EXPLOSION_DAMAGE_TO_ZOMBIES,
          EXPLODER_PARTICLE_COUNT,
          EXPLODER_PARTICLE_SPEED,
      )
      from game.systems.collisions import check_collision_circle
      import math

      # Damage player if within radius
      if check_collision_circle(
          explosion_pos,
          EXPLODER_EXPLOSION_RADIUS,
          self.player.pos,
          self.player.radius,
      ):
          self.player.hp -= EXPLODER_EXPLOSION_DAMAGE_TO_PLAYER

      # Damage nearby zombies (potential chain reactions)
      newly_dead_exploders = []
      for zombie in self.zombies:
          if check_collision_circle(
              explosion_pos,
              EXPLODER_EXPLOSION_RADIUS,
              zombie.pos,
              zombie.radius,
          ):
              zombie.hp -= EXPLODER_EXPLOSION_DAMAGE_TO_ZOMBIES

              # Check if zombie died from explosion
              if zombie.hp <= 0:
                  # If it's an Exploder, queue for chain reaction
                  if zombie.variant == "exploder":
                      newly_dead_exploders.append(zombie.pos.copy())

      # Spawn enhanced explosion particle effect
      for _ in range(EXPLODER_PARTICLE_COUNT):
          angle = random.uniform(0, 2 * math.pi)
          speed = EXPLODER_PARTICLE_SPEED * random.uniform(0.75, 1.25)
          vel = pygame.Vector2(math.cos(angle) * speed, math.sin(angle) * speed)
          self.blood_particles.append(BloodParticle(explosion_pos, vel))

      # Chain reaction: recursively explode newly killed Exploders
      for exploder_pos in newly_dead_exploders:
          self.apply_explosion(exploder_pos)
  ```
- **MIRROR**: `spawn_blood_splash()` method (lines 82-99), collision patterns from collisions.py
- **IMPORTS**: Import constants inside method to avoid circular imports (same pattern as Zombie.update for spitter)
- **GOTCHA**: Use `zombie.pos.copy()` for chain reactions to avoid reference issues
- **VALIDATE**:
  ```bash
  /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/.venv/bin/python -m ruff check zombie-shooter/src/game/scenes/play.py
  ```

### Task 3: UPDATE `zombie-shooter/src/game/scenes/play.py` - Trigger explosion on death

- **ACTION**: MODIFY death handler to call apply_explosion for Exploder deaths
- **IMPLEMENT** (modify lines 197-202):
  ```python
  # Only spawn gore and remove zombie if HP depleted
  if zombie.hp <= 0:
      # Check if exploder variant - trigger explosion BEFORE removal
      if zombie.variant == "exploder":
          self.apply_explosion(zombie.pos)

      # Standard death handling (all variants)
      self.spawn_blood_splash(zombie.pos)
      self.blood_decals.append(BloodDecal(zombie.pos))
      self.dead_zombies.append(DeadZombie(zombie.pos))
      zombies_to_remove.add(z_idx)
      self.kills += 1
  ```
- **MIRROR**: Existing death detection pattern (lines 197-202)
- **LOCATION**: Line 199 (add 2 lines before spawn_blood_splash)
- **GOTCHA**: Call explosion BEFORE spawning blood splash, so explosion particles layer correctly
- **VALIDATE**:
  ```bash
  /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/.venv/bin/python -m ruff check zombie-shooter/src/game/scenes/play.py
  ```

### Task 4: CREATE exploder zombie sprites

- **ACTION**: CREATE orange/yellow-tinted sprite assets for exploder variant
- **IMPLEMENT**: Python script to generate tinted sprites
  ```python
  """Generate orange/yellow-tinted exploder zombie sprites."""
  from pathlib import Path
  import pygame

  pygame.init()
  pygame.display.set_mode((1, 1))

  script_dir = Path(__file__).resolve().parent
  assets_dir = script_dir / "src/assets/zombies"
  exploder_dir = script_dir / "src/assets/zombies/exploder"
  exploder_dir.mkdir(parents=True, exist_ok=True)

  directions = ["walk_down", "walk_up", "walk_left", "walk_right"]

  for direction in directions:
      original_path = assets_dir / f"{direction}.png"
      original = pygame.image.load(str(original_path))

      # Create orange-tinted version
      tinted = original.copy()
      orange_overlay = pygame.Surface(original.get_size()).convert_alpha()
      orange_overlay.fill((255, 140, 0, 0))  # Orange tint (explosive color)
      tinted.blit(orange_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

      # Add yellow highlight for extra visibility
      yellow_overlay = pygame.Surface(original.get_size()).convert_alpha()
      yellow_overlay.fill((200, 180, 0, 0))  # Yellow highlight
      tinted.blit(yellow_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

      # Save
      output_path = exploder_dir / f"{direction}.png"
      pygame.image.save(tinted, str(output_path))
      print(f"Created {output_path}")

  print("Exploder sprites created successfully!")
  ```
- **MIRROR**: Phase 2 runner sprite generation, Phase 3 tank sprite generation
- **RUN**:
  ```bash
  /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/.venv/bin/python zombie-shooter/create_exploder_sprites.py
  ```
- **VALIDATE**: Check files exist
  ```bash
  ls -la zombie-shooter/src/assets/zombies/exploder/
  ```
- **EXPECTED OUTPUT**: 4 sprite files (walk_down.png, walk_up.png, walk_left.png, walk_right.png)

### Task 5: CREATE `zombie-shooter/tests/test_exploder_variant.py`

- **ACTION**: CREATE integration tests for exploder variant behavior
- **IMPLEMENT**:
  ```python
  """Tests for exploder zombie variant."""

  from __future__ import annotations

  import pygame
  from unittest.mock import MagicMock

  from game.core.constants import ZOMBIE_VARIANTS, EXPLODER_EXPLOSION_RADIUS
  from game.entities.zombie import Zombie
  from game.scenes.play import PlayScene


  pygame.init()


  def test_exploder_variant_has_correct_stats() -> None:
      """Test that exploder zombie initializes with correct variant stats."""
      exploder = Zombie(pygame.Vector2(100, 100), variant="exploder")

      assert exploder.variant == "exploder"
      assert exploder.hp == 1  # One-shot kill
      assert exploder.speed == 140  # Normal speed
      assert exploder.radius == 16  # Normal hitbox


  def test_exploder_variant_dies_in_one_hit() -> None:
      """Test that exploder dies from single bullet hit."""
      exploder = Zombie(pygame.Vector2(100, 100), variant="exploder")

      exploder.hp -= 1  # Simulate bullet hit

      assert exploder.hp <= 0  # Dead


  def test_exploder_explosion_damages_nearby_zombies() -> None:
      """Test that explosion damages nearby zombies within radius."""
      game = MagicMock()
      scene = PlayScene(game)

      exploder = Zombie(pygame.Vector2(100, 100), variant="exploder")
      nearby = Zombie(pygame.Vector2(150, 100))  # 50px away (within 80px)
      far = Zombie(pygame.Vector2(300, 100))  # 200px away (outside 80px)

      scene.zombies.extend([exploder, nearby, far])

      # Kill exploder with bullet
      from game.entities.bullet import Bullet
      bullet = Bullet(pygame.Vector2(98, 98), pygame.Vector2(1, 0))
      scene.bullets.append(bullet)
      scene.update(0.01)

      # Nearby should take damage, far should not
      assert nearby.hp < 1  # Was damaged by explosion
      assert far.hp == 1  # Untouched


  def test_exploder_explosion_damages_player() -> None:
      """Test that explosion damages player if within radius."""
      game = MagicMock()
      scene = PlayScene(game)

      exploder = Zombie(pygame.Vector2(100, 100), variant="exploder")
      scene.zombies.append(exploder)

      # Move player close to exploder
      scene.player.pos = pygame.Vector2(150, 100)  # 50px away (within 80px)
      initial_hp = scene.player.hp

      # Kill exploder
      from game.entities.bullet import Bullet
      bullet = Bullet(pygame.Vector2(98, 98), pygame.Vector2(1, 0))
      scene.bullets.append(bullet)
      scene.update(0.01)

      # Player should take damage
      assert scene.player.hp < initial_hp


  def test_exploder_chain_reaction() -> None:
      """Test that exploding Exploder triggers nearby Exploders (chain reaction)."""
      game = MagicMock()
      scene = PlayScene(game)

      # Create two Exploders within explosion radius of each other
      exploder1 = Zombie(pygame.Vector2(100, 100), variant="exploder")
      exploder2 = Zombie(pygame.Vector2(150, 100), variant="exploder")  # 50px away
      normal = Zombie(pygame.Vector2(140, 100))  # Between them

      scene.zombies.extend([exploder1, exploder2, normal])

      # Kill first Exploder
      from game.entities.bullet import Bullet
      bullet = Bullet(pygame.Vector2(98, 98), pygame.Vector2(1, 0))
      scene.bullets.append(bullet)
      scene.update(0.01)

      # Both Exploders should be dead (chain reaction)
      # Normal zombie between them should take 2 damage (one from each explosion)
      assert exploder1.hp <= 0
      assert exploder2.hp <= 0
      assert normal.hp <= -1  # Took damage from both explosions


  def test_exploder_does_not_damage_far_zombies() -> None:
      """Test that explosion only affects zombies within radius."""
      game = MagicMock()
      scene = PlayScene(game)

      exploder = Zombie(pygame.Vector2(100, 100), variant="exploder")
      far_zombie = Zombie(pygame.Vector2(300, 300))  # ~283px away (outside 80px)

      scene.zombies.extend([exploder, far_zombie])

      # Kill Exploder
      from game.entities.bullet import Bullet
      bullet = Bullet(pygame.Vector2(98, 98), pygame.Vector2(1, 0))
      scene.bullets.append(bullet)
      scene.update(0.01)

      # Far zombie should be untouched
      assert far_zombie.hp == 1


  def test_exploder_spawns_enhanced_particles() -> None:
      """Test that Exploder death spawns more particles than normal death."""
      game = MagicMock()
      scene = PlayScene(game)

      exploder = Zombie(pygame.Vector2(100, 100), variant="exploder")
      scene.zombies.append(exploder)

      initial_particles = len(scene.blood_particles)

      # Kill Exploder
      from game.entities.bullet import Bullet
      bullet = Bullet(pygame.Vector2(98, 98), pygame.Vector2(1, 0))
      scene.bullets.append(bullet)
      scene.update(0.01)

      # Should have spawned explosion particles (16) + blood splash particles (8)
      # Total: 24 particles
      assert len(scene.blood_particles) > initial_particles + 16


  def test_exploder_variant_loads_unique_sprites() -> None:
      """Test that exploder loads variant-specific sprites."""
      exploder = Zombie(pygame.Vector2(100, 100), variant="exploder")

      # Should have sprites for all 4 directions
      assert "down" in exploder.sprites
      assert "up" in exploder.sprites
      assert "left" in exploder.sprites
      assert "right" in exploder.sprites

      # Each direction should have 3 frames
      for direction in ["down", "up", "left", "right"]:
          assert len(exploder.sprites[direction]) == 3


  def test_exploder_variant_constants_defined() -> None:
      """Test that exploder variant is properly defined in constants."""
      assert "exploder" in ZOMBIE_VARIANTS

      exploder_stats = ZOMBIE_VARIANTS["exploder"]
      assert exploder_stats["speed"] == 140
      assert exploder_stats["hp"] == 1
      assert exploder_stats["radius"] == 16
      assert exploder_stats["weight"] == 1.0  # 10% spawn rate
  ```
- **MIRROR**: `test_tank_variant.py` structure, `test_gore_integration.py` for PlayScene integration
- **IMPORTS**: Zombie, PlayScene, ZOMBIE_VARIANTS, MagicMock, Bullet
- **VALIDATE**:
  ```bash
  export PYTHONPATH="zombie-shooter/src" && /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/.venv/bin/python -m pytest zombie-shooter/tests/test_exploder_variant.py -v
  ```

---

## Testing Strategy

### Unit Tests to Write

| Test File                          | Test Cases                                                        | Validates                       |
| ---------------------------------- | ----------------------------------------------------------------- | ------------------------------- |
| `tests/test_exploder_variant.py`   | stats, one-hit death, AOE damage, chain reaction, sprites, radius | Exploder variant behavior       |

### Edge Cases Checklist

- [ ] Exploder spawns with correct stats (HP=1, speed=140, radius=16)
- [ ] Exploder dies in 1 bullet hit (HP=1→0)
- [ ] Explosion damages nearby zombies (within 80px) by 1 HP
- [ ] Explosion damages player (within 80px) by 10 HP
- [ ] Explosion does NOT damage far entities (outside 80px radius)
- [ ] Chain reactions work (Exploder kills Exploder recursively)
- [ ] Multiple Exploders can chain in sequence
- [ ] Normal death effects spawn (corpse, blood pool, blood splash)
- [ ] Enhanced explosion particles spawn (16 particles, faster)
- [ ] Exploder loads unique orange/yellow sprites
- [ ] Exploder spawns at 10% rate (weight=1.0)

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

**EXPECT**: All tests pass (109 existing + 10 new exploder tests = 119 total)

### Level 3: FULL_SUITE

```bash
export PYTHONPATH="zombie-shooter/src" && /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/.venv/bin/python -m pytest zombie-shooter/tests/ && /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/.venv/bin/python -m ruff check zombie-shooter/src/
```

**EXPECT**: All tests pass, linting passes, exit 0

### Level 4: MANUAL_VALIDATION

1. **Start game**: `python zombie-shooter/src/game/main.py`
2. **Verify exploder spawning**: Wait 10-15 seconds, look for slow orange/yellow zombies
3. **Verify explosion**:
   - Shoot exploder → large particle burst (16 particles, fast)
   - Check player HP decreases if standing close
   - Check nearby zombies take damage
4. **Verify chain reactions**:
   - Wait for 2-3 Exploders to cluster
   - Shoot one → watch cascade explosions
5. **Verify radius**: Explosion should affect ~80px radius (approx 2-3 zombie widths)
6. **Check performance**: Game maintains 60 FPS with explosions and chain reactions
7. **Visual distinction**: Orange/yellow color clearly distinguishes Exploder from other variants

---

## Acceptance Criteria

- [ ] All specified functionality implemented per user story
- [ ] Level 1-3 validation commands pass with exit 0
- [ ] Unit tests cover Exploder behavior (death, AOE, chain reactions)
- [ ] Code mirrors existing patterns (collision, particles, death handling)
- [ ] No regressions in existing tests (109/109 still pass + 10 new = 119/119)
- [ ] Exploder sprites created and loaded correctly (orange/yellow-tinted, 4 directions)
- [ ] Exploder spawns at 10% rate when enabled (weight=1.0)
- [ ] Explosion damages player (10 HP) if within 80px
- [ ] Explosion damages zombies (1 HP each) if within 80px
- [ ] Chain reactions work (Exploder kills trigger more Exploders)
- [ ] Enhanced explosion particle effect spawns (16 particles, 300px/s, 0.5s lifetime)
- [ ] Performance stable (60 FPS with multiple explosions)

---

## Completion Checklist

- [ ] Task 1: Constants updated (explosion params + exploder weight 0→1.0)
- [ ] Task 2: apply_explosion() method added to PlayScene
- [ ] Task 3: Death handler triggers explosion for Exploder variant
- [ ] Task 4: Exploder sprites created (orange/yellow-tinted, 4 directions)
- [ ] Task 5: Unit tests written and passing (10 tests)
- [ ] Level 1: Linting passes (ruff check)
- [ ] Level 2: Unit tests pass (pytest)
- [ ] Level 3: Full suite passes (tests + lint)
- [ ] Level 4: Manual validation passed (gameplay testing)
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk                                    | Likelihood | Impact | Mitigation                                                                          |
| --------------------------------------- | ---------- | ------ | ----------------------------------------------------------------------------------- |
| Chain reactions cause infinite loops    | LOW        | HIGH   | Zombies removed after all chain reactions complete, HP check prevents re-explosion  |
| Player gets killed by own explosion     | MEDIUM     | MEDIUM | Intentional risk/reward mechanic - player must maintain distance                    |
| Explosion radius too large/small        | MEDIUM     | MEDIUM | 80px tested in design (2-3 zombie widths), tunable in Phase 6 if needed            |
| Chain reactions cause performance drops | LOW        | MEDIUM | Recursive calls are depth-limited by zombie count, max ~50 zombies                  |
| Explosion particles obscure gameplay    | LOW        | LOW    | 16 particles with 0.5s lifetime clears quickly, not blocking                        |
| Orange tint not distinct enough         | LOW        | MEDIUM | Use orange (255, 140, 0) + yellow (200, 180, 0) composite for high visibility      |
| Exploder spawn rate feels unbalanced    | MEDIUM     | MEDIUM | 10% weight (1.0) is moderate, tune in Phase 6 if needed                            |

---

## Notes

**Design Decisions:**

1. **Explosion Damage: 10 HP (player), 1 HP (zombies)**: Player has 100 HP total, so 10 explosions = death. Creates meaningful risk. Zombies have 1-3 HP, so 1 damage is significant.

2. **Explosion Radius: 80px**: Approximately 2-3 zombie widths (16-24px radius each). Large enough for tactical impact, small enough to require positioning.

3. **Chain Reactions: Recursive**: When explosion kills an Exploder, it triggers immediately. Simple implementation, dramatic gameplay effect.

4. **Enhanced Particles: 16 (vs 8) at 300px/s (vs 150)**: Double particle count, double speed = visually distinct "explosion" vs "blood splash".

5. **Explosion Timing: Instant**: No delay between death and explosion. Explosion particles spawn alongside normal gore.

6. **Orange + Yellow Tint**: Composite tint creates "fiery/explosive" aesthetic. High contrast with green (normal/spitter), red (runner), blue (tank).

7. **10% Spawn Weight**: Matches Spitter (1.0). Balanced spawn mix: Normal=63.6%, Runner=13.6%, Tank=13.6%, Exploder=9.1%, Spitter=9.1%.

**Pattern Reuse:**

- Circle collision from `collisions.py` - proven efficient
- Particle spawn from `spawn_blood_splash()` - just modify counts/speed
- Death detection from `play.py:197` - inject 2 lines
- Sprite tinting from Phases 2 & 3 - exact same technique
- HP damage from acid projectile pattern - same `entity.hp -= amount`

**Why Phase 4 is MEDIUM Complexity:**

- New AOE system (zombie-to-zombie damage) - not just player damage
- Recursive chain reactions - requires careful implementation
- Enhanced particle effects - more particles, different parameters
- BUT: Reuses existing collision, HP, particle, death systems
- No new entity types, no new rendering systems

**Tactical Depth Created:**

1. **Risk/Reward Positioning**: Kill Exploder close = crowd clear but self-damage. Kill far = safe but less strategic value.
2. **Strategic Timing**: Wait for zombies to cluster around Exploder before killing it for maximum AOE value.
3. **Chain Reaction Mastery**: Position multiple Exploders to create cascading explosions.
4. **Emergency Crowd Control**: Low on ammo? Use Exploder to clear horde.
5. **Exploder Prioritization**: Kill Exploder early (prevent clusters) vs late (maximize AOE).

**Future Enhancements (Phase 6):**

- Warning pulse: 0.5s before explosion (optional visual feedback)
- Orange explosion particles: Custom particle class vs reusing blood particles
- Explosion radius indicator: Visual circle showing blast radius
- Explosion camera shake: Juice for dramatic effect
- Exploder fuse timer: Self-destruct after X seconds (alternative to death-only)

**Phase 4 → Phase 6 Transition:**

After Phase 4, Phase 6 (Polish & Balance) is unblocked. Phase 6 depends on Phases 2, 3, 4, 5 all being complete. Exploder completes the variant roster, ready for final tuning.
