"""Shared weapon icon art used by both the HUD and pickup entities."""

from __future__ import annotations

import pygame

from game.core.constants import HUD_ICON_H, HUD_ICON_W


def build_weapon_icons() -> dict[str, pygame.Surface]:
    """Build weapon icon surfaces for all known weapon types.

    Each surface is HUD_ICON_W × HUD_ICON_H (52 × 30) on a transparent
    SRCALPHA background, silhouette colour (200, 200, 200).

    Returns:
        Dict mapping weapon name to Surface.
    """
    icons: dict[str, pygame.Surface] = {}
    w, h = HUD_ICON_W, HUD_ICON_H  # 52 x 30
    c = (200, 200, 200)

    for weapon in ("pistol", "shotgun", "smg"):
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 0))

        if weapon == "pistol":
            # Body center-right, short barrel right, grip below
            pygame.draw.rect(surf, c, pygame.Rect(w // 2 - 6, h // 2 - 5, 20, 10))
            pygame.draw.rect(surf, c, pygame.Rect(w - 16, h // 2 - 3, 16, 6))
            pygame.draw.rect(surf, c, pygame.Rect(w // 2 - 2, h // 2 + 5, 8, 14))
            pygame.draw.line(
                surf, (180, 180, 180),
                (w // 2 + 6, h // 2 + 4), (w // 2 + 10, h // 2 + 10), 2,
            )

        elif weapon == "shotgun":
            # Long barrel across top, body center, pump, stock left
            pygame.draw.rect(surf, c, pygame.Rect(8, h // 2 - 3, w - 10, 6))
            pygame.draw.rect(surf, c, pygame.Rect(w // 3, h // 2 - 5, 18, 10))
            pygame.draw.rect(surf, c, pygame.Rect(w // 2 - 2, h // 2 - 6, 8, 4))
            pygame.draw.rect(surf, c, pygame.Rect(2, h // 2 - 8, 12, 16))
            pygame.draw.circle(surf, (180, 180, 180), (w - 4, h // 2), 4)

        else:  # smg
            # Boxy body, short barrel, vertical mag, small stock
            pygame.draw.rect(surf, c, pygame.Rect(w // 4, h // 2 - 5, 24, 10))
            pygame.draw.rect(surf, c, pygame.Rect(w // 4 + 24, h // 2 - 3, 12, 6))
            pygame.draw.rect(surf, c, pygame.Rect(w // 4 + 8, h // 2 + 5, 8, 14))
            pygame.draw.rect(surf, c, pygame.Rect(4, h // 2 - 4, 10, 8))

        icons[weapon] = surf

    return icons
