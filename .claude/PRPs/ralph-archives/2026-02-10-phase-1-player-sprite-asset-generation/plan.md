# Feature: Player Sprite Asset Generation (Phase 1)

## Summary

Create a programmatic sprite generation script using pygame to generate Rambo-like player character sprites (48x48 pixels, 3-frame walk cycles in 4 directions, 1-frame shooting poses in 4 directions). The script will output 8 PNG files to `src/assets/players/` directory, mirroring the existing zombie sprite generation pattern from `scripts/generate_placeholder_sprites.py`. This is Phase 1 of the Rambo Player Sprite & Animations PRD.

## User Story

As a player of the zombie shooter game
I want to see an animated Rambo character with visible legs walking and gun shooting
So that I can feel immersed in the action with a polished visual experience matching the zombie sprite quality

## Problem Statement

The player character is currently rendered as a plain blue circle (18px radius), which looks mundane and breaks immersion. With all 5 zombie variants now featuring detailed 48x48 animated sprites (3-frame walk cycles), the primitive player rendering creates a visual mismatch that makes gameplay feel unpolished.

## Solution Statement

Generate programmatic pixel art sprites using pygame primitives (rectangles, circles, pixel manipulation) to create a Rambo-like character appearance with:
- Muscular action hero physique
- Red headband (iconic Rambo feature)
- Tan/brown skin tone
- Green/brown tactical outfit
- Black gun visible in hand
- 3-frame walk animations showing leg movement
- 1-frame shooting poses with extended gun

Output format matches zombie sprite system: horizontal sprite sheets (144×48 for walk, 48×48 for shoot) stored in `src/assets/players/` directory.

## Metadata

| Field            | Value                                             |
| ---------------- | ------------------------------------------------- |
| Type             | NEW_CAPABILITY |
| Complexity       | MEDIUM |
| Systems Affected | Asset generation (new script), asset directory structure |
| Dependencies     | pygame 2.6.1 (already installed), Python 3.11+ |
| Estimated Tasks  | 6 |

---

## UX Design

### Before State
```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌─────────────┐         ┌─────────────┐         ┌─────────────┐            ║
║   │  Game Start │ ──────► │   Player    │ ──────► │  No Sprites │            ║
║   │             │         │   Entity    │         │  Available  │            ║
║   └─────────────┘         └─────────────┘         └─────────────┘            ║
║                                                                               ║
║   USER_FLOW: Developer needs to create player sprites manually or source     ║
║              externally before implementing animation system                  ║
║                                                                               ║
║   PAIN_POINT: No player sprite assets exist; only blue circle rendering      ║
║                                                                               ║
║   DATA_FLOW: Player.draw() → pygame.draw.circle() → Blue circle on screen    ║
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
║   │ Run Script  │ ──────► │  Generate   │ ──────► │  8 PNG Files│            ║
║   │ create_     │         │  Rambo      │         │  in assets/ │            ║
║   │ player_     │         │  Sprites    │         │  players/   │            ║
║   │ sprites.py  │         │             │         │             │            ║
║   └─────────────┘         └─────────────┘         └─────────────┘            ║
║                                   │                                           ║
║                                   ▼                                           ║
║                          ┌─────────────┐                                      ║
║                          │ 48x48 pixel │                                      ║
║                          │ sprites with│                                      ║
║                          │ walk + shoot│                                      ║
║                          │ animations  │                                      ║
║                          └─────────────┘                                      ║
║                                                                               ║
║   USER_FLOW: Developer runs generation script once → sprites created         ║
║              automatically → ready for Phase 2 integration                    ║
║                                                                               ║
║   VALUE_ADD: Automated sprite generation matching zombie style; no manual    ║
║              pixel art needed; consistent 48x48 format; immediate availability║
║                                                                               ║
║   DATA_FLOW: pygame primitives → Surface composition → sprite sheets →       ║
║              PNG files saved to disk                                          ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| `src/assets/players/` | Directory doesn't exist | Contains 8 PNG files (walk_down.png, walk_up.png, walk_left.png, walk_right.png, shoot_down.png, shoot_up.png, shoot_left.png, shoot_right.png) | Sprite assets available for Phase 2 integration |
| `scripts/` directory | Only zombie sprite generation scripts | Adds `create_player_sprites.py` | Reproducible player sprite generation |
| Developer workflow | Must source external sprites or create manually | Run Python script to auto-generate sprites | Fully automated asset pipeline |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `/Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/scripts/generate_placeholder_sprites.py` | 1-225 | **EXACT PATTERN TO MIRROR** - complete sprite generation architecture: surface creation, frame positioning, per-direction draw functions, main() structure |
| P1 | `/Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/create_tank_sprites.py` | 1-40 | Color overlay technique using `pygame.BLEND_RGBA_ADD` for variant generation |
| P1 | `/Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/create_exploder_sprites.py` | 1-40 | Alternative color blending approach for sprite variants |
| P2 | `/Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/src/game/core/constants.py` | 69-71 | Sprite size constants: `ZOMBIE_SPRITE_SIZE = 48`, `ZOMBIE_FRAME_COUNT = 3`, `ZOMBIE_ANIMATION_FPS = 10` |
| P2 | `/Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/src/game/assets/loader.py` | 17-48 | Image loading with `convert_alpha()` - ensures sprites load with proper transparency |

**External Documentation:**

| Source | Section | Why Needed |
|--------|---------|------------|
| [pygame.draw Documentation v2.6.0](https://www.pygame.org/docs/ref/draw.html) | Drawing primitives (rect, circle, polygon) | Core drawing functions for creating programmatic pixel art |
| [pygame.Surface Documentation v2.6.0](https://www.pygame.org/docs/ref/surface.html) | SRCALPHA flag, convert_alpha() | Transparency handling for sprite sheets |
| [pygame.image Documentation v2.6.0](https://www.pygame.org/docs/ref/image.html) | save() function | Saving generated sprites as PNG files |
| [Pygame Sprite Sheets Wiki](https://www.pygame.org/wiki/Spritesheet) | Best practices for sprite sheet layout | Standard conventions for horizontal sprite sheets |

---

## Patterns to Mirror

**SPRITE GENERATION ARCHITECTURE:**
```python
# SOURCE: scripts/generate_placeholder_sprites.py:1-225
# COPY THIS PATTERN:

