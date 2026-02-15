"""Asset loading and caching for zombie shooter."""

from __future__ import annotations

from pathlib import Path

import pygame

# Module-level cache for loaded sprites
_sprite_cache: dict[str, dict[str, list[pygame.Surface]]] = {}

# Asset directory relative to this file
# From src/game/assets/loader.py → src/assets
ASSETS_DIR = Path(__file__).resolve().parent.parent.parent / "assets"


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
    # Skip conversion if no display is set (e.g., during testing)
    try:
        if surface.get_alpha() is not None or surface.get_colorkey() is not None:
            return surface.convert_alpha()
        return surface.convert()
    except pygame.error:
        # No video mode set - return unconverted surface (testing scenario)
        return surface


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
    sprite_size: int = 32, frame_count: int = 3, variant: str = "normal"
) -> dict[str, list[pygame.Surface]]:
    """Load zombie sprites for all 4 directions.

    Args:
        sprite_size: Width/height of each sprite frame in pixels.
        frame_count: Number of animation frames per direction.
        variant: Zombie variant type ("normal", "runner", "tank", etc.).

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
    cache_key = f"zombie_{variant}"
    if cache_key in _sprite_cache:
        return _sprite_cache[cache_key]

    # Determine sprite directory based on variant
    if variant == "normal":
        zombies_dir = ASSETS_DIR / "zombies"
    else:
        zombies_dir = ASSETS_DIR / "zombies" / variant

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


def load_player_sprites(
    sprite_size: int = 48, frame_count: int = 3
) -> dict[str, list[pygame.Surface]]:
    """Load player sprites for all 4 directions (walk + shoot).

    Args:
        sprite_size: Width/height of each sprite frame in pixels.
        frame_count: Number of walk animation frames per direction.

    Returns:
        Dictionary mapping direction to list of frame surfaces
        (walk frames + shoot sprite):
        {
            "down": [walk_frame0, walk_frame1, walk_frame2, shoot_frame],
            "up": [walk_frame0, walk_frame1, walk_frame2, shoot_frame],
            "left": [walk_frame0, walk_frame1, walk_frame2, shoot_frame],
            "right": [walk_frame0, walk_frame1, walk_frame2, shoot_frame]
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
        # Load walk sprite sheet for this direction
        walk_sheet_path = players_dir / f"walk_{direction}.png"
        walk_sheet = load_image(walk_sheet_path)

        # Split into walk frames
        walk_frames = split_sprite_sheet(walk_sheet, sprite_size, frame_count)

        # Load shoot sprite (single frame)
        shoot_sprite_path = players_dir / f"shoot_{direction}.png"
        shoot_sprite = load_image(shoot_sprite_path)

        # Combine walk frames + shoot sprite
        sprites[direction] = walk_frames + [shoot_sprite]

    # Cache for future calls
    _sprite_cache[cache_key] = sprites

    return sprites


def clear_cache() -> None:
    """Clear the sprite cache (useful for testing)."""
    _sprite_cache.clear()
