"""Pickup entity for zombie shooter."""

from __future__ import annotations

import pygame

from game.core.constants import HUD_ICON_H, HUD_ICON_W, PICKUP_RADIUS, PICKUP_TTL
from game.systems.weapon_art import build_weapon_icons

# Module-level icon cache: built once, reused by all Pickup instances.
_pickup_icons: dict[str, pygame.Surface] | None = None


def _get_pickup_icons() -> dict[str, pygame.Surface]:
    """Return scaled weapon icon surfaces, building them on first call.

    Icons are scaled from HUD size (52×30) to fit within the pickup area.

    Returns:
        Dict mapping weapon name to scaled Surface.
    """
    global _pickup_icons
    if _pickup_icons is None:
        raw = build_weapon_icons()
        icon_w = PICKUP_RADIUS * 2          # 40 px wide
        icon_h = icon_w * HUD_ICON_H // HUD_ICON_W  # ~23 px — keep aspect ratio
        _pickup_icons = {
            k: pygame.transform.scale(v, (icon_w, icon_h))
            for k, v in raw.items()
        }
    return _pickup_icons


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
        """Draw pickup to screen as a weapon icon with glow ring.

        Args:
            screen: Pygame surface to draw on.
        """
        cx = int(self.pos.x)
        cy = int(self.pos.y)

        # Glow ring colour per weapon type
        glow_colors = {
            "pistol": (200, 160, 60),   # warm gold
            "shotgun": (180, 80, 60),   # orange-red
            "smg": (60, 160, 200),      # cyan
        }
        glow = glow_colors.get(self.weapon_type, (160, 160, 160))

        # Dark backing disc
        pygame.draw.circle(screen, (20, 20, 20), (cx, cy), self.radius)
        # Coloured glow ring
        pygame.draw.circle(screen, glow, (cx, cy), self.radius, 3)

        # Weapon icon centred on position
        icons = _get_pickup_icons()
        icon = icons.get(self.weapon_type)
        if icon is not None:
            ir = icon.get_rect(center=(cx, cy))
            # Tint icon to match glow colour before blitting
            tinted = icon.copy()
            tinted.fill((*glow, 0), special_flags=pygame.BLEND_RGB_MULT)
            screen.blit(tinted, ir)
