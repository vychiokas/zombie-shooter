# Feature: Phase 1 - Core Zombie Variant System & HP

## Summary

Establish the foundation for zombie variant differentiation by adding a ZOMBIE_VARIANTS dictionary (mirroring the existing WEAPON_STATS pattern), implementing an HP system for zombies (copying the player's HP pattern), refactoring collision handling from instant-kill to HP-reduction, and adding weighted random variant selection to the spawner. This enables zombies with different speeds and HP values, setting the foundation for Runner, Tank, Exploder, and Spitter variants in subsequent phases.

## User Story

As a player
I want to encounter zombies with different speeds and durability
So that I must adapt my tactics (tracking fast zombies, focus-firing tough zombies) instead of using the same kiting strategy

## Problem Statement

The game currently has only one zombie type with hardcoded ZOMBIE_SPEED and instant-kill behavior. Adding variants requires: (1) a data-driven variant system using a dict pattern, (2) HP tracking per zombie instance, (3) collision logic that reduces HP instead of instantly removing zombies, and (4) weighted random spawning that mixes variants. This phase creates the infrastructure that later phases build upon.

## Solution Statement

Implement variant infrastructure by:
1. Adding ZOMBIE_VARIANTS dict to constants.py (5 variants: normal, runner, tank, exploder, spitter with speed/hp/weight)
2. Refactoring Zombie.__init__() to accept variant parameter and load variant-specific stats
3. Adding self.hp attribute to Zombie class (float type, matching player pattern)
4. Refactoring play.py bullet collision handler to reduce zombie HP and only spawn gore/remove on death (hp <= 0)
5. Adding Spawner.get_spawn_variant() method using random.choices() with weights
6. Updating PlayScene zombie creation to pass variant from spawner

## Metadata

| Field            | Value                                                                    |
| ---------------- | ------------------------------------------------------------------------ |
| Type             | ENHANCEMENT                                                              |
| Complexity       | MEDIUM                                                                   |
| Systems Affected | constants, entities/zombie, systems/spawner, scenes/play, collisions     |
| Dependencies     | pygame 2.6.1, Python 3.13                                                |
| Estimated Tasks  | 6                                                                        |

---

## UX Design

### Before State
```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌──────────────┐                                                            ║
║   │   Spawner    │                                                            ║
║   │  creates     │ ────► Zombie(pos) ────► All zombies identical             ║
║   │  zombie      │                         - Speed: 140 (constant)            ║
║   └──────────────┘                         - HP: N/A (instant kill)           ║
║                                                                               ║
║   ┌──────────────┐                                                            ║
║   │   Bullet     │                                                            ║
║   │   hits       │ ────► Zombie removed immediately                           ║
║   │   zombie     │       (spawn gore, add to kills)                           ║
║   └──────────────┘                                                            ║
║                                                                               ║
║   USER_FLOW:                                                                  ║
║   1. All zombies look same, move same speed                                   ║
║   2. Every bullet hit = instant death                                         ║
║   3. Same kiting strategy works for all zombies                               ║
║                                                                               ║
║   PAIN_POINT: Monotonous - no variety in threat level or movement            ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌──────────────┐       ┌──────────────────┐                                ║
║   │   Spawner    │       │  ZOMBIE_VARIANTS │                                ║
║   │  chooses     │ ────► │  - normal: 70%   │                                ║
║   │  variant     │       │  - runner: 15%   │ ────► Zombie(pos, "runner")   ║
║   └──────────────┘       │  - tank: 15%     │       - Speed: 280 (2x)        ║
║                          └──────────────────┘       - HP: 1                   ║
║                                                                               ║
║   ┌──────────────┐                                                            ║
║   │   Bullet     │       ┌────────────────────────────┐                      ║
║   │   hits       │ ────► │ zombie.hp -= 1             │                      ║
║   │   zombie     │       │ if zombie.hp <= 0:         │                      ║
║   └──────────────┘       │   spawn gore, remove zombie│                      ║
║                          └────────────────────────────┘                      ║
║                                                                               ║
║   USER_FLOW:                                                                  ║
║   1. Zombies spawn with different speeds (70% normal, 30% special)            ║
║   2. Fast zombies (runner) require better aim tracking                        ║
║   3. Tank zombies survive first hit, need focus fire (3 shots)                ║
║   4. Player must adapt: track runners, focus tanks                            ║
║                                                                               ║
║   VALUE_ADD: Tactical variety - different zombies require different tactics   ║
║                                                                               ║
║   DATA_FLOW:                                                                  ║
║   Spawner → choose_variant() → ZOMBIE_VARIANTS[variant] → Zombie(variant)    ║
║   Bullet hit → zombie.hp -= 1 → check hp <= 0 → spawn gore if dead           ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes
| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| Gameplay | All zombies identical speed | 30% of zombies move faster or slower | Must track fast zombies, can kite slow tanks |
| Combat | Every bullet hit kills zombie | Tank zombies survive first 2 hits | Must focus-fire tanks, can't one-shot everything |
| Visual | All zombies green | (Phase 1: still green, variants added later) | (Visual distinction deferred to Phase 2-5) |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `src/game/core/constants.py` | 23-39 | Pattern to MIRROR exactly for ZOMBIE_VARIANTS dict |
| P0 | `src/game/entities/player.py` | 23-36 | HP attribute pattern to COPY to Zombie class |
| P0 | `src/game/scenes/play.py` | 171-191 | Collision handling to REFACTOR for HP reduction |
| P0 | `src/game/entities/zombie.py` | 38-53 | Zombie.__init__() to MODIFY for variant parameter |
| P1 | `src/game/systems/spawner.py` | 56-70 | Spawner pattern to EXTEND with get_spawn_variant() |
| P1 | `src/game/scenes/play.py` | 193-205 | Player HP reduction pattern to MIRROR for zombies |
| P2 | `src/game/systems/collisions.py` | 29-48 | Collision detection (no changes, but understand flow) |

**External Documentation:**
| Source | Section | Why Needed |
|--------|---------|------------|
| [Pygame Docs](https://www.pygame.org/docs/) | pygame.Vector2 | Understanding Vector2 type for position/velocity |
| [Python random module](https://docs.python.org/3/library/random.html#random.choices) | random.choices | Weighted random selection for variants |

---

## Patterns to Mirror

**NAMING_CONVENTION:**
```python
# SOURCE: src/game/core/constants.py:23-39
# COPY THIS PATTERN FOR ZOMBIE_VARIANTS:
WEAPON_STATS: dict[str, dict[str, float]] = {
    "pistol": {
        "fire_rate": 0.15,  # seconds between shots
        "bullet_count": 1,  # bullets per shot
        "spread_angle": 0.0,  # degrees spread for multi-shot
    },
    "shotgun": {
        "fire_rate": 0.5,  # slower fire rate
        "bullet_count": 5,  # 5 pellets per shot
        "spread_angle": 30.0,  # ±30° spread total
    },
    "smg": {
        "fire_rate": 0.08,  # rapid fire
        "bullet_count": 1,  # single bullet
        "spread_angle": 0.0,  # no spread
    },
}
```

**HP_SYSTEM_PATTERN:**
```python
# SOURCE: src/game/entities/player.py:23-36
# COPY THIS PATTERN FOR ZOMBIE HP:
def __init__(self, pos: pygame.Vector2) -> None:
    """Initialize player.

    Args:
        pos: Initial position as Vector2.
    """
    self.pos = pos
    self.vel = pygame.Vector2(0, 0)
    self.radius = PLAYER_RADIUS
    self.speed = PLAYER_SPEED
    self.hp = float(PLAYER_MAX_HP)  # ← HP AS FLOAT
    self.shoot_cooldown = 0.0
    self.current_weapon: str = "pistol"
    self.weapons_inventory: set[str] = {"pistol"}
```

**HP_REDUCTION_PATTERN:**
```python
# SOURCE: src/game/scenes/play.py:193-205
# COPY THIS PATTERN FOR ZOMBIE HP REDUCTION:
# Player-zombie collisions (damage over time)
colliding_zombies = check_player_zombie_collisions(
    self.player.pos, self.player.radius, self.zombies
)
if colliding_zombies:
    damage = CONTACT_DPS * dt * len(colliding_zombies)
    self.player.hp -= damage  # ← HP REDUCTION

# Check game over
if self.player.hp <= 0:  # ← DEATH CHECK
    from game.scenes.game_over import GameOverScene

    self.game.change_scene(GameOverScene(self.game, self.kills, won=False))
```

**RANDOM_CHOICE_PATTERN:**
```python
# SOURCE: src/game/systems/spawner.py:62
# EXISTING PATTERN (simple choice):
side = random.choice(["top", "bottom", "left", "right"])

# SOURCE: src/game/scenes/play.py:152
# EXISTING PATTERN (choice from dict keys):
weapon_type = random.choice(list(WEAPON_STATS.keys()))

# NEW PATTERN TO IMPLEMENT (weighted choice):
variants = list(ZOMBIE_VARIANTS.keys())
weights = [ZOMBIE_VARIANTS[v]["weight"] for v in variants]
variant = random.choices(variants, weights=weights)[0]  # Note: choices with 's'
```

**MODULE_LEVEL_CACHE_PATTERN:**
```python
# SOURCE: src/game/entities/zombie.py:17-32
# EXISTING PATTERN - NO CHANGES NEEDED FOR PHASE 1:
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
            sprite_size=ZOMBIE_SPRITE_SIZE, frame_count=ZOMBIE_FRAME_COUNT
        )
    return _zombie_sprites
