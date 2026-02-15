"""Generate Rambo-like player sprites with walking and shooting animations."""

from __future__ import annotations

from pathlib import Path

import pygame

# Constants matching game constants
SPRITE_SIZE = 48  # Match zombie sprite size
FRAME_COUNT = 3  # 3-frame walk cycle

# Color palette - Rambo-inspired colors for retro pixel art
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

# Outlines (for definition)
OUTLINE_DARK = (20, 20, 20)


def draw_player_down(surface: pygame.Surface, x_offset: int, frame: int) -> None:
    """Draw player facing down with walking animation.

    Args:
        surface: The sprite sheet surface to draw on
        x_offset: Horizontal offset for this frame (frame * SPRITE_SIZE)
        frame: Frame number (0, 1, 2) for walk cycle
    """
    center_x = x_offset + SPRITE_SIZE // 2

    # Frame 0: Neutral stance - legs together
    # Frame 1: Left leg forward (+2px), right leg back (-2px)
    # Frame 2: Right leg forward (+2px), left leg back (-2px)
    if frame == 0:
        left_leg_offset = 0
        right_leg_offset = 0
    elif frame == 1:
        left_leg_offset = 2  # Left leg forward
        right_leg_offset = -2  # Right leg back
    else:  # frame == 2
        left_leg_offset = -2  # Left leg back
        right_leg_offset = 2  # Right leg forward

    # Draw legs (back layer)
    left_leg_y = 38 + left_leg_offset
    right_leg_y = 38 + right_leg_offset
    pygame.draw.rect(
        surface, OUTFIT_BROWN, (center_x - 7, 28, 6, left_leg_y - 28)
    )  # Left leg
    pygame.draw.rect(
        surface, OUTFIT_BROWN, (center_x + 1, 28, 6, right_leg_y - 28)
    )  # Right leg

    # Draw body torso (muscular rectangle)
    pygame.draw.rect(surface, OUTFIT_GREEN, (center_x - 8, 16, 16, 14))  # Torso

    # Draw arms with gun (right arm extends forward holding gun)
    # Left arm at side
    pygame.draw.rect(surface, SKIN_TAN, (center_x - 10, 18, 3, 10))  # Left arm

    # Right arm forward with gun
    pygame.draw.rect(surface, SKIN_TAN, (center_x + 7, 18, 3, 12))  # Right arm

    # Gun (L-shape extending from right hand)
    pygame.draw.rect(surface, GUN_BLACK, (center_x + 7, 28, 4, 8))  # Gun barrel down
    pygame.draw.rect(
        surface, GUN_BLACK, (center_x + 6, 28, 6, 3)
    )  # Gun handle horizontal

    # Draw head (circle)
    pygame.draw.circle(surface, SKIN_TAN, (center_x, 10), 7)

    # Draw headband (iconic red band)
    pygame.draw.rect(surface, HEADBAND_RED, (center_x - 7, 6, 14, 3))  # Red headband

    # Eyes (small dark pixels)
    pygame.draw.circle(surface, OUTLINE_DARK, (center_x - 3, 10), 1)  # Left eye
    pygame.draw.circle(surface, OUTLINE_DARK, (center_x + 3, 10), 1)  # Right eye


def draw_player_up(surface: pygame.Surface, x_offset: int, frame: int) -> None:
    """Draw player facing up (back view) with walking animation.

    Args:
        surface: The sprite sheet surface to draw on
        x_offset: Horizontal offset for this frame
        frame: Frame number (0, 1, 2) for walk cycle
    """
    center_x = x_offset + SPRITE_SIZE // 2

    # Walking animation - leg positions
    if frame == 0:
        left_leg_offset = 0
        right_leg_offset = 0
    elif frame == 1:
        left_leg_offset = -2  # Left leg back
        right_leg_offset = 2  # Right leg forward
    else:  # frame == 2
        left_leg_offset = 2  # Left leg forward
        right_leg_offset = -2  # Right leg back

    # Draw legs (back layer) - visible from back
    left_leg_y = 12 + left_leg_offset
    right_leg_y = 12 + right_leg_offset
    pygame.draw.rect(
        surface, OUTFIT_BROWN, (center_x - 7, left_leg_y, 6, 28 - left_leg_y)
    )
    pygame.draw.rect(
        surface, OUTFIT_BROWN, (center_x + 1, right_leg_y, 6, 28 - right_leg_y)
    )

    # Draw back of head (no face visible)
    pygame.draw.circle(surface, SKIN_SHADOW, (center_x, 10), 7)

    # Draw headband (back view - still visible)
    pygame.draw.rect(surface, HEADBAND_SHADOW, (center_x - 7, 6, 14, 3))

    # Draw body torso (back view)
    pygame.draw.rect(surface, OUTFIT_GREEN, (center_x - 8, 16, 16, 14))

    # Draw arms at sides (back view)
    pygame.draw.rect(surface, SKIN_SHADOW, (center_x - 10, 18, 3, 10))  # Left arm
    pygame.draw.rect(surface, SKIN_SHADOW, (center_x + 7, 18, 3, 10))  # Right arm

    # Gun visible at side (held in right hand)
    pygame.draw.rect(surface, GUN_BLACK, (center_x + 8, 20, 2, 6))