import pygame
from pathlib import Path

# Constants
SPRITE_SIZE = 48  # Match zombie sprite size
FRAME_COUNT = 3   # Match zombie frame count

def draw_player_down(surface: pygame.Surface, x_offset: int, frame: int) -> None:
    """Draw player facing down with walking animation.

    Args:
        surface: The sprite sheet surface to draw on
        x_offset: Horizontal offset for this frame (frame * SPRITE_SIZE)
        frame: Frame number (0, 1, 2) for walk cycle
    """
    center_x = x_offset + SPRITE_SIZE // 2
    center_y = SPRITE_SIZE // 2

    # Body, head, arms, legs based on frame
    # Frame-specific positioning for walk cycle
    pass

def create_sprite_sheet(direction: str, output_path: Path) -> None:
    """Create a sprite sheet with 3 frames for a direction.

    Creates a horizontal sprite sheet (144x48 pixels) with 3 animation frames
    laid out left-to-right. Uses SRCALPHA for transparency.
    """
    sheet_width = SPRITE_SIZE * FRAME_COUNT
    sheet_height = SPRITE_SIZE

    # CRITICAL: pygame.SRCALPHA creates transparent background
    surface = pygame.Surface((sheet_width, sheet_height), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))  # Fill with transparent pixels

    for frame in range(FRAME_COUNT):
        x_offset = frame * SPRITE_SIZE

        if direction == "down":
            draw_player_down(surface, x_offset, frame)
        elif direction == "up":
            draw_player_up(surface, x_offset, frame)
        elif direction == "left":
            draw_player_left(surface, x_offset, frame)
        elif direction == "right":
            draw_player_right(surface, x_offset, frame)

    pygame.image.save(surface, str(output_path))
    print(f"Created: {output_path}")

def main() -> None:
    """Generate all player sprite sheets."""
    pygame.init()

    # Path resolution: script_dir → project_root → assets
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    assets_dir = project_root / "src" / "assets" / "players"
    assets_dir.mkdir(parents=True, exist_ok=True)

    directions = ["down", "up", "left", "right"]
    for direction in directions:
        output_path = assets_dir / f"walk_{direction}.png"
        create_sprite_sheet(direction, output_path)

    print(f"✓ Generated {len(directions)} walk sprite sheets")
    print(f"✓ Output directory: {assets_dir}")

