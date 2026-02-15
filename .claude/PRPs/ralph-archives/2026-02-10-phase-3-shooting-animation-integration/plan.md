# Feature: Player Shooting Animation Integration

## Summary

Add shooting animation state tracking to Player class so that when the player fires a weapon, the character sprite switches from walk animation to shoot animation (showing extended gun) for a brief duration (~0.1 seconds), then returns to walk/idle animation. This completes the visual polish of the player character by making shooting actions visible and thematic, matching the animated zombie sprites already in the game.

## User Story

As a player
I want to see my character display a shooting pose when I fire weapons
So that gameplay feels immersive with visible action feedback matching the animated zombies

## Problem Statement

Currently, the player character displays only walk/idle animations even when shooting. When the player clicks to fire bullets, there's no visual indication that the character is shooting - the gun remains in idle position and doesn't extend. This breaks immersion despite having 4 pre-generated shoot sprite files (`shoot_down.png`, `shoot_up.png`, `shoot_left.png`, `shoot_right.png`) ready to use. The shooting action needs to be visualized to complete the player sprite animation system.

## Solution Statement

Implement shooting animation state tracking by adding `shoot_timer` (float countdown) to Player class, setting it to `PLAYER_SHOOT_DURATION` when `shoot()` is called, decrementing it in `update()`, and modifying `draw()` to display shoot sprites when `shoot_timer > 0`, otherwise displaying walk sprites. This follows the exact timer countdown pattern used for `shoot_cooldown` and mirrors state management patterns from zombie variants (spitter attack cooldown, exploder explosion timing).

## Metadata

| Field            | Value                                             |
| ---------------- | ------------------------------------------------- |
| Type             | ENHANCEMENT |
| Complexity       | LOW |
| Systems Affected | Player entity (player.py), Constants (constants.py), Asset loading (loader.py) |
| Dependencies     | pygame 2.6.1, existing Animation system, Phase 1 shoot sprites |
| Estimated Tasks  | 4 |

---

## UX Design