def draw_player_left(surface: pygame.Surface, x_offset: int, frame: int) -> None:
    """Draw player facing left (side view) with walking animation.

    Args:
        surface: The sprite sheet surface to draw on
        x_offset: Horizontal offset for this frame
        frame: Frame number (0, 1, 2) for walk cycle
    """
    center_x = x_offset + SPRITE_SIZE // 2

    # Walking animation - leg side-to-side movement
    if frame == 0:
        front_leg_x = 0
        back_leg_x = 0
    elif frame == 1:
        front_leg_x = 2  # Front leg forward
        back_leg_x = -2  # Back leg back
    else:  # frame == 2
        front_leg_x = -2  # Front leg back
        back_leg_x = 2  # Back leg forward

    # Draw legs (side view - one in front, one behind)
    # Back leg
    pygame.draw.rect(surface, OUTFIT_BROWN, (center_x - 3 + back_leg_x, 26, 5, 12))
    # Front leg
    pygame.draw.rect(surface, OUTFIT_BROWN, (center_x - 2 + front_leg_x, 26, 5, 12))

    # Draw body (side profile - narrower)
    pygame.draw.rect(surface, OUTFIT_GREEN, (center_x - 4, 16, 8, 12))

    # Draw left arm forward with gun extended
    pygame.draw.rect(surface, SKIN_TAN, (center_x - 12, 20, 10, 3))  # Arm extended left

    # Gun extending left
    pygame.draw.rect(
        surface, GUN_BLACK, (center_x - 16, 19, 6, 2)
    )  # Gun barrel horizontal
    pygame.draw.rect(surface, GUN_BLACK, (center_x - 11, 19, 2, 4))  # Gun grip

    # Draw head (side profile)
    pygame.draw.circle(surface, SKIN_TAN, (center_x, 10), 6)

    # Headband (side view)
    pygame.draw.rect(surface, HEADBAND_RED, (center_x - 6, 6, 12, 3))

    # Eye (single eye visible from side)
    pygame.draw.circle(surface, OUTLINE_DARK, (center_x - 2, 10), 1)


def draw_player_right(surface: pygame.Surface, x_offset: int, frame: int) -> None:
    """Draw player facing right (side view) with walking animation.

    Args:
        surface: The sprite sheet surface to draw on
        x_offset: Horizontal offset for this frame
        frame: Frame number (0, 1, 2) for walk cycle
    """
    center_x = x_offset + SPRITE_SIZE // 2

    # Walking animation - leg side-to-side movement
    if frame == 0:
        front_leg_x = 0
        back_leg_x = 0
    elif frame == 1:
        front_leg_x = -2  # Front leg forward
        back_leg_x = 2  # Back leg back
    else:  # frame == 2
        front_leg_x = 2  # Front leg back
        back_leg_x = -2  # Back leg forward

    # Draw legs (side view)
    # Back leg
    pygame.draw.rect(surface, OUTFIT_BROWN, (center_x - 2 + back_leg_x, 26, 5, 12))
    # Front leg
    pygame.draw.rect(surface, OUTFIT_BROWN, (center_x - 3 + front_leg_x, 26, 5, 12))

    # Draw body (side profile)
    pygame.draw.rect(surface, OUTFIT_GREEN, (center_x - 4, 16, 8, 12))

    # Draw right arm forward with gun extended
    pygame.draw.rect(surface, SKIN_TAN, (center_x + 2, 20, 10, 3))  # Arm extended right

    # Gun extending right
    pygame.draw.rect(
        surface, GUN_BLACK, (center_x + 10, 19, 6, 2)
    )  # Gun barrel horizontal
    pygame.draw.rect(surface, GUN_BLACK, (center_x + 9, 19, 2, 4))  # Gun grip

    # Draw head (side profile)
    pygame.draw.circle(surface, SKIN_TAN, (center_x, 10), 6)

    # Headband (side view)
    pygame.draw.rect(surface, HEADBAND_RED, (center_x - 6, 6, 12, 3))

    # Eye (single eye visible from side)
    pygame.draw.circle(surface, OUTLINE_DARK, (center_x + 2, 10), 1)


