"""Tests for pickup spawning integration in PlayScene."""

from __future__ import annotations

from unittest.mock import MagicMock

import pygame

from game.core.constants import (
    HEIGHT,
    PICKUP_SPAWN_MARGIN,
    PICKUP_SPAWN_RATE,
    WIDTH,
)
from game.scenes.play import PlayScene

# Initialize pygame once for all tests
pygame.init()


def test_play_scene_initializes_pickups() -> None:
    """Test that PlayScene initializes with empty pickups list."""
    game = MagicMock()
    scene = PlayScene(game)
    assert scene.pickups == []
    assert scene.pickup_spawn_timer == 0.0


def test_pickup_spawn_timer_increments() -> None:
    """Test that pickup spawn timer increments with dt."""
    game = MagicMock()
    scene = PlayScene(game)
    initial_timer = scene.pickup_spawn_timer
    scene.update(0.5)
    assert scene.pickup_spawn_timer == initial_timer + 0.5


def test_pickup_spawns_after_spawn_rate() -> None:
    """Test that pickup spawns after PICKUP_SPAWN_RATE seconds."""
    game = MagicMock()
    scene = PlayScene(game)
    assert len(scene.pickups) == 0

    # Update with exactly spawn rate time
    scene.update(PICKUP_SPAWN_RATE)

    # Should have spawned one pickup
    assert len(scene.pickups) == 1
    # Timer should reset
    assert scene.pickup_spawn_timer == 0.0


def test_pickup_spawn_timer_resets() -> None:
    """Test that pickup spawn timer resets after spawning."""
    game = MagicMock()
    scene = PlayScene(game)

    # Advance time to spawn
    scene.update(PICKUP_SPAWN_RATE)

    assert scene.pickup_spawn_timer == 0.0
    assert len(scene.pickups) == 1


def test_pickup_spawn_position_within_margins() -> None:
    """Test that spawned pickup is within safe margins."""
    game = MagicMock()
    scene = PlayScene(game)

    # Spawn multiple pickups to check randomness
    for _ in range(5):
        scene.update(PICKUP_SPAWN_RATE)

    # Check all pickups are within safe area
    for pickup in scene.pickups:
        assert PICKUP_SPAWN_MARGIN <= pickup.pos.x <= WIDTH - PICKUP_SPAWN_MARGIN
        assert PICKUP_SPAWN_MARGIN <= pickup.pos.y <= HEIGHT - PICKUP_SPAWN_MARGIN


def test_pickup_has_weapon_type() -> None:
    """Test that spawned pickup has a weapon type."""
    game = MagicMock()
    scene = PlayScene(game)

    scene.update(PICKUP_SPAWN_RATE)

    assert len(scene.pickups) == 1
    pickup = scene.pickups[0]
    assert pickup.weapon_type in ["pistol", "shotgun", "smg"]


def test_player_collects_pickup() -> None:
    """Test that player collects pickup on collision."""
    game = MagicMock()
    scene = PlayScene(game)

    # Spawn a pickup directly at player position for guaranteed collision
    from game.entities.pickup import Pickup

    pickup = Pickup(scene.player.pos.copy(), "shotgun")
    scene.pickups.append(pickup)

    assert scene.player.current_weapon == "pistol"  # Default weapon

    # Update should trigger collision
    scene.update(0.01)

    # Player should have picked up shotgun
    assert scene.player.current_weapon == "shotgun"
    # Pickup should be removed
    assert len(scene.pickups) == 0


def test_pickup_despawns_after_ttl() -> None:
    """Test that pickup despawns after TTL expires."""
    game = MagicMock()
    scene = PlayScene(game)

    # Spawn a pickup
    scene.update(PICKUP_SPAWN_RATE)
    assert len(scene.pickups) == 1

    # Get TTL from pickup
    pickup = scene.pickups[0]
    ttl = pickup.ttl

    # Update with time less than TTL but enough to expire it
    # Use small increments to avoid spawning a new pickup
    time_step = 1.0
    elapsed = 0.0
    while elapsed < ttl:
        scene.update(time_step)
        elapsed += time_step
        # Reset spawn timer to prevent new spawn
        scene.pickup_spawn_timer = 0.0

    # Pickup should be removed after exceeding TTL
    assert len(scene.pickups) == 0
