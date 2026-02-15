"""Bullet entity for zombie shooter."""

from __future__ import annotations

import pygame

from game.core.constants import BULLET_RADIUS, BULLET_SPEED, BULLET_TTL, HEIGHT, WIDTH


class Bullet:
    """Bullet entity with directional movement and TTL."""

    def __init__(self, pos: pygame.Vector2, direction: pygame.Vector2) -> None:
        """Initialize bullet.

        Args:
            pos: Starting position as Vector2.
            direction: Direction vector to travel.
        """
        self.pos = pos.copy()  # Copy to avoid reference issues
        self.vel = direction.normalize() * BULLET_SPEED
        self.radius = BULLET_RADIUS
        self.ttl = BULLET_TTL

    def update(self, dt: float) -> bool:
        """Update bullet position and TTL.

        Args:
            dt: Delta time in seconds.

        Returns:
            True if bullet is still alive, False if should be removed.
        """
        self.pos += self.vel * dt
        self.ttl -= dt
        return self.is_alive()

    def is_alive(self) -> bool:
        """Check if bullet should be removed.

        Returns:
            True if bullet is still valid, False otherwise.
        """
        if self.ttl <= 0:
            return False
        if self.pos.x < 0 or self.pos.x > WIDTH:
            return False
        return not (self.pos.y < 0 or self.pos.y > HEIGHT)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw bullet to screen.

        Args:
            screen: Pygame surface to draw on.
        """
        # Draw yellow circle
        pygame.draw.circle(
            screen, (255, 255, 0), (int(self.pos.x), int(self.pos.y)), self.radius
        )
