"""Tests for Pickup entity."""

from __future__ import annotations

import pygame

from game.entities.pickup import Pickup


def test_pickup_initialization() -> None:
    """Test that Pickup initializes with correct attributes."""
    pos = pygame.Vector2(100, 200)
    weapon_type = "shotgun"

    pickup = Pickup(pos, weapon_type)

    assert pickup.pos.x == 100
    assert pickup.pos.y == 200
    assert pickup.weapon_type == "shotgun"
    assert pickup.radius == 20  # PICKUP_RADIUS
    assert pickup.ttl > 0


def test_pickup_position_copy() -> None:
    """Test that Pickup copies position to avoid reference issues."""
    pos = pygame.Vector2(100, 200)
    pickup = Pickup(pos, "pistol")

    # Modify original position
    pos.x = 500

    # Pickup position should be unchanged
    assert pickup.pos.x == 100


def test_pickup_update_decreases_ttl() -> None:
    """Test that update() decreases TTL."""
    pickup = Pickup(pygame.Vector2(0, 0), "smg")
    initial_ttl = pickup.ttl

    is_alive = pickup.update(1.0)  # 1 second elapsed

    assert pickup.ttl == initial_ttl - 1.0
    assert is_alive is True


def test_pickup_dies_when_ttl_expires() -> None:
    """Test that Pickup becomes not alive when TTL <= 0."""
    pickup = Pickup(pygame.Vector2(0, 0), "pistol")
    pickup.ttl = 0.5

    # Update with large dt to expire TTL
    is_alive = pickup.update(1.0)

    assert pickup.ttl <= 0
    assert is_alive is False


def test_pickup_is_alive() -> None:
    """Test is_alive() method."""
    pickup = Pickup(pygame.Vector2(0, 0), "shotgun")

    assert pickup.is_alive() is True

    pickup.ttl = 0
    assert pickup.is_alive() is False

    pickup.ttl = -1
    assert pickup.is_alive() is False


def test_pickup_weapon_types() -> None:
    """Test that all weapon types can be created."""
    for weapon in ["pistol", "shotgun", "smg"]:
        pickup = Pickup(pygame.Vector2(0, 0), weapon)
        assert pickup.weapon_type == weapon


def test_pickup_draw_no_error() -> None:
    """Test that draw() executes without errors."""
    pickup = Pickup(pygame.Vector2(100, 100), "pistol")
    screen = pygame.Surface((800, 600))

    # Should not raise exception
    pickup.draw(screen)
