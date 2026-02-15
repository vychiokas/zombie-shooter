"""Generate zombie sprites with arms, legs, and walking animation."""

from __future__ import annotations

from pathlib import Path

import pygame

# Constants matching game constants
SPRITE_SIZE = 48  # Increased from 32 for bigger zombies
FRAME_COUNT = 3


def draw_zombie_down(surface: pygame.Surface, x_offset: int, frame: int) -> None:
    """Draw zombie facing down (toward camera) with walking animation."""
    center_x = x_offset + SPRITE_SIZE // 2

    # Colors
    green = (0, 180, 50)
    dark_green = (0, 140, 40)
    white = (255, 255, 255)
    black = (0, 0, 0)

    # Walking animation - leg positions (scaled 1.5x)
    if frame == 0:  # Left leg forward
        left_leg_y = 39
        right_leg_y = 36
    elif frame == 1:  # Standing
        left_leg_y = 38
        right_leg_y = 38
    else:  # Right leg forward (frame == 2)
        left_leg_y = 36
        right_leg_y = 39

    # Legs (drawn first, behind body)
    pygame.draw.line(surface, dark_green, (center_x - 5, 30), (center_x - 5, left_leg_y), 5)
    pygame.draw.line(surface, dark_green, (center_x + 5, 30), (center_x + 5, right_leg_y), 5)

    # Body (oval)
    pygame.draw.ellipse(surface, green, (center_x - 8, 18, 15, 15))

    # Arms (slightly swaying)
    arm_offset = (frame - 1) * 2  # Slight sway: -2, 0, 2
    pygame.draw.line(surface, green, (center_x - 8, 23), (center_x - 12, 27 + arm_offset), 3)
    pygame.draw.line(surface, green, (center_x + 8, 23), (center_x + 12, 27 + arm_offset), 3)

    # Head
    pygame.draw.circle(surface, green, (center_x, 12), 6)

    # Eyes
    pygame.draw.circle(surface, black, (center_x - 3, 12), 2)
    pygame.draw.circle(surface, black, (center_x + 3, 12), 2)


def draw_zombie_up(surface: pygame.Surface, x_offset: int, frame: int) -> None:
    """Draw zombie facing up (away from camera) with walking animation."""
    center_x = x_offset + SPRITE_SIZE // 2

    # Colors
    green = (0, 180, 50)
    dark_green = (0, 140, 40)

    # Walking animation - leg positions (scaled 1.5x)
    if frame == 0:  # Left leg forward
        left_leg_y = 9
        right_leg_y = 12
    elif frame == 1:  # Standing
        left_leg_y = 11
        right_leg_y = 11
    else:  # Right leg forward
        left_leg_y = 12
        right_leg_y = 9

    # Head (back of head visible)
    pygame.draw.circle(surface, green, (center_x, 12), 6)

    # Body (oval)
    pygame.draw.ellipse(surface, green, (center_x - 8, 18, 15, 15))

    # Arms (slightly swaying)
    arm_offset = (frame - 1) * 2
    pygame.draw.line(surface, green, (center_x - 8, 23), (center_x - 12, 27 + arm_offset), 3)
    pygame.draw.line(surface, green, (center_x + 8, 23), (center_x + 12, 27 + arm_offset), 3)

    # Legs (visible at top since walking away)
    pygame.draw.line(surface, dark_green, (center_x - 5, 15), (center_x - 5, left_leg_y), 5)
    pygame.draw.line(surface, dark_green, (center_x + 5, 15), (center_x + 5, right_leg_y), 5)


def draw_zombie_left(surface: pygame.Surface, x_offset: int, frame: int) -> None:
    """Draw zombie facing left (side view) with walking animation."""
    center_x = x_offset + SPRITE_SIZE // 2
    center_y = 24  # Scaled 1.5x

    # Colors
    green = (0, 180, 50)
    dark_green = (0, 140, 40)
    black = (0, 0, 0)

    # Walking animation - leg positions (side view, scaled 1.5x)
    if frame == 0:  # Left leg forward
        front_leg_x = center_x - 3
        back_leg_x = center_x + 2
    elif frame == 1:  # Standing
        front_leg_x = center_x
        back_leg_x = center_x
    else:  # Right leg forward
        front_leg_x = center_x + 2
        back_leg_x = center_x - 3

    # Legs
    pygame.draw.line(surface, dark_green, (back_leg_x, center_y + 6), (back_leg_x, center_y + 15), 5)
    pygame.draw.line(surface, dark_green, (front_leg_x, center_y + 6), (front_leg_x, center_y + 15), 5)

    # Body (side profile - narrower)
    pygame.draw.ellipse(surface, green, (center_x - 5, center_y - 6, 9, 15))

    # Arm (one visible in side view)
    arm_swing = (frame - 1) * 3
    pygame.draw.line(surface, green, (center_x, center_y), (center_x - 8, center_y + 5 + arm_swing), 3)

    # Head
    pygame.draw.circle(surface, green, (center_x, center_y - 12), 6)

    # Eye (one visible from side)
    pygame.draw.circle(surface, black, (center_x - 3, center_y - 12), 2)


def draw_zombie_right(surface: pygame.Surface, x_offset: int, frame: int) -> None:
    """Draw zombie facing right (side view) with walking animation."""
    center_x = x_offset + SPRITE_SIZE // 2
    center_y = 24  # Scaled 1.5x

    # Colors
    green = (0, 180, 50)
    dark_green = (0, 140, 40)
    black = (0, 0, 0)

    # Walking animation - leg positions (side view, mirrored, scaled 1.5x)
    if frame == 0:  # Left leg forward (appears back when facing right)
        front_leg_x = center_x + 3
        back_leg_x = center_x - 2
    elif frame == 1:  # Standing
        front_leg_x = center_x
        back_leg_x = center_x
    else:  # Right leg forward (appears front when facing right)
        front_leg_x = center_x - 2
        back_leg_x = center_x + 3

    # Legs
    pygame.draw.line(surface, dark_green, (back_leg_x, center_y + 6), (back_leg_x, center_y + 15), 5)
    pygame.draw.line(surface, dark_green, (front_leg_x, center_y + 6), (front_leg_x, center_y + 15), 5)

    # Body (side profile - narrower)
    pygame.draw.ellipse(surface, green, (center_x - 5, center_y - 6, 9, 15))

    # Arm (one visible in side view)
    arm_swing = (frame - 1) * 3
    pygame.draw.line(surface, green, (center_x, center_y), (center_x + 8, center_y + 5 + arm_swing), 3)

    # Head
    pygame.draw.circle(surface, green, (center_x, center_y - 12), 6)

    # Eye (one visible from side)
    pygame.draw.circle(surface, black, (center_x + 3, center_y - 12), 2)


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

    # Draw 3 walking animation frames
    for frame in range(FRAME_COUNT):
        x_offset = frame * SPRITE_SIZE

        # Draw zombie based on direction
        if direction == "down":
            draw_zombie_down(surface, x_offset, frame)
        elif direction == "up":
            draw_zombie_up(surface, x_offset, frame)
        elif direction == "left":
            draw_zombie_left(surface, x_offset, frame)
        elif direction == "right":
            draw_zombie_right(surface, x_offset, frame)

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
    print("✓ Zombies now have heads, bodies, arms, and legs!")
    print("✓ Walking animation with leg movement across 3 frames")


if __name__ == "__main__":
    main()
