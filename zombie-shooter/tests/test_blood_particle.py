"""Tests for blood particle entity."""

from __future__ import annotations

import pygame

from game.entities.blood_particle import BloodParticle

# Initialize pygame once for all tests
pygame.init()


def test_blood_particle_initialization() -> None:
    """Test that BloodParticle initializes with correct attributes."""
    pos = pygame.Vector2(100, 200)
    vel = pygame.Vector2(50, -30)

    particle = BloodParticle(pos, vel)

    assert particle.pos.x == 100
    assert particle.pos.y == 200
    assert particle.vel.x == 50
    assert particle.vel.y == -30
    assert particle.lifetime > 0
    assert particle.radius == 3
    assert particle.is_alive() is True


def test_blood_particle_update_moves_position() -> None:
    """Test that update() moves particle based on velocity."""
    particle = BloodParticle(pygame.Vector2(0, 0), pygame.Vector2(100, 0))

    particle.update(0.1)  # 0.1 seconds

    assert particle.pos.x == 10  # 100 * 0.1
    assert particle.pos.y == 0


def test_blood_particle_update_decreases_lifetime() -> None:
    """Test that update() decreases lifetime."""
    particle = BloodParticle(pygame.Vector2(0, 0), pygame.Vector2(0, 0))
    initial_lifetime = particle.lifetime

    is_alive = particle.update(0.2)

    assert particle.lifetime == initial_lifetime - 0.2
    assert is_alive is True


def test_blood_particle_dies_when_lifetime_expires() -> None:
    """Test that particle becomes not alive when lifetime <= 0."""
    particle = BloodParticle(pygame.Vector2(0, 0), pygame.Vector2(0, 0))
    particle.lifetime = 0.1

    is_alive = particle.update(0.5)  # Exceed lifetime

    assert particle.lifetime <= 0
    assert is_alive is False


def test_blood_particle_alpha_fades_over_time() -> None:
    """Test that alpha decreases as lifetime decreases."""
    particle = BloodParticle(pygame.Vector2(0, 0), pygame.Vector2(0, 0))

    alpha_start = particle.get_alpha()
    particle.update(0.4)  # Half of 0.8s lifetime
    alpha_mid = particle.get_alpha()
    particle.update(0.35)  # Near end
    alpha_end = particle.get_alpha()

    assert alpha_start == 255  # Full opacity
    assert 100 < alpha_mid < 150  # Mid-fade
    assert alpha_end < 50  # Nearly transparent


def test_blood_particle_draw_no_error() -> None:
    """Test that draw() executes without errors."""
    particle = BloodParticle(pygame.Vector2(100, 100), pygame.Vector2(0, 0))
    screen = pygame.Surface((800, 600))

    particle.draw(screen)  # Should not raise exception


def test_blood_particle_pos_copy_independence() -> None:
    """Test that particle pos is independent of source pos."""
    source_pos = pygame.Vector2(50, 50)
    particle = BloodParticle(source_pos, pygame.Vector2(0, 0))

    source_pos.x = 999

    assert particle.pos.x == 50  # Should not change