if __name__ == "__main__":
    main()
```

**PYGAME DRAWING PRIMITIVES:**
```python
# SOURCE: scripts/generate_placeholder_sprites.py:14-166
# PATTERN: Use simple geometric shapes for retro pixel art

# Rectangle drawing (body, limbs)
pygame.draw.rect(surface, color, pygame.Rect(x, y, width, height))

# Circle drawing (head, joints)
pygame.draw.circle(surface, color, (center_x, center_y), radius)

# Polygon drawing (complex shapes)
pygame.draw.polygon(surface, color, [(x1, y1), (x2, y2), (x3, y3)])

# Pixel-level control (fine details)
surface.set_at((x, y), color)  # Set individual pixel
```

**COLOR PALETTE (Rambo Character):**
```python
# Rambo-inspired colors for retro pixel art

# Skin tones
SKIN_TAN = (210, 180, 140)
SKIN_SHADOW = (180, 140, 100)

# Headband (iconic red)
HEADBAND_RED = (200, 40, 40)
HEADBAND_SHADOW = (150, 20, 20)

# Clothing (tactical green/brown)
OUTFIT_GREEN = (80, 100, 60)
OUTFIT_BROWN = (100, 80, 50)
OUTFIT_SHADOW = (60, 60, 40)

# Gun (black with highlights)
GUN_BLACK = (30, 30, 30)
GUN_HIGHLIGHT = (60, 60, 60)

# Outlines (optional for definition)
OUTLINE_DARK = (20, 20, 20)
```

**WALK CYCLE ANIMATION PATTERN:**
```python
# SOURCE: scripts/generate_placeholder_sprites.py:14-80
# PATTERN: Three-frame walk cycle with leg alternation

def draw_player_down(surface: pygame.Surface, x_offset: int, frame: int) -> None:
    center_x = x_offset + SPRITE_SIZE // 2

    # Frame 0: Neutral stance (both legs together)
    if frame == 0:
        left_leg_offset = 0
        right_leg_offset = 0

    # Frame 1: Left leg forward, right leg back
    elif frame == 1:
        left_leg_offset = 2   # Move left leg forward
        right_leg_offset = -2  # Move right leg back

    # Frame 2: Right leg forward, left leg back
    else:  # frame == 2
        left_leg_offset = -2   # Move left leg back
        right_leg_offset = 2   # Move right leg forward

    # Draw legs with calculated offsets
    # Draw body (torso remains stable)
    # Draw arms with gun
    # Draw head with headband
```

**SHOOTING SPRITE PATTERN:**
```python
# Single-frame shooting pose with extended gun arm

def create_shooting_sprite(direction: str, output_path: Path) -> None:
    """Create a single-frame shooting sprite (48x48).

    Shows gun extended in facing direction. Unlike walk sprites,
    this is a single frame (not a sheet).
    """
    surface = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))

    center_x = SPRITE_SIZE // 2
    center_y = SPRITE_SIZE // 2

    # Draw body in shooting stance
    # Extend gun arm in facing direction
    # Other arm positioned for recoil/support

    pygame.image.save(surface, str(output_path))