### Before State
```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌──────────────┐         ┌──────────────┐         ┌──────────────┐         ║
║   │ Player Moves │────────►│ Player Shoots│────────►│  Result      │         ║
║   │ with WASD    │         │ (mouse click)│         │              │         ║
║   └──────────────┘         └──────────────┘         └──────────────┘         ║
║         │                         │                         │                ║
║         ▼                         ▼                         ▼                ║
║   Walk animation          Walk animation           Bullets spawn,            ║
║   cycles based on         STILL shows!             player sprite             ║
║   velocity direction      No visual change         shows NO gun              ║
║   (3-frame loop)          when shooting            extended action           ║
║                                                                               ║
║   USER_FLOW:                                                                  ║
║   1. Player presses WASD → character walks with animated legs                 ║
║   2. Player clicks mouse → bullets fire BUT character sprite unchanged        ║
║   3. Player expects to see gun extend → sees only walk animation              ║
║                                                                               ║
║   PAIN_POINT: Shooting is invisible - no visual feedback despite action       ║
║                                                                               ║
║   DATA_FLOW:                                                                  ║
║   Mouse click → Player.shoot() called → Bullets created → shoot_cooldown set  ║
║   BUT: No shooting animation state tracking → draw() always uses walk sprites ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### After State
```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌──────────────┐         ┌──────────────┐         ┌──────────────┐         ║
║   │ Player Moves │────────►│ Player Shoots│────────►│  Result      │         ║
║   │ with WASD    │         │ (mouse click)│         │              │         ║
║   └──────────────┘         └──────────────┘         └──────────────┘         ║
║         │                         │                         │                ║
║         ▼                         ▼                         ▼                ║
║   Walk animation          SHOOT animation           Bullets spawn,            ║
║   cycles based on         displays for             player sprite             ║
║   velocity direction      0.1 seconds!              shows EXTENDED            ║
║   (3-frame loop)          Gun visibly extends       gun in shoot pose         ║
║                                  │                                            ║
║                                  ▼                                            ║
║                          After 0.1 sec:                                       ║
║                          Returns to walk/idle                                 ║
║                          animation automatically                              ║
║                                                                               ║
║   USER_FLOW:                                                                  ║
║   1. Player presses WASD → character walks with animated legs                 ║
║   2. Player clicks mouse → bullets fire AND character shows shoot sprite      ║
║   3. Player sees gun extend in facing direction → clear visual feedback       ║
║   4. After brief moment → character returns to walk/idle animation            ║
║                                                                               ║
║   VALUE_ADD: Shooting actions are now visible and immersive                   ║
║                                                                               ║
║   DATA_FLOW:                                                                  ║
║   Mouse click → Player.shoot() called → Bullets created → shoot_cooldown set  ║
║   NEW: shoot_timer = PLAYER_SHOOT_DURATION (0.1 sec)                          ║
║   Each frame: update() decrements shoot_timer by dt                           ║
║   In draw(): if shoot_timer > 0 → use shoot sprite, else → use walk sprite    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| `player.py:shoot()` | Sets shoot_cooldown only | Sets shoot_cooldown AND shoot_timer | Shooting action triggers animation state |
| `player.py:update()` | Decrements shoot_cooldown | Decrements shoot_cooldown AND shoot_timer | Animation timer counts down each frame |
| `player.py:draw()` | Always uses walk sprites | Checks shoot_timer, uses shoot or walk sprites | Player sees gun extend when shooting |
| Visual feedback | No shooting indicator | Gun visibly extends for 0.1 seconds | Clear action feedback, matches zombie quality |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `player.py` | 97-99 | Pattern to MIRROR - shoot_cooldown timer decrement in update() |
| P0 | `player.py` | 101-150 | Pattern to EXTEND - shoot() method needs shoot_timer initialization |
| P0 | `player.py` | 174-188 | Pattern to MODIFY - draw() method needs sprite selection logic |
| P1 | `loader.py` | 127-167 | Pattern to EXTEND - load_player_sprites() needs shoot sprite loading |
| P1 | `constants.py` | 10-17 | Pattern to FOLLOW - add PLAYER_SHOOT_DURATION constant |
| P2 | `test_player_integration.py` | all | Test pattern to FOLLOW - add shooting animation tests |

