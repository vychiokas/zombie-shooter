"""Pickup entity for zombie shooter."""

from __future__ import annotations

import pygame

from game.core.constants import PICKUP_RADIUS, PICKUP_TTL


class Pickup:
    """Collectible pickup entity with weapon type and TTL."""

    def __init__(self, pos: pygame.Vector2, weapon_type: str) -> None:
        """Initialize pickup.

        Args:
            pos: Starting position as Vector2.
            weapon_type: Type of weapon ("pistol", "shotgun", or "smg").
        """
        self.pos = pos.copy()  # Copy to avoid reference issues
        self.radius = PICKUP_RADIUS
        self.weapon_type = weapon_type
        self.ttl = PICKUP_TTL

    def update(self, dt: float) -> bool:
        """Update pickup TTL.

        Args:
            dt: Delta time in seconds.

        Returns:
            True if pickup is still alive, False if should be removed.
        """
        self.ttl -= dt
        return self.is_alive()

    def is_alive(self) -> bool:
        """Check if pickup is still alive.

        Returns:
            True if TTL > 0, False otherwise.
        """
        return self.ttl > 0

    def draw(self, screen: pygame.Surface) -> None:
        """Draw pickup to screen as colored rectangle.

        Args:
            screen: Pygame surface to draw on.
        """
        # Color mapping for weapon types
        colors = {
            "pistol": (255, 200, 100),  # Yellow/orange
            "shotgun": (255, 100, 100),  # Red
            "smg": (100, 200, 255),  # Cyan
        }
        color = colors.get(self.weapon_type, (200, 200, 200))  # Gray fallback

        # Draw rectangle centered on position
        pygame.draw.rect(
            screen,
            color,
            pygame.Rect(
                int(self.pos.x) - self.radius,  # Left edge
                int(self.pos.y) - self.radius,  # Top edge
                self.radius * 2,  # Width (square)
                self.radius * 2,  # Height (square)
            ),
        )
