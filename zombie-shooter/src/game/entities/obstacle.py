"""Obstacle entity for zombie shooter world."""

from __future__ import annotations

import math
import random

import pygame

from game.core.constants import OBSTACLE_DEFS


class Obstacle:
    """Solid world obstacle with shape-based collision and varied color."""

    def __init__(
        self,
        obstacle_type: str,
        shape: str,
        pos: pygame.Vector2,
        width: float,
        height: float,
        color: tuple[int, int, int],
        flicker: bool = False,
    ) -> None:
        """Initialize obstacle.

        Args:
            obstacle_type: Kind of obstacle ("house", "tree", "car", "pond", "barrel").
            shape: Collision/visual shape ("rect", "circle", "ellipse").
            pos: Center position as Vector2.
            width: Width in pixels (rect/ellipse) or diameter (circle).
            height: Height in pixels (rect/ellipse) or diameter (circle).
            color: Base RGB color tuple.
            flicker: True if obstacle should animate (burning barrels).
        """
        self.obstacle_type = obstacle_type
        self.shape = shape
        self.pos = pos.copy()
        self.width = width
        self.height = height
        self.color = color
        self.flicker = flicker
        self.solid = True
        # radius = half-width; used for circle collision (tree, barrel)
        self.radius = width / 2

    def get_rect(self) -> pygame.Rect:
        """Return axis-aligned bounding rect (for rect and ellipse obstacles).

        Returns:
            Pygame Rect centered on self.pos.
        """
        return pygame.Rect(
            int(self.pos.x - self.width / 2),
            int(self.pos.y - self.height / 2),
            int(self.width),
            int(self.height),
        )

    def draw(self, screen: pygame.Surface, time: float = 0.0) -> None:
        """Draw obstacle to screen with pixel-art detail per type.

        Args:
            screen: Pygame surface to draw on.
            time: Elapsed game time in seconds (used for flicker animation).
        """
        color = self.color
        flicker_t = 0.0

        # Burning barrel flicker: oscillate between orange and darker ember
        if self.flicker:
            flicker_t = (math.sin(time * 8.0) + 1.0) / 2.0
            r = int(self.color[0] + flicker_t * 60)
            g = int(self.color[1] + flicker_t * 20)
            b = self.color[2]
            color = (min(255, r), min(255, g), b)

        cx = int(self.pos.x)
        cy = int(self.pos.y)
        dark = (max(0, color[0] - 28), max(0, color[1] - 28), max(0, color[2] - 28))

        if self.shape == "circle":
            r_int = int(self.radius)
            pygame.draw.circle(screen, color, (cx, cy), r_int)
            pygame.draw.circle(screen, dark, (cx, cy), r_int, 2)

            if self.obstacle_type == "tree":
                # Inner darker mass for canopy depth
                inner_r = max(3, r_int * 2 // 3)
                inner_c = (
                    max(0, color[0] - 16),
                    max(0, color[1] - 16),
                    max(0, color[2] - 8),
                )
                pygame.draw.circle(screen, inner_c, (cx, cy), inner_r)
                # Highlight cluster at top-left (sun-lit leaves)
                hi = (
                    min(255, color[0] + 24),
                    min(255, color[1] + 24),
                    min(255, color[2] + 14),
                )
                pygame.draw.circle(
                    screen, hi, (cx - r_int // 3, cy - r_int // 3), max(2, r_int // 4)
                )

            elif self.obstacle_type == "barrel":
                # Horizontal band lines across barrel body (stave-wrap effect)
                band_c = (
                    max(0, color[0] - 45),
                    max(0, color[1] - 38),
                    max(0, color[2] - 22),
                )
                for band_y in range(cy - r_int + 3, cy + r_int - 1, 5):
                    dy = band_y - cy
                    if abs(dy) >= r_int:
                        continue
                    half_w = int(math.sqrt(r_int * r_int - dy * dy))
                    pygame.draw.line(
                        screen, band_c, (cx - half_w, band_y), (cx + half_w, band_y), 2
                    )
                # Lid highlight (top cap)
                lid_c = (
                    min(255, color[0] + 18),
                    min(255, color[1] + 14),
                    min(255, color[2] + 8),
                )
                pygame.draw.ellipse(
                    screen,
                    lid_c,
                    pygame.Rect(cx - r_int + 2, cy - r_int, r_int * 2 - 4, r_int // 2),
                )
                # Ember glow for burning barrels
                if self.flicker and flicker_t > 0.0:
                    glow_r = max(2, int(r_int * 0.55 * flicker_t + 1))
                    glow_c = (min(255, 220 + int(flicker_t * 35)), 80, 0)
                    pygame.draw.circle(
                        screen, glow_c, (cx, cy - r_int - glow_r + 1), glow_r
                    )

        elif self.shape == "rect":
            rect = self.get_rect()
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, dark, rect, 2)

            if self.obstacle_type == "house":
                mortar = (
                    max(0, color[0] - 22),
                    max(0, color[1] - 18),
                    max(0, color[2] - 14),
                )
                # Horizontal brick-row mortar lines every 6px
                brick_rows = range(rect.top + 6, rect.bottom - 2, 6)
                for row_y in brick_rows:
                    pygame.draw.line(
                        screen, mortar,
                        (rect.left + 2, row_y), (rect.right - 2, row_y), 1,
                    )
                # Alternating vertical brick joints
                for row_idx, row_y in enumerate(brick_rows):
                    offset = (row_idx % 2) * 8
                    for jx in range(rect.left + offset + 8, rect.right - 2, 16):
                        pygame.draw.line(
                            screen, mortar, (jx, row_y - 5), (jx, row_y), 1
                        )
                # Two windows with cross-bar detail
                win_c = (
                    max(0, color[0] - 12),
                    max(0, color[1] - 8),
                    min(255, color[2] + 8),
                )
                bar_c = (
                    max(0, win_c[0] - 18),
                    max(0, win_c[1] - 18),
                    max(0, win_c[2] - 18),
                )
                win_w, win_h = 18, 14
                wy = rect.top + 14
                for wx in (rect.left + 12, rect.right - 12 - win_w):
                    pygame.draw.rect(screen, win_c, pygame.Rect(wx, wy, win_w, win_h))
                    wmx, wmy = wx + win_w // 2, wy + win_h // 2
                    pygame.draw.line(screen, bar_c, (wmx, wy), (wmx, wy + win_h), 1)
                    pygame.draw.line(screen, bar_c, (wx, wmy), (wx + win_w, wmy), 1)
                # Door at bottom-center
                door_w, door_h = 12, 16
                door_c = (
                    max(0, color[0] - 38),
                    max(0, color[1] - 32),
                    max(0, color[2] - 26),
                )
                pygame.draw.rect(
                    screen,
                    door_c,
                    pygame.Rect(
                        rect.centerx - door_w // 2,
                        rect.bottom - door_h - 2,
                        door_w,
                        door_h,
                    ),
                )

            elif self.obstacle_type == "car":
                # Roof panel (darker, inset)
                roof_c = (
                    max(0, color[0] - 22),
                    max(0, color[1] - 22),
                    max(0, color[2] - 22),
                )
                mx = int(self.width * 0.22)
                my = int(self.height * 0.18)
                rw, rh = int(self.width * 0.56), int(self.height * 0.64)
                pygame.draw.rect(
                    screen, roof_c,
                    pygame.Rect(rect.left + mx, rect.top + my, rw, rh),
                )
                # Windshield strips (lighter glass)
                ws_c = (
                    min(255, color[0] + 28),
                    min(255, color[1] + 32),
                    min(255, color[2] + 38),
                )
                if self.width > self.height:
                    # Horizontal car
                    ws_h = max(3, int(self.height * 0.28))
                    ws_w = int(self.width * 0.18)
                    fy = rect.centery - ws_h // 2
                    pygame.draw.rect(
                        screen, ws_c, pygame.Rect(rect.left + 4, fy, ws_w, ws_h)
                    )
                    pygame.draw.rect(
                        screen, ws_c,
                        pygame.Rect(rect.right - 4 - ws_w, fy, ws_w, ws_h),
                    )
                else:
                    # Vertical car
                    ws_w = max(3, int(self.width * 0.28))
                    ws_h = int(self.height * 0.18)
                    tx = rect.centerx - ws_w // 2
                    pygame.draw.rect(
                        screen, ws_c, pygame.Rect(tx, rect.top + 4, ws_w, ws_h)
                    )
                    pygame.draw.rect(
                        screen, ws_c,
                        pygame.Rect(tx, rect.bottom - 4 - ws_h, ws_w, ws_h),
                    )

        elif self.shape == "ellipse":
            surf = pygame.Surface((int(self.width), int(self.height)), pygame.SRCALPHA)
            r, g, b = color
            w_i, h_i = int(self.width), int(self.height)
            pygame.draw.ellipse(surf, (r, g, b, 220), pygame.Rect(0, 0, w_i, h_i))
            # Concentric ripple rings
            ripple_c = (min(255, r + 18), min(255, g + 18), min(255, b + 24), 170)
            for inset in (7, 14):
                inner = pygame.Rect(inset, inset // 2, w_i - inset * 2, h_i - inset)
                if inner.width > 4 and inner.height > 4:
                    pygame.draw.ellipse(surf, ripple_c, inner, 2)
            # Outline
            pygame.draw.ellipse(
                surf, (max(0, r - 22), max(0, g - 22), max(0, b - 22), 255),
                pygame.Rect(0, 0, w_i, h_i), 2,
            )
            bx = int(self.pos.x - self.width / 2)
            by = int(self.pos.y - self.height / 2)
            screen.blit(surf, (bx, by))


def build_obstacles(seed: int = 42) -> list[Obstacle]:
    """Build the fixed obstacle list from OBSTACLE_DEFS with seeded color variation.

    Args:
        seed: RNG seed for reproducible color offsets across runs.

    Returns:
        List of Obstacle instances ready for use in PlayScene.
    """
    rng = random.Random(seed)
    obstacles: list[Obstacle] = []

    for obs_type, shape, cx, cy, w, h, base_color, flicker in OBSTACLE_DEFS:
        r = max(0, min(255, base_color[0] + rng.randint(-15, 15)))
        g = max(0, min(255, base_color[1] + rng.randint(-15, 15)))
        b = max(0, min(255, base_color[2] + rng.randint(-15, 15)))
        varied_color = (r, g, b)

        obstacles.append(
            Obstacle(
                obstacle_type=obs_type,
                shape=shape,
                pos=pygame.Vector2(cx, cy),
                width=float(w),
                height=float(h),
                color=varied_color,
                flicker=flicker,
            )
        )

    return obstacles
