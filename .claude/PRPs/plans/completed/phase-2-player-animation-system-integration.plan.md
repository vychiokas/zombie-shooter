# Feature: Player Animation System Integration (Phase 2)

## Summary

Replace the player's blue circle rendering with sprite-based animation system by integrating the Animation class and player sprites (generated in Phase 1) into the Player entity. Mirror the exact pattern used for zombie sprite integration: add module-level sprite caching, load sprites via `load_player_sprites()` function in loader.py, instantiate Animation class in Player.__init__(), update animation state in Player.update(), and replace circle rendering with sprite blitting in Player.draw(). Add required constants (PLAYER_SPRITE_SIZE, PLAYER_FRAME_COUNT, PLAYER_ANIMATION_FPS) to constants.py.

## User Story

As a player of the zombie shooter game
I want to see my character animated with visible legs walking when I move
So that I feel immersed in the action with a polished visual experience matching the zombie sprite quality

## Problem Statement

The player character is currently rendered as a primitive blue circle (18px radius), which breaks immersion compared to the polished 48x48 animated zombie sprites with 3-frame walk cycles. Phase 1 generated the required player sprite assets, but they are not yet integrated into the Player class. The game needs to load these sprites, animate them based on player movement direction and velocity, and render them instead of the circle.

## Solution Statement

Integrate sprite-based animation into the Player class by exactly mirroring the zombie sprite integration pattern. Add `load_player_sprites()` function to loader.py that loads the 8 sprite files from `src/assets/players/` directory and caches them. Modify Player class to: (1) load sprites via module-level cache function, (2) create Animation instance with 3 frames at 10 FPS, (3) call animation.update() with velocity each frame, (4) replace circle drawing with sprite blitting using current animation frame and direction. Add sprite size constants to constants.py matching zombie values (48px, 3 frames, 10 FPS).

## Metadata

| Field            | Value                                             |
| ---------------- | ------------------------------------------------- |
| Type             | ENHANCEMENT |
| Complexity       | LOW |
| Systems Affected | Player entity, Asset loader, Constants, Animation system (integration only) |
| Dependencies     | pygame 2.6.1, Animation class (existing), Player sprites from Phase 1 |
| Estimated Tasks  | 5 |

---

## UX Design