def draw_player_shoot_down(surface: pygame.Surface, x_offset: int) -> None:
    """Draw player shooting downward (single frame).

    Args:
        surface: The sprite surface to draw on
        x_offset: Horizontal offset (typically 0 for single frame)
    """
    center_x = x_offset + SPRITE_SIZE // 2

    # Stable shooting stance - legs spread slightly
    pygame.draw.rect(surface, OUTFIT_BROWN, (center_x - 7, 28, 6, 10))  # Left leg
    pygame.draw.rect(surface, OUTFIT_BROWN, (center_x + 1, 28, 6, 10))  # Right leg

    # Body torso
    pygame.draw.rect(surface, OUTFIT_GREEN, (center_x - 8, 16, 16, 14))

    # Arms - both extended downward holding gun
    pygame.draw.rect(surface, SKIN_TAN, (center_x - 6, 18, 3, 12))  # Left arm
    pygame.draw.rect(surface, SKIN_TAN, (center_x + 3, 18, 3, 12))  # Right arm

    # Gun extended downward (both hands)
    pygame.draw.rect(surface, GUN_BLACK, (center_x - 3, 28, 6, 10))  # Gun barrel down
    pygame.draw.rect(surface, GUN_BLACK, (center_x - 4, 28, 8, 3))  # Gun body

    # Head
    pygame.draw.circle(surface, SKIN_TAN, (center_x, 10), 7)

    # Headband
    pygame.draw.rect(surface, HEADBAND_RED, (center_x - 7, 6, 14, 3))

    # Eyes
    pygame.draw.circle(surface, OUTLINE_DARK, (center_x - 3, 10), 1)
    pygame.draw.circle(surface, OUTLINE_DARK, (center_x + 3, 10), 1)


def draw_player_shoot_up(surface: pygame.Surface, x_offset: int) -> None:
    """Draw player shooting upward (single frame).

    Args:
        surface: The sprite surface to draw on
        x_offset: Horizontal offset
    """
    center_x = x_offset + SPRITE_SIZE // 2

    # Legs stable
    pygame.draw.rect(surface, OUTFIT_BROWN, (center_x - 7, 20, 6, 18))  # Left leg
    pygame.draw.rect(surface, OUTFIT_BROWN, (center_x + 1, 20, 6, 18))  # Right leg

    # Body leaning slightly back
    pygame.draw.rect(surface, OUTFIT_GREEN, (center_x - 8, 8, 16, 14))

    # Arms raised upward with gun
    pygame.draw.rect(surface, SKIN_TAN, (center_x - 6, 6, 3, 10))  # Left arm
    pygame.draw.rect(surface, SKIN_TAN, (center_x + 3, 6, 3, 10))  # Right arm

    # Gun pointing up
    pygame.draw.rect(surface, GUN_BLACK, (center_x - 3, 2, 6, 8))  # Gun barrel up
    pygame.draw.rect(surface, GUN_BLACK, (center_x - 4, 8, 8, 3))  # Gun body

    # Head (back view)
    pygame.draw.circle(surface, SKIN_SHADOW, (center_x, 18), 7)

    # Headband (back)
    pygame.draw.rect(surface, HEADBAND_SHADOW, (center_x - 7, 14, 14, 3))


