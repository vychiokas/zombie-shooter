"""Zombie spawning system."""

from __future__ import annotations

import random

import pygame

from game.core.constants import (
    HEIGHT,
    SPAWN_INTERVAL_MIN,
    SPAWN_INTERVAL_START,
    SPAWN_RAMP_SECONDS,
    WIDTH,
    ZOMBIE_VARIANTS,
)


class ZombieSpawner:
    """System for spawning zombies with difficulty ramping."""

    def __init__(self) -> None:
        """Initialize spawner."""
        self.spawn_timer = SPAWN_INTERVAL_START

    def update(self, dt: float, elapsed_time: float) -> bool:
        """Update spawn timer.

        Args:
            dt: Delta time in seconds.
            elapsed_time: Total time elapsed in game.

        Returns:
            True when ready to spawn a zombie, False otherwise.
        """
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self.spawn_timer = self.get_spawn_interval(elapsed_time)
            return True
        return False

    def get_spawn_interval(self, elapsed_time: float) -> float:
        """Calculate spawn interval with linear ramp.

        Args:
            elapsed_time: Total time elapsed in game.

        Returns:
            Spawn interval in seconds.
        """
        progress = min(elapsed_time / SPAWN_RAMP_SECONDS, 1.0)
        return (
            SPAWN_INTERVAL_START
            - (SPAWN_INTERVAL_START - SPAWN_INTERVAL_MIN) * progress
        )

    def get_spawn_position(self) -> pygame.Vector2:
        """Get random position at screen edge.

        Returns:
            Random Vector2 position at screen boundary.
        """
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            return pygame.Vector2(random.uniform(0, WIDTH), 0)
        elif side == "bottom":
            return pygame.Vector2(random.uniform(0, WIDTH), HEIGHT)
        elif side == "left":
            return pygame.Vector2(0, random.uniform(0, HEIGHT))
        else:  # right
            return pygame.Vector2(WIDTH, random.uniform(0, HEIGHT))

    def get_spawn_variant(self) -> str:
        """Choose zombie variant using weighted random selection.

        Returns:
            Variant type string (e.g., "normal", "runner", "tank").
        """
        variants = list(ZOMBIE_VARIANTS.keys())
        weights = [ZOMBIE_VARIANTS[v]["weight"] for v in variants]
        return random.choices(variants, weights=weights)[0]
