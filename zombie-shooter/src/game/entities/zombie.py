"""Zombie entity for zombie shooter."""

from __future__ import annotations

import pygame

from game.assets.loader import load_zombie_sprites
from game.core.constants import (
    ZOMBIE_ANIMATION_FPS,
    ZOMBIE_FRAME_COUNT,
    ZOMBIE_SPRITE_SIZE,
    ZOMBIE_VARIANTS,
)
from game.systems.animation import Animation
from game.systems.collisions import resolve_entity_vs_obstacles

# Module-level sprite loading (shared across all instances by variant)
_zombie_sprites: dict[str, dict[str, list[pygame.Surface]]] = {}


def _load_sprites(variant: str = "normal") -> dict[str, list[pygame.Surface]]:
    """Load zombie sprites once per variant and cache at module level.

    Args:
        variant: Zombie variant type ("normal", "runner", "tank", etc.).

    Returns:
        Dictionary mapping direction to list of sprite frames.
    """
    if variant not in _zombie_sprites:
        _zombie_sprites[variant] = load_zombie_sprites(
            sprite_size=ZOMBIE_SPRITE_SIZE,
            frame_count=ZOMBIE_FRAME_COUNT,
            variant=variant,
        )
    return _zombie_sprites[variant]


class Zombie:
    """Zombie entity that seeks player."""

    def __init__(self, pos: pygame.Vector2, variant: str = "normal") -> None:
        """Initialize zombie.

        Args:
            pos: Starting position as Vector2.
            variant: Zombie type ("normal", "runner", "tank", "exploder", "spitter").
        """
        self.pos = pos
        self.variant = variant
        variant_stats = ZOMBIE_VARIANTS[variant]
        self.hp = float(variant_stats["hp"])
        self.vel = pygame.Vector2(0, 0)  # Initialize velocity for animation
        self.radius = int(variant_stats["radius"])
        self.speed = variant_stats["speed"]

        # Load variant-specific sprites and create animation instance
        self.sprites = _load_sprites(variant)
        self.animation = Animation(
            frame_count=ZOMBIE_FRAME_COUNT, fps=ZOMBIE_ANIMATION_FPS
        )

        # Attack cooldown for spitter variant
        self.attack_cooldown = 0.0
        self.pending_projectiles: list[tuple[pygame.Vector2, pygame.Vector2]] = []

    def update(
        self,
        dt: float,
        player_pos: pygame.Vector2,
        obstacles: list | None = None,
    ) -> None:
        """Move toward player position.

        Args:
            dt: Delta time in seconds.
            player_pos: Target player position to move toward.
            obstacles: List of Obstacle instances for collision resolution.
        """
        direction = player_pos - self.pos
        if direction.length() > 0:
            self.vel = direction.normalize() * self.speed
            self.pos += self.vel * dt
        else:
            # Explicitly set zero velocity when stationary
            self.vel = pygame.Vector2(0, 0)

        # Obstacle push-out (applied after movement)
        if obstacles:
            self.pos = resolve_entity_vs_obstacles(self.pos, self.radius, obstacles)

        # Update animation based on current velocity
        self.animation.update(dt, self.vel)

        # Spitter variant attack behavior
        if self.variant == "spitter":
            from game.core.constants import (
                SPITTER_ATTACK_COOLDOWN,
                SPITTER_ATTACK_RANGE,
            )

            self.attack_cooldown -= dt
            distance = (player_pos - self.pos).length()

            # Attack if in range and cooldown ready
            if distance <= SPITTER_ATTACK_RANGE and self.attack_cooldown <= 0:
                # Calculate direction to player
                attack_direction = (player_pos - self.pos).normalize()
                # Store projectile data for PlayScene to collect
                self.pending_projectiles.append((self.pos.copy(), attack_direction))
                self.attack_cooldown = SPITTER_ATTACK_COOLDOWN

    def draw(self, screen: pygame.Surface) -> None:
        """Draw zombie to screen.

        Args:
            screen: Pygame surface to draw on.
        """
        # Get current animation frame
        direction = self.animation.get_current_direction()
        frame_index = self.animation.get_current_frame_index()
        sprite = self.sprites[direction][frame_index]

        # Center sprite on zombie position
        sprite_rect = sprite.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        screen.blit(sprite, sprite_rect)
