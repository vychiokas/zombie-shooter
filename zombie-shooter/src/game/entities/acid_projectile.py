"""Acid projectile entity for spitter zombie attacks."""

from __future__ import annotations

import pygame

from game.core.constants import (
    ACID_PROJECTILE_DAMAGE,
    ACID_PROJECTILE_RADIUS,
    ACID_PROJECTILE_SPEED,
    ACID_PROJECTILE_TTL,
    HEIGHT,
    WIDTH,
)


class AcidProjectile:
    """Acid projectile entity with directional movement and TTL."""

    def __init__(self, pos: pygame.Vector2, direction: pygame.Vector2) -> None:
        """Initialize acid projectile.

        Args:
            pos: Starting position as Vector2.
            direction: Direction vector (will be normalized).
        """
        self.pos = pos.copy()  # Copy to avoid reference issues
        self.vel = direction.normalize() * ACID_PROJECTILE_SPEED
        self.radius = ACID_PROJECTILE_RADIUS
        self.ttl = ACID_PROJECTILE_TTL
        self.damage = ACID_PROJECTILE_DAMAGE

    def update(self, dt: float) -> bool:
        """Update projectile position and TTL.

        Args:
            dt: Delta time in seconds.

        Returns:
            True if projectile should remain in list, False if should be removed.
        """
        self.pos += self.vel * dt
        self.ttl -= dt
        return self.is_alive()

    def is_alive(self) -> bool:
        """Check if projectile should be removed.

        Returns:
            True if projectile is still active, False if expired or off-screen.
        """
        if self.ttl <= 0:
            return False
        if self.pos.x < 0 or self.pos.x > WIDTH:
            return False
        return not (self.pos.y < 0 or self.pos.y > HEIGHT)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw acid projectile as green circle.

        Args:
            screen: Pygame surface to draw on.
        """
        pygame.draw.circle(
            screen, (100, 255, 100), (int(self.pos.x), int(self.pos.y)), self.radius
        )