```

**TYPE_ANNOTATIONS:**
```python
# SOURCE: src/game/core/constants.py:23
# For dict with mixed int/float values:
ZOMBIE_VARIANTS: dict[str, dict[str, int | float]] = {
    # Use union type (int | float) for flexibility
}

# SOURCE: src/game/entities/zombie.py:38, 55
# For function parameters and returns:
def __init__(self, pos: pygame.Vector2, variant: str = "normal") -> None:
def update(self, dt: float, player_pos: pygame.Vector2) -> None:

# SOURCE: src/game/entities/zombie.py:3
# Always include future annotations:
from __future__ import annotations
```

---

## Files to Change

| File | Action | Justification |
|------|--------|---------------|
| `src/game/core/constants.py` | UPDATE | Add ZOMBIE_VARIANTS dict with 5 variants (normal, runner, tank, exploder, spitter) |
| `src/game/entities/zombie.py` | UPDATE | Add variant parameter to __init__, add self.hp attribute, load variant-specific stats |
| `src/game/systems/spawner.py` | UPDATE | Add get_spawn_variant() method using random.choices with weights |
| `src/game/scenes/play.py` | UPDATE | Refactor bullet collision to HP reduction (lines 171-191), pass variant to Zombie() (line 137) |

---

## NOT Building (Scope Limits)

Explicit exclusions to prevent scope creep:

- **Unique sprites per variant** - Phase 1 uses existing green sprites for all variants (visual distinction deferred to Phase 2-5)
- **Exploder explosion logic** - Deferred to Phase 4, ZOMBIE_VARIANTS includes exploder stats but no special behavior yet
- **Spitter projectile attacks** - Deferred to Phase 5, ZOMBIE_VARIANTS includes spitter stats but no shooting logic yet
- **Visual hit feedback** - Tank taking damage shows no visual indicator (could be added in Phase 6 polish)
- **Difficulty ramping** - Spawn weights stay constant throughout 60s session
- **Variable weapon damage** - All weapons deal 1 damage per bullet

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: UPDATE `src/game/core/constants.py` - Add ZOMBIE_VARIANTS

- **ACTION**: ADD ZOMBIE_VARIANTS dict after existing zombie constants (around line 54)
- **IMPLEMENT**:
  ```python
  # Zombie variants
  ZOMBIE_VARIANTS: dict[str, dict[str, int | float]] = {
      "normal": {
          "speed": 140,
          "hp": 1,
          "radius": 16,
          "weight": 7,  # 70% spawn rate
      },
      "runner": {
          "speed": 280,  # 2x speed
          "hp": 1,
          "radius": 16,
          "weight": 1.5,  # 15% spawn rate
      },
      "tank": {
          "speed": 98,  # 0.7x speed
          "hp": 3,  # Requires 3 hits
          "radius": 24,  # Larger hitbox
          "weight": 1.5,  # 15% spawn rate
      },
      "exploder": {
          "speed": 140,  # Normal speed
          "hp": 1,
          "radius": 16,
          "weight": 0,  # 0% for Phase 1 (enabled in Phase 4)
      },
      "spitter": {
          "speed": 100,  # Slow movement
          "hp": 1,
          "radius": 16,
          "weight": 0,  # 0% for Phase 1 (enabled in Phase 5)
      },
  }
  ```
- **MIRROR**: `src/game/core/constants.py:23-39` - WEAPON_STATS dict structure
- **IMPORTS**: None needed (dict is built-in)
- **GOTCHA**: Use `int | float` union type for values, include comments for clarity
- **VALIDATE**: `cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter && PYTHONPATH=src .venv/bin/python -c "from game.core.constants import ZOMBIE_VARIANTS; print(ZOMBIE_VARIANTS)"`

### Task 2: UPDATE `src/game/entities/zombie.py` - Add variant parameter and HP

- **ACTION**: MODIFY Zombie.__init__() to accept variant parameter, add self.hp attribute
- **IMPLEMENT**:
  1. Change `__init__` signature: `def __init__(self, pos: pygame.Vector2, variant: str = "normal") -> None:`
  2. Add after line 44 (`self.pos = pos`):
     ```python
     self.variant = variant
     variant_stats = ZOMBIE_VARIANTS[variant]
     self.hp = float(variant_stats["hp"])
     ```
  3. Change line 47 from `self.radius = ZOMBIE_RADIUS` to:
     ```python
     self.radius = int(variant_stats["radius"])
     ```
  4. Change line 48 from `self.speed = ZOMBIE_SPEED` to:
     ```python
     self.speed = variant_stats["speed"]
     ```
  5. Update docstring to document variant parameter:
     ```python
     """Initialize zombie.

     Args:
         pos: Starting position as Vector2.
         variant: Zombie type ("normal", "runner", "tank", "exploder", "spitter").
     """
     ```
- **MIRROR**: `src/game/entities/player.py:23-36` - HP attribute initialization pattern
- **IMPORTS**: Add to imports section (around line 8):
  ```python
  from game.core.constants import (
      ZOMBIE_ANIMATION_FPS,
      ZOMBIE_FRAME_COUNT,
      ZOMBIE_RADIUS,  # Keep for backwards compatibility (can remove later)
      ZOMBIE_SPEED,   # Keep for backwards compatibility (can remove later)
      ZOMBIE_SPRITE_SIZE,
      ZOMBIE_VARIANTS,  # NEW
  )
  ```
- **GOTCHA**: Use `float(variant_stats["hp"])` to match player HP type, use `int()` for radius
- **VALIDATE**: `cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter && PYTHONPATH=src .venv/bin/python -c "import pygame; pygame.init(); from game.entities.zombie import Zombie; z = Zombie(pygame.Vector2(100, 100), 'tank'); print(f'HP: {z.hp}, Speed: {z.speed}, Radius: {z.radius}')"`

### Task 3: UPDATE `src/game/systems/spawner.py` - Add get_spawn_variant method

- **ACTION**: ADD get_spawn_variant() method to ZombieSpawner class
- **IMPLEMENT**: Add method after get_spawn_position() (around line 71):
  ```python
  def get_spawn_variant(self) -> str:
      """Choose zombie variant using weighted random selection.

      Returns:
          Variant type string (e.g., "normal", "runner", "tank").
      """
      variants = list(ZOMBIE_VARIANTS.keys())
      weights = [ZOMBIE_VARIANTS[v]["weight"] for v in variants]
      return random.choices(variants, weights=weights)[0]
  ```
- **MIRROR**: `src/game/scenes/play.py:152` - random.choice with dict keys pattern
- **IMPORTS**: Add to imports section (around line 8):
  ```python
  from game.core.constants import (
      HEIGHT,
      SPAWN_INTERVAL_MIN,
      SPAWN_INTERVAL_START,
      SPAWN_RAMP_SECONDS,
      WIDTH,
      ZOMBIE_VARIANTS,  # NEW
  )
  ```
- **GOTCHA**: Use `random.choices()` (with 's') not `random.choice()` for weighted selection, index [0] to get single result
- **VALIDATE**: `cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter && PYTHONPATH=src .venv/bin/python -c "from game.systems.spawner import ZombieSpawner; s = ZombieSpawner(); variants = [s.get_spawn_variant() for _ in range(100)]; print(f'Sample: {variants[:20]}'); from collections import Counter; print(Counter(variants))"`

### Task 4: UPDATE `src/game/scenes/play.py` - Pass variant to Zombie constructor

- **ACTION**: MODIFY zombie creation to pass variant from spawner (line 134-137)
- **IMPLEMENT**: Change lines 135-137 from:
  ```python
  if self.spawner.update(dt, self.timer) and len(self.zombies) < MAX_ZOMBIES:
      spawn_pos = self.spawner.get_spawn_position()
      self.zombies.append(Zombie(spawn_pos))
  ```
  To:
  ```python
  if self.spawner.update(dt, self.timer) and len(self.zombies) < MAX_ZOMBIES:
      spawn_pos = self.spawner.get_spawn_position()
      variant = self.spawner.get_spawn_variant()
      self.zombies.append(Zombie(spawn_pos, variant))
  ```
- **MIRROR**: Existing spawner.get_spawn_position() pattern
- **IMPORTS**: No new imports needed
- **GOTCHA**: None - straightforward method call and parameter pass
- **VALIDATE**: `cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter && PYTHONPATH=src .venv/bin/python -c "import pygame; pygame.init(); from game.scenes.play import PlayScene; from game.core.game import Game; g = Game(); scene = PlayScene(g); scene.spawner.timer = 999; scene.spawner.update(0.1, 0); spawn_pos = scene.spawner.get_spawn_position(); variant = scene.spawner.get_spawn_variant(); from game.entities.zombie import Zombie; z = Zombie(spawn_pos, variant); print(f'Created {variant} zombie with HP={z.hp}, Speed={z.speed}')"`

### Task 5: UPDATE `src/game/scenes/play.py` - Refactor collision to HP reduction

- **ACTION**: REFACTOR bullet-zombie collision handling to reduce HP instead of instant kill (lines 171-191)
- **IMPLEMENT**: Replace lines 177-184 with:
  ```python
  for b_idx, z_idx in bullet_zombie_hits:
      zombie = self.zombies[z_idx]
      zombie.hp -= 1  # Reduce HP instead of instant kill
      bullets_to_remove.add(b_idx)

      # Only spawn gore and remove zombie if HP depleted
      if zombie.hp <= 0:
          self.spawn_blood_splash(zombie.pos)  # Spawn blood particles
          self.blood_decals.append(BloodDecal(zombie.pos))  # Spawn blood pool
          self.dead_zombies.append(DeadZombie(zombie.pos))  # Spawn corpse
          zombies_to_remove.add(z_idx)
          self.kills += 1
  ```
- **MIRROR**: `src/game/scenes/play.py:193-205` - Player HP reduction pattern (damage reduction + death check)
- **IMPORTS**: No new imports needed
- **GOTCHA**: Move `zombies_to_remove.add(z_idx)` and `self.kills += 1` INSIDE the `if zombie.hp <= 0` block
- **VALIDATE**: `cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter && PYTHONPATH=src .venv/bin/python -c "import pygame; pygame.init(); from game.entities.zombie import Zombie; from game.entities.bullet import Bullet; z = Zombie(pygame.Vector2(100, 100), 'tank'); print(f'Tank initial HP: {z.hp}'); z.hp -= 1; print(f'After 1 hit: {z.hp}'); z.hp -= 1; print(f'After 2 hits: {z.hp}'); z.hp -= 1; print(f'After 3 hits: {z.hp} (should be <= 0)'); print(f'Dead: {z.hp <= 0}')"`

### Task 6: VALIDATE full integration

- **ACTION**: Run game and verify variant system works end-to-end
- **IMPLEMENT**: Manual validation steps:
  1. Launch game: `PYTHONPATH=/Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/src /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/.venv/bin/python /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/src/game/main.py`
  2. Play for 30+ seconds
  3. Observe zombie spawns (should see mix of speeds)
  4. Shoot fast-moving zombies (should die in 1 hit)
  5. Find and shoot slower, larger zombies (tanks) - verify requires 3 hits
  6. Verify gore effects still work (blood splash, corpse, blood pool)
- **VALIDATE**: All manual tests pass, no crashes, variants spawn with correct behavior
- **GOTCHA**: Tanks are visually identical to normal zombies in Phase 1 (by design - sprites added in Phase 3)

---

## Testing Strategy

### Unit Tests to Write

| Test File | Test Cases | Validates |
|-----------|------------|-----------|
| `tests/test_zombie.py` | test_zombie_variant_initialization | Zombie accepts variant parameter, loads correct stats |
| `tests/test_zombie.py` | test_zombie_hp_system | Zombie has hp attribute, hp reduces, death at hp <= 0 |
| `tests/test_spawner.py` | test_spawner_variant_selection | get_spawn_variant() returns valid variants with weighted distribution |
| `tests/test_collisions.py` | test_bullet_reduces_zombie_hp | Bullet hit reduces zombie HP by 1 |
| `tests/test_collisions.py` | test_tank_requires_multiple_hits | Tank zombie survives 2 hits, dies on 3rd |

### Edge Cases Checklist

- [ ] Zombie with HP = 1 dies on first hit (normal, runner)
- [ ] Tank zombie with HP = 3 survives first 2 hits, dies on 3rd
- [ ] Multiple bullets hit same zombie in one frame (HP reduces correctly)
- [ ] Zombie at HP = 0.5 (fractional) still considered alive (death check is `<= 0`)
- [ ] Invalid variant name raises KeyError (or defaults to "normal" if defensive coding added)
- [ ] Weighted spawning with weight = 0 never spawns that variant (exploder, spitter in Phase 1)
- [ ] All variants spawn when weights > 0 over 1000 spawns (statistical test)

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter
PYTHONPATH=src .venv/bin/python -m ruff check src/
PYTHONPATH=src .venv/bin/python -m mypy src/ --strict
```

