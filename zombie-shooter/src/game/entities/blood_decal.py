"""Blood decal entity for gore effects."""

from __future__ import annotations

import pygame

from game.core.constants import BLOOD_POOL_SIZE, CORPSE_PERSISTENCE


class BloodDecal:
    """Blood pool decal that persists under corpses."""

    def __init__(self, pos: pygame.Vector2) -> None:
        """Initialize blood decal.

        Args:
            pos: Position where blood pool appears.
        """
        self.pos = pos.copy()  # Copy to avoid reference issues
        self.lifetime = CORPSE_PERSISTENCE  # Seconds (matches corpse duration)
        self.size = BLOOD_POOL_SIZE  # Diameter in pixels
        self.color = (120, 0, 0)  # Dark red for blood pool

    def update(self, dt: float) -> bool:
        """Update blood decal lifetime.

        Args:
            dt: Delta time in seconds.

        Returns:
            True if decal is still alive, False if should be removed.
        """
        self.lifetime -= dt  # Countdown
        return self.is_alive()

    def is_alive(self) -> bool:
        """Check if decal should still exist.

        Returns:
            True if lifetime > 0, False otherwise.
        """
        return self.lifetime > 0

    def draw(self, screen: pygame.Surface) -> None:
        """Render blood decal with alpha transparency.

        Args:
            screen: Pygame surface to draw on.
        """
        # Create temporary surface for alpha blending
        temp_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)

        # Semi-transparent dark red (alpha 200 for layering)
        color_with_alpha = (*self.color, 200)

        # Draw ellipse on temp surface (centered)
        rect = pygame.Rect(0, 0, self.size, self.size)
        pygame.draw.ellipse(temp_surface, color_with_alpha, rect)

        # Blit temp surface to screen (centered on position)
        screen.blit(
            temp_surface,
            (int(self.pos.x) - self.size // 2, int(self.pos.y) - self.size // 2),
        )