### Before State
```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌─────────────┐         ┌─────────────┐         ┌─────────────┐            ║
║   │ Player moves│ ──────► │  Player.    │ ──────► │   Blue      │            ║
║   │ with WASD   │         │  draw()     │         │   Circle    │            ║
║   └─────────────┘         └─────────────┘         └─────────────┘            ║
║                                                                               ║
║   USER_FLOW: Player presses WASD keys → Player position updates →            ║
║              Blue circle redraws at new position (no visual movement)         ║
║                                                                               ║
║   PAIN_POINT: Cannot see character walking, no legs moving, no directional   ║
║               animation, immersion broken by primitive rendering              ║
║                                                                               ║
║   DATA_FLOW: Input → Player.vel updated → Player.pos updated →               ║
║              pygame.draw.circle() renders static blue circle                  ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### After State
```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌─────────────┐         ┌─────────────┐         ┌─────────────┐            ║
║   │ Player moves│ ──────► │  Animation  │ ──────► │ Animated    │            ║
║   │ with WASD   │         │  .update()  │         │ Rambo Sprite│            ║
║   └─────────────┘         │  detects    │         │ with legs   │            ║
║                           │  direction  │         │ walking     │            ║
║                           └─────────────┘         └─────────────┘            ║
║                                   │                       ▲                   ║
║                                   ▼                       │                   ║
║                          ┌─────────────┐         ┌───────┴─────┐             ║
║                          │   Cycles    │────────►│ Player.draw()│             ║
║                          │   frames    │         │ blits sprite │             ║
║                          │   0→1→2     │         │ at position  │             ║
║                          └─────────────┘         └──────────────┘             ║
║                                                                               ║
║   USER_FLOW: Player presses WASD keys → Player.vel computed →                ║
║              Animation.update(dt, vel) detects direction + cycles frames →    ║
║              Player.draw() blits correct animated sprite frame                ║
║                                                                               ║
║   VALUE_ADD: Player sees Rambo character walking with visible leg movement,  ║
║              animation matches zombie sprite quality, direction changes clear,║
║              immersion restored with polished sprite rendering                ║
║                                                                               ║
║   DATA_FLOW: Input → Player.vel → Animation.update(dt, vel) →                ║
║              Animation detects direction (up/down/left/right) + frame index → ║
║              Player.sprites[direction][frame] → screen.blit(sprite, rect)     ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| `Player.draw()` | Renders blue circle with pygame.draw.circle() | Blits animated sprite from loaded sprite sheets | Player sees Rambo character with visible walking animation |
| `Player.update()` | Only updates position from velocity | Also calls animation.update(dt, vel) to cycle frames | Animation syncs with movement direction and speed |
| Game startup | Player entity initializes with basic attributes | Also loads sprite cache and creates Animation instance | Sprites loaded once at startup (cached) |
| Moving with WASD | Circle moves smoothly but no visual animation | Character sprite animates with 3-frame walk cycle, legs visible moving | Clear visual feedback of movement with directional animation |
| Stationary idle | Circle remains static | Character shows idle stance (walk frame 0) | Character visible even when not moving |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `/Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/src/game/entities/zombie.py` | 16-115 | **EXACT PATTERN TO MIRROR** - complete sprite integration: module cache, sprite loading, Animation instance, update() call, draw() implementation |
| P0 | `/Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/src/game/entities/player.py` | 20-156 | Current Player class structure - understand existing __init__, update(), draw() to modify |
| P1 | `/Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/src/game/assets/loader.py` | 74-124 | Sprite loading function pattern - load_zombie_sprites() to mirror for load_player_sprites() |
| P1 | `/Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/src/game/systems/animation.py` | 10-91 | Animation class API - how to instantiate, update, and query for frames |
| P2 | `/Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/src/game/core/constants.py` | 10-71 | Constants structure - where to add PLAYER sprite constants |
| P2 | `/Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/tests/test_zombie_integration.py` | 13-122 | Test patterns for sprite integration - exact tests to mirror for player |

**External Documentation:**