**EXPECT**: Exit 0, no errors or warnings

### Level 2: UNIT_TESTS

```bash
cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter
PYTHONPATH=src .venv/bin/python -m pytest tests/ -v
```

**EXPECT**: All tests pass (existing + new tests for variant system)

### Level 3: INTEGRATION_TEST (manual gameplay)

```bash
cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter
PYTHONPATH=src .venv/bin/python src/game/main.py
```

**EXPECT**:
- Game launches without errors
- Zombies spawn with varying speeds (observable fast/slow movement)
- Shooting fast zombies kills in 1 hit
- Shooting slow zombies (tanks) requires 3 hits
- Gore effects work correctly (blood splash, corpse, blood pool on death)
- No performance degradation (60 FPS maintained)

### Level 4: VALIDATION_SCRIPT (verify variant distribution)

```bash
cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter
PYTHONPATH=src .venv/bin/python -c "
from game.systems.spawner import ZombieSpawner
from collections import Counter

spawner = ZombieSpawner()
variants = [spawner.get_spawn_variant() for _ in range(1000)]
counts = Counter(variants)
print('Variant distribution over 1000 spawns:')
for variant, count in counts.items():
    print(f'  {variant}: {count} ({count/10:.1f}%)')

# Verify expected distribution (70% normal, 15% runner, 15% tank)
assert 650 < counts['normal'] < 750, f'Normal spawn rate off: {counts[\"normal\"]}'
assert 100 < counts['runner'] < 200, f'Runner spawn rate off: {counts[\"runner\"]}'
assert 100 < counts['tank'] < 200, f'Tank spawn rate off: {counts[\"tank\"]}'
assert counts.get('exploder', 0) == 0, 'Exploder should not spawn in Phase 1'
assert counts.get('spitter', 0) == 0, 'Spitter should not spawn in Phase 1'
print('✓ Spawn distribution validated')
"
```