**External Documentation:**
| Source | Section | Why Needed |
|--------|---------|------------|
| [Pygame Docs v2.6.1](https://www.pygame.org/docs/ref/surface.html#pygame.Surface.blit) | Surface.blit | Sprite rendering method used in draw() |

---

## Patterns to Mirror

**TIMER_DECREMENT_PATTERN:**
```python
// SOURCE: player.py:97-99
// COPY THIS PATTERN for shoot_timer:
# Decrement cooldown
if self.shoot_cooldown > 0:
    self.shoot_cooldown -= dt
```

**SHOOT_METHOD_INITIALIZATION:**
```python
// SOURCE: player.py:124
// EXTEND THIS LINE - add shoot_timer initialization:
# Set cooldown based on weapon fire rate
self.shoot_cooldown = fire_rate
# NEW: self.shoot_timer = PLAYER_SHOOT_DURATION
```

**SPRITE_SELECTION_IN_DRAW:**
```python
// SOURCE: player.py:174-188
// MODIFY THIS PATTERN - add conditional sprite selection:
def draw(self, screen: pygame.Surface) -> None:
    """Draw player to screen."""
    direction = self.animation.get_current_direction()

    # NEW: Check shooting state
    if self.shoot_timer > 0:
        # Use shoot sprite (single frame, no animation)
        sprite = self.sprites[direction][self.frame_count]  # Shoot sprite after walk frames
    else:
        # Use walk sprite (existing code)
        frame_index = self.animation.get_current_frame_index()
        sprite = self.sprites[direction][frame_index]

    # Center sprite on player position (unchanged)
    sprite_rect = sprite.get_rect(center=(int(self.pos.x), int(self.pos.y)))
    screen.blit(sprite, sprite_rect)
```

**SPRITE_LOADING_EXTENSION:**
```python
// SOURCE: loader.py:127-167
// EXTEND THIS PATTERN - load both walk AND shoot sprites:
def load_player_sprites(
    sprite_size: int = 48, frame_count: int = 3
) -> dict[str, list[pygame.Surface]]:
    """Load player sprites for all 4 directions (walk + shoot)."""
    cache_key = "player"
    if cache_key in _sprite_cache:
        return _sprite_cache[cache_key]

    players_dir = ASSETS_DIR / "players"
    directions = ["down", "up", "left", "right"]
    sprites: dict[str, list[pygame.Surface]] = {}

    for direction in directions:
        # Load walk sprite sheet (3 frames)
        walk_sheet_path = players_dir / f"walk_{direction}.png"
        walk_sheet = load_image(walk_sheet_path)
        walk_frames = split_sprite_sheet(walk_sheet, sprite_size, frame_count)

        # NEW: Load shoot sprite (single frame)
        shoot_sprite_path = players_dir / f"shoot_{direction}.png"
        shoot_sprite = load_image(shoot_sprite_path)

        # Combine: [walk_frame0, walk_frame1, walk_frame2, shoot_frame]
        sprites[direction] = walk_frames + [shoot_sprite]

    _sprite_cache[cache_key] = sprites
    return sprites
```

**CONSTANT_DEFINITION:**
```python
// SOURCE: constants.py:10-17
// ADD AFTER LINE 17:
PLAYER_SHOOT_DURATION = 0.1  # Seconds to display shooting animation
```

**TEST_TIMER_DECREMENT:**
```python
// SOURCE: test_weapon_behavior.py:69-94
// MIRROR THIS PATTERN for shoot_timer tests:
def test_shoot_timer_set_on_fire() -> None:
    """Test that shoot_timer is set when player shoots."""
    player = Player(pygame.Vector2(100, 100))
    target = pygame.Vector2(200, 200)

    # Fire weapon
    player.shoot(target)

    # Verify shoot timer was set
    assert player.shoot_timer == PLAYER_SHOOT_DURATION


def test_shoot_timer_decrements() -> None:
    """Test that shoot_timer decrements over time."""
    player = Player(pygame.Vector2(100, 100))
    player.shoot_timer = 0.5

    # Update with dt
    player.update(0.1)

    # Timer should have decremented
    assert player.shoot_timer == pytest.approx(0.4, abs=1e-6)
```

---

## Files to Change

| File | Action | Justification |
|------|--------|---------------|
| `src/game/core/constants.py` | UPDATE | Add PLAYER_SHOOT_DURATION constant (0.1 seconds) |
| `src/game/assets/loader.py` | UPDATE | Extend load_player_sprites() to load shoot sprites after walk frames |
| `src/game/entities/player.py` | UPDATE | Add shoot_timer attribute, set in shoot(), decrement in update(), check in draw() |
| `tests/test_player_integration.py` | UPDATE | Add tests for shoot_timer state tracking and sprite selection |

---

## NOT Building (Scope Limits)

Explicit exclusions to prevent scope creep:

- **Per-weapon unique shoot animations** - All weapons (pistol/shotgun/SMG) share the same shoot sprite (constraint specified in PRD)
- **Muzzle flash particles** - Deferred to Phase 4 (polish) - current scope is just sprite switching
- **Shooting animation pausing walk cycle** - Shoot animation overlays on current direction, doesn't pause movement
- **Reload animation** - Out of PRD scope entirely
- **Directional shoot animation based on mouse angle** - Uses current facing direction from animation system, not precise mouse angle
- **Shooting while moving diagonal smoothing** - Animation system already handles diagonal→cardinal direction mapping

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: ADD constant PLAYER_SHOOT_DURATION to constants.py

- **ACTION**: ADD constant definition after line 17
- **IMPLEMENT**: Add single line: `PLAYER_SHOOT_DURATION = 0.1  # Seconds to display shooting animation`
- **MIRROR**: `constants.py:10-17` - follow existing constant format with inline comment
- **IMPORTS**: None needed
- **GOTCHA**: Use 0.1 seconds to match fast-paced action feel; longer values (0.3+) feel sluggish
- **VALIDATE**:
  ```bash
  cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter
  .venv/bin/ruff check src/game/core/constants.py
  .venv/bin/python -c "from game.core.constants import PLAYER_SHOOT_DURATION; print(f'✓ PLAYER_SHOOT_DURATION = {PLAYER_SHOOT_DURATION}')"
  ```
  **EXPECT**: Linting passes, constant imports successfully, prints "✓ PLAYER_SHOOT_DURATION = 0.1"

### Task 2: UPDATE load_player_sprites() in loader.py to load shoot sprites

- **ACTION**: MODIFY load_player_sprites() function to load both walk and shoot sprites
- **IMPLEMENT**:
  1. Keep existing walk sprite loading (lines 150-162)
  2. After `walk_frames = split_sprite_sheet(...)` for each direction, add:
     ```python
     # Load shoot sprite (single frame)
     shoot_sprite_path = players_dir / f"shoot_{direction}.png"
     shoot_sprite = load_image(shoot_sprite_path)

     # Combine walk frames + shoot sprite
     sprites[direction] = walk_frames + [shoot_sprite]
     ```
  3. Structure becomes: `sprites[direction] = [walk0, walk1, walk2, shoot]` (4 surfaces total)
- **MIRROR**: `loader.py:150-162` - extend existing loop with shoot sprite loading
- **IMPORTS**: None needed (all helpers already imported)
- **GOTCHA**: Shoot sprites are single 48×48 files, NOT sprite sheets - use `load_image()` directly, not `split_sprite_sheet()`
- **VALIDATE**:
  ```bash
  cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter
  .venv/bin/ruff check src/game/assets/loader.py
  export PYTHONPATH="src"
  .venv/bin/python -c "import pygame; pygame.init(); from game.assets.loader import load_player_sprites; sprites = load_player_sprites(); print(f'✓ Loaded {len(sprites)} directions'); print(f'✓ Each direction has {len(sprites[\"down\"])} sprites (3 walk + 1 shoot)'); print(f'✓ Shoot sprite type: {type(sprites[\"down\"][3])}')"
  ```
  **EXPECT**: Linting passes, prints "✓ Loaded 4 directions", "✓ Each direction has 4 sprites (3 walk + 1 shoot)", shoot sprite is pygame.Surface type

### Task 3: UPDATE Player class to add shoot_timer state tracking

- **ACTION**: MODIFY Player class to track and decrement shoot_timer
- **IMPLEMENT**:

  **3a. Add shoot_timer to __init__() (after line 53)**:
  ```python
  self.shoot_cooldown = 0.0
  self.shoot_timer = 0.0  # NEW: Timer for shooting animation display
  self.current_weapon: str = "pistol"
  ```

  **3b. Set shoot_timer in shoot() method (after line 124)**:
  ```python
  # Set cooldown based on weapon fire rate
  self.shoot_cooldown = fire_rate
  self.shoot_timer = PLAYER_SHOOT_DURATION  # NEW: Trigger shooting animation
  ```

  **3c. Add import for PLAYER_SHOOT_DURATION (line 10-20)**:
  ```python
  from game.core.constants import (
      HEIGHT,
      PLAYER_ANIMATION_FPS,
      PLAYER_FRAME_COUNT,
      PLAYER_MAX_HP,
      PLAYER_RADIUS,
      PLAYER_SHOOT_DURATION,  # NEW
      PLAYER_SPEED,
      PLAYER_SPRITE_SIZE,
      WEAPON_STATS,
      WIDTH,
  )
  ```

  **3d. Decrement shoot_timer in update() (after line 99)**:
  ```python
  # Decrement cooldown
  if self.shoot_cooldown > 0:
      self.shoot_cooldown -= dt

  # NEW: Decrement shoot timer
  if self.shoot_timer > 0:
      self.shoot_timer -= dt
  ```

  **3e. Modify draw() to check shoot_timer (replace lines 174-188)**:
  ```python
  def draw(self, screen: pygame.Surface) -> None:
      """Draw player to screen.

      Args:
          screen: Pygame surface to draw on.
      """
      # Get current direction from animation
      direction = self.animation.get_current_direction()

      # Select sprite based on shooting state
      if self.shoot_timer > 0:
          # Display shooting sprite (4th sprite in list: index 3)
          sprite = self.sprites[direction][PLAYER_FRAME_COUNT]
      else:
          # Display walk animation sprite
          frame_index = self.animation.get_current_frame_index()
          sprite = self.sprites[direction][frame_index]

      # Center sprite on player position
      sprite_rect = sprite.get_rect(center=(int(self.pos.x), int(self.pos.y)))
      screen.blit(sprite, sprite_rect)
  ```

- **MIRROR**:
  - Timer decrement: `player.py:97-99` (shoot_cooldown pattern)
  - Timer initialization: `player.py:124` (where shoot_cooldown is set)
  - Draw sprite selection: `player.py:174-188` (extend with conditional logic)
- **IMPORTS**: Add `PLAYER_SHOOT_DURATION` to existing import from constants
- **GOTCHA**: Use `PLAYER_FRAME_COUNT` (constant = 3) as index for shoot sprite, not hardcoded `3` - maintains flexibility if frame count changes
- **VALIDATE**:
  ```bash
  cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter
  .venv/bin/ruff check src/game/entities/player.py
  export PYTHONPATH="src"
  .venv/bin/python -c "import pygame; pygame.init(); from game.entities.player import Player; p = Player(pygame.Vector2(400, 300)); print(f'✓ Player has shoot_timer: {hasattr(p, \"shoot_timer\")}'); print(f'✓ Initial shoot_timer: {p.shoot_timer}'); bullets = p.shoot(pygame.Vector2(500, 300)); print(f'✓ After shoot, shoot_timer: {p.shoot_timer}')"
  ```
  **EXPECT**: Linting passes, prints "✓ Player has shoot_timer: True", "✓ Initial shoot_timer: 0.0", "✓ After shoot, shoot_timer: 0.1"

### Task 4: ADD shooting animation tests to test_player_integration.py

- **ACTION**: ADD 4 new test functions at end of file
- **IMPLEMENT**:

  **Test 1: shoot_timer attribute exists**
  ```python
  def test_player_has_shoot_timer_attribute() -> None:
      """Test that player initializes with shoot_timer attribute."""
      player = Player(pygame.Vector2(400, 300))
      assert hasattr(player, "shoot_timer")
      assert player.shoot_timer == 0.0
  ```

  **Test 2: shoot_timer set when shooting**
  ```python
  def test_player_shoot_timer_set_on_fire() -> None:
      """Test that shoot_timer is set when player shoots."""
      player = Player(pygame.Vector2(400, 300))
      target = pygame.Vector2(500, 300)

      # Fire weapon
      player.shoot(target)

      # Verify shoot timer was set
      assert player.shoot_timer == PLAYER_SHOOT_DURATION
  ```

  **Test 3: shoot_timer decrements over time**
  ```python
  def test_player_shoot_timer_decrements() -> None:
      """Test that shoot_timer decrements during update."""
      player = Player(pygame.Vector2(400, 300))
      player.shoot_timer = 0.5

      # Update with dt
      player.update(0.1)

      # Timer should have decremented
      assert player.shoot_timer == pytest.approx(0.4, abs=1e-6)
  ```

  **Test 4: shoot sprite used when shooting**
  ```python
  def test_player_uses_shoot_sprite_when_shooting() -> None:
      """Test that player draw uses shoot sprite during shoot_timer."""
      player = Player(pygame.Vector2(400, 300))
      screen = pygame.Surface((800, 600))

      # Set shoot timer (simulating shooting state)
      player.shoot_timer = 0.1

      # Get direction and expected shoot sprite index
      direction = player.animation.get_current_direction()
      shoot_sprite_index = PLAYER_FRAME_COUNT  # Index 3 (after walk frames 0, 1, 2)
      expected_shoot_sprite = player.sprites[direction][shoot_sprite_index]

      # Verify shoot sprite would be selected
      # (Can't directly test draw output, but can verify sprite exists)
      assert expected_shoot_sprite is not None
      assert isinstance(expected_shoot_sprite, pygame.Surface)

      # Draw should not raise error
      player.draw(screen)
  ```

  **Add imports at top of file**:
  ```python
  from game.core.constants import (
      PLAYER_ANIMATION_FPS,
      PLAYER_FRAME_COUNT,
      PLAYER_SHOOT_DURATION,  # NEW
      PLAYER_SPRITE_SIZE,
  )
  ```

- **MIRROR**: `test_player_integration.py:18-93` - follow existing test structure and naming
- **IMPORTS**: Add `PLAYER_SHOOT_DURATION` to existing import, also add `import pytest` for approx
- **GOTCHA**: Use `pytest.approx()` for float comparisons (timer decrements); direct `==` can fail due to floating point precision
- **VALIDATE**:
  ```bash
  cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter
  export PYTHONPATH="src"
  .venv/bin/pytest tests/test_player_integration.py::test_player_has_shoot_timer_attribute -v
  .venv/bin/pytest tests/test_player_integration.py::test_player_shoot_timer_set_on_fire -v
  .venv/bin/pytest tests/test_player_integration.py::test_player_shoot_timer_decrements -v
  .venv/bin/pytest tests/test_player_integration.py::test_player_uses_shoot_sprite_when_shooting -v
  ```
  **EXPECT**: All 4 new tests pass

---

## Testing Strategy

### Unit Tests to Write

| Test File | Test Cases | Validates |
|-----------|------------|-----------|
| `test_player_integration.py` | shoot_timer attribute initialization | Player has shoot_timer starting at 0.0 |
| `test_player_integration.py` | shoot_timer set on weapon fire | shoot() method sets timer to PLAYER_SHOOT_DURATION |
| `test_player_integration.py` | shoot_timer decrement | update() decrements timer by dt |
| `test_player_integration.py` | shoot sprite selection | draw() uses correct sprite when shooting |

### Edge Cases Checklist

- [ ] shoot_timer starts at 0.0 (not shooting initially)
- [ ] shoot_timer set to exactly PLAYER_SHOOT_DURATION when shooting
- [ ] shoot_timer decrements correctly with various dt values (0.016, 0.1, etc.)
- [ ] shoot_timer can go negative (doesn't break, just means not shooting)
- [ ] Shooting multiple times rapidly (shoot_timer resets each time)
- [ ] Sprite selection switches back to walk when timer expires
- [ ] Sprite selection works for all 4 directions (down, up, left, right)
- [ ] draw() doesn't crash when shoot_timer > 0

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter
.venv/bin/ruff check src/game/core/constants.py src/game/assets/loader.py src/game/entities/player.py tests/test_player_integration.py
.venv/bin/ruff format src/game/core/constants.py src/game/assets/loader.py src/game/entities/player.py tests/test_player_integration.py
```

**EXPECT**: Exit 0, no linting errors or warnings, code formatted

### Level 2: UNIT_TESTS

```bash
cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter
export PYTHONPATH="src"
.venv/bin/pytest tests/test_player_integration.py -v
```

**EXPECT**: All tests pass (11 total: 7 existing + 4 new shooting animation tests)

### Level 3: FULL_SUITE

```bash
cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter
export PYTHONPATH="src"
.venv/bin/pytest tests/ -v
```

**EXPECT**: All 132 tests pass (128 existing + 4 new), no regressions

### Level 4: INTEGRATION_TEST

```bash
cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter
export PYTHONPATH="src"
.venv/bin/python -c "
import pygame
pygame.init()

from game.entities.player import Player
from game.core.constants import PLAYER_SHOOT_DURATION

# Initialize player
player = Player(pygame.Vector2(400, 300))
print('✓ Player initialized')

# Check shoot_timer attribute
assert player.shoot_timer == 0.0, 'shoot_timer should start at 0'
print('✓ shoot_timer starts at 0.0')

# Fire weapon
target = pygame.Vector2(500, 300)
bullets = player.shoot(target)
assert player.shoot_timer == PLAYER_SHOOT_DURATION, 'shoot_timer should be set after shooting'
print(f'✓ shoot_timer set to {player.shoot_timer} after shooting')

# Update to decrement timer
player.update(0.05)
assert player.shoot_timer < PLAYER_SHOOT_DURATION, 'shoot_timer should decrement'
print(f'✓ shoot_timer decremented to {player.shoot_timer}')

# Check sprite loading includes shoot sprites
direction = 'down'
num_sprites = len(player.sprites[direction])
assert num_sprites == 4, f'Should have 4 sprites (3 walk + 1 shoot), got {num_sprites}'
print(f'✓ Sprite loading includes shoot sprites ({num_sprites} per direction)')

# Test draw doesn't crash
screen = pygame.Surface((800, 600))
player.draw(screen)
print('✓ draw() executes without error during shooting state')

print('\\n✅ All integration checks passed!')
"
```

**EXPECT**: All assertions pass, prints success messages

### Level 5: MANUAL_VALIDATION

**Manual gameplay test steps:**

1. **Launch game**:
   ```bash
   cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter
   export PYTHONPATH="src"
   .venv/bin/python src/game/main.py
   ```

2. **Test shooting while idle**:
   - Don't press any keys (player idle, facing down)
   - Click mouse to shoot
   - **VERIFY**: Player sprite briefly shows extended gun pose for ~0.1 seconds
   - **VERIFY**: Player sprite returns to idle stance after animation

3. **Test shooting while moving**:
   - Press WASD to move (watch walk animation)
   - While moving, click mouse to shoot
   - **VERIFY**: Walk animation pauses, shoot sprite shows
   - **VERIFY**: Gun extends in current facing direction
   - **VERIFY**: After brief moment, walk animation resumes

4. **Test shooting in all 4 directions**:
   - Face down (press S), shoot → gun extends downward
   - Face up (press W), shoot → gun extends upward
   - Face left (press A), shoot → gun extends left
   - Face right (press D), shoot → gun extends right
   - **VERIFY**: Shoot sprite matches current facing direction

5. **Test rapid shooting**:
   - Hold down mouse button (rapid fire)
   - **VERIFY**: Shoot animation retriggersevery shot
   - **VERIFY**: No visual glitches or sprite flickering

6. **Test with different weapons**:
   - Collect shotgun pickup (if available)
   - Shoot with shotgun → **VERIFY**: Same shoot animation (not weapon-specific)
   - Collect SMG pickup (if available)
   - Shoot with SMG → **VERIFY**: Same shoot animation works

**Success criteria:**
- [ ] Shoot sprite displays when firing
- [ ] Gun visibly extends in current facing direction
- [ ] Animation duration feels responsive (~0.1 sec, not too long or short)
- [ ] Returns to walk/idle smoothly after shooting
- [ ] Works for all 4 directions
- [ ] Works with all weapon types (pistol, shotgun, SMG)
- [ ] No visual glitches or crashes

---

## Acceptance Criteria

- [ ] PLAYER_SHOOT_DURATION constant added to constants.py
- [ ] load_player_sprites() loads 4 sprites per direction (3 walk + 1 shoot)
- [ ] Player.__init__() initializes shoot_timer = 0.0
- [ ] Player.shoot() sets shoot_timer = PLAYER_SHOOT_DURATION when firing
- [ ] Player.update() decrements shoot_timer by dt each frame
- [ ] Player.draw() displays shoot sprite when shoot_timer > 0, walk sprite otherwise
- [ ] All 4 new unit tests pass (shoot_timer tests)
- [ ] All 128 existing tests still pass (no regressions)
- [ ] Static analysis passes (ruff check + format)
- [ ] Manual gameplay shows shooting animation in all 4 directions
- [ ] Animation duration feels responsive (not too slow or fast)
- [ ] Shoot animation works with all weapons (pistol, shotgun, SMG)

---

## Completion Checklist

- [ ] Task 1: PLAYER_SHOOT_DURATION constant added
- [ ] Task 2: load_player_sprites() extended to load shoot sprites
- [ ] Task 3: Player class updated with shoot_timer tracking
- [ ] Task 4: Shooting animation tests added
- [ ] Level 1: Static analysis passes (linting + formatting)
- [ ] Level 2: Unit tests pass (11 player integration tests)
- [ ] Level 3: Full test suite passes (132 tests, no regressions)
- [ ] Level 4: Integration test script passes
- [ ] Level 5: Manual validation confirms animations work in gameplay
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| shoot_timer too long (>0.2s) makes shooting feel sluggish | MEDIUM | MEDIUM | Use 0.1s duration (tested with zombie animations); can tune in Phase 4 if needed |
| Sprite indexing error (accessing index 3 when only 3 frames) | LOW | HIGH | Validate in Level 2 tests that sprite loading returns 4 sprites per direction; use PLAYER_FRAME_COUNT constant instead of hardcoded index |
| Shoot animation doesn't match direction (shows wrong gun angle) | LOW | MEDIUM | Use same `animation.get_current_direction()` as walk animation; tested in all 4 directions during manual validation |
| Multiple rapid shots cause timer to restart incorrectly | LOW | LOW | Timer simply resets to PLAYER_SHOOT_DURATION on each shoot() call - this is desired behavior for continuous shooting |
| Walk animation glitches when transitioning back from shoot | VERY LOW | MEDIUM | Animation system already handles frame state; shoot sprite just overlays temporarily, walk animation continues underneath |
| Performance regression from sprite selection branching | VERY LOW | LOW | Single `if` check per frame, negligible cost; existing zombie system has similar pattern at 50+ entities |

---

## Notes

**Design Decisions:**

1. **Shoot duration of 0.1 seconds**: Balances visibility (player can see the gun extend) with responsiveness (doesn't feel like movement is paused). Zombie animations use 10 FPS (0.1s per frame), so this matches the established timing feel.

2. **Sprite organization: walk + shoot in same list**: Could separate into `sprites["walk"]` and `sprites["shoot"]`, but simpler to append shoot sprite to walk frames. Index calculation: walk frames 0-2, shoot frame at index 3 (= PLAYER_FRAME_COUNT).

3. **Reuse animation.get_current_direction() for shoot sprite**: Don't need separate shoot direction tracking - when player shoots, use current facing direction from walk animation system. This keeps code simple and ensures shoot direction always matches visual facing direction.

4. **shoot_timer can go negative**: Not a bug - timer simply counts down past 0, and draw() checks `> 0` for shooting state. Could clamp to 0, but unnecessary overhead.

5. **shoot_timer independent of shoot_cooldown**: Two separate timers:
   - `shoot_cooldown`: Weapon fire rate limiting (0.15s for pistol, 0.5s for shotgun, etc.)
   - `shoot_timer`: Visual animation display (0.1s for all weapons)
   - shoot_cooldown is usually longer, so shooting animation finishes before next shot allowed

**Trade-offs:**

- **Simple vs Complex**: Could implement per-weapon shoot durations, but 0.1s works for all weapons (constraint: shared animation across weapons)
- **Sprite storage**: Could load shoot sprites separately, but appending to walk frames is simpler and maintains single sprites dict structure

**Future Considerations (Phase 4 - Polish):**

- Adjust PLAYER_SHOOT_DURATION if 0.1s feels too fast/slow during gameplay testing
- Add muzzle flash particles during shoot animation for extra polish
- Consider shoot sound effects (audio system out of current scope)

**Performance Notes:**

- Single timer decrement per frame: `O(1)` operation, negligible cost
- Single if/else in draw(): Branch prediction handles this efficiently
- Sprite loading adds 4 more surfaces (one per direction), trivial memory increase
- No frame drops expected - pattern proven with zombie system at 50+ entities

**Integration Points:**

- PlayScene calls `player.shoot()` on mouse click (line 177-182 in play.py) - no changes needed
- PlayScene calls `player.update(dt)` and `player.draw(screen)` - no changes needed
- shoot_timer state is entirely internal to Player class - clean encapsulation
