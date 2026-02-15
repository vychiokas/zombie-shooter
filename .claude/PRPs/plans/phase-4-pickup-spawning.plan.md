# Feature: Phase 4 - Pickup Spawning

## Summary

Integrate weapon pickups into the main gameplay loop by adding timer-based spawning to PlayScene, player-pickup collision detection, and weapon swapping on collection. Pickups spawn every ~15 seconds at random interior positions (avoiding screen edges), players collect them by touching, and the current weapon changes instantly. This phase brings the pickup system to life by making pickups appear automatically and be collectible during gameplay.

## User Story

As a player
I want weapon pickups to appear automatically during gameplay
So that I can collect them to change my weapon and vary my combat strategy

## Problem Statement

The Pickup entity exists (Phase 2 complete) but is not integrated into the game. Players have no way to encounter pickups during gameplay because they never spawn, and there's no collision detection to collect them. The weapon system data model exists (Phase 1) but the player can't change weapons during a game session.

## Solution Statement

Add a countdown timer (`pickup_spawn_timer`) to PlayScene that triggers every PICKUP_SPAWN_RATE seconds to spawn a random weapon pickup at a safe interior position. Implement `check_player_pickup_collisions()` in the collisions module following the existing player-zombie collision pattern. On collision, set `player.current_weapon` to the pickup's weapon type and remove the pickup from the scene. This completes the pickup gameplay loop: spawn → player sees → player navigates → player collects → weapon changes.

## Metadata

| Field            | Value                              |
| ---------------- | ---------------------------------- |
| Type             | NEW_CAPABILITY                     |
| Complexity       | MEDIUM                             |
| Systems Affected | PlayScene (main game loop), collision system |
| Dependencies     | pygame>=2.6.0, Phase 1 (WEAPON_STATS, player.current_weapon), Phase 2 (Pickup class) |
| Estimated Tasks  | 6                                  |

---

## UX Design

### Before State
```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌──────────┐                                                                ║
║   │  Player  │  ◄── shoots, moves, avoids zombies                             ║
║   │ (pistol) │      current_weapon = "pistol" (never changes)                 ║
║   └──────────┘                                                                ║
║        ▲                                                                      ║
║        │                                                                      ║
║   ┌──────────┐                                                                ║
║   │ Zombies  │  ◄── spawn automatically, seek player                          ║
║   └──────────┘                                                                ║
║                                                                               ║
║   ┌──────────┐                                                                ║
║   │ Pickups  │  ◄── exist as entity class but NEVER APPEAR                    ║
║   │ (Phase 2)│                                                                ║
║   └──────────┘                                                                ║
║                                                                               ║
║   PAIN_POINT:                                                                 ║
║   - Pickups never spawn during gameplay                                       ║
║   - No collision detection for pickup collection                              ║
║   - Player stuck with pistol for entire 60-second session                     ║
║   - Weapon variety system exists but is unused                                ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌──────────┐         ┌──────────┐                                           ║
║   │  Player  │ ──────► │ Pickups  │  ◄── Spawn every ~15s                     ║
║   │          │  touch  │          │      Random positions                     ║
║   └──────────┘         └──────────┘      3 weapon types                       ║
║        │                     │                                                ║
║        │  collects pickup    │                                                ║
║        └─────────────────────┘                                                ║
║                  │                                                            ║
║                  ▼                                                            ║
║        player.current_weapon changes                                          ║
║        "pistol" → "shotgun" → "smg"                                           ║
║                                                                               ║
║   USER_FLOW:                                                                  ║
║   1. Timer counts down: pickup_spawn_timer -= dt                              ║
║   2. When timer reaches 0: spawn pickup at random position                    ║
║   3. Pickup rendered on screen (colored rectangle)                            ║
║   4. Player sees pickup, navigates toward it                                  ║
║   5. Player touches pickup: collision detected                                ║
║   6. player.current_weapon = pickup.weapon_type                               ║
║   7. Pickup removed from scene                                                ║
║   8. Timer resets to 15s for next spawn                                       ║
║                                                                               ║
║   VALUE_ADD:                                                                  ║
║   - Dynamic weapon changes during gameplay                                    ║
║   - Strategic decisions: risk going for pickup vs. staying safe               ║
║   - Varied combat encounters based on available weapons                       ║
║   - Pickups appear predictably (~15s) but at unpredictable positions          ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes
| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| Gameplay map | No pickups appear | Pickups spawn every ~15s at random positions | Can see collectible weapons |
| Player movement | Only dodge zombies | Navigate to pickups while dodging zombies | Strategic positioning |
| Weapon state | Stuck with pistol | Changes when collecting pickups | Dynamic combat variety |
| Collision | Only bullets/zombies | Player-pickup detection added | Can collect pickups by touch |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `zombie-shooter/src/game/scenes/play.py` | 33-46, 60-119 | Pattern to MIRROR - __init__ lists, update() loop structure, collision handling |
| P0 | `zombie-shooter/src/game/systems/spawner.py` | 25-70 | Timer-based spawning pattern, position generation |
| P0 | `zombie-shooter/src/game/systems/collisions.py` | 51-68 | Player collision pattern to FOLLOW for pickups |
| P1 | `zombie-shooter/src/game/entities/pickup.py` | 13-23 | Pickup constructor and interface |
| P1 | `zombie-shooter/src/game/core/constants.py` | 23-44 | WEAPON_STATS keys, PICKUP_SPAWN_RATE, screen dimensions |

**External Documentation:**
| Source | Section | Why Needed |
|--------|---------|------------|
| [Python random module](https://docs.python.org/3/library/random.html) | random.choice(), random.uniform() | Selecting random weapons and spawn positions |

---

## Patterns to Mirror

### PLAYSCENE_INITIALIZATION - Entity Lists

**SOURCE:** `zombie-shooter/src/game/scenes/play.py:33-46`

**COPY THIS PATTERN:**
```python
def __init__(self, game: Game) -> None:
    """Initialize play scene.

    Args:
        game: Game instance for scene switching.
    """
    self.game = game
    self.player = Player(pygame.Vector2(WIDTH / 2, HEIGHT / 2))
    self.bullets: list[Bullet] = []
    self.zombies: list[Zombie] = []
    self.spawner = ZombieSpawner()
    self.timer = 0.0
    self.kills = 0
    self.font = pygame.font.Font(None, 36)
