"""Game class managing pygame lifecycle and scene switching."""

from __future__ import annotations

import pygame

from game.core.constants import FPS, HEIGHT, WIDTH
from game.core.scene import Scene


class Game:
    """Main game class managing pygame and scene switching."""

    def __init__(self) -> None:
        """Initialize pygame and create window."""
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Zombie Shooter")
        self.clock = pygame.time.Clock()
        self.running = False
        self.scene: Scene | None = None

    def change_scene(self, new_scene: Scene) -> None:
        """Switch to a new scene.

        Args:
            new_scene: Scene instance to switch to.
        """
        self.scene = new_scene

    def quit(self) -> None:
        """Signal the game to exit."""
        self.running = False

    def run(self) -> None:
        """Run the main game loop."""
        if self.scene is None:
            raise ValueError("No initial scene set. Call change_scene() before run().")

        self.running = True

        while self.running:
            # Calculate delta time in seconds
            dt = self.clock.tick(FPS) / 1000.0

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if self.scene:
                    self.scene.handle_event(event)

            # Update and draw scene
            if self.scene:
                self.scene.update(dt)
                self.scene.draw(self.screen)

            pygame.display.flip()

        pygame.quit()