def draw_player_shoot_left(surface: pygame.Surface, x_offset: int) -> None:
    """Draw player shooting left (single frame).

    Args:
        surface: The sprite surface to draw on
        x_offset: Horizontal offset
    """
    center_x = x_offset + SPRITE_SIZE // 2

    # Legs in stable stance
    pygame.draw.rect(surface, OUTFIT_BROWN, (center_x - 4, 26, 5, 12))  # Back leg
    pygame.draw.rect(surface, OUTFIT_BROWN, (center_x - 2, 26, 5, 12))  # Front leg

    # Body
    pygame.draw.rect(surface, OUTFIT_GREEN, (center_x - 4, 16, 8, 12))

    # Arms extended left with gun
    pygame.draw.rect(
        surface, SKIN_TAN, (center_x - 14, 20, 12, 3)
    )  # Both arms extended

    # Gun extended left
    pygame.draw.rect(surface, GUN_BLACK, (center_x - 20, 19, 8, 2))  # Gun barrel longer
    pygame.draw.rect(surface, GUN_BLACK, (center_x - 13, 18, 2, 5))  # Gun grip

    # Head
    pygame.draw.circle(surface, SKIN_TAN, (center_x, 10), 6)

    # Headband
    pygame.draw.rect(surface, HEADBAND_RED, (center_x - 6, 6, 12, 3))

    # Eye
    pygame.draw.circle(surface, OUTLINE_DARK, (center_x - 2, 10), 1)


def draw_player_shoot_right(surface: pygame.Surface, x_offset: int) -> None:
    """Draw player shooting right (single frame).

    Args:
        surface: The sprite surface to draw on
        x_offset: Horizontal offset
    """
    center_x = x_offset + SPRITE_SIZE // 2

    # Legs in stable stance
    pygame.draw.rect(surface, OUTFIT_BROWN, (center_x - 1, 26, 5, 12))  # Back leg
    pygame.draw.rect(surface, OUTFIT_BROWN, (center_x - 3, 26, 5, 12))  # Front leg

    # Body
    pygame.draw.rect(surface, OUTFIT_GREEN, (center_x - 4, 16, 8, 12))

    # Arms extended right with gun
    pygame.draw.rect(surface, SKIN_TAN, (center_x + 2, 20, 12, 3))  # Both arms extended

    # Gun extended right
    pygame.draw.rect(surface, GUN_BLACK, (center_x + 12, 19, 8, 2))  # Gun barrel longer
    pygame.draw.rect(surface, GUN_BLACK, (center_x + 11, 18, 2, 5))  # Gun grip

    # Head
    pygame.draw.circle(surface, SKIN_TAN, (center_x, 10), 6)

    # Headband
    pygame.draw.rect(surface, HEADBAND_RED, (center_x - 6, 6, 12, 3))

    # Eye
    pygame.draw.circle(surface, OUTLINE_DARK, (center_x + 2, 10), 1)


def create_sprite_sheet(direction: str, output_path: Path) -> None:
    """Create a sprite sheet with 3 frames for a direction.

    Creates a horizontal sprite sheet (144x48 pixels) with 3 animation frames
    laid out left-to-right. Uses SRCALPHA for transparency.

    Args:
        direction: Direction name (down, up, left, right)
        output_path: Path to save PNG file
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


def create_shooting_sprite(direction: str, output_path: Path) -> None:
    """Create a single-frame shooting sprite (48x48).

    Shows gun extended in facing direction. Unlike walk sprites,
    this is a single frame (not a sheet).

    Args:
        direction: Direction name (down, up, left, right)
        output_path: Path to save PNG file
    """
    surface = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))

    x_offset = 0  # Single frame, no offset needed

    if direction == "down":
        draw_player_shoot_down(surface, x_offset)
    elif direction == "up":
        draw_player_shoot_up(surface, x_offset)
    elif direction == "left":
        draw_player_shoot_left(surface, x_offset)
    elif direction == "right":
        draw_player_shoot_right(surface, x_offset)

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

    # Generate walk animations (sprite sheets)
    for direction in directions:
        output_path = assets_dir / f"walk_{direction}.png"
        create_sprite_sheet(direction, output_path)

    # Generate shooting poses (single frames)
    for direction in directions:
        output_path = assets_dir / f"shoot_{direction}.png"
        create_shooting_sprite(direction, output_path)

    print(f"\n✓ Generated {len(directions)} walk sprite sheets (3 frames each)")
    print(f"✓ Generated {len(directions)} shooting sprites (single frame)")
    print(f"✓ Output directory: {assets_dir}")


if __name__ == "__main__":
    main()