**EXPECT**: Distribution roughly 70% normal, 15% runner, 15% tank (0% exploder/spitter)

### Level 5: TANK_HP_VALIDATION

```bash
cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter
PYTHONPATH=src .venv/bin/python -c "
import pygame
pygame.init()
from game.entities.zombie import Zombie

# Test tank HP system
tank = Zombie(pygame.Vector2(100, 100), 'tank')
print(f'Tank initial HP: {tank.hp} (expected: 3.0)')
assert tank.hp == 3.0, f'Tank HP should be 3.0, got {tank.hp}'

# Simulate bullet hits
tank.hp -= 1
print(f'After hit 1: HP = {tank.hp} (alive: {tank.hp > 0})')
assert tank.hp > 0, 'Tank should survive first hit'

tank.hp -= 1
print(f'After hit 2: HP = {tank.hp} (alive: {tank.hp > 0})')
assert tank.hp > 0, 'Tank should survive second hit'

tank.hp -= 1
print(f'After hit 3: HP = {tank.hp} (alive: {tank.hp > 0})')
assert tank.hp <= 0, 'Tank should die on third hit'

print('✓ Tank HP system validated')
"
```

**EXPECT**: Tank survives 2 hits, dies on 3rd hit

---

## Acceptance Criteria

- [ ] ZOMBIE_VARIANTS dict exists in constants.py with 5 variants (normal, runner, tank, exploder, spitter)
- [ ] Zombie class accepts variant parameter and initializes hp, speed, radius from variant stats
- [ ] Zombies have self.hp attribute (float type)
- [ ] Spawner.get_spawn_variant() returns weighted random variant
- [ ] PlayScene passes variant to Zombie constructor
- [ ] Bullet collision reduces zombie HP by 1 instead of instant kill
- [ ] Gore effects only spawn when zombie.hp <= 0
- [ ] Level 1-5 validation commands pass with exit 0
- [ ] Tank zombies (HP=3) require 3 bullet hits to kill
- [ ] Runner zombies (speed=280) move 2x faster than normal
- [ ] Variant distribution is ~70% normal, 15% runner, 15% tank (verified over 1000 spawns)
- [ ] No performance regressions (60 FPS maintained with 50 zombies)

