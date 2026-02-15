"""Tests for gore system integration in PlayScene."""

from __future__ import annotations

from unittest.mock import MagicMock

import pygame

from game.core.constants import BLOOD_PARTICLE_COUNT
from game.entities.zombie import Zombie
from game.scenes.play import PlayScene

# Initialize pygame once for all tests
pygame.init()


def test_play_scene_initializes_gore_lists() -> None:
    """Test that PlayScene initializes with empty gore entity lists."""
    game = MagicMock()
    scene = PlayScene(game)

    assert scene.blood_particles == []
    assert scene.dead_zombies == []
    assert scene.blood_decals == []


def test_gore_spawns_on_zombie_kill() -> None:
    """Test that killing a zombie spawns gore entities."""
    game = MagicMock()
    scene = PlayScene(game)

    # Add a zombie and bullet
    zombie = Zombie(pygame.Vector2(100, 100))
    scene.zombies.append(zombie)

    from game.entities.bullet import Bullet
    bullet = Bullet(pygame.Vector2(98, 98), pygame.Vector2(1, 0))
    scene.bullets.append(bullet)

    # Verify initial state
    assert len(scene.blood_particles) == 0
    assert len(scene.dead_zombies) == 0
    assert len(scene.blood_decals) == 0

    # Update to trigger collision
    scene.update(0.01)

    # Should have spawned gore entities
    assert len(scene.blood_particles) == BLOOD_PARTICLE_COUNT  # 8 particles
    assert len(scene.dead_zombies) == 1  # 1 corpse
    assert len(scene.blood_decals) == 1  # 1 blood pool

    # Zombie and bullet should be removed
    assert len(scene.zombies) == 0
    assert len(scene.bullets) == 0


def test_gore_entities_cleanup_after_ttl() -> None:
    """Test that gore entities are removed after TTL expires."""
    game = MagicMock()
    scene = PlayScene(game)

    # Add a zombie and bullet to trigger gore spawn
    zombie = Zombie(pygame.Vector2(100, 100))
    scene.zombies.append(zombie)

    from game.entities.bullet import Bullet
    bullet = Bullet(pygame.Vector2(98, 98), pygame.Vector2(1, 0))
    scene.bullets.append(bullet)

    # Trigger kill
    scene.update(0.01)

    # Verify gore spawned
    assert len(scene.dead_zombies) == 1
    assert len(scene.blood_decals) == 1
    blood_particle_count = len(scene.blood_particles)
    assert blood_particle_count == BLOOD_PARTICLE_COUNT

    # Fast-forward past blood particle lifetime (0.8s)
    for _ in range(10):
        scene.update(0.1)  # Total 1.0s
        scene.pickup_spawn_timer = 0.0  # Prevent pickup spawning

    # Blood particles should be gone (0.8s lifetime)
    assert len(scene.blood_particles) == 0

    # Corpse and decal should still exist (10.0s lifetime)
    assert len(scene.dead_zombies) == 1
    assert len(scene.blood_decals) == 1

    # Fast-forward past corpse persistence (10.0s total)
    for _ in range(95):  # 95 * 0.1 = 9.5s more (total 10.5s)
        scene.update(0.1)
        scene.pickup_spawn_timer = 0.0

    # All gore should be removed
    assert len(scene.dead_zombies) == 0
    assert len(scene.blood_decals) == 0


def test_multiple_simultaneous_kills() -> None:
    """Test that multiple simultaneous kills spawn correct gore counts."""
    game = MagicMock()
    scene = PlayScene(game)

    # Add 5 zombies at different positions
    for i in range(5):
        zombie = Zombie(pygame.Vector2(100 + i * 50, 100))
        scene.zombies.append(zombie)

    # Add 5 bullets to kill them all
    from game.entities.bullet import Bullet
    for i in range(5):
        bullet = Bullet(pygame.Vector2(100 + i * 50, 100), pygame.Vector2(1, 0))
        scene.bullets.append(bullet)

    # Trigger collisions
    scene.update(0.01)

    # Should have spawned gore for all 5 kills
    assert len(scene.blood_particles) == 5 * BLOOD_PARTICLE_COUNT  # 5 * 8 = 40
    assert len(scene.dead_zombies) == 5
    assert len(scene.blood_decals) == 5

    # All zombies and bullets should be removed
    assert len(scene.zombies) == 0
    assert len(scene.bullets) == 0