```

**Phase 4 applies:**
- Add `self.pickups: list[Pickup] = []` after zombies list
- Add `self.pickup_spawn_timer: float = PICKUP_SPAWN_RATE` after spawner
- Import Pickup from entities, PICKUP_SPAWN_RATE from constants

---

### TIMER_BASED_SPAWNING - Countdown Pattern

**SOURCE:** `zombie-shooter/src/game/systems/spawner.py:25-39`

**COPY THIS PATTERN:**
```python
def update(self, dt: float, elapsed_time: float) -> bool:
    """Update spawn timer.

    Args:
        dt: Delta time in seconds.
        elapsed_time: Total time elapsed in game.

    Returns:
        True when ready to spawn a zombie, False otherwise.
    """
    self.spawn_timer -= dt
    if self.spawn_timer <= 0:
        self.spawn_timer = self.get_spawn_interval(elapsed_time)
        return True
    return False
```

**Phase 4 applies in PlayScene.update():**
```python
# Spawn pickups on timer
self.pickup_spawn_timer -= dt
if self.pickup_spawn_timer <= 0:
    self.pickup_spawn_timer = PICKUP_SPAWN_RATE  # Reset to 15.0
    # Spawn pickup logic here
```

---

### COLLISION_DETECTION - Player Collision Function

**SOURCE:** `zombie-shooter/src/game/systems/collisions.py:51-68`

**COPY THIS PATTERN:**
```python
def check_player_zombie_collisions(
    player_pos: pygame.Vector2, player_radius: float, zombies: list
) -> list[int]:
    """Check player-zombie collisions.

    Args:
        player_pos: Player position.
        player_radius: Player collision radius.
        zombies: List of zombie entities.

    Returns:
        List of zombie indices that are colliding with player.
    """
    colliding = []
    for z_idx, zombie in enumerate(zombies):
        if check_collision_circle(
            player_pos, player_radius, zombie.pos, zombie.radius
        ):
            colliding.append(z_idx)
    return colliding
```

**Phase 4 applies - create similar function:**
```python
def check_player_pickup_collisions(
    player_pos: pygame.Vector2, player_radius: float, pickups: list
) -> list[int]:
    """Check player-pickup collisions.

    Args:
        player_pos: Player position.
        player_radius: Player collision radius.
        pickups: List of pickup entities.

    Returns:
        List of pickup indices that are colliding with player.
    """
    colliding = []
    for p_idx, pickup in enumerate(pickups):
        if check_collision_circle(
            player_pos, player_radius, pickup.pos, pickup.radius
        ):
            colliding.append(p_idx)
    return colliding
