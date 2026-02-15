"""Tests for asset loading system."""

from __future__ import annotations

import pygame
import pytest

from game.assets.loader import (
    ASSETS_DIR,
    clear_cache,
    load_image,
    load_player_sprites,
    load_zombie_sprites,
    split_sprite_sheet,
)
from game.core.constants import (
    PLAYER_FRAME_COUNT,
    PLAYER_SPRITE_SIZE,
    ZOMBIE_FRAME_COUNT,
    ZOMBIE_SPRITE_SIZE,
)

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
        assert len(frames) == ZOMBIE_FRAME_COUNT, (
            f"Direction {direction} has wrong frame count"
        )

        # Verify each frame is a valid Surface
        for i, frame in enumerate(frames):
            assert isinstance(frame, pygame.Surface), (
                f"Frame {i} in {direction} is not a Surface"
            )
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


def test_player_sprite_files_exist() -> None:
    """Test that all 4 player sprite sheets exist."""
    players_dir = ASSETS_DIR / "players"
    assert players_dir.exists()

    # Check that all 4 directions exist
    for direction in ["down", "up", "left", "right"]:
        sprite_path = players_dir / f"walk_{direction}.png"
        assert sprite_path.exists(), f"Missing player sprite: walk_{direction}.png"


def test_load_player_sprites_structure() -> None:
    """Test that load_player_sprites returns correct structure."""
    clear_cache()  # Start fresh

    sprites = load_player_sprites(
        sprite_size=PLAYER_SPRITE_SIZE, frame_count=PLAYER_FRAME_COUNT
    )

    # Verify directions present
    assert "down" in sprites
    assert "up" in sprites
    assert "left" in sprites
    assert "right" in sprites

    # Verify each direction has correct frame count (3 walk + 1 shoot = 4 total)
    for _direction, frames in sprites.items():
        assert len(frames) == PLAYER_FRAME_COUNT + 1  # 3 walk frames + 1 shoot frame

        for frame in frames:
            assert isinstance(frame, pygame.Surface)
            assert frame.get_width() == PLAYER_SPRITE_SIZE
            assert frame.get_height() == PLAYER_SPRITE_SIZE


def test_load_player_sprites_caching() -> None:
    """Test that player sprites are cached and reused."""
    clear_cache()

    sprites1 = load_player_sprites(
        sprite_size=PLAYER_SPRITE_SIZE, frame_count=PLAYER_FRAME_COUNT
    )
    sprites2 = load_player_sprites(
        sprite_size=PLAYER_SPRITE_SIZE, frame_count=PLAYER_FRAME_COUNT
    )

    # Should be the exact same dict object (cached)
    assert sprites1 is sprites2
