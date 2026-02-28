"""Collision detection system."""

from __future__ import annotations

import math

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


def resolve_circle_vs_circle_obstacle(
    entity_pos: pygame.Vector2,
    entity_radius: float,
    obstacle_pos: pygame.Vector2,
    obstacle_radius: float,
) -> pygame.Vector2:
    """Push entity out of a circular obstacle using minimum separation.

    Args:
        entity_pos: Entity center position.
        entity_radius: Entity collision radius.
        obstacle_pos: Obstacle center position.
        obstacle_radius: Obstacle collision radius.

    Returns:
        Corrected entity position (unchanged if no overlap).
    """
    diff = entity_pos - obstacle_pos
    dist = diff.length()
    min_dist = entity_radius + obstacle_radius

    if dist < min_dist:
        if dist > 0:
            return obstacle_pos + diff.normalize() * min_dist
        # Exactly on center — push upward
        return pygame.Vector2(obstacle_pos.x, obstacle_pos.y - min_dist)
    return pygame.Vector2(entity_pos)


def resolve_circle_vs_rect_obstacle(
    entity_pos: pygame.Vector2,
    entity_radius: float,
    obstacle_rect: pygame.Rect,
) -> pygame.Vector2:
    """Push entity circle out of a rectangular obstacle (AABB).

    Uses closest-point-on-rect method: finds nearest point on the rect to
    entity center, then pushes entity out along that normal. For entity
    centers inside the rect, falls back to axis-of-least-overlap push.

    Args:
        entity_pos: Entity center position.
        entity_radius: Entity collision radius.
        obstacle_rect: Obstacle axis-aligned bounding rect.

    Returns:
        Corrected entity position (unchanged if no overlap).
    """
    closest_x = max(
        float(obstacle_rect.left), min(entity_pos.x, float(obstacle_rect.right))
    )
    closest_y = max(
        float(obstacle_rect.top), min(entity_pos.y, float(obstacle_rect.bottom))
    )

    diff_x = entity_pos.x - closest_x
    diff_y = entity_pos.y - closest_y
    dist_sq = diff_x * diff_x + diff_y * diff_y

    if dist_sq >= entity_radius * entity_radius:
        return pygame.Vector2(entity_pos)  # no overlap

    new_pos = pygame.Vector2(entity_pos)

    if dist_sq > 0:
        # Push along normal from closest point to entity center
        dist = math.sqrt(dist_sq)
        new_pos.x = closest_x + (diff_x / dist) * entity_radius
        new_pos.y = closest_y + (diff_y / dist) * entity_radius
    else:
        # Entity center is inside rect — push out on axis with smaller overlap
        cx = float(obstacle_rect.centerx)
        cy = float(obstacle_rect.centery)
        half_w = obstacle_rect.width / 2.0 + entity_radius
        half_h = obstacle_rect.height / 2.0 + entity_radius

        push_x = half_w - abs(entity_pos.x - cx)
        push_y = half_h - abs(entity_pos.y - cy)

        if push_x < push_y:
            sign_x = 1.0 if entity_pos.x >= cx else -1.0
            new_pos.x = cx + sign_x * half_w
        else:
            sign_y = 1.0 if entity_pos.y >= cy else -1.0
            new_pos.y = cy + sign_y * half_h

    return new_pos


def resolve_entity_vs_obstacles(
    entity_pos: pygame.Vector2,
    entity_radius: float,
    obstacles: list,
) -> pygame.Vector2:
    """Apply push-out resolution against all solid obstacles.

    Args:
        entity_pos: Entity center position.
        entity_radius: Entity collision radius.
        obstacles: List of Obstacle instances.

    Returns:
        Corrected entity position after all push-outs.
    """
    pos = pygame.Vector2(entity_pos)

    for obstacle in obstacles:
        if not obstacle.solid:
            continue

        if obstacle.shape == "circle":
            pos = resolve_circle_vs_circle_obstacle(
                pos, entity_radius, obstacle.pos, obstacle.radius
            )
        else:
            # rect and ellipse both use AABB
            pos = resolve_circle_vs_rect_obstacle(
                pos, entity_radius, obstacle.get_rect()
            )

    return pos
