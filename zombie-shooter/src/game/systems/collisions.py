"""Collision detection system."""

from __future__ import annotations

import pygame


def check_collision_circle(
    pos1: pygame.Vector2, r1: float, pos2: pygame.Vector2, r2: float
) -> bool:
    """Check if two circles overlap using distance squared (no sqrt).

    Args:
        pos1: Position of first circle.
        r1: Radius of first circle.
        pos2: Position of second circle.
        r2: Radius of second circle.

    Returns:
        True if circles overlap, False otherwise.
    """
    dx = pos2.x - pos1.x
    dy = pos2.y - pos1.y
    distance_squared = dx * dx + dy * dy
    radius_sum = r1 + r2
    return distance_squared <= radius_sum * radius_sum


def check_bullet_zombie_collisions(
    bullets: list, zombies: list
) -> list[tuple[int, int]]:
    """Check all bullet-zombie collisions.

    Args:
        bullets: List of bullet entities.
        zombies: List of zombie entities.

    Returns:
        List of (bullet_idx, zombie_idx) tuples for collisions.
    """
    collisions = []
    for b_idx, bullet in enumerate(bullets):
        for z_idx, zombie in enumerate(zombies):
            if check_collision_circle(
                bullet.pos, bullet.radius, zombie.pos, zombie.radius
            ):
                collisions.append((b_idx, z_idx))
    return collisions


def check_player_zombie_collisions(
    player_pos: pygame.Vector2, player_radius: float, zombies: list
) -> list[int]:
    """Check player-zombie collisions.

    Args:
        player_pos: Player position.
        player_radius: Player collision radius.
        zombies: List of zombie entities.

    Returns:
        List of zombie indices that are colliding with player.
    """
    colliding = []
    for z_idx, zombie in enumerate(zombies):
        if check_collision_circle(player_pos, player_radius, zombie.pos, zombie.radius):
            colliding.append(z_idx)
    return colliding


def check_player_pickup_collisions(
    player_pos: pygame.Vector2, player_radius: float, pickups: list
) -> list[int]:
    """Check player-pickup collisions.

    Args:
        player_pos: Player position.
        player_radius: Player collision radius.
        pickups: List of pickup entities.

    Returns:
        List of pickup indices that are colliding with player.
    """
    colliding = []
    for p_idx, pickup in enumerate(pickups):
        if check_collision_circle(player_pos, player_radius, pickup.pos, pickup.radius):
            colliding.append(p_idx)
    return colliding


def check_acid_projectile_player_collisions(
    player_pos: pygame.Vector2, player_radius: float, projectiles: list
) -> list[int]:
    """Check player-acid projectile collisions.

    Args:
        player_pos: Player position as Vector2.
        player_radius: Player collision radius.
        projectiles: List of AcidProjectile instances.

    Returns:
        List of projectile indices that collided with player.
    """
    colliding = []
    for p_idx, projectile in enumerate(projectiles):
        if check_collision_circle(
            player_pos, player_radius, projectile.pos, projectile.radius
        ):
            colliding.append(p_idx)
    return colliding