```

---

### ENTITY_LIST_MANAGEMENT - TTL Filtering

**SOURCE:** `zombie-shooter/src/game/scenes/play.py:77-78`

**COPY THIS PATTERN:**
```python
# Update bullets and remove dead ones
self.bullets = [b for b in self.bullets if b.update(dt)]
```

**Phase 4 applies:**
```python
# Update pickups and remove expired ones (TTL-based)
self.pickups = [p for p in self.pickups if p.update(dt)]
```

---

### COLLISION_REMOVAL - Set-Based Index Removal

**SOURCE:** `zombie-shooter/src/game/scenes/play.py:90-105`

**COPY THIS PATTERN:**
```python
bullet_zombie_hits = check_bullet_zombie_collisions(self.bullets, self.zombies)

# Remove hit bullets and zombies (reverse order to avoid index issues)
bullets_to_remove = set()
zombies_to_remove = set()
for b_idx, z_idx in bullet_zombie_hits:
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

**Phase 4 applies:**
```python
colliding_pickups = check_player_pickup_collisions(
    self.player.pos, self.player.radius, self.pickups
)

# Handle pickup collection
pickup_indices_to_remove = set()
for p_idx in colliding_pickups:
    self.player.current_weapon = self.pickups[p_idx].weapon_type
    pickup_indices_to_remove.add(p_idx)

self.pickups = [
    p for i, p in enumerate(self.pickups) if i not in pickup_indices_to_remove
]
```

---

### RANDOM_POSITION_GENERATION - Interior Spawn

**SOURCE:** Adapted from `zombie-shooter/src/game/systems/spawner.py:56-70` (edge spawn) to interior spawn

**ADAPT THIS PATTERN:**
```python
# Zombies spawn at EDGES (top/bottom/left/right)
side = random.choice(["top", "bottom", "left", "right"])
if side == "top":
    return pygame.Vector2(random.uniform(0, WIDTH), 0)
```

**Phase 4 adapts to INTERIOR spawn with margin:**
```python
# Pickups spawn INSIDE screen with margin from edges
PICKUP_SPAWN_MARGIN = 100  # pixels buffer from edge
spawn_pos = pygame.Vector2(
    random.uniform(PICKUP_SPAWN_MARGIN, WIDTH - PICKUP_SPAWN_MARGIN),
    random.uniform(PICKUP_SPAWN_MARGIN, HEIGHT - PICKUP_SPAWN_MARGIN),
)
```

---

### DRAWING_LOOP - Entity Rendering

**SOURCE:** `zombie-shooter/src/game/scenes/play.py:130-141`

**COPY THIS PATTERN:**
```python
# Draw bullets
for bullet in self.bullets:
    bullet.draw(screen)

# Draw zombies
for zombie in self.zombies:
    zombie.draw(screen)
```

**Phase 4 applies:**
```python
# Draw pickups (after zombies, before HUD)
for pickup in self.pickups:
    pickup.draw(screen)
```

---

## Files to Change

| File                             | Action | Justification                            |
| -------------------------------- | ------ | ---------------------------------------- |
| `zombie-shooter/src/game/core/constants.py` | UPDATE | Add PICKUP_SPAWN_MARGIN constant (100 pixels) |
| `zombie-shooter/src/game/systems/collisions.py` | UPDATE | Add check_player_pickup_collisions() function |
| `zombie-shooter/src/game/scenes/play.py` | UPDATE | Add pickup spawning, collision, and rendering logic |
| `zombie-shooter/tests/test_pickup_spawning.py` | CREATE | Integration tests for pickup spawning system |

---

## NOT Building (Scope Limits)

Explicit exclusions to prevent scope creep:

- **Weapon behavior changes** - Phase 3 will modify Player.shoot() to use WEAPON_STATS. Phase 4 only changes current_weapon string.
- **HUD weapon display** - Phase 5 will render weapon name to screen. Phase 4 just swaps the internal state.
- **Pickup spawn on zombie kill** - PRD specified timer-based spawning (~15s). Kill-based spawning deferred.
- **Pickup selection UI** - Automatic weapon swap on contact (no "press E to pick up" prompt).
- **Multiple pickups of same type** - If player already has weapon, still swaps (no "already equipped" check).

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: UPDATE `zombie-shooter/src/game/core/constants.py`

