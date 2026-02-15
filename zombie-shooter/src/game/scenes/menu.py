"""Menu scene for zombie shooter."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from game.core.constants import WIDTH
from game.core.scene import Scene

if TYPE_CHECKING:
    from game.core.game import Game


class MenuScene(Scene):
    """Main menu scene."""

    def __init__(self, game: Game) -> None:
        """Initialize menu scene.

        Args:
            game: Game instance for scene switching.
        """
        self.game = game
        self.font_large = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 36)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle menu events.

        Args:
            event: Pygame event to process.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                from game.scenes.play import PlayScene

                self.game.change_scene(PlayScene(self.game))
            elif event.key == pygame.K_ESCAPE:
                self.game.quit()

    def update(self, dt: float) -> None:
        """Update menu (no-op for static menu).

        Args:
            dt: Delta time in seconds.
        """
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Draw menu to screen.

        Args:
            screen: Pygame surface to draw on.
        """
        screen.fill((0, 0, 0))  # Black background

        # Title
        title_surface = self.font_large.render("Zombie Shooter", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(WIDTH // 2, 200))
        screen.blit(title_surface, title_rect)

        # Instructions
        start_surface = self.font_small.render(
            "Press ENTER to Start", True, (200, 200, 200)
        )
        start_rect = start_surface.get_rect(center=(WIDTH // 2, 350))
        screen.blit(start_surface, start_rect)

        quit_surface = self.font_small.render(
            "Press ESC to Quit", True, (200, 200, 200)
        )
        quit_rect = quit_surface.get_rect(center=(WIDTH // 2, 400))
        screen.blit(quit_surface, quit_rect)
