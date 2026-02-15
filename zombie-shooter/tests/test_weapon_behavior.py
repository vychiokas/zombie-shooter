"""Tests for weapon behavior and firing patterns."""

from __future__ import annotations

import pygame

from game.core.constants import WEAPON_STATS
from game.entities.player import Player

# Initialize pygame once for all tests
pygame.init()


def test_pistol_fires_single_bullet() -> None:
    """Test that pistol fires a single bullet."""
    player = Player(pygame.Vector2(100, 100))
    player.current_weapon = "pistol"

    # Shoot at target position
    target = pygame.Vector2(200, 200)
    bullets = player.shoot(target)

    # Pistol should fire 1 bullet
    assert len(bullets) == 1


def test_shotgun_fires_five_bullets() -> None:
    """Test that shotgun fires five bullets."""
    player = Player(pygame.Vector2(100, 100))
    player.current_weapon = "shotgun"

    # Shoot at target position
    target = pygame.Vector2(200, 200)
    bullets = player.shoot(target)

    # Shotgun should fire 5 bullets
    assert len(bullets) == 5


def test_shotgun_spread_pattern() -> None:
    """Test that shotgun bullets spread in a pattern."""
    player = Player(pygame.Vector2(100, 100))
    player.current_weapon = "shotgun"

    # Shoot straight up
    target = pygame.Vector2(100, 0)
    bullets = player.shoot(target)

    # All bullets should start at same position
    for bullet in bullets:
        assert bullet.pos == player.pos

    # Bullets should have different directions (spread)
    directions = [bullet.vel.normalize() for bullet in bullets]

    # Check that directions are not all the same
    assert not all(d == directions[0] for d in directions)


def test_smg_fire_rate() -> None:
    """Test that SMG has faster fire rate than pistol."""
    smg_rate = WEAPON_STATS["smg"]["fire_rate"]
    pistol_rate = WEAPON_STATS["pistol"]["fire_rate"]

    # SMG should fire faster (lower cooldown)
    assert smg_rate < pistol_rate


def test_weapon_cooldowns() -> None:
    """Test that weapon cooldowns are set correctly."""
    player = Player(pygame.Vector2(100, 100))
    target = pygame.Vector2(200, 200)

    # Test pistol cooldown
    player.current_weapon = "pistol"
    player.shoot(target)
    assert player.shoot_cooldown == WEAPON_STATS["pistol"]["fire_rate"]

    # Reset cooldown
    player.shoot_cooldown = 0.0

    # Test shotgun cooldown
    player.current_weapon = "shotgun"
    player.shoot(target)
    assert player.shoot_cooldown == WEAPON_STATS["shotgun"]["fire_rate"]

    # Reset cooldown
    player.shoot_cooldown = 0.0

    # Test SMG cooldown
    player.current_weapon = "smg"
    player.shoot(target)
    assert player.shoot_cooldown == WEAPON_STATS["smg"]["fire_rate"]


def test_pistol_single_shot_on_cooldown() -> None:
    """Test that weapons respect cooldown."""
    player = Player(pygame.Vector2(100, 100))
    target = pygame.Vector2(200, 200)

    # First shot should work
    bullets = player.shoot(target)
    assert len(bullets) == 1

    # Second shot immediately should fail (on cooldown)
    bullets = player.shoot(target)
    assert len(bullets) == 0


def test_smg_fires_single_bullet() -> None:
    """Test that SMG fires a single bullet per shot."""
    player = Player(pygame.Vector2(100, 100))
    player.current_weapon = "smg"

    # Shoot at target position
    target = pygame.Vector2(200, 200)
    bullets = player.shoot(target)

    # SMG should fire 1 bullet (rapid fire, not spread)
    assert len(bullets) == 1
