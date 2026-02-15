"""Tests for gore entity timing precision and TTL accuracy."""

from __future__ import annotations

import pygame

from game.core.constants import BLOOD_PARTICLE_LIFETIME, CORPSE_PERSISTENCE
from game.entities.blood_decal import BloodDecal
from game.entities.blood_particle import BloodParticle
from game.entities.dead_zombie import DeadZombie

# Initialize pygame once for all tests
pygame.init()


def test_corpse_ttl_accuracy() -> None:
    """Test that corpse lifetime decreases accurately over time."""
    corpse = DeadZombie(pygame.Vector2(100, 100))

    # Initial lifetime should be CORPSE_PERSISTENCE (10.0s)
    assert abs(corpse.lifetime - CORPSE_PERSISTENCE) < 0.01

    # Update 101 times with dt=0.1s (total 10.1s - exceeds TTL)
    for _ in range(101):
        corpse.update(0.1)

    # After 10.1s, corpse should be below 0 lifetime
    assert corpse.lifetime < 0  # Should be negative
    assert corpse.is_alive() is False  # Should be dead


def test_blood_decal_ttl_accuracy() -> None:
    """Test that blood decal lifetime decreases accurately over time."""
    decal = BloodDecal(pygame.Vector2(200, 200))

    # Initial lifetime should be CORPSE_PERSISTENCE (10.0s)
    assert abs(decal.lifetime - CORPSE_PERSISTENCE) < 0.01

    # Update 101 times with dt=0.1s (total 10.1s - exceeds TTL)
    for _ in range(101):
        decal.update(0.1)

    # After 10.1s, decal should be below 0 lifetime
    assert decal.lifetime < 0  # Should be negative
    assert decal.is_alive() is False


def test_blood_particle_ttl_accuracy() -> None:
    """Test that blood particle lifetime decreases accurately over time."""
    particle = BloodParticle(pygame.Vector2(300, 300), pygame.Vector2(10, 10))

    # Initial lifetime should be BLOOD_PARTICLE_LIFETIME (0.8s)
    assert abs(particle.lifetime - BLOOD_PARTICLE_LIFETIME) < 0.01

    # Update 9 times with dt=0.1s (total 0.9s - exceeds TTL)
    for _ in range(9):
        particle.update(0.1)

    # After 0.9s, particle should be below 0 lifetime
    assert particle.lifetime < 0  # Should be negative
    assert particle.is_alive() is False


def test_gore_ttl_synchronized() -> None:
    """Test that corpse and decal have identical lifetime values initially."""
    corpse = DeadZombie(pygame.Vector2(100, 100))
    decal = BloodDecal(pygame.Vector2(100, 100))

    # Both should start with CORPSE_PERSISTENCE
    assert abs(corpse.lifetime - CORPSE_PERSISTENCE) < 0.01
    assert abs(decal.lifetime - CORPSE_PERSISTENCE) < 0.01

    # Both should have identical initial lifetime
    assert abs(corpse.lifetime - decal.lifetime) < 0.01

    # Update both with same dt
    corpse.update(0.5)
    decal.update(0.5)

    # Both should have decreased by same amount
    expected_lifetime = CORPSE_PERSISTENCE - 0.5
    assert abs(corpse.lifetime - expected_lifetime) < 0.01
    assert abs(decal.lifetime - expected_lifetime) < 0.01

    # Still synchronized
    assert abs(corpse.lifetime - decal.lifetime) < 0.01
