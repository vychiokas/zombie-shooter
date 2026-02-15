"""Tests for blood decal entity."""

from __future__ import annotations

import pygame

from game.entities.blood_decal import BloodDecal

# Initialize pygame once for all tests
pygame.init()


def test_blood_decal_initialization() -> None:
    """Test that BloodDecal initializes with correct attributes."""
    pos = pygame.Vector2(100, 200)

    decal = BloodDecal(pos)

    assert decal.pos.x == 100
    assert decal.pos.y == 200
    assert decal.lifetime > 0
    assert decal.size == 28
    assert decal.is_alive() is True


def test_blood_decal_update_decreases_lifetime() -> None:
    """Test that update() decreases lifetime."""
    decal = BloodDecal(pygame.Vector2(0, 0))
    initial_lifetime = decal.lifetime

    is_alive = decal.update(0.2)

    assert decal.lifetime == initial_lifetime - 0.2
    assert is_alive is True


def test_blood_decal_update_returns_true_when_alive() -> None:
    """Test that update() returns True when decal is alive."""
    decal = BloodDecal(pygame.Vector2(0, 0))
    decal.lifetime = 5.0

    is_alive = decal.update(0.1)

    assert is_alive is True


def test_blood_decal_dies_when_lifetime_expires() -> None:
    """Test that decal becomes not alive when lifetime <= 0."""
    decal = BloodDecal(pygame.Vector2(0, 0))
    decal.lifetime = 0.1

    is_alive = decal.update(0.5)  # Exceed lifetime

    assert decal.lifetime <= 0
    assert is_alive is False


def test_blood_decal_draw_no_error() -> None:
    """Test that draw() executes without errors."""
    decal = BloodDecal(pygame.Vector2(100, 100))
    screen = pygame.Surface((800, 600))

    decal.draw(screen)  # Should not raise exception


def test_blood_decal_pos_copy_independence() -> None:
    """Test that decal pos is independent of source pos."""
    source_pos = pygame.Vector2(50, 50)
    decal = BloodDecal(source_pos)

    source_pos.x = 999

    assert decal.pos.x == 50  # Should not change
