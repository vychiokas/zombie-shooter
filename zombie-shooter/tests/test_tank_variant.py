"""Tests for tank zombie variant."""

from __future__ import annotations

import pygame

from game.core.constants import ZOMBIE_VARIANTS
from game.entities.zombie import Zombie

pygame.init()


def test_tank_variant_has_correct_stats() -> None:
    """Test that tank zombie initializes with correct variant stats."""
    tank = Zombie(pygame.Vector2(100, 100), variant="tank")

    assert tank.variant == "tank"
    assert tank.hp == 3  # Requires 3 hits
    assert tank.speed == 98  # 0.7x normal speed (140 * 0.7 = 98)
    assert tank.radius == 24  # Larger hitbox (16 * 1.5 = 24)


def test_tank_variant_survives_one_hit() -> None:
    """Test that tank survives first hit (HP reduces but tank lives)."""
    tank = Zombie(pygame.Vector2(100, 100), variant="tank")

    initial_hp = tank.hp
    tank.hp -= 1  # Simulate bullet hit

    assert tank.hp == initial_hp - 1
    assert tank.hp == 2  # Still alive with 2 HP


def test_tank_variant_survives_two_hits() -> None:
    """Test that tank survives second hit."""
    tank = Zombie(pygame.Vector2(100, 100), variant="tank")

    tank.hp -= 1  # First hit
    tank.hp -= 1  # Second hit

    assert tank.hp == 1  # Still alive with 1 HP


def test_tank_variant_dies_after_three_hits() -> None:
    """Test that tank dies after third hit."""
    tank = Zombie(pygame.Vector2(100, 100), variant="tank")

    tank.hp -= 1  # First hit: 3→2
    tank.hp -= 1  # Second hit: 2→1
    tank.hp -= 1  # Third hit: 1→0

    assert tank.hp <= 0  # Dead


def test_tank_variant_moves_slower_than_normal() -> None:
    """Test that tank moves slower than normal zombie."""
    tank = Zombie(pygame.Vector2(100, 100), variant="tank")
    normal = Zombie(pygame.Vector2(200, 200), variant="normal")

    assert tank.speed < normal.speed
    assert tank.speed == 98
    assert normal.speed == 140


def test_tank_variant_has_larger_hitbox() -> None:
    """Test that tank has larger collision radius than normal zombie."""
    tank = Zombie(pygame.Vector2(100, 100), variant="tank")
    normal = Zombie(pygame.Vector2(200, 200), variant="normal")

    assert tank.radius > normal.radius
    assert tank.radius == 24
    assert normal.radius == 16


def test_tank_variant_loads_unique_sprites() -> None:
    """Test that tank loads variant-specific sprites."""
    tank = Zombie(pygame.Vector2(100, 100), variant="tank")

    # Should have sprites for all 4 directions
    assert "down" in tank.sprites
    assert "up" in tank.sprites
    assert "left" in tank.sprites
    assert "right" in tank.sprites

    # Each direction should have 3 frames
    for direction in ["down", "up", "left", "right"]:
        assert len(tank.sprites[direction]) == 3


def test_tank_variant_constants_defined() -> None:
    """Test that tank variant is properly defined in constants."""
    assert "tank" in ZOMBIE_VARIANTS

    tank_stats = ZOMBIE_VARIANTS["tank"]
    assert tank_stats["speed"] == 98
    assert tank_stats["hp"] == 3
    assert tank_stats["radius"] == 24
    assert tank_stats["weight"] == 1.5  # 15% spawn rate
