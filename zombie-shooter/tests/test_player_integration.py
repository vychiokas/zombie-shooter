"""Tests for player animation integration."""

from __future__ import annotations

import unittest.mock as mock

import pygame
import pytest

from game.core.constants import (
    PLAYER_ANIMATION_FPS,
    PLAYER_FRAME_COUNT,
    PLAYER_SHOOT_DURATION,
    PLAYER_SPRITE_SIZE,
)
from game.entities.player import Player

# Initialize pygame once for all tests
pygame.init()


def test_player_has_animation_instance() -> None:
    """Test that player initializes with Animation instance."""
    player = Player(pygame.Vector2(400, 300))
    assert hasattr(player, "animation")
    assert player.animation is not None


def test_player_has_sprites_loaded() -> None:
    """Test that player sprites are loaded correctly."""
    player = Player(pygame.Vector2(400, 300))
    assert hasattr(player, "sprites")
    assert player.sprites is not None

    # Check all 4 directions exist
    assert "down" in player.sprites
    assert "up" in player.sprites
    assert "left" in player.sprites
    assert "right" in player.sprites

    # Check each direction has frames (3 walk + 1 shoot = 4 total)
    for _direction, frames in player.sprites.items():
        assert len(frames) == PLAYER_FRAME_COUNT + 1  # 3 walk frames + 1 shoot frame
        for frame in frames:
            assert isinstance(frame, pygame.Surface)
            assert frame.get_width() == PLAYER_SPRITE_SIZE
            assert frame.get_height() == PLAYER_SPRITE_SIZE


def test_player_has_velocity_attribute() -> None:
    """Test that player has velocity attribute for animation."""
    player = Player(pygame.Vector2(400, 300))
    assert hasattr(player, "vel")
    assert isinstance(player.vel, pygame.Vector2)


def test_player_animation_updates_on_movement() -> None:
    """Test that animation.update() is called during player update."""
    player = Player(pygame.Vector2(400, 300))

    # Mock keyboard input for rightward movement
    with mock.patch('pygame.key.get_pressed') as mock_keys:
        mock_keys.return_value = {
            pygame.K_a: False,
            pygame.K_d: True,  # Moving right
            pygame.K_w: False,
            pygame.K_s: False,
        }
        # Update player (will call animation.update())
        player.update(0.1)

    # Velocity should be non-zero during movement
    assert player.vel.length() > 0
    # Direction should be "right" for rightward movement
    assert player.animation.get_current_direction() == "right"


def test_player_renders_without_error() -> None:
    """Test that player.draw() executes without errors."""
    player = Player(pygame.Vector2(400, 300))
    screen = pygame.Surface((800, 600))

    # Should not raise exception
    player.draw(screen)


def test_player_animation_fps_matches_constant() -> None:
    """Test that animation FPS matches defined constant."""
    player = Player(pygame.Vector2(400, 300))
    expected_frame_duration = 1.0 / PLAYER_ANIMATION_FPS
    assert player.animation.frame_duration == expected_frame_duration


def test_player_sprites_are_shared() -> None:
    """Test that player sprites are shared across instances (cached)."""
    player1 = Player(pygame.Vector2(100, 100))
    player2 = Player(pygame.Vector2(200, 200))

    # Should be the exact same dict object (module-level cache)
    assert player1.sprites is player2.sprites


def test_player_has_shoot_timer_attribute() -> None:
    """Test that player initializes with shoot_timer attribute."""
    player = Player(pygame.Vector2(400, 300))
    assert hasattr(player, "shoot_timer")
    assert player.shoot_timer == 0.0


def test_player_shoot_timer_set_on_fire() -> None:
    """Test that shoot_timer is set when player shoots."""
    player = Player(pygame.Vector2(400, 300))
    target = pygame.Vector2(500, 300)

    # Fire weapon
    player.shoot(target)

    # Verify shoot timer was set
    assert player.shoot_timer == PLAYER_SHOOT_DURATION


def test_player_shoot_timer_decrements() -> None:
    """Test that shoot_timer decrements during update."""
    player = Player(pygame.Vector2(400, 300))
    player.shoot_timer = 0.5

    # Update with dt
    player.update(0.1)

    # Timer should have decremented
    assert player.shoot_timer == pytest.approx(0.4, abs=1e-6)


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
