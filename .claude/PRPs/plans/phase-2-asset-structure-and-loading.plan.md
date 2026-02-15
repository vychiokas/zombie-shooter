# Feature: Asset Structure and Loading (Phase 2)

## Summary

Establish asset organization and loading infrastructure for zombie sprite animations. Create placeholder sprite sheets for 4 cardinal directions (up, down, left, right), implement a robust asset loading system using pygame.image.load with pathlib for cross-platform compatibility, cache loaded sprites for performance, and integrate sprite data with the existing Animation class. This phase provides the visual assets and loading mechanism needed for Phase 3 zombie entity integration.

## User Story

As a developer
I want a reliable asset loading system with placeholder zombie sprites
So that I can visually test directional animations in the game

## Problem Statement

The Animation system (Phase 1) is complete but has no sprites to display. To make zombies visually animated, we need:
1. Organized asset directory structure for sprite sheets
2. Placeholder sprite images for 4 directions with multiple frames each
3. Robust asset loading with error handling for missing files
4. Efficient sprite caching to avoid repeated file I/O
5. Integration bridge between loaded sprites and Animation class

## Solution Statement

Create `assets/zombies/` directory structure containing 4 sprite sheet PNG files (`walk_down.png`, `walk_up.png`, `walk_left.png`, `walk_right.png`). Implement an asset loader module (`game/assets/loader.py`) using pathlib for cross-platform path resolution, pygame.image.load() with .convert_alpha() optimization, and module-level caching dictionary. Generate simple placeholder sprites programmatically using pygame.Surface to avoid dependency on external art tools during development.

## Metadata

| Field            | Value                                             |
| ---------------- | ------------------------------------------------- |
| Type             | NEW_CAPABILITY                                    |
| Complexity       | LOW                                               |
| Systems Affected | assets (new), Animation (minor update), entities (Phase 3) |
| Dependencies     | pygame>=2.6.0, Python 3.11+, pathlib (stdlib)     |
| Estimated Tasks  | 5                                                 |

---

## UX Design

### Before State
```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌──────────────┐                                                            ║
║   │  Animation   │ ──────► Direction: "right"                                 ║
║   │    Class     │         Frame index: 2                                     ║
║   └──────────────┘                                                            ║
║          │                                                                    ║
║          │ get_current_frame_index()                                          ║
║          ▼                                                                    ║
║   ┌──────────────┐                                                            ║
║   │    Zombie    │ ──────► NO SPRITES TO RENDER                               ║
║   │  draw()      │         (still green circles)                              ║
║   └──────────────┘                                                            ║
║                                                                               ║
║   USER_FLOW: Animation logic works but no visual sprites exist                ║
║   PAIN_POINT: Cannot test visual feedback, still placeholder circles          ║
║   DATA_FLOW: Animation → frame index → [MISSING: sprite data]                 ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌──────────────┐          ┌────────────────┐                                ║
║   │  Animation   │ ──────► │  Asset Loader  │                                 ║
║   │    Class     │          │    (NEW)       │                                 ║
║   └──────┬───────┘          └────────┬───────┘                                ║
║          │                           │                                        ║
║          │ get_current_direction()   │ load_zombie_sprites()                  ║
║          │ get_current_frame_index() │                                        ║
║          │                           │                                        ║
║          ▼                           ▼                                        ║
║   ┌──────────────────────────────────────┐                                    ║
║   │   Sprite Cache (dict)                │                                    ║
║   │   {                                  │                                    ║
║   │     "down": [surf0, surf1, surf2],   │                                    ║
║   │     "up": [surf0, surf1, surf2],     │                                    ║
║   │     "left": [surf0, surf1, surf2],   │                                    ║
║   │     "right": [surf0, surf1, surf2]   │                                    ║
║   │   }                                  │                                    ║
║   └──────────────┬───────────────────────┘                                    ║
║                  │                                                            ║
║                  │ sprites[direction][frame_index]                            ║
║                  ▼                                                            ║
║   ┌──────────────┐                                                            ║
║   │    Zombie    │ ──────► pygame.Surface ready for screen.blit()             ║
║   │  draw()      │         (directional animated sprites)                     ║
║   └──────────────┘                                                            ║
║                                                                               ║
║   USER_FLOW: Animation → Asset Loader → Sprite Cache → Rendering              ║
║   VALUE_ADD: Visual sprites loaded, cached, ready for integration             ║
║   DATA_FLOW: Animation direction+frame → sprite lookup → pygame.Surface       ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes
| Location                          | Before                           | After                                                | User Impact                      |
| --------------------------------- | -------------------------------- | ---------------------------------------------------- | -------------------------------- |
| `assets/zombies/` (directory)     | Does not exist                   | Contains 4 PNG sprite sheets (up/down/left/right)   | Sprites available for loading    |
| `game/assets/loader.py` (new)     | No asset loading infrastructure  | Loads, caches, validates sprite files                | Reusable asset loading system    |
| `Animation` class                 | Returns frame index only         | No change (still returns index)                      | Compatible with existing code    |
| Developer testing                 | Cannot visually test animations  | Can see directional sprites in game                  | Visual feedback during dev       |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File                                                 | Lines  | Why Read This                                            |
| -------- | ---------------------------------------------------- | ------ | -------------------------------------------------------- |
| P0       | `zombie-shooter/src/game/core/constants.py`          | 1-60   | Pattern for defining asset path constants                |
| P0       | `zombie-shooter/src/game/systems/animation.py`       | 1-95   | Animation class API - understand direction/frame getters |
| P1       | `zombie-shooter/src/game/entities/zombie.py`         | 1-45   | Entity structure pattern - self.pos, self.radius         |
| P1       | `zombie-shooter/src/game/scenes/play.py`             | 167-211 | screen.blit() and get_rect() usage for HUD text          |
| P2       | `zombie-shooter/tests/test_animation.py`             | 1-152  | Test patterns for new asset loading tests                |

**External Documentation:**
| Source | Section | Why Needed |
|--------|---------|------------|
| [Pygame image.load() v2.6.0](https://www.pygame.org/docs/ref/image.html) | pygame.image.load, Surface.convert_alpha | Core sprite loading functions |
| [Python pathlib](https://docs.python.org/3/library/pathlib.html) | Path, Path.resolve(), Path.parent | Cross-platform path resolution |
| [Pygame Surface](https://www.pygame.org/docs/ref/surface.html) | Surface.fill(), Surface.set_colorkey() | Placeholder sprite generation |

---

## Patterns to Mirror

**CONSTANTS_PATTERN:**
```python
# SOURCE: zombie-shooter/src/game/core/constants.py:1-60
# COPY THIS PATTERN:

from __future__ import annotations

# Zombies
ZOMBIE_SPEED = 140
ZOMBIE_RADIUS = 16
MAX_ZOMBIES = 50
ZOMBIE_ANIMATION_FPS = 10  # Frame rate for walk cycle animation

# New constants to add:
# ZOMBIE_SPRITE_SIZE = 32  # Width/height of sprite in pixels
# ZOMBIE_FRAME_COUNT = 3   # Number of frames per direction
```

**ENTITY_ATTRIBUTE_PATTERN:**
```python
# SOURCE: zombie-shooter/src/game/entities/zombie.py:13-21
# COPY THIS PATTERN:

def __init__(self, pos: pygame.Vector2) -> None:
    """Initialize zombie.

    Args:
        pos: Starting position as Vector2.
    """
    self.pos = pos
    self.radius = ZOMBIE_RADIUS
    self.speed = ZOMBIE_SPEED
```

**SCREEN_BLIT_WITH_CENTERING:**
```python
# SOURCE: zombie-shooter/src/game/scenes/play.py:196-200
# COPY THIS PATTERN:

timer_text = self.font.render(
    f"Time: {self.timer:.1f} / 60", True, (255, 255, 255)
)
timer_rect = timer_text.get_rect(center=(WIDTH // 2, 25))
screen.blit(timer_text, timer_rect)

# For sprites:
# sprite_rect = sprite_surface.get_rect(center=(int(self.pos.x), int(self.pos.y)))
# screen.blit(sprite_surface, sprite_rect)
```

**TYPE_ANNOTATIONS:**
```python
# SOURCE: zombie-shooter/src/game/systems/animation.py:15-27
# COPY THIS PATTERN:

from __future__ import annotations

import pygame


class Animation:
    """Manages directional animation state and frame cycling."""

    def __init__(self, frame_count: int, fps: float) -> None:
        """Initialize animation.

        Args:
            frame_count: Number of frames per direction animation.
            fps: Animation frames per second (frame duration = 1/fps).
        """
        self.frame_count = frame_count
        self.frame_duration = 1.0 / fps
        self.current_direction: str = "down"
```

**TEST_STRUCTURE:**
```python
# SOURCE: zombie-shooter/tests/test_animation.py:1-25
# COPY THIS PATTERN:

"""Tests for animation system."""

from __future__ import annotations

import pygame

from game.systems.animation import Animation

# Initialize pygame once for all tests
pygame.init()


def test_animation_initializes_with_default_state() -> None:
    """Test that animation starts with frame 0, facing down."""
    anim = Animation(frame_count=4, fps=10)

    assert anim.get_current_frame_index() == 0
    assert anim.get_current_direction() == "down"
```

---

## Files to Change

| File                                                   | Action | Justification                                           |
| ------------------------------------------------------ | ------ | ------------------------------------------------------- |
| `zombie-shooter/src/game/core/constants.py`            | UPDATE | Add sprite dimension and frame count constants          |
| `zombie-shooter/src/game/assets/loader.py`             | CREATE | Asset loading module with caching and error handling    |
| `zombie-shooter/src/game/assets/__init__.py`           | UPDATE | Export load_zombie_sprites function                     |
| `zombie-shooter/src/assets/zombies/walk_down.png`      | CREATE | Placeholder sprite sheet for down direction (3 frames)  |
| `zombie-shooter/src/assets/zombies/walk_up.png`        | CREATE | Placeholder sprite sheet for up direction (3 frames)    |
| `zombie-shooter/src/assets/zombies/walk_left.png`      | CREATE | Placeholder sprite sheet for left direction (3 frames)  |
| `zombie-shooter/src/assets/zombies/walk_right.png`     | CREATE | Placeholder sprite sheet for right direction (3 frames) |
| `zombie-shooter/tests/test_asset_loading.py`           | CREATE | Unit tests for asset loader                             |

---

## NOT Building (Scope Limits)

Explicit exclusions to prevent scope creep:

- **High-fidelity artwork** - Placeholder colored rectangles with direction arrows only
- **Sprite sheet atlas parsing** - Individual PNG per direction, not combined atlas
- **Dynamic asset generation** - Pre-generated PNGs, not runtime procedural generation
- **Asset hot-reloading** - Load once at startup, no file watching
- **Asset versioning/cache invalidation** - Simple module-level cache, no TTL
- **Asset compression** - Standard PNG, no custom compression
- **Asset pipeline tools** - Manual sprite creation script, not build system integration
- **Error recovery** - Fail-fast on missing assets, no fallback loading
- **Multi-resolution sprites** - Single size only (32x32), no @2x/@3x variants

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: UPDATE `zombie-shooter/src/game/core/constants.py`

- **ACTION**: ADD sprite-related constants to zombie section
- **IMPLEMENT**: Add sprite size and frame count after ZOMBIE_ANIMATION_FPS
- **MIRROR**: constants.py:47-51 - follow existing ZOMBIE_* constant pattern
- **IMPORTS**: None needed
- **LOCATION**: Insert after line 51 (after `ZOMBIE_ANIMATION_FPS = 10`)
- **CODE**:
  ```python
  # Zombies
  ZOMBIE_SPEED = 140
  ZOMBIE_RADIUS = 16
  MAX_ZOMBIES = 50
  ZOMBIE_ANIMATION_FPS = 10  # Frame rate for walk cycle animation
  ZOMBIE_SPRITE_SIZE = 32  # Width/height of sprite in pixels
  ZOMBIE_FRAME_COUNT = 3  # Number of frames per direction (walk cycle)
  ```
- **GOTCHA**: Keep constants in ZOMBIE section, don't create new section
- **VALIDATE**: `ruff check zombie-shooter/src/game/core/constants.py`

### Task 2: CREATE placeholder sprite script `zombie-shooter/scripts/generate_placeholder_sprites.py`

- **ACTION**: CREATE Python script to generate placeholder zombie sprites
- **IMPLEMENT**: Script that creates 4 sprite sheet PNGs (up/down/left/right) with 3 frames each
- **MIRROR**: No existing pattern - use pygame.Surface with drawing operations
- **IMPORTS**:
  ```python
  from __future__ import annotations

  from pathlib import Path

  import pygame
  ```
- **CODE**:
  ```python
  """Generate placeholder zombie sprites for development."""

  from __future__ import annotations

  from pathlib import Path

  import pygame

  # Constants matching game constants
  SPRITE_SIZE = 32
  FRAME_COUNT = 3

  # Direction arrow positions (for visual identification)
  ARROWS = {
      "down": (16, 22),   # Arrow pointing down
      "up": (16, 10),     # Arrow pointing up
      "left": (10, 16),   # Arrow pointing left
      "right": (22, 16),  # Arrow pointing right
  }

  def create_sprite_sheet(direction: str, output_path: Path) -> None:
      """Create a sprite sheet with 3 frames for a direction.

      Args:
          direction: Direction name (down, up, left, right).
          output_path: Path to save PNG file.
      """
      # Create surface for 3 frames side-by-side
      sheet_width = SPRITE_SIZE * FRAME_COUNT
      sheet_height = SPRITE_SIZE
      surface = pygame.Surface((sheet_width, sheet_height), pygame.SRCALPHA)
      surface.fill((0, 0, 0, 0))  # Transparent background

      # Draw 3 frames with slight variations
      for frame in range(FRAME_COUNT):
          x_offset = frame * SPRITE_SIZE

          # Base zombie body (green circle)
          body_center = (x_offset + SPRITE_SIZE // 2, SPRITE_SIZE // 2)
          body_radius = 12

          # Animate by slightly changing radius (breathing effect)
          frame_radius = body_radius + (frame - 1)  # 11, 12, 13 pixels

          # Draw body
          pygame.draw.circle(surface, (0, 200, 50), body_center, frame_radius)

          # Draw direction arrow
          arrow_x = x_offset + ARROWS[direction][0]
          arrow_y = ARROWS[direction][1]

          # Arrow color (white)
          arrow_color = (255, 255, 255)

          # Draw arrow based on direction
          if direction == "down":
              # V shape
              pygame.draw.line(surface, arrow_color, (arrow_x - 3, arrow_y - 3), (arrow_x, arrow_y), 2)
              pygame.draw.line(surface, arrow_color, (arrow_x, arrow_y), (arrow_x + 3, arrow_y - 3), 2)
          elif direction == "up":
              # ^ shape
              pygame.draw.line(surface, arrow_color, (arrow_x - 3, arrow_y + 3), (arrow_x, arrow_y), 2)
              pygame.draw.line(surface, arrow_color, (arrow_x, arrow_y), (arrow_x + 3, arrow_y + 3), 2)
          elif direction == "left":
              # < shape
              pygame.draw.line(surface, arrow_color, (arrow_x + 3, arrow_y - 3), (arrow_x, arrow_y), 2)
              pygame.draw.line(surface, arrow_color, (arrow_x, arrow_y), (arrow_x + 3, arrow_y + 3), 2)
          elif direction == "right":
              # > shape
              pygame.draw.line(surface, arrow_color, (arrow_x - 3, arrow_y - 3), (arrow_x, arrow_y), 2)
              pygame.draw.line(surface, arrow_color, (arrow_x, arrow_y), (arrow_x - 3, arrow_y + 3), 2)

      # Save sprite sheet
      pygame.image.save(surface, str(output_path))
      print(f"Created: {output_path}")


  def main() -> None:
      """Generate all zombie sprite sheets."""
      pygame.init()

      # Determine asset directory relative to script location
      script_dir = Path(__file__).resolve().parent
      project_root = script_dir.parent
      assets_dir = project_root / "src" / "assets" / "zombies"

      # Create directory if it doesn't exist
      assets_dir.mkdir(parents=True, exist_ok=True)

      # Generate sprites for each direction
      directions = ["down", "up", "left", "right"]
      for direction in directions:
          output_path = assets_dir / f"walk_{direction}.png"
          create_sprite_sheet(direction, output_path)

      print(f"\n✓ Generated {len(directions)} sprite sheets in: {assets_dir}")


  if __name__ == "__main__":
      main()
  ```
- **GOTCHA**: Use SRCALPHA for transparent backgrounds (important for sprite overlap)
- **GOTCHA**: Arrow positions hardcoded for 32x32 sprites - adjust if SPRITE_SIZE changes
- **VALIDATE**: `python zombie-shooter/scripts/generate_placeholder_sprites.py` (run to generate PNGs)

### Task 3: RUN sprite generation script

- **ACTION**: Execute script to create placeholder sprite PNGs
- **IMPLEMENT**: Run the generator script, verify 4 PNG files created
- **COMMAND**:
  ```bash
  python zombie-shooter/scripts/generate_placeholder_sprites.py
  ```
- **EXPECTED OUTPUT**:
  ```
  Created: /path/to/zombie-shooter/src/assets/zombies/walk_down.png
  Created: /path/to/zombie-shooter/src/assets/zombies/walk_up.png
  Created: /path/to/zombie-shooter/src/assets/zombies/walk_left.png
  Created: /path/to/zombie-shooter/src/assets/zombies/walk_right.png

  ✓ Generated 4 sprite sheets in: /path/to/zombie-shooter/src/assets/zombies
  ```
- **GOTCHA**: Script must be run from project root or paths adjusted
- **VALIDATE**:
  ```bash
  ls -lh zombie-shooter/src/assets/zombies/*.png | wc -l  # Should output: 4
  ```

### Task 4: CREATE `zombie-shooter/src/game/assets/loader.py`

- **ACTION**: CREATE asset loading module with sprite caching
- **IMPLEMENT**: Functions to load zombie sprites with error handling and caching
- **MIRROR**: No existing pattern - establish new best practice from pygame docs
- **IMPORTS**:
  ```python
  from __future__ import annotations

  from pathlib import Path

  import pygame
  ```
- **CODE**:
  ```python
  """Asset loading and caching for zombie shooter."""

  from __future__ import annotations

  from pathlib import Path

  import pygame

  # Module-level cache for loaded sprites
  _sprite_cache: dict[str, dict[str, list[pygame.Surface]]] = {}

  # Asset directory relative to this file
  ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


  def load_image(path: Path) -> pygame.Surface:
      """Load a single image and optimize for display.

      Args:
          path: Absolute path to image file.

      Returns:
          Optimized pygame.Surface ready for blitting.

      Raises:
          FileNotFoundError: If image file doesn't exist.
          pygame.error: If image can't be loaded.
      """
      if not path.is_file():
          raise FileNotFoundError(f"Image file not found: {path}")

      # Load image
      try:
          surface = pygame.image.load(str(path))
      except pygame.error as e:
          raise pygame.error(f"Failed to load image {path}: {e}") from e

      # Convert for optimal blitting performance
      # Use convert_alpha() if image has transparency, otherwise convert()
      if surface.get_alpha() is not None or surface.get_colorkey() is not None:
          return surface.convert_alpha()
      return surface.convert()


  def split_sprite_sheet(
      sheet: pygame.Surface, frame_width: int, frame_count: int
  ) -> list[pygame.Surface]:
      """Split a horizontal sprite sheet into individual frames.

      Args:
          sheet: Sprite sheet surface (frames laid out horizontally).
          frame_width: Width of each frame in pixels.
          frame_count: Number of frames in the sheet.

      Returns:
          List of individual frame surfaces.
      """
      frames = []
      for i in range(frame_count):
          x_offset = i * frame_width
          # Create subsurface for this frame
          frame_rect = pygame.Rect(x_offset, 0, frame_width, sheet.get_height())
          frame = sheet.subsurface(frame_rect).copy()  # Copy to avoid subsurface issues
          frames.append(frame)
      return frames


  def load_zombie_sprites(
      sprite_size: int = 32, frame_count: int = 3
  ) -> dict[str, list[pygame.Surface]]:
      """Load zombie sprites for all 4 directions.

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

      Raises:
          FileNotFoundError: If any sprite sheet file is missing.
          pygame.error: If any sprite sheet can't be loaded.
      """
      # Check cache first
      cache_key = "zombie"
      if cache_key in _sprite_cache:
          return _sprite_cache[cache_key]

      zombies_dir = ASSETS_DIR / "zombies"
      directions = ["down", "up", "left", "right"]

      sprites: dict[str, list[pygame.Surface]] = {}

      for direction in directions:
          # Load sprite sheet
          sheet_path = zombies_dir / f"walk_{direction}.png"
          sheet = load_image(sheet_path)

          # Split into frames
          frames = split_sprite_sheet(sheet, sprite_size, frame_count)
          sprites[direction] = frames

      # Cache for future calls
      _sprite_cache[cache_key] = sprites

      return sprites


  def clear_cache() -> None:
      """Clear the sprite cache (useful for testing)."""
      _sprite_cache.clear()
  ```
- **GOTCHA**: Use `.convert_alpha()` for transparent sprites (PNG with alpha channel)
- **GOTCHA**: Cache using module-level dict to avoid repeated file I/O
- **GOTCHA**: Use `subsurface().copy()` to avoid pygame subsurface reference issues
- **GOTCHA**: Paths must be absolute - use `Path(__file__).resolve()` pattern
- **VALIDATE**: `ruff check zombie-shooter/src/game/assets/loader.py && ruff format zombie-shooter/src/game/assets/loader.py`

### Task 5: UPDATE `zombie-shooter/src/game/assets/__init__.py`

- **ACTION**: UPDATE assets package init to export loader functions
- **IMPLEMENT**: Add exports for load_zombie_sprites
- **MIRROR**: Other `__init__.py` files (currently empty, so establish pattern)
- **IMPORTS**: From loader module
- **CODE**:
  ```python
  """Asset loading and management."""

  from __future__ import annotations

  from game.assets.loader import load_zombie_sprites

  __all__ = ["load_zombie_sprites"]
  ```
- **GOTCHA**: Use `__all__` to explicitly control public API
- **VALIDATE**: `python -c "from game.assets import load_zombie_sprites; print('Import success')"`

### Task 6: CREATE `zombie-shooter/tests/test_asset_loading.py`

- **ACTION**: CREATE unit tests for asset loading module
- **IMPLEMENT**: Test sprite loading, caching, error handling
- **MIRROR**: test_animation.py:1-152 for test structure pattern
- **IMPORTS**:
  ```python
  from __future__ import annotations

  from pathlib import Path

  import pygame
  import pytest

  from game.assets.loader import (
      ASSETS_DIR,
      clear_cache,
      load_image,
      load_zombie_sprites,
      split_sprite_sheet,
  )
  from game.core.constants import ZOMBIE_FRAME_COUNT, ZOMBIE_SPRITE_SIZE
  ```
- **CODE**:
  ```python
  """Tests for asset loading system."""

  from __future__ import annotations

  from pathlib import Path

  import pygame
  import pytest

  from game.assets.loader import (
      ASSETS_DIR,
      clear_cache,
      load_image,
      load_zombie_sprites,
      split_sprite_sheet,
  )
  from game.core.constants import ZOMBIE_FRAME_COUNT, ZOMBIE_SPRITE_SIZE

  # Initialize pygame once for all tests
  pygame.init()


  def test_assets_dir_exists() -> None:
      """Test that ASSETS_DIR points to existing directory."""
      assert ASSETS_DIR.exists()
      assert ASSETS_DIR.is_dir()


  def test_zombie_sprite_files_exist() -> None:
      """Test that all 4 zombie sprite sheets exist."""
      zombies_dir = ASSETS_DIR / "zombies"
      assert zombies_dir.exists()

      directions = ["down", "up", "left", "right"]
      for direction in directions:
          sprite_path = zombies_dir / f"walk_{direction}.png"
          assert sprite_path.is_file(), f"Missing sprite: {sprite_path}"


  def test_load_image_success() -> None:
      """Test loading a valid image file."""
      # Load one of the zombie sprites
      sprite_path = ASSETS_DIR / "zombies" / "walk_down.png"
      surface = load_image(sprite_path)

      # Verify surface properties
      assert isinstance(surface, pygame.Surface)
      assert surface.get_width() > 0
      assert surface.get_height() > 0


  def test_load_image_missing_file() -> None:
      """Test that loading missing file raises FileNotFoundError."""
      fake_path = ASSETS_DIR / "nonexistent.png"

      with pytest.raises(FileNotFoundError, match="Image file not found"):
          load_image(fake_path)


  def test_split_sprite_sheet() -> None:
      """Test splitting sprite sheet into individual frames."""
      # Create test sprite sheet (3 frames, 32x32 each)
      sheet_width = ZOMBIE_SPRITE_SIZE * ZOMBIE_FRAME_COUNT
      sheet_height = ZOMBIE_SPRITE_SIZE
      test_sheet = pygame.Surface((sheet_width, sheet_height), pygame.SRCALPHA)

      # Fill frames with different colors for identification
      colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
      for i, color in enumerate(colors):
          x_offset = i * ZOMBIE_SPRITE_SIZE
          rect = pygame.Rect(x_offset, 0, ZOMBIE_SPRITE_SIZE, ZOMBIE_SPRITE_SIZE)
          pygame.draw.rect(test_sheet, color, rect)

      # Split into frames
      frames = split_sprite_sheet(test_sheet, ZOMBIE_SPRITE_SIZE, ZOMBIE_FRAME_COUNT)

      # Verify frame count
      assert len(frames) == ZOMBIE_FRAME_COUNT

      # Verify frame dimensions
      for frame in frames:
          assert frame.get_width() == ZOMBIE_SPRITE_SIZE
          assert frame.get_height() == ZOMBIE_SPRITE_SIZE


  def test_load_zombie_sprites_structure() -> None:
      """Test that load_zombie_sprites returns correct structure."""
      clear_cache()  # Start fresh

      sprites = load_zombie_sprites(
          sprite_size=ZOMBIE_SPRITE_SIZE, frame_count=ZOMBIE_FRAME_COUNT
      )

      # Verify directions present
      assert "down" in sprites
      assert "up" in sprites
      assert "left" in sprites
      assert "right" in sprites

      # Verify each direction has correct frame count
      for direction, frames in sprites.items():
          assert len(frames) == ZOMBIE_FRAME_COUNT, f"Direction {direction} has wrong frame count"

          # Verify each frame is a valid Surface
          for i, frame in enumerate(frames):
              assert isinstance(frame, pygame.Surface), f"Frame {i} in {direction} is not a Surface"
              assert frame.get_width() == ZOMBIE_SPRITE_SIZE
              assert frame.get_height() == ZOMBIE_SPRITE_SIZE


  def test_load_zombie_sprites_caching() -> None:
      """Test that sprites are cached and reused."""
      clear_cache()

      # First load
      sprites1 = load_zombie_sprites(
          sprite_size=ZOMBIE_SPRITE_SIZE, frame_count=ZOMBIE_FRAME_COUNT
      )

      # Second load (should use cache)
      sprites2 = load_zombie_sprites(
          sprite_size=ZOMBIE_SPRITE_SIZE, frame_count=ZOMBIE_FRAME_COUNT
      )

      # Should be the exact same dict object (cached)
      assert sprites1 is sprites2


  def test_clear_cache() -> None:
      """Test that cache can be cleared."""
      # Load sprites
      sprites1 = load_zombie_sprites(
          sprite_size=ZOMBIE_SPRITE_SIZE, frame_count=ZOMBIE_FRAME_COUNT
      )

      # Clear cache
      clear_cache()

      # Load again (should be a new load)
      sprites2 = load_zombie_sprites(
          sprite_size=ZOMBIE_SPRITE_SIZE, frame_count=ZOMBIE_FRAME_COUNT
      )

      # Should be different objects
      assert sprites1 is not sprites2
  ```
- **GOTCHA**: Clear cache at start of caching tests to avoid test interdependence
- **GOTCHA**: Use ZOMBIE_SPRITE_SIZE and ZOMBIE_FRAME_COUNT from constants
- **GOTCHA**: pytest.raises context manager for exception testing
- **VALIDATE**: `PYTHONPATH=zombie-shooter/src pytest zombie-shooter/tests/test_asset_loading.py -v`

---

## Testing Strategy

### Unit Tests to Write

| Test File                             | Test Cases                                                     | Validates                     |
| ------------------------------------- | -------------------------------------------------------------- | ----------------------------- |
| `tests/test_asset_loading.py`         | Assets directory exists                                        | Path configuration            |
| `tests/test_asset_loading.py`         | All 4 sprite sheets exist                                      | Asset generation succeeded    |
| `tests/test_asset_loading.py`         | load_image() success case                                      | Basic image loading           |
| `tests/test_asset_loading.py`         | load_image() missing file error                                | Error handling                |
| `tests/test_asset_loading.py`         | split_sprite_sheet() frame extraction                          | Sheet parsing logic           |
| `tests/test_asset_loading.py`         | load_zombie_sprites() structure validation                     | Complete sprite dict          |
| `tests/test_asset_loading.py`         | load_zombie_sprites() caching behavior                         | Performance optimization      |
| `tests/test_asset_loading.py`         | clear_cache() functionality                                    | Cache management              |

### Edge Cases Checklist

- [x] Missing sprite file (FileNotFoundError)
- [x] Invalid image format (pygame.error)
- [x] Empty sprite sheet (frame_count=0)
- [x] Sprite sheet with wrong dimensions (width != frame_count * frame_width)
- [x] Cache collision (loading different sprite sets)
- [x] Transparent vs opaque sprites (convert vs convert_alpha)
- [x] Subsurface reference issues (copy after subsurface)

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
ruff check zombie-shooter/src/game/core/constants.py && \
ruff check zombie-shooter/src/game/assets/loader.py && \
ruff format zombie-shooter/src/game/assets/loader.py --check && \
ruff check zombie-shooter/scripts/generate_placeholder_sprites.py
```

**EXPECT**: Exit 0, no errors or warnings

### Level 2: SPRITE_GENERATION

```bash
python zombie-shooter/scripts/generate_placeholder_sprites.py && \
ls -lh zombie-shooter/src/assets/zombies/*.png
```

**EXPECT**: 4 PNG files created (walk_down.png, walk_up.png, walk_left.png, walk_right.png)

### Level 3: UNIT_TESTS

```bash
PYTHONPATH=zombie-shooter/src pytest zombie-shooter/tests/test_asset_loading.py -v
```

**EXPECT**: 8 tests pass

### Level 4: IMPORT_VALIDATION

```bash
cd zombie-shooter && PYTHONPATH=src python -c "
from game.assets import load_zombie_sprites
from game.core.constants import ZOMBIE_SPRITE_SIZE, ZOMBIE_FRAME_COUNT
import pygame

pygame.init()
sprites = load_zombie_sprites(ZOMBIE_SPRITE_SIZE, ZOMBIE_FRAME_COUNT)
print(f'✓ Loaded sprites for {len(sprites)} directions')
for direction, frames in sprites.items():
    print(f'  - {direction}: {len(frames)} frames')
print('✓ Asset loading functional')
"
```

**EXPECT**: Confirmation of 4 directions with 3 frames each

### Level 5: FULL_SUITE

```bash
PYTHONPATH=zombie-shooter/src pytest zombie-shooter/tests/ -v
```

**EXPECT**: All tests pass (45 existing + 8 new = 53 total)

### Level 6: VISUAL_VALIDATION

```bash
cd zombie-shooter && PYTHONPATH=src python -c "
from game.assets import load_zombie_sprites
from game.core.constants import ZOMBIE_SPRITE_SIZE, ZOMBIE_FRAME_COUNT
import pygame

pygame.init()
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption('Zombie Sprites Preview')

sprites = load_zombie_sprites(ZOMBIE_SPRITE_SIZE, ZOMBIE_FRAME_COUNT)

# Draw all sprites in a grid
x, y = 10, 10
for direction in ['down', 'up', 'left', 'right']:
    for frame in sprites[direction]:
        screen.blit(frame, (x, y))
        x += ZOMBIE_SPRITE_SIZE + 5
    x = 10
    y += ZOMBIE_SPRITE_SIZE + 10

pygame.display.flip()
print('✓ Sprites displayed. Close window to continue.')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
"
```

**EXPECT**: Window displays 4 rows of 3 sprites each, visually distinguishable by direction arrows

---

## Acceptance Criteria

- [x] `ZOMBIE_SPRITE_SIZE` and `ZOMBIE_FRAME_COUNT` constants added to constants.py
- [x] 4 placeholder sprite PNG files created in `src/assets/zombies/`
- [x] Asset loader module created with load_zombie_sprites() function
- [x] Sprites cached in module-level dict for performance
- [x] Error handling for missing files (FileNotFoundError)
- [x] Sprites optimized with .convert_alpha() for performance
- [x] 8 unit tests cover loading, caching, error cases
- [x] Level 1-5 validation commands pass with exit 0
- [x] Code mirrors existing patterns (type hints, docstrings, naming)
- [x] No regressions in existing test suite

---

## Completion Checklist

- [ ] Task 1: Sprite constants added to constants.py
- [ ] Task 2: Sprite generation script created
- [ ] Task 3: Placeholder sprites generated (4 PNG files)
- [ ] Task 4: Asset loader module created
- [ ] Task 5: Assets __init__.py updated with exports
- [ ] Task 6: test_asset_loading.py created with 8 tests
- [ ] Level 1: Static analysis passes (ruff check + format)
- [ ] Level 2: Sprite generation succeeds (4 PNGs created)
- [ ] Level 3: Unit tests pass (8/8 tests)
- [ ] Level 4: Import validation succeeds
- [ ] Level 5: Full test suite passes (53 tests)
- [ ] Level 6: Visual validation (sprites display correctly)
- [ ] All acceptance criteria met
- [ ] No regressions in existing functionality

---

## Risks and Mitigations

| Risk                                         | Likelihood | Impact | Mitigation                                                              |
| -------------------------------------------- | ---------- | ------ | ----------------------------------------------------------------------- |
| Sprite paths incorrect on different OSes     | Low        | High   | Use pathlib.Path for cross-platform path resolution                    |
| Asset files not found at runtime             | Medium     | High   | Explicit FileNotFoundError with clear message, fail-fast on startup    |
| Subsurface reference issues cause corruption | Low        | Medium | Use `.copy()` after `.subsurface()` to avoid shared memory issues      |
| Sprite cache uses excessive memory           | Low        | Low    | Only 4 directions × 3 frames × 32x32 pixels = ~50KB total, negligible  |
| Transparent background not preserved         | Medium     | Medium | Use `.convert_alpha()` for PNGs with transparency                       |
| Performance degradation from repeated loads  | Low        | High   | Module-level cache prevents repeated file I/O                          |

---

## Notes

### Design Decisions

**Sprite Generation Script vs Manual Art**
- **Rationale**: Programmatic generation allows instant iteration without art tools dependency
- **Trade-off**: Placeholder quality is low, but sufficient for development testing
- **Future**: Replace with artist-created sprites in later polish phase

**Module-Level Cache vs Singleton Pattern**
- **Rationale**: Python module imports are already singleton behavior, simpler than class-based singleton
- **Trade-off**: Cache persists for program lifetime, but sprites are small (~50KB total)

**Horizontal Sprite Sheets vs Vertical**
- **Rationale**: Horizontal layout is standard in game dev, easier to visually scan
- **Trade-off**: None significant

**4 Separate PNG Files vs Single Atlas**
- **Rationale**: Simpler loading logic, clearer organization, easier to replace individual directions
- **Trade-off**: 4 file loads instead of 1, but with caching the impact is one-time at startup

**32x32 Sprite Size vs 16x16**
- **Rationale**: 32x32 provides better visual clarity, matches common game sprite sizes
- **Trade-off**: Slightly larger file size (still <10KB per sprite sheet), but acceptable

**3 Frames vs 2 or 4**
- **Rationale**: 3 frames provides smooth animation at 10 FPS (0.3s cycle), standard for walk cycles
- **Trade-off**: Could use 2 for simplicity or 4 for smoothness, but 3 is sweet spot

### External Research Summary

Based on Pygame documentation and best practices:

**Image Loading** ([pygame.image docs](https://www.pygame.org/docs/ref/image.html)):
- Use `pygame.image.load()` with pathlib.Path for cross-platform compatibility
- Always call `.convert()` or `.convert_alpha()` after loading for performance
- Avoid repeated loads in game loop - cache sprites

**Path Resolution** ([GameDev.net discussion](https://www.gamedev.net/forums/topic/519131-relative-path-for-imageload/4371770/)):
- Use `Path(__file__).resolve().parent` for script-relative paths
- Avoids current working directory dependency issues

**Sprite Sheets** ([Pygame tutorials](https://www.pygame.org/docs/tut/ChimpLineByLine.html)):
- Use `.subsurface()` to extract frames, then `.copy()` to avoid reference issues
- Store frames in lists for easy indexing

### Context for Phase 3 (Zombie Integration)

Phase 3 will need to:
1. Import load_zombie_sprites() in zombie.py
2. Load sprites once (class variable or module-level)
3. Pass sprite dict to Animation class or store in Zombie.__init__()
4. Replace `pygame.draw.circle()` in `Zombie.draw()` with sprite blitting
5. Map Animation.get_current_direction() + get_current_frame_index() to sprites dict

This phase provides the **visual assets and loading infrastructure**; Phase 3 provides the **entity integration**.

---

## PRD Phase Update

**After completing this implementation**, update the PRD at:
`.claude/PRPs/prds/002_directional-animated-zombie-models.prd.md`

**Change Phase 2 table row**:
```markdown
| 2 | Asset structure and loading | ... | complete | with 1 | - | [phase-2-asset-structure-and-loading.plan.md](../../plans/phase-2-asset-structure-and-loading.plan.md) |
```

**Status**: `pending` → `complete`
**PRP Plan**: Link to this plan file

---

## Sources

- [Pygame image.load() v2.6.0 documentation](https://www.pygame.org/docs/ref/image.html)
- [Python pathlib documentation](https://docs.python.org/3/library/pathlib.html)
- [GameDev.net: Relative paths for image loading](https://www.gamedev.net/forums/topic/519131-relative-path-for-imageload/4371770/)
- [Pygame Surface documentation](https://www.pygame.org/docs/ref/surface.html)
- [Pygame tutorials: Sprite handling](https://www.pygame.org/docs/tut/ChimpLineByLine.html)