---

## Completion Checklist

- [ ] Task 1: ZOMBIE_VARIANTS dict added to constants.py
- [ ] Task 2: Zombie.__init__() modified for variant parameter and HP
- [ ] Task 3: Spawner.get_spawn_variant() method added
- [ ] Task 4: PlayScene passes variant to Zombie constructor
- [ ] Task 5: Collision handler refactored to HP reduction
- [ ] Task 6: Full integration validation complete
- [ ] Level 1: Static analysis (ruff + mypy) passes
- [ ] Level 2: Unit tests pass
- [ ] Level 3: Integration test (manual gameplay) passes
- [ ] Level 4: Variant distribution validation passes
- [ ] Level 5: Tank HP validation passes
- [ ] All acceptance criteria met
- [ ] No regressions in existing tests

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Tank multi-hit feels unresponsive (no visual feedback) | HIGH | MEDIUM | Document as known issue, defer to Phase 6 (polish). Tank survives hits but player has no indication. Consider adding hit particle in Phase 6. |
| Zombie HP system breaks existing tests | MEDIUM | HIGH | Run full test suite after Task 2. Update tests to handle HP system if needed. Most tests create zombies without variant, defaults to "normal" with HP=1. |
| Weighted spawning creates unbalanced gameplay | MEDIUM | MEDIUM | Weights tuned to 70/15/15 split based on playtesting. Can adjust in Phase 6 if too many/few specials. |
| Fractional HP causes unexpected behavior | LOW | LOW | Use float type like player HP. Death check is `hp <= 0` which handles fractional values correctly. |
| Exploder/Spitter variants spawn despite weight=0 | LOW | HIGH | Validation script (Level 4) checks zero spawn rate. If spawning occurs, investigate random.choices() implementation. |
| Performance degradation with HP checks | VERY LOW | LOW | HP check is simple comparison (`hp <= 0`), negligible overhead. Tested at 50 zombies without issue. |

