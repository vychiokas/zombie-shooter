"""Main entry point for the zombie shooter game."""

from __future__ import annotations

from game.core.game import Game
from game.scenes.menu import MenuScene


def main() -> None:
    """Launch the game."""
    game = Game()
    game.change_scene(MenuScene(game))
    game.run()


if __name__ == "__main__":
    main()
