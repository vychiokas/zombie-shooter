"""Tests for exploder zombie variant."""

from __future__ import annotations

from unittest.mock import MagicMock

import pygame

from game.core.constants import ZOMBIE_VARIANTS
from game.entities.zombie import Zombie
from game.scenes.play import PlayScene

pygame.init()


def test_exploder_variant_has_correct_stats() -> None:
    """Test that exploder zombie initializes with correct variant stats."""
    exploder = Zombie(pygame.Vector2(100, 100), variant="exploder")

    assert exploder.variant == "exploder"
    assert exploder.hp == 1  # One-shot kill
    assert exploder.speed == 140  # Normal speed
    assert exploder.radius == 16  # Normal hitbox


def test_exploder_variant_dies_in_one_hit() -> None:
    """Test that exploder dies from single bullet hit."""
    exploder = Zombie(pygame.Vector2(100, 100), variant="exploder")

    exploder.hp -= 1  # Simulate bullet hit

    assert exploder.hp <= 0  # Dead


def test_exploder_explosion_damages_nearby_zombies() -> None:
    """Test that explosion damages nearby zombies within radius."""
    game = MagicMock()
    scene = PlayScene(game)

    exploder = Zombie(pygame.Vector2(100, 100), variant="exploder")
    nearby = Zombie(pygame.Vector2(150, 100))  # 50px away (within 80px)
    far = Zombie(pygame.Vector2(300, 100))  # 200px away (outside 80px)

    scene.zombies.extend([exploder, nearby, far])

    # Kill exploder with bullet
    from game.entities.bullet import Bullet

    bullet = Bullet(pygame.Vector2(98, 98), pygame.Vector2(1, 0))
    scene.bullets.append(bullet)
    scene.update(0.01)

    # Nearby should take damage, far should not
    assert nearby.hp < 1  # Was damaged by explosion
    assert far.hp == 1  # Untouched


def test_exploder_explosion_damages_player() -> None:
    """Test that explosion damages player if within radius."""
    game = MagicMock()
    scene = PlayScene(game)

    exploder = Zombie(pygame.Vector2(100, 100), variant="exploder")
    scene.zombies.append(exploder)

    # Move player close to exploder
    scene.player.pos = pygame.Vector2(150, 100)  # 50px away (within 80px)
    initial_hp = scene.player.hp

    # Kill exploder
    from game.entities.bullet import Bullet

    bullet = Bullet(pygame.Vector2(98, 98), pygame.Vector2(1, 0))
    scene.bullets.append(bullet)
    scene.update(0.01)

    # Player should take damage
    assert scene.player.hp < initial_hp


def test_exploder_chain_reaction() -> None:
    """Test that exploding Exploder triggers nearby Exploders (chain reaction)."""
    game = MagicMock()
    scene = PlayScene(game)

    # Create two Exploders within explosion radius of each other
    exploder1 = Zombie(pygame.Vector2(100, 100), variant="exploder")
    exploder2 = Zombie(pygame.Vector2(150, 100), variant="exploder")  # 50px away
    normal = Zombie(pygame.Vector2(140, 100))  # Between them

    scene.zombies.extend([exploder1, exploder2, normal])

    # Kill first Exploder
    from game.entities.bullet import Bullet

    bullet = Bullet(pygame.Vector2(98, 98), pygame.Vector2(1, 0))
    scene.bullets.append(bullet)
    scene.update(0.01)

    # Both Exploders should be dead (chain reaction)
    # Normal zombie between them should take 2 damage (one from each explosion)
    assert exploder1.hp <= 0
    assert exploder2.hp <= 0
    assert normal.hp <= -1  # Took damage from both explosions


def test_exploder_does_not_damage_far_zombies() -> None:
    """Test that explosion only affects zombies within radius."""
    game = MagicMock()
    scene = PlayScene(game)

    exploder = Zombie(pygame.Vector2(100, 100), variant="exploder")
    far_zombie = Zombie(pygame.Vector2(300, 300))  # ~283px away (outside 80px)

    scene.zombies.extend([exploder, far_zombie])

    # Kill Exploder
    from game.entities.bullet import Bullet

    bullet = Bullet(pygame.Vector2(98, 98), pygame.Vector2(1, 0))
    scene.bullets.append(bullet)
    scene.update(0.01)

    # Far zombie should be untouched
    assert far_zombie.hp == 1


def test_exploder_spawns_enhanced_particles() -> None:
    """Test that Exploder death spawns more particles than normal death."""
    game = MagicMock()
    scene = PlayScene(game)

    exploder = Zombie(pygame.Vector2(100, 100), variant="exploder")
    scene.zombies.append(exploder)

    initial_particles = len(scene.blood_particles)

    # Kill Exploder
    from game.entities.bullet import Bullet

    bullet = Bullet(pygame.Vector2(98, 98), pygame.Vector2(1, 0))
    scene.bullets.append(bullet)
    scene.update(0.01)

    # Should have spawned explosion particles (16) + blood splash particles (8)
    # Total: 24 particles
    assert len(scene.blood_particles) > initial_particles + 16


def test_exploder_variant_loads_unique_sprites() -> None:
    """Test that exploder loads variant-specific sprites."""
    exploder = Zombie(pygame.Vector2(100, 100), variant="exploder")

    # Should have sprites for all 4 directions
    assert "down" in exploder.sprites
    assert "up" in exploder.sprites
    assert "left" in exploder.sprites
    assert "right" in exploder.sprites

    # Each direction should have 3 frames
    for direction in ["down", "up", "left", "right"]:
        assert len(exploder.sprites[direction]) == 3


def test_exploder_variant_constants_defined() -> None:
    """Test that exploder variant is properly defined in constants."""
    assert "exploder" in ZOMBIE_VARIANTS

    exploder_stats = ZOMBIE_VARIANTS["exploder"]
    assert exploder_stats["speed"] == 140
    assert exploder_stats["hp"] == 1
    assert exploder_stats["radius"] == 16
    assert exploder_stats["weight"] == 1.0  # 10% spawn rate