```

---

## Files to Change

| File | Action | Justification |
|------|--------|---------------|
| `zombie-shooter/scripts/create_player_sprites.py` | CREATE | New sprite generation script for player character - mirrors `generate_placeholder_sprites.py` pattern |
| `zombie-shooter/src/assets/players/walk_down.png` | CREATE | Walk animation sprite sheet facing down (144×48, 3 frames) |
| `zombie-shooter/src/assets/players/walk_up.png` | CREATE | Walk animation sprite sheet facing up (144×48, 3 frames) |
| `zombie-shooter/src/assets/players/walk_left.png` | CREATE | Walk animation sprite sheet facing left (144×48, 3 frames) |
| `zombie-shooter/src/assets/players/walk_right.png` | CREATE | Walk animation sprite sheet facing right (144×48, 3 frames) |
| `zombie-shooter/src/assets/players/shoot_down.png` | CREATE | Shooting pose facing down (48×48, single frame) |
| `zombie-shooter/src/assets/players/shoot_up.png` | CREATE | Shooting pose facing up (48×48, single frame) |
| `zombie-shooter/src/assets/players/shoot_left.png` | CREATE | Shooting pose facing left (48×48, single frame) |
| `zombie-shooter/src/assets/players/shoot_right.png` | CREATE | Shooting pose facing right (48×48, single frame) |

---

## NOT Building (Scope Limits)

Explicit exclusions to prevent scope creep:

- **Multiple character variants/skins** - Single Rambo character only; no customization system
- **Hand-drawn detailed pixel art** - Using programmatic generation with geometric shapes; not professional artist-quality sprites
- **Per-weapon animation variants** - One shooting animation shared across all guns (pistol, shotgun, SMG)
- **Idle animation** - Will reuse walk frame 0; dedicated idle sprites deferred to later phases
- **Damage/hit animation** - Player damage shown via HP counter only
- **Death animation** - Game over screen handles player death
- **Reload animation** - Not in scope for MVP
- **Muzzle flash** - Optional polish for Phase 4; not in asset generation phase

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: CREATE `zombie-shooter/scripts/create_player_sprites.py` - Script structure and constants

- **ACTION**: CREATE sprite generation script with imports, constants, and main entry point
- **IMPLEMENT**:
  - Import statements: `pygame`, `pathlib.Path`
  - Constants: `SPRITE_SIZE = 48`, `FRAME_COUNT = 3`
  - Color palette: Define colors for skin, headband, outfit, gun (see Patterns section)
  - `main()` function: Initialize pygame, create output directory, loop over directions
- **MIRROR**: `scripts/generate_placeholder_sprites.py:1-10, 200-224` - exact structure
- **GOTCHA**: Must call `pygame.init()` before creating surfaces; use `Path(__file__).resolve().parent` for reliable path resolution
- **VALIDATE**: Script runs without errors and creates `src/assets/players/` directory
  ```bash
  cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter
  python scripts/create_player_sprites.py
  # Should output: "✓ Output directory: .../src/assets/players"
  ```

### Task 2: CREATE draw functions for walk animations - Down direction

- **ACTION**: Implement `draw_player_down(surface, x_offset, frame)` with 3-frame walk cycle
- **IMPLEMENT**:
  - **Frame 0**: Neutral stance - legs together, arms at sides holding gun down
  - **Frame 1**: Left leg forward (+2px), right leg back (-2px), slight torso lean
  - **Frame 2**: Right leg forward (+2px), left leg back (-2px), opposite lean
  - Draw order (back-to-front): legs → body torso → arms/gun → head → headband
  - Body parts: Head circle (8px radius), torso rect (16px wide × 20px tall), arms rect (4px wide), legs rect (6px wide × 12px tall), gun L-shape (8px + 4px)
- **MIRROR**: `scripts/generate_placeholder_sprites.py:14-41` - zombie walk down pattern
- **GOTCHA**: Use `center_x = x_offset + SPRITE_SIZE // 2` for horizontal frame positioning; legs must show visible movement (2-3 pixel shifts minimum)
- **VALIDATE**: Add test code to `main()` to generate only `walk_down.png`, visually inspect frames show leg movement
  ```bash
  python scripts/create_player_sprites.py
  # Open walk_down.png in image viewer - should see 3 frames with leg animation
  ```

### Task 3: CREATE draw functions for walk animations - Up, Left, Right directions

- **ACTION**: Implement `draw_player_up()`, `draw_player_left()`, `draw_player_right()` with directional walk cycles
- **IMPLEMENT**:
  - **Up**: Back view - show back of head, shoulders, legs moving (similar to down but no face)
  - **Left**: Side view - show profile, one arm forward with gun, leg movement side-to-side
  - **Right**: Side view - mirror of left (or draw separately with gun on right side)
  - Maintain same frame pattern: 0 = neutral, 1 = left leg forward, 2 = right leg forward
- **MIRROR**: `scripts/generate_placeholder_sprites.py:44-166` - zombie walk up/left/right patterns
- **GOTCHA**: Left/right views require different body proportions (wider for side profile); gun should be visible in hand for all directions
- **VALIDATE**: Generate all 4 walk sprite sheets, verify each shows distinct direction and smooth walk cycle
  ```bash
  python scripts/create_player_sprites.py
  # Should create walk_down.png, walk_up.png, walk_left.png, walk_right.png
  ls -lh src/assets/players/
  # Verify 4 files exist, each 144×48 pixels (3 frames horizontal)
  ```