**ACTION**: ADD PICKUP_SPAWN_MARGIN constant

**IMPLEMENT**:
Add after PICKUP_TTL (line 44):
```python
PICKUP_SPAWN_MARGIN = 100  # pixels buffer from screen edge for safe spawn area
```

**MIRROR**: `constants.py:16-20` - constant naming and inline comment pattern

**IMPORTS**: None needed

**GOTCHA**:
- Use int value (100 not 100.0) since it's a pixel measurement
- Place in "# Pickups" section for logical grouping

**VALIDATE**:
```bash
python -m py_compile zombie-shooter/src/game/core/constants.py
```
Expected: No output (successful compilation)

---

### Task 2: UPDATE `zombie-shooter/src/game/systems/collisions.py`

**ACTION**: ADD check_player_pickup_collisions() function

**IMPLEMENT**:
Add after check_player_zombie_collisions (after line 68):
```python


def check_player_pickup_collisions(
    player_pos: pygame.Vector2, player_radius: float, pickups: list
) -> list[int]:
    """Check player-pickup collisions.

    Args:
        player_pos: Player position.
        player_radius: Player collision radius.
        pickups: List of pickup entities.

    Returns:
        List of pickup indices that are colliding with player.
    """
    colliding = []
    for p_idx, pickup in enumerate(pickups):
        if check_collision_circle(
            player_pos, player_radius, pickup.pos, pickup.radius
        ):
            colliding.append(p_idx)
    return colliding
```

**MIRROR**: `collisions.py:51-68` - check_player_zombie_collisions pattern exactly

**IMPORTS**: None needed (check_collision_circle already imported)

**GOTCHA**:
- Use same parameter names and docstring style
- Return list of indices (not pickup objects)
- Use enumerate() for index tracking

**VALIDATE**:
```bash
python -m py_compile zombie-shooter/src/game/systems/collisions.py && zombie-shooter/.venv/bin/ruff check zombie-shooter/src/game/systems/collisions.py
```
Expected: Compilation succeeds, ruff passes

---

### Task 3: UPDATE `zombie-shooter/src/game/scenes/play.py` - Imports

**ACTION**: ADD imports for Pickup, random, and new constants

**IMPLEMENT**:
Update imports section (lines 3-18):
```python
"""Play scene for zombie shooter game."""

from __future__ import annotations

import random  # ADD THIS LINE

import pygame

from game.core.constants import (
    CONTACT_DPS,
    HEIGHT,
    MAX_ZOMBIES,
    PICKUP_SPAWN_MARGIN,  # ADD THIS LINE
    PICKUP_SPAWN_RATE,    # ADD THIS LINE
    SURVIVE_SECONDS,
    WEAPON_STATS,         # ADD THIS LINE
    WIDTH,
)
from game.core.game import Game
from game.core.scene import Scene
from game.entities.bullet import Bullet
from game.entities.pickup import Pickup  # ADD THIS LINE
from game.entities.player import Player
from game.entities.zombie import Zombie
from game.systems.collisions import (
    check_bullet_zombie_collisions,
    check_player_pickup_collisions,  # ADD THIS LINE
    check_player_zombie_collisions,
)
from game.systems.spawner import ZombieSpawner
```

**MIRROR**: Existing import structure - alphabetical within groups

**GOTCHA**:
- Import `random` at top level (standard library)
- Add constants in alphabetical order within constants group
- Add Pickup after Bullet in entities group

**VALIDATE**:
```bash
python -m py_compile zombie-shooter/src/game/scenes/play.py
```
Expected: No output (successful compilation)

---

### Task 4: UPDATE `zombie-shooter/src/game/scenes/play.py` - __init__

**ACTION**: ADD pickups list and spawn timer to PlayScene initialization

**IMPLEMENT**:
In `__init__` method, add after line 43 (self.spawner):
```python
    self.pickups: list[Pickup] = []
    self.pickup_spawn_timer: float = PICKUP_SPAWN_RATE
```

**MIRROR**: `play.py:41-43` - entity list and timer initialization pattern

**GOTCHA**:
- Place after zombies list for logical grouping (all entity lists together)
- Use type hints: `list[Pickup]` and `float`
- Initialize timer to PICKUP_SPAWN_RATE (spawns first pickup after 15s)