| Source | Section | Why Needed |
|--------|---------|------------|
| [pygame.Surface Documentation](https://www.pygame.org/docs/ref/surface.html#pygame.Surface.get_rect) | get_rect(), blit() | Sprite positioning and rendering methods |
| [pygame.Rect Documentation](https://www.pygame.org/docs/ref/rect.html#pygame.Rect.center) | center attribute | Center-based sprite positioning (used in zombie pattern) |

---

## Patterns to Mirror

**MODULE-LEVEL SPRITE CACHING:**
```python
# SOURCE: zombie.py:16-35
# COPY THIS PATTERN FOR PLAYER:

# Module-level sprite loading (shared across all instances)
_player_sprites: dict[str, list[pygame.Surface]] | None = None

def _load_sprites() -> dict[str, list[pygame.Surface]]:
    """Load player sprites once and cache at module level."""
    global _player_sprites
    if _player_sprites is None:
        _player_sprites = load_player_sprites(
            sprite_size=PLAYER_SPRITE_SIZE,
            frame_count=PLAYER_FRAME_COUNT,
        )
    return _player_sprites
```

**PLAYER __INIT__ INTEGRATION:**
```python
# SOURCE: zombie.py:41-60
# PATTERN TO ADD TO Player.__init__():

# Load sprites and create animation instance
self.sprites = _load_sprites()
self.animation = Animation(
    frame_count=PLAYER_FRAME_COUNT, fps=PLAYER_ANIMATION_FPS
)
```

**ANIMATION UPDATE IN update():**
```python
# SOURCE: zombie.py:66-82
# PATTERN TO ADD TO Player.update():

# Update animation based on current velocity
self.animation.update(dt, self.vel)
```

**SPRITE RENDERING IN draw():**
```python
# SOURCE: zombie.py:102-115
# REPLACE Player.draw() CIRCLE WITH THIS:

def draw(self, screen: pygame.Surface) -> None:
    """Draw player to screen."""
    # Get current animation frame
    direction = self.animation.get_current_direction()
    frame_index = self.animation.get_current_frame_index()
    sprite = self.sprites[direction][frame_index]

    # Center sprite on player position
    sprite_rect = sprite.get_rect(center=(int(self.pos.x), int(self.pos.y)))
    screen.blit(sprite, sprite_rect)
```

**SPRITE LOADING FUNCTION:**
```python
# SOURCE: loader.py:74-124
# CREATE load_player_sprites() FOLLOWING THIS PATTERN:

def load_player_sprites(
    sprite_size: int = 48, frame_count: int = 3
) -> dict[str, list[pygame.Surface]]:
    """Load player sprites for all 4 directions.

    Args:
        sprite_size: Width/height of each sprite frame in pixels.
        frame_count: Number of animation frames per direction.

    Returns:
        Dictionary mapping direction to list of frame surfaces:
        {
            "down": [frame0, frame1, frame2],
            "up": [frame0, frame1, frame2],
            "left": [frame0, frame1, frame2],
            "right": [frame0, frame1, frame2]
        }
    """
    # Check cache first
    cache_key = "player"
    if cache_key in _sprite_cache:
        return _sprite_cache[cache_key]

    # Player sprites directory
    players_dir = ASSETS_DIR / "players"
    directions = ["down", "up", "left", "right"]
    sprites: dict[str, list[pygame.Surface]] = {}

    for direction in directions:
        # Load sprite sheet for this direction
        sheet_path = players_dir / f"walk_{direction}.png"
        sheet = load_image(sheet_path)

        # Split into frames
        frames = split_sprite_sheet(sheet, sprite_size, frame_count)
        sprites[direction] = frames

    # Cache for future calls
    _sprite_cache[cache_key] = sprites
    return sprites
```

**CONSTANTS DEFINITION:**
```python
# SOURCE: constants.py:65-71
# ADD AFTER PLAYER CONSTANTS (line 13):

PLAYER_ANIMATION_FPS = 10  # Frame rate for walk cycle animation
PLAYER_SPRITE_SIZE = 48  # Width/height of sprite in pixels
PLAYER_FRAME_COUNT = 3  # Number of frames per direction (walk cycle)
```

---

## Files to Change

| File | Action | Justification |
|------|--------|---------------|
| `zombie-shooter/src/game/core/constants.py` | UPDATE | Add PLAYER_SPRITE_SIZE, PLAYER_FRAME_COUNT, PLAYER_ANIMATION_FPS constants (after line 13) |
| `zombie-shooter/src/game/assets/loader.py` | UPDATE | Add load_player_sprites() function (after load_zombie_sprites(), before cache clear) |
| `zombie-shooter/src/game/entities/player.py` | UPDATE | Add sprite loading imports, module cache function, modify __init__/update/draw methods |
| `zombie-shooter/tests/test_asset_loading.py` | UPDATE | Add tests for load_player_sprites() - structure, caching, dimensions |
| `zombie-shooter/tests/test_player_integration.py` | CREATE | New test file for player sprite integration (mirror test_zombie_integration.py) |

---

## NOT Building (Scope Limits)

Explicit exclusions to prevent scope creep:

- **Shooting animation** - Deferred to Phase 3; this phase only implements walk animations
- **Idle animation** - Using walk frame 0 (same as zombie pattern); dedicated idle deferred
- **Damage/hit animation** - Not in scope; player damage shown via HP counter only
- **Death animation** - Not in scope; game over screen handles player death
- **Per-weapon sprite variants** - Not in scope; one character appearance for all weapons
- **Character customization** - Not in scope; single Rambo character only
- **Sprite visual improvements** - Asset generation complete in Phase 1; no sprite modifications here

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: UPDATE `constants.py` - Add player sprite constants

- **ACTION**: ADD three new constants after PLAYER_MAX_HP (line 13)
- **IMPLEMENT**:
  ```python
  PLAYER_ANIMATION_FPS = 10  # Frame rate for walk cycle animation
  PLAYER_SPRITE_SIZE = 48  # Width/height of sprite in pixels
  PLAYER_FRAME_COUNT = 3  # Number of frames per direction (walk cycle)
  ```
- **MIRROR**: `constants.py:65-71` - zombie constants pattern with comments
- **RATIONALE**: Match zombie values (48px, 3 frames, 10 FPS) for visual consistency
- **GOTCHA**: Place after PLAYER constants block (lines 10-13), before CONTACT_DPS
- **VALIDATE**:
  ```bash
  cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter
  .venv/bin/ruff check src/game/core/constants.py
  ```
  **EXPECT**: Exit 0, no errors

### Task 2: UPDATE `loader.py` - Add load_player_sprites() function

- **ACTION**: ADD new function `load_player_sprites()` after `load_zombie_sprites()` (after line 124, before `clear_cache()`)
- **IMPLEMENT**: Function following exact pattern from load_zombie_sprites() but for player directory
  - Cache key: `"player"` (no variant needed)
  - Directory: `ASSETS_DIR / "players"`
  - File pattern: `f"walk_{direction}.png"`
  - Return same structure: `dict[str, list[pygame.Surface]]`
  - Use existing `load_image()` and `split_sprite_sheet()` helpers
- **MIRROR**: `loader.py:74-124` - exact function structure, cache check, directory handling, frame splitting
- **IMPORTS**: None needed (all helpers already imported)
- **GOTCHA**: No variant parameter for player (simpler than zombie); cache key is just `"player"`
- **VALIDATE**:
  ```bash
  cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter
  .venv/bin/ruff check src/game/assets/loader.py
  .venv/bin/python -c "from game.assets.loader import load_player_sprites; sprites = load_player_sprites(); print('✓ load_player_sprites() works:', 'down' in sprites)"
  ```
  **EXPECT**: Linting passes, function imports and executes, prints "✓ load_player_sprites() works: True"

### Task 3: UPDATE `player.py` - Add sprite loading and Animation integration

- **ACTION**: MODIFY Player class to load sprites and integrate Animation
- **IMPLEMENT**:
  1. **Add imports** (after line 6):
     ```python
     from game.systems.animation import Animation
     from game.assets.loader import load_player_sprites
     from game.core.constants import (
         PLAYER_SPRITE_SIZE,
         PLAYER_FRAME_COUNT,
         PLAYER_ANIMATION_FPS,
     )
     ```

  2. **Add module-level cache function** (after imports, before Player class):
     ```python
     # Module-level sprite loading (shared across all instances)
     _player_sprites: dict[str, list[pygame.Surface]] | None = None

     def _load_sprites() -> dict[str, list[pygame.Surface]]:
         """Load player sprites once and cache at module level."""
         global _player_sprites
         if _player_sprites is None:
             _player_sprites = load_player_sprites(
                 sprite_size=PLAYER_SPRITE_SIZE,
                 frame_count=PLAYER_FRAME_COUNT,
             )
         return _player_sprites
     ```

  3. **Modify Player.__init__()** (add after line 36):
     ```python
     # Load sprites and create animation instance
     self.sprites = _load_sprites()
     self.animation = Animation(
         frame_count=PLAYER_FRAME_COUNT, fps=PLAYER_ANIMATION_FPS
     )
     ```

  4. **Modify Player.update()** (add after line 63, after velocity calculation):
     ```python
     # Update animation based on current velocity
     self.animation.update(dt, self.vel)
     ```

  5. **Replace Player.draw()** (lines 146-155, entire method):
     ```python
     def draw(self, screen: pygame.Surface) -> None:
         """Draw player to screen."""
         # Get current animation frame
         direction = self.animation.get_current_direction()
         frame_index = self.animation.get_current_frame_index()
         sprite = self.sprites[direction][frame_index]

         # Center sprite on player position
         sprite_rect = sprite.get_rect(center=(int(self.pos.x), int(self.pos.y)))
         screen.blit(sprite, sprite_rect)
     ```

- **MIRROR**: `zombie.py:16-115` - exact integration pattern (cache, init, update, draw)
- **GOTCHA**: Player already has `self.vel` initialized (line 30) - perfect for animation.update()
- **VALIDATE**:
  ```bash
  cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter
  .venv/bin/ruff check src/game/entities/player.py
  .venv/bin/python -c "
  import pygame
  pygame.init()
  from game.entities.player import Player
  player = Player(pygame.Vector2(400, 300))
  print('✓ Player initializes with sprites:', hasattr(player, 'sprites'))
  print('✓ Player has animation:', hasattr(player, 'animation'))
  "
  ```
  **EXPECT**: Linting passes, Player initializes with sprites and animation attributes

### Task 4: UPDATE `test_asset_loading.py` - Add player sprite loading tests

- **ACTION**: ADD test functions for load_player_sprites() after zombie sprite tests (after line 147)
- **IMPLEMENT**: Three test functions mirroring zombie sprite tests:
  1. `test_load_player_sprites_structure()` - Verify directions, frame count, dimensions
  2. `test_load_player_sprites_caching()` - Verify caching works (same object returned)
  3. `test_player_sprite_files_exist()` - Verify all 4 walk sprite files exist in assets/players/
- **MIRROR**: `test_asset_loading.py:84-147` - exact test structure for player
- **IMPORTS**: `load_player_sprites, PLAYER_SPRITE_SIZE, PLAYER_FRAME_COUNT` (add to existing imports)
- **GOTCHA**: Use `PLAYER_SPRITE_SIZE` and `PLAYER_FRAME_COUNT` constants, not zombie values
- **VALIDATE**:
  ```bash
  cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter
  export PYTHONPATH="src"
  .venv/bin/pytest tests/test_asset_loading.py::test_load_player_sprites_structure -v
  .venv/bin/pytest tests/test_asset_loading.py::test_load_player_sprites_caching -v
  .venv/bin/pytest tests/test_asset_loading.py::test_player_sprite_files_exist -v
  ```
  **EXPECT**: All 3 tests pass

### Task 5: CREATE `test_player_integration.py` - Integration tests for player sprite system

- **ACTION**: CREATE new test file mirroring test_zombie_integration.py
- **IMPLEMENT**: Test functions (minimum 5 tests):
  1. `test_player_has_animation_instance()` - Verify Player.animation exists
  2. `test_player_has_sprites_loaded()` - Verify Player.sprites has all directions
  3. `test_player_has_velocity_attribute()` - Verify Player.vel exists (required for animation)
  4. `test_player_animation_updates_on_movement()` - Simulate movement, verify animation updates
  5. `test_player_renders_without_error()` - Call draw() without exceptions
- **MIRROR**: `test_zombie_integration.py:13-122` - exact test patterns for player
- **IMPORTS**: `Player, Animation, PLAYER_FRAME_COUNT, PLAYER_ANIMATION_FPS, PLAYER_SPRITE_SIZE`
- **GOTCHA**: Player doesn't need `player_pos` parameter in update() (uses keyboard input); test with `player.update(0.1)` only
- **VALIDATE**:
  ```bash
  cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter
  export PYTHONPATH="src"
  .venv/bin/pytest tests/test_player_integration.py -v
  ```
  **EXPECT**: All tests pass (minimum 5 tests)

---

## Testing Strategy

### Unit Tests to Write

| Test File | Test Cases | Validates |
|-----------|------------|-----------|
| `test_asset_loading.py` | test_load_player_sprites_structure, test_load_player_sprites_caching, test_player_sprite_files_exist | Player sprite loading works correctly, caching enabled, files exist |
| `test_player_integration.py` | test_player_has_animation_instance, test_player_has_sprites_loaded, test_player_animation_updates_on_movement, test_player_renders_without_error | Player sprite system fully integrated, animation updates, rendering works |

### Edge Cases Checklist

- [x] Sprite loading handles missing files (already tested in zombie pattern)
- [x] Animation handles zero velocity (stationary - shows frame 0)
- [x] Animation handles all 4 cardinal directions (up, down, left, right)
- [x] Animation cycles frames correctly over time (frame 0 → 1 → 2 → 0)
- [x] Sprite positioning centers correctly on player position
- [x] Cache prevents re-loading sprites (same object returned)
- [x] Player.draw() doesn't crash with missing animation/sprites (tested in integration tests)

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter
.venv/bin/ruff check src/game/core/constants.py
.venv/bin/ruff check src/game/assets/loader.py
.venv/bin/ruff check src/game/entities/player.py
.venv/bin/ruff format src/game/core/constants.py
.venv/bin/ruff format src/game/assets/loader.py
.venv/bin/ruff format src/game/entities/player.py
```

**EXPECT**: Exit 0, no linting errors, code formatted

### Level 2: UNIT_TESTS

```bash
cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter
export PYTHONPATH="src"
.venv/bin/pytest tests/test_asset_loading.py::test_load_player_sprites_structure -v
.venv/bin/pytest tests/test_asset_loading.py::test_load_player_sprites_caching -v
.venv/bin/pytest tests/test_asset_loading.py::test_player_sprite_files_exist -v
.venv/bin/pytest tests/test_player_integration.py -v
```

**EXPECT**: All new tests pass (minimum 8 tests: 3 asset loading + 5 integration)

### Level 3: FULL_SUITE

```bash
cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter
export PYTHONPATH="src"
.venv/bin/pytest tests/ -v
```

**EXPECT**: All 118+ existing tests still pass (no regressions), new tests pass

### Level 4: MANUAL_VALIDATION

**Run the game and verify visually:**

```bash
cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter
export PYTHONPATH="src"
.venv/bin/python src/game/main.py
```

**Test checklist during gameplay:**
- [ ] Player character shows Rambo sprite (not blue circle)
- [ ] Walking with WASD shows 3-frame walk animation (legs moving)
- [ ] Walking up shows up-facing sprite
- [ ] Walking down shows down-facing sprite
- [ ] Walking left shows left-facing sprite
- [ ] Walking right shows right-facing sprite
- [ ] Stationary player shows idle stance (walk frame 0)
- [ ] Animation is smooth (10 FPS, no stuttering)
- [ ] Sprite is centered on player position (collision still works)
- [ ] Red headband visible (Rambo character appearance)
- [ ] 60 FPS maintained (no performance regression)

### Level 5: SMOKE_TEST

Quick validation that player sprite loads without errors:

```bash
cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter
.venv/bin/python -c "
import pygame
pygame.init()
from game.entities.player import Player

# Create player and verify sprite loading
player = Player(pygame.Vector2(400, 300))
print('Player sprites loaded:', 'down' in player.sprites)
print('Animation created:', player.animation is not None)
print('Animation FPS:', 1.0 / player.animation.frame_duration)
print('Frame count:', player.animation.frame_count)

# Verify all directions loaded
for direction in ['down', 'up', 'left', 'right']:
    frames = player.sprites[direction]
    print(f'{direction}: {len(frames)} frames, first frame: {frames[0].get_width()}x{frames[0].get_height()}')

print('✓ All checks passed')
"
```

**EXPECT**: Output shows all directions loaded with 3 frames each, 48x48 pixels, 10 FPS

---

## Acceptance Criteria

- [ ] Constants added to constants.py (PLAYER_SPRITE_SIZE=48, PLAYER_FRAME_COUNT=3, PLAYER_ANIMATION_FPS=10)
- [ ] load_player_sprites() function added to loader.py and works correctly
- [ ] Player class loads sprites via module-level cache
- [ ] Player class has Animation instance initialized with correct parameters
- [ ] Player.update() calls animation.update(dt, vel) every frame
- [ ] Player.draw() renders sprite (not circle) using current animation frame and direction
- [ ] All 4 directions animate correctly (up, down, left, right)
- [ ] Walk cycle shows 3-frame leg movement animation
- [ ] Stationary player shows idle stance (frame 0)
- [ ] Static analysis passes (ruff check, ruff format)
- [ ] All new unit tests pass (3 asset loading tests + 5 integration tests)
- [ ] All existing tests still pass (no regressions)
- [ ] Manual gameplay test confirms sprites visible and animating smoothly

---

## Completion Checklist

- [ ] Task 1: Constants added to constants.py
- [ ] Task 2: load_player_sprites() function added to loader.py
- [ ] Task 3: Player class modified (sprites, animation, update, draw)
- [ ] Task 4: Asset loading tests added to test_asset_loading.py
- [ ] Task 5: Integration tests created in test_player_integration.py
- [ ] Level 1: Static analysis passes (linting + formatting)
- [ ] Level 2: Unit tests pass (new tests)
- [ ] Level 3: Full test suite passes (no regressions)
- [ ] Level 4: Manual validation confirms sprites animate correctly
- [ ] Level 5: Smoke test passes
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Sprite positioning incorrect (not centered) | LOW | MEDIUM | Use exact zombie pattern with get_rect(center=...) - proven to work; test with manual gameplay |
| Animation doesn't match movement direction | LOW | MEDIUM | Animation.update() uses proven atan2-based direction detection from zombie system; already tested |
| Performance regression from sprite rendering | VERY LOW | LOW | Zombie system renders 50+ sprites at 60 FPS; single player sprite negligible cost |
| Sprite files not found at runtime | LOW | HIGH | Phase 1 already generated sprites; add test_player_sprite_files_exist() to catch this early |
| Animation not syncing with velocity | LOW | MEDIUM | Player.vel already exists (line 30); just needs animation.update(dt, vel) call - simple integration |
| Module cache causes stale sprites | VERY LOW | LOW | Same pattern as zombies - cache invalidation not needed for static assets |

---

## Notes

**Design Decisions:**

1. **Mirror zombie pattern exactly**: The zombie sprite integration is proven to work at scale (50+ entities) and has comprehensive tests. Using the same pattern ensures consistency and reduces risk.

2. **No variant system for player**: Unlike zombies (5 variants), player has single appearance. Simplified cache pattern: single global `_player_sprites` instead of dict keyed by variant.

3. **Same sprite size as zombies (48x48)**: Maintains visual consistency and allows reuse of existing constants/systems. Player and zombies share same animation FPS (10 FPS) for uniform feel.

4. **Walk frame 0 for idle**: Following zombie pattern - when stationary, animation resets to frame 0. No dedicated idle animation needed (deferred to Phase 4 polish if desired).

5. **Center-based positioning**: Using `sprite_rect.center` ensures sprite centers on player.pos, maintaining collision accuracy with existing hitbox system.

**Trade-offs:**

- **Simple vs Complex**: Could add per-direction idle frames, but using walk frame 0 is simpler and matches zombie system.
- **Cache strategy**: Could use per-instance sprites, but module-level cache is more efficient (single load for all Player instances, though game only has one).

**Future Considerations (Phase 3):**

- Shooting animation integration will add `is_shooting` flag and conditional rendering in draw()
- Shoot sprites already exist from Phase 1 (`shoot_*.png`) but not loaded yet
- Phase 3 will need to modify load_player_sprites() to also load shoot sprites or create separate load function

**Performance Notes:**

- Single sprite blit per frame (player) vs previous circle draw - negligible difference
- Sprite caching means no per-frame file I/O
- Animation frame calculation is simple integer math - no performance concern
- Proven at scale with zombie system (50+ simultaneous animated entities at 60 FPS)

**Integration Points:**

- PlayScene already calls player.update(dt) and player.draw(screen) - no changes needed there
- Player.vel already calculated correctly in update() - perfect input for animation system
- Animation class already tested thoroughly in test_animation.py - no changes needed
- Asset loading infrastructure already exists and is proven - just adding one function

---

*Generated: 2026-02-10*
*Phase: 2 of 4*
*Depends on: Phase 1 (complete)*
*Enables: Phase 3 (shooting animation)*
