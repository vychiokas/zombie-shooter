"""Tests for dead zombie entity."""

from __future__ import annotations

import pygame

from game.entities.dead_zombie import DeadZombie

# Initialize pygame once for all tests
pygame.init()


def test_dead_zombie_initialization() -> None:
    """Test that DeadZombie initializes with correct attributes."""
    pos = pygame.Vector2(100, 200)

    corpse = DeadZombie(pos)

    assert corpse.pos.x == 100
    assert corpse.pos.y == 200
    assert corpse.lifetime > 0
    assert corpse.is_alive() is True
    assert corpse.sprite is not None


def test_dead_zombie_update_decreases_lifetime() -> None:
    """Test that update() decreases lifetime."""
    corpse = DeadZombie(pygame.Vector2(0, 0))
    initial_lifetime = corpse.lifetime

    is_alive = corpse.update(0.2)

    assert corpse.lifetime == initial_lifetime - 0.2
    assert is_alive is True


def test_dead_zombie_update_returns_true_when_alive() -> None:
    """Test that update() returns True when corpse is alive."""
    corpse = DeadZombie(pygame.Vector2(0, 0))
    corpse.lifetime = 5.0

    is_alive = corpse.update(0.1)

    assert is_alive is True


def test_dead_zombie_dies_when_lifetime_expires() -> None:
    """Test that corpse becomes not alive when lifetime <= 0."""
    corpse = DeadZombie(pygame.Vector2(0, 0))
    corpse.lifetime = 0.1

    is_alive = corpse.update(0.5)  # Exceed lifetime

    assert corpse.lifetime <= 0
    assert is_alive is False


def test_dead_zombie_draw_no_error() -> None:
    """Test that draw() executes without errors."""
    corpse = DeadZombie(pygame.Vector2(100, 100))
    screen = pygame.Surface((800, 600))

    corpse.draw(screen)  # Should not raise exception


def test_dead_zombie_pos_copy_independence() -> None:
    """Test that corpse pos is independent of source pos."""
    source_pos = pygame.Vector2(50, 50)
    corpse = DeadZombie(source_pos)

    source_pos.x = 999

    assert corpse.pos.x == 50  # Should not change