**VALIDATE**:
```bash
python -m py_compile zombie-shooter/src/game/scenes/play.py && zombie-shooter/.venv/bin/ruff check zombie-shooter/src/game/scenes/play.py
```
Expected: Compilation and lint pass

---

### Task 5: UPDATE `zombie-shooter/src/game/scenes/play.py` - update() method

**ACTION**: ADD pickup spawning, collision, and collection logic to update loop

**IMPLEMENT**:
In `update()` method, add AFTER zombie collision handling (after line 113), BEFORE lose condition check (before line 115):

```python
        # Update pickups and remove expired ones (TTL-based)
        self.pickups = [p for p in self.pickups if p.update(dt)]

        # Spawn pickups on timer
        self.pickup_spawn_timer -= dt
        if self.pickup_spawn_timer <= 0:
            self.pickup_spawn_timer = PICKUP_SPAWN_RATE
            weapon_choice = random.choice(list(WEAPON_STATS.keys()))
            spawn_pos = pygame.Vector2(
                random.uniform(PICKUP_SPAWN_MARGIN, WIDTH - PICKUP_SPAWN_MARGIN),
                random.uniform(PICKUP_SPAWN_MARGIN, HEIGHT - PICKUP_SPAWN_MARGIN),
            )
            self.pickups.append(Pickup(spawn_pos, weapon_choice))

        # Check player-pickup collisions
        colliding_pickups = check_player_pickup_collisions(
            self.player.pos, self.player.radius, self.pickups
        )

        # Handle pickup collection
        pickup_indices_to_remove = set()
        for p_idx in colliding_pickups:
            self.player.current_weapon = self.pickups[p_idx].weapon_type
            pickup_indices_to_remove.add(p_idx)

        self.pickups = [
            p for i, p in enumerate(self.pickups) if i not in pickup_indices_to_remove
        ]
```

**MIRROR**:
- Line ~78: Pickup update follows bullet update pattern
- Lines 80-83: Timer spawning follows zombie spawner pattern
- Lines 90-105: Collision removal follows bullet-zombie pattern

**GOTCHA**:
- Call `list(WEAPON_STATS.keys())` - random.choice needs list, not dict_keys
- Use `random.uniform()` for float positions, not `random.randint()`
- Pass `spawn_pos` to Pickup constructor, not create inline
- Set `player.current_weapon` BEFORE removing pickup (index still valid)
- Use set-based removal to handle multiple simultaneous pickups

**VALIDATE**:
```bash
python -m py_compile zombie-shooter/src/game/scenes/play.py && zombie-shooter/.venv/bin/ruff check zombie-shooter/src/game/scenes/play.py
```
Expected: Compilation and lint pass

---

### Task 6: UPDATE `zombie-shooter/src/game/scenes/play.py` - draw() method

**ACTION**: ADD pickup rendering to draw loop

**IMPLEMENT**:
In `draw()` method, add AFTER zombie drawing (after line 141), BEFORE HUD rendering (before line 143):

```python
        # Draw pickups
        for pickup in self.pickups:
            pickup.draw(screen)
```

**MIRROR**: `play.py:130-141` - entity drawing loop pattern

**GOTCHA**:
- Place AFTER zombies so pickups render on top
- Place BEFORE HUD so text always appears over pickups
- Simple for-loop, no list comprehension needed

**VALIDATE**:
```bash
python -m py_compile zombie-shooter/src/game/scenes/play.py && zombie-shooter/.venv/bin/ruff check zombie-shooter/src/game/scenes/play.py
```
Expected: Compilation and lint pass

---

### Task 7: CREATE `zombie-shooter/tests/test_pickup_spawning.py`

**ACTION**: CREATE integration tests for pickup spawning system

