"""Tests for acid projectile entity."""

from __future__ import annotations

import pygame

from game.core.constants import (
    ACID_PROJECTILE_DAMAGE,
    ACID_PROJECTILE_RADIUS,
    ACID_PROJECTILE_SPEED,
    ACID_PROJECTILE_TTL,
)
from game.entities.acid_projectile import AcidProjectile

pygame.init()


def test_acid_projectile_initialization() -> None:
    """Test that acid projectile initializes with correct attributes."""
    pos = pygame.Vector2(100, 100)
    direction = pygame.Vector2(1, 0)
    projectile = AcidProjectile(pos, direction)

    assert projectile.pos.x == 100
    assert projectile.pos.y == 100
    assert projectile.radius == ACID_PROJECTILE_RADIUS
    assert projectile.ttl == ACID_PROJECTILE_TTL
    assert projectile.damage == ACID_PROJECTILE_DAMAGE


def test_acid_projectile_position_copy() -> None:
    """Test that acid projectile copies position (no reference issues)."""
    pos = pygame.Vector2(100, 100)
    direction = pygame.Vector2(1, 0)
    projectile = AcidProjectile(pos, direction)

    pos.x = 200  # Modify original
    assert projectile.pos.x == 100  # Projectile position unchanged


def test_acid_projectile_update_moves_position() -> None:
    """Test that acid projectile moves based on velocity."""
    projectile = AcidProjectile(pygame.Vector2(100, 100), pygame.Vector2(1, 0))
    initial_x = projectile.pos.x

    projectile.update(0.1)

    assert projectile.pos.x > initial_x
    # Speed is 300, so in 0.1 seconds moves 30 pixels
    assert abs(projectile.pos.x - (initial_x + ACID_PROJECTILE_SPEED * 0.1)) < 0.1


def test_acid_projectile_update_decreases_ttl() -> None:
    """Test that acid projectile TTL decreases over time."""
    projectile = AcidProjectile(pygame.Vector2(100, 100), pygame.Vector2(1, 0))
    initial_ttl = projectile.ttl

    projectile.update(0.5)

    assert projectile.ttl < initial_ttl
    assert abs(projectile.ttl - (initial_ttl - 0.5)) < 0.01


def test_acid_projectile_dies_when_ttl_expires() -> None:
    """Test that acid projectile is removed after TTL expires."""
    projectile = AcidProjectile(pygame.Vector2(100, 100), pygame.Vector2(1, 0))

    is_alive = projectile.update(ACID_PROJECTILE_TTL + 0.5)

    assert is_alive is False


def test_acid_projectile_dies_off_screen() -> None:
    """Test that acid projectile is removed when off-screen."""
    projectile = AcidProjectile(pygame.Vector2(100, 100), pygame.Vector2(-1, 0))

    # Move far off screen
    for _ in range(100):
        projectile.update(0.1)

    assert projectile.is_alive() is False


def test_acid_projectile_draw_no_error() -> None:
    """Test that acid projectile draws without error."""
    projectile = AcidProjectile(pygame.Vector2(100, 100), pygame.Vector2(1, 0))
    screen = pygame.Surface((800, 600))

    projectile.draw(screen)  # Should not raise
