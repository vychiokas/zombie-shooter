"""Tests for zombie animation integration."""

from __future__ import annotations

import pygame

from game.entities.zombie import Zombie

# Initialize pygame once for all tests
pygame.init()


def test_zombie_has_animation_instance() -> None:
    """Test that zombie initializes with Animation instance."""
    zombie = Zombie(pygame.Vector2(100, 100))
    assert hasattr(zombie, "animation")
    assert zombie.animation is not None


def test_zombie_has_sprites_loaded() -> None:
    """Test that zombie sprites are loaded correctly."""
    zombie = Zombie(pygame.Vector2(100, 100))
    assert hasattr(zombie, "sprites")
    assert zombie.sprites is not None

    # Check all 4 directions exist
    assert "down" in zombie.sprites
    assert "up" in zombie.sprites
    assert "left" in zombie.sprites
    assert "right" in zombie.sprites

    # Check each direction has frames
    for _direction, frames in zombie.sprites.items():
        assert len(frames) == 3  # ZOMBIE_FRAME_COUNT
        for frame in frames:
            assert isinstance(frame, pygame.Surface)


def test_zombie_has_velocity_attribute() -> None:
    """Test that zombie has velocity attribute for animation."""
    zombie = Zombie(pygame.Vector2(100, 100))
    assert hasattr(zombie, "vel")
    assert isinstance(zombie.vel, pygame.Vector2)


def test_zombie_animation_updates_on_movement() -> None:
    """Test that animation.update() is called during zombie update."""
    zombie = Zombie(pygame.Vector2(100, 100))

    # Move zombie to the right
    player_pos = pygame.Vector2(200, 100)
    zombie.update(0.1, player_pos)

    # Animation should have updated (velocity is non-zero)
    assert zombie.vel.length() > 0
    # Direction should be "right" for rightward movement
    assert zombie.animation.get_current_direction() == "right"


def test_zombie_velocity_set_correctly() -> None:
    """Test that zombie velocity is set during update."""
    zombie = Zombie(pygame.Vector2(100, 100))

    # Move zombie to the right
    zombie.update(0.1, pygame.Vector2(200, 100))

    # Velocity should be non-zero
    assert zombie.vel.length() > 0
    # Velocity magnitude should be zombie speed
    assert abs(zombie.vel.length() - 140.0) < 0.1  # ZOMBIE_SPEED = 140


def test_zombie_renders_without_error() -> None:
    """Test that zombie draw() doesn't raise exceptions."""
    zombie = Zombie(pygame.Vector2(100, 100))

    # Create a test surface
    screen = pygame.Surface((800, 600))

    # Should not raise any errors
    zombie.draw(screen)


def test_zombie_collision_unchanged() -> None:
    """Test that zombie collision attributes (pos, radius) are unchanged."""
    zombie = Zombie(pygame.Vector2(100, 100))

    # Collision attributes should still exist
    assert hasattr(zombie, "pos")
    assert hasattr(zombie, "radius")
    assert zombie.radius == 16  # ZOMBIE_RADIUS

    # Position should update correctly
    zombie.update(0.1, pygame.Vector2(200, 200))
    assert zombie.pos != pygame.Vector2(100, 100)  # Position changed


def test_multiple_zombies_animate_independently() -> None:
    """Test that multiple zombies have independent animation timers."""
    zombie1 = Zombie(pygame.Vector2(100, 100))
    zombie2 = Zombie(pygame.Vector2(200, 200))

    # Move zombies in different directions
    zombie1.update(0.1, pygame.Vector2(200, 100))  # Right
    zombie2.update(0.1, pygame.Vector2(200, 300))  # Down

    # Directions should be different
    assert zombie1.animation.get_current_direction() == "right"
    assert zombie2.animation.get_current_direction() == "down"

    # Animations are independent instances
    assert zombie1.animation is not zombie2.animation


def test_zombie_sprites_are_shared() -> None:
    """Test that zombie sprites are shared across instances (cached)."""
    zombie1 = Zombie(pygame.Vector2(100, 100))
    zombie2 = Zombie(pygame.Vector2(200, 200))

    # Sprites should be the same object (module-level cache)
    assert zombie1.sprites is zombie2.sprites
