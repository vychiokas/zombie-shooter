"""Dead zombie entity for gore effects."""

from __future__ import annotations

import pygame

from game.assets.loader import load_zombie_sprites
from game.core.constants import (
    CORPSE_PERSISTENCE,
    ZOMBIE_FRAME_COUNT,
    ZOMBIE_SPRITE_SIZE,
)

# Module-level sprite loading (shared across all instances)
_dead_zombie_sprite: pygame.Surface | None = None


def _load_dead_zombie_sprite() -> pygame.Surface:
    """Load and rotate zombie sprite for fallen corpse effect.

    Returns:
        Rotated zombie sprite (90° clockwise for fallen effect).
    """
    global _dead_zombie_sprite
    if _dead_zombie_sprite is None:
        # Load zombie sprites
        zombie_sprites = load_zombie_sprites(
            sprite_size=ZOMBIE_SPRITE_SIZE, frame_count=ZOMBIE_FRAME_COUNT
        )
        # Use down direction, first frame as base
        base_sprite = zombie_sprites["down"][0]
        # Rotate 90° clockwise (negative angle) for fallen effect
        _dead_zombie_sprite = pygame.transform.rotate(base_sprite, -90)
    return _dead_zombie_sprite


class DeadZombie:
    """Dead zombie corpse that persists temporarily."""

    def __init__(self, pos: pygame.Vector2) -> None:
        """Initialize dead zombie corpse.

        Args:
            pos: Position where zombie died.
        """
        self.pos = pos.copy()  # Copy to avoid reference issues
        self.lifetime = CORPSE_PERSISTENCE  # Seconds
        self.sprite = _load_dead_zombie_sprite()

    def update(self, dt: float) -> bool:
        """Update corpse lifetime.

        Args:
            dt: Delta time in seconds.

        Returns:
            True if corpse is still alive, False if should be removed.
        """
        self.lifetime -= dt  # Countdown
        return self.is_alive()

    def is_alive(self) -> bool:
        """Check if corpse should still exist.

        Returns:
            True if lifetime > 0, False otherwise.
        """
        return self.lifetime > 0

    def draw(self, screen: pygame.Surface) -> None:
        """Render dead zombie sprite.

        Args:
            screen: Pygame surface to draw on.
        """
        # Center sprite on position
        rect = self.sprite.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        screen.blit(self.sprite, rect)