**IMPLEMENT**:
```python
"""Integration tests for pickup spawning and collection."""

from __future__ import annotations

import pygame

from game.core.constants import PICKUP_SPAWN_RATE, WEAPON_STATS
from game.entities.pickup import Pickup
from game.scenes.play import PlayScene
from game.systems.collisions import check_player_pickup_collisions


def test_pickup_spawn_timer_initialization() -> None:
    """Test that pickup spawn timer is initialized correctly."""
    pygame.init()
    from game.core.game import Game

    game = Game()
    scene = PlayScene(game)

    assert scene.pickup_spawn_timer == PICKUP_SPAWN_RATE
    assert scene.pickups == []


def test_pickup_spawns_after_timer() -> None:
    """Test that pickup spawns when timer expires."""
    pygame.init()
    from game.core.game import Game

    game = Game()
    scene = PlayScene(game)

    # Fast-forward timer beyond spawn rate
    scene.pickup_spawn_timer = 0.1
    scene.update(0.2)  # dt > timer, should spawn

    assert len(scene.pickups) == 1
    assert scene.pickups[0].weapon_type in WEAPON_STATS


def test_pickup_spawn_timer_resets() -> None:
    """Test that timer resets after spawning."""
    pygame.init()
    from game.core.game import Game

    game = Game()
    scene = PlayScene(game)

    scene.pickup_spawn_timer = 0.1
    scene.update(0.2)

    # Timer should reset to PICKUP_SPAWN_RATE
    assert scene.pickup_spawn_timer == PICKUP_SPAWN_RATE


def test_player_pickup_collision_detection() -> None:
    """Test that player-pickup collisions are detected."""
    player_pos = pygame.Vector2(100, 100)
    player_radius = 18

    # Pickup at same position (should collide)
    pickup1 = Pickup(pygame.Vector2(100, 100), "shotgun")

    # Pickup far away (should not collide)
    pickup2 = Pickup(pygame.Vector2(500, 500), "smg")

    pickups = [pickup1, pickup2]

    colliding = check_player_pickup_collisions(player_pos, player_radius, pickups)

    assert 0 in colliding  # pickup1 collides
    assert 1 not in colliding  # pickup2 doesn't collide


def test_pickup_collection_changes_weapon() -> None:
    """Test that collecting pickup changes player weapon."""
    pygame.init()
    from game.core.game import Game

    game = Game()
    scene = PlayScene(game)

    # Spawn pickup at player position
    scene.pickups.append(Pickup(scene.player.pos, "shotgun"))

    initial_weapon = scene.player.current_weapon
    assert initial_weapon == "pistol"

    # Update should detect collision and swap weapon
    scene.update(0.016)  # One frame

    assert scene.player.current_weapon == "shotgun"
    assert len(scene.pickups) == 0  # Pickup removed


def test_pickup_collection_removes_pickup() -> None:
    """Test that collected pickups are removed from scene."""
    pygame.init()
    from game.core.game import Game

    game = Game()
    scene = PlayScene(game)

    # Add multiple pickups, one at player position
    scene.pickups.append(Pickup(pygame.Vector2(500, 500), "smg"))
    scene.pickups.append(Pickup(scene.player.pos, "shotgun"))  # Colliding
    scene.pickups.append(Pickup(pygame.Vector2(300, 300), "pistol"))

    assert len(scene.pickups) == 3

    scene.update(0.016)

    # Only colliding pickup should be removed
    assert len(scene.pickups) == 2
    assert scene.player.current_weapon == "shotgun"


def test_multiple_pickups_spawn_over_time() -> None:
    """Test that multiple pickups spawn as timer cycles."""
    pygame.init()
    from game.core.game import Game

    game = Game()
    scene = PlayScene(game)

    # Fast-forward through two spawn cycles
    scene.pickup_spawn_timer = 0.1
    scene.update(0.2)  # First spawn
    assert len(scene.pickups) == 1

    scene.pickup_spawn_timer = 0.1
    scene.update(0.2)  # Second spawn
    assert len(scene.pickups) == 2
```

**MIRROR**: `test_weapon_constants.py:1-43` - pytest structure, docstrings

**PATTERN**:
- One test per behavior
- Descriptive names: `test_<what>_<scenario>()`
- Google-style docstrings
- Initialize pygame before creating PlayScene
- Use assert statements

**GOTCHA**:
- Must call `pygame.init()` before creating Game/PlayScene instances
- Import Game inside test functions (avoids circular import issues)
- Use small dt values (0.016 = ~60 FPS) for frame simulation

**VALIDATE**:
```bash
PYTHONPATH=zombie-shooter/src zombie-shooter/.venv/bin/python -m pytest zombie-shooter/tests/test_pickup_spawning.py -v
```
Expected: 8 tests pass

---

### Task 8: RUN full validation suite

**ACTION**: Verify all changes integrate correctly

**IMPLEMENT**: Run comprehensive validation

**VALIDATE**:
```bash
zombie-shooter/.venv/bin/ruff format zombie-shooter && zombie-shooter/.venv/bin/ruff check zombie-shooter && PYTHONPATH=zombie-shooter/src zombie-shooter/.venv/bin/python -m pytest zombie-shooter -q
```

