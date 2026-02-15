"""Tests for collision detection system."""

from __future__ import annotations

import pygame

from game.entities.bullet import Bullet
from game.entities.zombie import Zombie
from game.systems.collisions import (
    check_bullet_zombie_collisions,
    check_collision_circle,
)


def test_check_collision_circle_overlapping() -> None:
    """Test that overlapping circles are detected."""
    pos1 = pygame.Vector2(0, 0)
    pos2 = pygame.Vector2(5, 0)
    assert check_collision_circle(pos1, 10, pos2, 10) is True


def test_check_collision_circle_touching() -> None:
    """Test that touching circles are detected."""
    pos1 = pygame.Vector2(0, 0)
    pos2 = pygame.Vector2(20, 0)
    assert check_collision_circle(pos1, 10, pos2, 10) is True


def test_check_collision_circle_separated() -> None:
    """Test that separated circles are not detected."""
    pos1 = pygame.Vector2(0, 0)
    pos2 = pygame.Vector2(25, 0)
    assert check_collision_circle(pos1, 10, pos2, 10) is False


def test_check_collision_circle_same_position() -> None:
    """Test collision at same position."""
    pos = pygame.Vector2(100, 100)
    assert check_collision_circle(pos, 5, pos, 5) is True


def test_check_bullet_zombie_collisions_empty() -> None:
    """Test with no bullets or zombies."""
    assert check_bullet_zombie_collisions([], []) == []


def test_check_bullet_zombie_collisions_no_hits() -> None:
    """Test when bullets and zombies don't collide."""
    bullet = Bullet(pygame.Vector2(0, 0), pygame.Vector2(1, 0))
    zombie = Zombie(pygame.Vector2(100, 100))
    collisions = check_bullet_zombie_collisions([bullet], [zombie])
    assert collisions == []


def test_check_bullet_zombie_collisions_hit() -> None:
    """Test when bullet hits zombie."""
    bullet = Bullet(pygame.Vector2(50, 50), pygame.Vector2(1, 0))
    zombie = Zombie(pygame.Vector2(52, 50))
    collisions = check_bullet_zombie_collisions([bullet], [zombie])
    assert len(collisions) == 1
    assert collisions[0] == (0, 0)