### Task 4: CREATE draw functions for shooting poses - All 4 directions

- **ACTION**: Implement `draw_player_shoot_down()`, `draw_player_shoot_up()`, `draw_player_shoot_left()`, `draw_player_shoot_right()`
- **IMPLEMENT**:
  - **Down**: Gun arm extended downward, body in shooting stance (feet planted)
  - **Up**: Gun arm raised upward, body leaning slightly back
  - **Left**: Gun extended to left side, body in profile, shooting pose
  - **Right**: Gun extended to right side, mirror of left
  - Gun should be visibly extended 6-8 pixels from body in firing direction
  - Legs in stable stance (both visible, slightly spread)
- **MIRROR**: Walk down frame 0 as base pose, then extend gun arm
- **GOTCHA**: Single frame per direction (48×48), not a sprite sheet; create new function `create_shooting_sprite()` separate from `create_sprite_sheet()`
- **VALIDATE**: Generate all 4 shooting sprites, verify gun extension is visible
  ```bash
  python scripts/create_player_sprites.py
  # Should create shoot_down.png, shoot_up.png, shoot_left.png, shoot_right.png
  ls -lh src/assets/players/
  # Verify 8 files total (4 walk + 4 shoot), shoot sprites are 48×48
  ```

### Task 5: UPDATE script main() - Generate all 8 sprite files

- **ACTION**: Complete `main()` to generate both walk sprite sheets and shooting sprites
- **IMPLEMENT**:
  ```python
  def main() -> None:
      pygame.init()

      script_dir = Path(__file__).resolve().parent
      project_root = script_dir.parent
      assets_dir = project_root / "src" / "assets" / "players"
      assets_dir.mkdir(parents=True, exist_ok=True)

      directions = ["down", "up", "left", "right"]

      # Generate walk animations (sprite sheets)
      for direction in directions:
          output_path = assets_dir / f"walk_{direction}.png"
          create_sprite_sheet(direction, output_path)

      # Generate shooting poses (single frames)
      for direction in directions:
          output_path = assets_dir / f"shoot_{direction}.png"
          create_shooting_sprite(direction, output_path)

      print(f"✓ Generated {len(directions)} walk sprite sheets (3 frames each)")
      print(f"✓ Generated {len(directions)} shooting sprites (single frame)")
      print(f"✓ Output directory: {assets_dir}")
  ```
- **MIRROR**: `scripts/generate_placeholder_sprites.py:200-224` - main structure
- **VALIDATE**: Run full script, verify console output and 8 files created
  ```bash
  python scripts/create_player_sprites.py
  # Expected output:
  # ✓ Generated 4 walk sprite sheets (3 frames each)
  # ✓ Generated 4 shooting sprites (single frame)
  # ✓ Output directory: .../src/assets/players

  ls -lh src/assets/players/
  # Should list 8 PNG files
  ```

### Task 6: VALIDATE sprite visual quality and dimensions

- **ACTION**: Manual inspection of generated sprites for visual quality and technical correctness
- **IMPLEMENT**:
  - Open each PNG in image viewer (Preview, GIMP, or custom pygame viewer)
  - **Verify walk sprites (144×48)**:
    - 3 distinct frames visible
    - Leg movement visible between frames (2-3 pixel shifts)
    - Rambo features visible: headband (red band on head), muscular build, gun in hand
    - Direction differences clear (facing down vs up vs left vs right)
  - **Verify shooting sprites (48×48)**:
    - Gun visibly extended in correct direction
    - Body in stable shooting stance
    - Consistent with walk sprites (same colors, proportions)
  - **Check transparency**: Background should be transparent (not black/white solid)
