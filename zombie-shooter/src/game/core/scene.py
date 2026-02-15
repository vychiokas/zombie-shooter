"""Base scene class for all game scenes."""

from __future__ import annotations

import pygame


class Scene:
    """Base class for all game scenes."""

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle pygame events.

        Args:
            event: Pygame event to process.
        """
        pass

    def update(self, dt: float) -> None:
        """Update scene logic.

        Args:
            dt: Delta time in seconds since last frame.
        """
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Draw scene to screen.

        Args:
            screen: Pygame surface to draw on.
        """
        pass