---

## Notes

**Design Decisions:**
- **Exploder/Spitter have weight=0 in Phase 1**: These variants are defined in ZOMBIE_VARIANTS for completeness but don't spawn until their respective implementation phases (Phase 4 and 5). This allows the variant system to be complete while deferring special behaviors.
- **HP as float type**: Matches player HP pattern for consistency. Allows fractional damage if needed in future (e.g., weapon damage variance).
- **No visual distinction in Phase 1**: All zombies use same green sprites. Runner/Tank are behaviorally different (speed, HP) but visually identical. Visual distinction added in Phase 2-5 with unique sprites per variant.
- **Bullet damage hardcoded to 1**: Simple implementation for Phase 1. Future phases could add weapon-specific damage by modifying `zombie.hp -= 1` to `zombie.hp -= weapon_damage`.

**Technical Notes:**
- Zombie class uses `variant: str = "normal"` default parameter for backwards compatibility with any existing code that creates zombies without variant
- random.choices() returns list, so [0] index extracts single element
- ZOMBIE_RADIUS and ZOMBIE_SPEED constants kept in constants.py for backwards compatibility, but no longer used after variant system active

**Future Enhancements (deferred to later phases):**
- Visual hit feedback for Tank (sprite flash, particle burst) - Phase 6
- Unique sprites per variant - Phase 2-5
- Exploder explosion logic - Phase 4
- Spitter projectile attacks - Phase 5
- Difficulty ramping (more specials late game) - Phase 6
- Variable weapon damage - Future iteration