Expected:
- `ruff format`: May reformat files (acceptable)
- `ruff check`: All checks passed, 0 errors
- `pytest -q`: All tests pass (27 total: 7 collision + 7 pickup + 5 weapon constants + 8 pickup spawning)

**GOTCHA**:
- If import errors, check PYTHONPATH is set correctly
- If tests fail, verify pickup spawning logic matches test expectations

---

## Testing Strategy

### Unit Tests to Write

| Test File                                | Test Cases                 | Validates      |
| ---------------------------------------- | -------------------------- | -------------- |
| `tests/test_pickup_spawning.py` | test_pickup_spawn_timer_initialization | Timer and list initialized |
| | test_pickup_spawns_after_timer | Timer triggers spawn |
| | test_pickup_spawn_timer_resets | Timer resets after spawn |
| | test_player_pickup_collision_detection | Collision function works |
| | test_pickup_collection_changes_weapon | Weapon swapping on collision |
| | test_pickup_collection_removes_pickup | Pickups removed when collected |
| | test_multiple_pickups_spawn_over_time | Multiple spawns work |

### Edge Cases Checklist

- [ ] Pickup spawns within screen bounds (no edge spawning)
- [ ] Pickup spawn timer resets correctly
- [ ] Random weapon selection covers all WEAPON_STATS keys
- [ ] Player-pickup collision detected at touch distance
- [ ] Multiple simultaneous pickup collisions handled (set-based removal)
- [ ] Collected pickups removed immediately (not next frame)
- [ ] Player weapon changes to pickup.weapon_type on collection
- [ ] Expired pickups (TTL) removed independently of collection
- [ ] Pickup list updates correctly each frame (TTL filtering)
- [ ] Drawing order correct (pickups visible, not hidden by HUD)

---

## Validation Commands

### Level 1: STATIC_ANALYSIS
```bash
zombie-shooter/.venv/bin/ruff format zombie-shooter && zombie-shooter/.venv/bin/ruff check zombie-shooter
```
**EXPECT**: Exit 0, all checks passed

### Level 2: UNIT_TESTS
```bash
PYTHONPATH=zombie-shooter/src zombie-shooter/.venv/bin/python -m pytest zombie-shooter/tests/test_pickup_spawning.py -v
```
**EXPECT**: 8 tests pass (spawn timer, spawn logic, collision detection, weapon swapping, removal)

### Level 3: FULL_SUITE
```bash
PYTHONPATH=zombie-shooter/src zombie-shooter/.venv/bin/python -m pytest zombie-shooter -q
```
**EXPECT**: All tests pass (27 total: 7 collision + 7 pickup + 5 weapon constants + 8 pickup spawning)

### Level 4: MANUAL_VALIDATION
```bash
PYTHONPATH=zombie-shooter/src zombie-shooter/.venv/bin/python -m game.main
```
**EXPECT**:
- Game launches successfully
- Pickups appear after ~15 seconds (colored rectangles)
- Player can walk over pickups to collect them
- Pickups disappear when collected
- New pickups spawn every ~15 seconds
- Multiple pickups can exist simultaneously

**Manual test steps:**
1. Launch game, start playing
2. Wait 15 seconds - pickup should spawn (yellow/red/cyan rectangle)
3. Navigate player to pickup
4. Touch pickup - it should disappear
5. Wait another 15 seconds - another pickup spawns
6. Verify pickups despawn after 30s if not collected (TTL)

---

## Acceptance Criteria

- [ ] PICKUP_SPAWN_MARGIN constant added to constants.py
- [ ] check_player_pickup_collisions() function added to collisions.py
- [ ] PlayScene has pickups list and pickup_spawn_timer
- [ ] Pickups spawn every ~15 seconds at random interior positions
- [ ] Player-pickup collision detection works
- [ ] Collecting pickup changes player.current_weapon
- [ ] Collected pickups removed from scene
- [ ] Pickups rendered on screen (colored rectangles)
- [ ] 8 integration tests written and passing
- [ ] Level 1-3 validation commands pass with exit 0
- [ ] Manual validation: pickups spawn, can be collected, weapon changes

---

## Completion Checklist

