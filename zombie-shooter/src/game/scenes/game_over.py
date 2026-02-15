"""Game over scene for zombie shooter."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from game.core.constants import WIDTH
from game.core.scene import Scene

if TYPE_CHECKING:
    from game.core.game import Game


class GameOverScene(Scene):
    """Game over / win screen scene."""

    def __init__(self, game: Game, kills: int, won: bool) -> None:
        """Initialize game over scene.

        Args:
            game: Game instance for scene switching.
            kills: Final kill count to display.
            won: True if player won, False if lost.
        """
        self.game = game
        self.kills = kills
        self.won = won
        self.font_large = pygame.font.Font(None, 74)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle game over events.

        Args:
            event: Pygame event to process.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                from game.scenes.play import PlayScene

                self.game.change_scene(PlayScene(self.game))
            elif event.key == pygame.K_ESCAPE:
                from game.scenes.menu import MenuScene

                self.game.change_scene(MenuScene(self.game))

    def update(self, dt: float) -> None:
        """Update game over (no-op for static screen).

        Args:
            dt: Delta time in seconds.
        """
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Draw game over screen.

        Args:
            screen: Pygame surface to draw on.
        """
        screen.fill((0, 0, 0))

        # Result text
        result_text = "You Win!" if self.won else "Game Over"
        result_color = (0, 255, 0) if self.won else (255, 0, 0)
        result_surface = self.font_large.render(result_text, True, result_color)
        result_rect = result_surface.get_rect(center=(WIDTH // 2, 150))
        screen.blit(result_surface, result_rect)

        # Kills text
        kills_surface = self.font_medium.render(
            f"Kills: {self.kills}", True, (255, 255, 255)
        )
        kills_rect = kills_surface.get_rect(center=(WIDTH // 2, 280))
        screen.blit(kills_surface, kills_rect)

        # Instructions
        restart_surface = self.font_small.render(
            "Press R to Restart", True, (200, 200, 200)
        )
        restart_rect = restart_surface.get_rect(center=(WIDTH // 2, 400))
        screen.blit(restart_surface, restart_rect)

        menu_surface = self.font_small.render(
            "Press ESC for Menu", True, (200, 200, 200)
        )
        menu_rect = menu_surface.get_rect(center=(WIDTH // 2, 450))
        screen.blit(menu_surface, menu_rect)
