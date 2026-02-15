"""Tests for gore system edge cases and boundary conditions."""

from __future__ import annotations

from unittest.mock import MagicMock

import pygame

from game.entities.blood_decal import BloodDecal
from game.entities.blood_particle import BloodParticle
from game.entities.dead_zombie import DeadZombie
from game.entities.zombie import Zombie
from game.scenes.play import PlayScene

# Initialize pygame once for all tests
pygame.init()


def test_gore_update_with_empty_lists() -> None:
    """Test that updating PlayScene with no gore entities causes no errors."""
    game = MagicMock()
    scene = PlayScene(game)

    # Verify lists are empty
    assert scene.blood_particles == []
    assert scene.dead_zombies == []
    assert scene.blood_decals == []

    # Update should not raise exception
    scene.update(0.1)

    # Lists should still be empty
    assert scene.blood_particles == []
    assert scene.dead_zombies == []
    assert scene.blood_decals == []


def test_gore_draw_with_empty_lists() -> None:
    """Test that drawing PlayScene with no gore entities causes no errors."""
    game = MagicMock()
    scene = PlayScene(game)

    # Verify lists are empty
    assert scene.blood_particles == []
    assert scene.dead_zombies == []
    assert scene.blood_decals == []

    # Create test screen
    screen = pygame.Surface((800, 600))

    # Draw should not raise exception
    scene.draw(screen)


def test_multiple_corpses_at_same_position() -> None:
    """Test that multiple zombies killed at identical position don't cause bugs."""
    game = MagicMock()
    scene = PlayScene(game)

    # Add 3 zombies at exact same position
    for _ in range(3):
        zombie = Zombie(pygame.Vector2(100, 100))
        scene.zombies.append(zombie)

    # Add 1 bullet at same position (will collide with all 3 zombies)
    from game.entities.bullet import Bullet
    bullet = Bullet(pygame.Vector2(100, 100), pygame.Vector2(1, 0))
    scene.bullets.append(bullet)

    # Trigger collisions
    scene.update(0.01)

    # Should have spawned gore for all 3 kills (even though only 1 bullet)
    # Note: Collision system detects all zombie-bullet overlaps
    assert len(scene.dead_zombies) >= 3  # At least 3 corpses
    assert len(scene.blood_decals) >= 3  # At least 3 blood pools

    # Draw should handle overlapping entities without errors
    screen = pygame.Surface((800, 600))
    scene.draw(screen)


def test_rapid_kill_spawn_cycle() -> None:
    """Test that killing 10 zombies in 0.1s works correctly."""
    game = MagicMock()
    scene = PlayScene(game)

    # Add 10 zombies
    for i in range(10):
        zombie = Zombie(pygame.Vector2(100 + i * 30, 100))
        scene.zombies.append(zombie)

    # Add 10 bullets
    from game.entities.bullet import Bullet
    for i in range(10):
        bullet = Bullet(pygame.Vector2(100 + i * 30, 100), pygame.Vector2(1, 0))
        scene.bullets.append(bullet)

    # Verify initial state
    assert len(scene.zombies) == 10
    assert len(scene.dead_zombies) == 0

    # Single update to trigger all collisions
    scene.update(0.01)

    # Verify all kills processed
    assert len(scene.zombies) == 0
    assert len(scene.dead_zombies) == 10
    assert len(scene.blood_decals) == 10


def test_gore_entities_beyond_ttl() -> None:
    """Test that entities with negative lifetime are safely removed."""
    game = MagicMock()
    scene = PlayScene(game)

    # Create gore entities and manually set lifetime to negative
    particle = BloodParticle(pygame.Vector2(100, 100), pygame.Vector2(10, 10))
    particle.lifetime = -1.0  # Expired
    scene.blood_particles.append(particle)

    corpse = DeadZombie(pygame.Vector2(200, 200))
    corpse.lifetime = -5.0  # Expired
    scene.dead_zombies.append(corpse)

    decal = BloodDecal(pygame.Vector2(300, 300))
    decal.lifetime = -2.0  # Expired
    scene.blood_decals.append(decal)

    # Verify entities added
    assert len(scene.blood_particles) == 1
    assert len(scene.dead_zombies) == 1
    assert len(scene.blood_decals) == 1

    # Update should remove expired entities
    scene.update(0.01)

    # All should be removed
    assert len(scene.blood_particles) == 0
    assert len(scene.dead_zombies) == 0
    assert len(scene.blood_decals) == 0