- [ ] Task 1: PICKUP_SPAWN_MARGIN added to constants.py
- [ ] Task 2: check_player_pickup_collisions() added to collisions.py
- [ ] Task 3: Imports updated in play.py
- [ ] Task 4: pickups list and timer added to PlayScene.__init__
- [ ] Task 5: Spawning and collision logic added to PlayScene.update()
- [ ] Task 6: Pickup drawing added to PlayScene.draw()
- [ ] Task 7: test_pickup_spawning.py created with 8 tests
- [ ] Task 8: Full validation suite passes
- [ ] Level 1: Static analysis passes
- [ ] Level 2: Unit tests pass (8/8 pickup spawning tests)
- [ ] Level 3: Full suite passes (27 tests)
- [ ] Level 4: Manual validation passes
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk               | Likelihood   | Impact       | Mitigation                              |
| ------------------ | ------------ | ------------ | --------------------------------------- |
| Pickups spawn off-screen | LOW | MEDIUM | Use PICKUP_SPAWN_MARGIN (100px) to ensure interior spawning |
| Multiple pickups at same position | LOW | LOW | Random uniform distribution makes collision rare, acceptable if happens |
| Player misses pickup (too small) | MEDIUM | LOW | PICKUP_RADIUS = 20 provides generous hitbox (tested in Phase 2) |
| Weapon swap while shooting | LOW | LOW | Phase 3 will handle weapon-specific shooting, Phase 4 just changes string |
| Timer drift/accumulation | LOW | LOW | Timer resets to fixed PICKUP_SPAWN_RATE, no drift possible |
| random.choice fails on empty dict | LOW | HIGH | WEAPON_STATS always has 3 keys (validated in Phase 1 tests) |
| Pickup spam if dt is large | LOW | MEDIUM | Timer only spawns once per trigger, resets to 15s immediately |

---

## Notes

**Design Decisions:**

1. **Timer-based spawning (not kill-based)**: PRD specified ~15 second intervals. This ensures predictable pickup availability regardless of player skill (kills vary, time is constant).

2. **Random interior positions (not edge)**: Unlike zombies (spawn at edges), pickups spawn inside the play area. This:
   - Makes them immediately visible
   - Creates risk/reward (navigate through zombies to reach pickup)
   - Avoids instant collection at spawn

3. **PICKUP_SPAWN_MARGIN = 100 pixels**: Prevents pickups spawning too close to screen edge where they might be:
   - Partially off-screen
   - Hard to navigate to (edge collision with boundary)
   - Less visible

4. **Set-based collision removal**: Even though players likely collect one pickup at a time, using set-based removal (like bullet-zombie collisions) handles edge case of multiple simultaneous pickups cleanly.

5. **Weapon swap without validation**: Player can collect same weapon type they already have. This is intentional:
   - Simpler logic (no "already equipped" check)
   - Collecting "refreshes" the weapon availability
   - Phase 5 HUD will show weapon name, so player aware of current weapon

6. **Spawn timer starts at PICKUP_SPAWN_RATE**: First pickup spawns after 15 seconds (not immediately at game start). This gives player time to encounter first zombies before adding pickup collection objective.

**Integration with Other Phases:**

- **Phase 1 (Weapon data model)**: Provides WEAPON_STATS keys for random selection, player.current_weapon attribute for swapping
- **Phase 2 (Pickup entity)**: Provides Pickup class with pos, weapon_type, radius, draw() - all used in Phase 4
- **Phase 3 (Weapon behavior)**: Will read player.current_weapon to vary shooting pattern (spread, rate) - Phase 4 just changes the string
- **Phase 5 (HUD integration)**: Will display player.current_weapon on screen - Phase 4 makes the value change
- **Phase 6 (Testing & validation)**: Will verify end-to-end gameplay with all systems integrated

**Performance Considerations:**

- Spawn rate (15s) means max ~4 pickups on screen simultaneously during 60s game
- TTL (30s) automatically cleans up uncollected pickups
- Collision detection is O(n) where n = pickup count (typically 1-4)
- No complex pathfinding or physics - just position generation and collision checks
- Negligible performance impact

**Gameplay Implications:**

- **Risk/reward decision**: Go for pickup (risk zombie contact) or play safe?
- **Strategic timing**: Collect when safe, not immediately at spawn
- **Weapon variety**: ~4 weapon swaps possible during 60s game (15s spawn * 4)
- **Dynamic combat**: Weapon changes force tactical adaptation
- **Visual feedback**: Colored rectangles provide instant weapon identification

---

**Sources:**
- [Python random module documentation](https://docs.python.org/3/library/random.html) - random.choice() and random.uniform() for weapon selection and position generation