- **MIRROR**: Compare to zombie sprites in `src/assets/zombies/` - similar visual quality and format
- **GOTCHA**: If sprites look too basic/geometric, iterate on draw functions to add more detail (shadows, outlines, muscle definition)
- **VALIDATE**: All 8 sprites pass visual inspection
  ```bash
  # Manual check
  open src/assets/players/*.png  # macOS
  # Or use Python to preview:
  cd scripts
  python -c "
  import pygame
  from pathlib import Path

  pygame.init()
  screen = pygame.display.set_mode((800, 600))
  clock = pygame.time.Clock()

  assets_dir = Path('../src/assets/players')
  sprites = [pygame.image.load(str(p)) for p in sorted(assets_dir.glob('*.png'))]

  running = True
  x_offset = 50
  while running:
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              running = False

      screen.fill((100, 100, 100))
      for i, sprite in enumerate(sprites):
          y_offset = 50 + (i * 60)
          screen.blit(sprite, (x_offset, y_offset))

      pygame.display.flip()
      clock.tick(5)

  pygame.quit()
  "
  ```

---

## Testing Strategy

### Unit Tests to Write

*Note: Sprite generation scripts typically don't have automated unit tests - validation is visual. However, we can add smoke tests.*

| Test File | Test Cases | Validates |
|-----------|------------|-----------|
| `tests/test_player_sprite_generation.py` (optional) | Test script runs without errors, directory created, 8 files exist | Script execution correctness |
| Manual visual inspection | Walk cycles show leg movement, shooting poses show gun extension, colors match Rambo theme | Visual quality |

### Edge Cases Checklist

- [ ] Script runs from different working directories (uses Path(__file__))
- [ ] Output directory creation works when path doesn't exist
- [ ] Overwriting existing sprites works (re-running script)
- [ ] All 8 files generated successfully (no partial output)
- [ ] Sprites have transparent backgrounds (SRCALPHA works)
- [ ] Sprite dimensions correct (144×48 for walk, 48×48 for shoot)

---

## Validation Commands

### Level 1: SCRIPT_EXECUTION

```bash
cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter
python scripts/create_player_sprites.py
```

**EXPECT**:
- Exit 0 (no Python exceptions)
- Console output showing file creation
- `src/assets/players/` directory exists with 8 PNG files

### Level 2: FILE_VERIFICATION

```bash
cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter
ls -lh src/assets/players/

# Verify file count
[ $(ls src/assets/players/*.png | wc -l) -eq 8 ] && echo "✓ 8 files created" || echo "✗ Wrong file count"

# Verify walk sprite dimensions (should be 144×48)
file src/assets/players/walk_down.png | grep -q "144 x 48" && echo "✓ Walk sprite dimensions correct" || echo "✗ Walk sprite dimensions wrong"

# Verify shoot sprite dimensions (should be 48×48)
file src/assets/players/shoot_down.png | grep -q "48 x 48" && echo "✓ Shoot sprite dimensions correct" || echo "✗ Shoot sprite dimensions wrong"
```

**EXPECT**:
- 8 PNG files exist
- Walk sprites are 144×48 pixels
- Shoot sprites are 48×48 pixels

### Level 3: VISUAL_QUALITY_INSPECTION

```bash
# Manual inspection - open in image viewer
open src/assets/players/*.png  # macOS
# Or: xdg-open src/assets/players/*.png  # Linux
# Or: start src/assets/players/*.png  # Windows
```

**EXPECT**:
- Walk sprites show 3 distinct frames with visible leg movement
- Shooting sprites show extended gun in correct direction
- Rambo features visible: red headband, muscular build, gun
- Transparent backgrounds (no solid color blocks)
- Visual quality comparable to zombie sprites

### Level 4: INTEGRATION_READINESS

```bash
# Verify sprites can be loaded by pygame (syntax check)
cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter
python -c "
import pygame
from pathlib import Path

pygame.init()

assets_dir = Path('src/assets/players')
for sprite_file in assets_dir.glob('*.png'):
    try:
        surface = pygame.image.load(str(sprite_file))
        print(f'✓ {sprite_file.name}: {surface.get_width()}×{surface.get_height()}')
    except Exception as e:
        print(f'✗ {sprite_file.name}: {e}')

pygame.quit()
"
```

**EXPECT**:
- All 8 sprites load without pygame errors
- Dimensions print correctly

### Level 5: LINTING (Optional)

```bash
cd /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter
ruff check scripts/create_player_sprites.py
ruff format scripts/create_player_sprites.py
```

**EXPECT**: Exit 0 (no linting errors)

---

## Acceptance Criteria

- [ ] Script `create_player_sprites.py` exists in `zombie-shooter/scripts/` directory
- [ ] Script runs without errors and completes successfully
- [ ] 8 PNG files created in `src/assets/players/` directory:
  - `walk_down.png`, `walk_up.png`, `walk_left.png`, `walk_right.png` (144×48 each)
  - `shoot_down.png`, `shoot_up.png`, `shoot_left.png`, `shoot_right.png` (48×48 each)
- [ ] Walk sprites show 3-frame animation cycles with visible leg movement
- [ ] Shooting sprites show extended gun in facing direction
- [ ] Rambo character features visible: red headband, muscular physique, gun
- [ ] Sprite quality comparable to zombie sprites (clear silhouette, retro pixel art style)
- [ ] Sprites have transparent backgrounds (not solid color)
- [ ] All sprites load correctly in pygame without errors

---

## Completion Checklist

- [ ] Task 1: Script structure and constants created
- [ ] Task 2: Walk down direction implemented with 3-frame animation
- [ ] Task 3: Walk up, left, right directions implemented
- [ ] Task 4: Shooting poses for all 4 directions implemented
- [ ] Task 5: Main function generates all 8 sprite files
- [ ] Task 6: Visual quality validation passed
- [ ] Level 1: Script execution successful
- [ ] Level 2: File verification passed (8 files, correct dimensions)
- [ ] Level 3: Visual quality inspection passed
- [ ] Level 4: Integration readiness verified (pygame loads sprites)
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Programmatic sprites look too basic/geometric compared to zombie sprites | MEDIUM | MEDIUM | Start simple, iterate on draw functions to add shadows, outlines, muscle definition; reference zombie sprite style closely |
| Walk cycle leg movement not visible enough | MEDIUM | LOW | Increase pixel offset for leg shifts (3-4 pixels instead of 2); add color contrast between legs and body |
| Rambo character not recognizable (doesn't look like action hero) | LOW | MEDIUM | Focus on iconic features: RED headband (must be prominent), muscular torso (wider rectangles), visible gun in hand; test with user feedback |
| Sprite dimensions incorrect (don't match 48x48 standard) | LOW | HIGH | Use constants for all dimensions; validate with `file` command or pygame inspection before marking complete |
| Transparency not working (solid backgrounds) | LOW | HIGH | Ensure `pygame.SRCALPHA` flag used; test with `surface.get_alpha()` before saving; validate by loading in pygame and checking transparency |
| Script path resolution fails on different systems | LOW | MEDIUM | Use `Path(__file__).resolve().parent` for reliable relative paths; test from multiple working directories |

---

## Notes

**Design Decisions:**

1. **Programmatic vs hand-drawn**: Using programmatic generation with pygame primitives because constraint requires AI-generated sprites and programmatic approach is most feasible and reproducible.

2. **Sprite size 48×48**: Matches zombie sprite system exactly - enables reuse of existing loading/animation infrastructure in Phase 2.

3. **3-frame walk cycle**: Mirrors zombie animation frame count - proven to work smoothly at 10 FPS.

4. **Single shooting pose per direction**: User constraint to limit scope; sufficient for MVP since one animation works across all weapons.

5. **Horizontal sprite sheet layout**: Standard pygame convention; matches zombie sprite format; simplifies frame splitting in loader.

**Trade-offs:**

- **Geometric shapes vs detailed pixel art**: Accepting simpler visual style for speed and automation; can iterate on detail in Phase 4 if needed.
- **Generic gun vs per-weapon sprites**: One gun appearance for all weapons (pistol/shotgun/SMG) to reduce scope; visually sufficient since shooting animation is brief.

**Future Considerations (Phase 4 polish):**

- Add muzzle flash pixels to shooting sprites for extra feedback
- Iterate on color palette if player doesn't stand out enough from zombies
- Add optional shadows/outlines for better definition
- Consider adding dedicated idle animation (currently using walk frame 0)

**External Research Sources:**

- [pygame.draw Documentation](https://www.pygame.org/docs/ref/draw.html) - Drawing primitives (rect, circle, polygon)
- [pygame.Surface Documentation](https://www.pygame.org/docs/ref/surface.html) - SRCALPHA transparency
- [pygame.image Documentation](https://www.pygame.org/docs/ref/image.html) - save() function for PNG output
- [Pygame Sprite Sheets Wiki](https://www.pygame.org/wiki/Spritesheet) - Best practices for sprite sheet layout
