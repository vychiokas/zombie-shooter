"""Player entity for zombie shooter."""

from __future__ import annotations

import math

import pygame

from game.assets.loader import load_player_sprites
from game.core.constants import (
    HEIGHT,
    PLAYER_ANIMATION_FPS,
    PLAYER_FRAME_COUNT,
    PLAYER_MAX_HP,
    PLAYER_RADIUS,
    PLAYER_SHOOT_DURATION,
    PLAYER_SPEED,
    PLAYER_SPRITE_SIZE,
    WEAPON_STATS,
    WIDTH,
)
from game.entities.bullet import Bullet
from game.systems.animation import Animation
from game.systems.collisions import resolve_entity_vs_obstacles

# Module-level sprite loading (shared across all instances)
_player_sprites: dict[str, list[pygame.Surface]] | None = None


def _load_sprites() -> dict[str, list[pygame.Surface]]:
    """Load player sprites once and cache at module level."""
    global _player_sprites
    if _player_sprites is None:
        _player_sprites = load_player_sprites(
            sprite_size=PLAYER_SPRITE_SIZE,
            frame_count=PLAYER_FRAME_COUNT,
        )
    return _player_sprites


class Player:
    """Player entity with movement and shooting."""

    def __init__(self, pos: pygame.Vector2) -> None:
        """Initialize player.

        Args:
            pos: Initial position as Vector2.
        """
        self.pos = pos
        self.vel = pygame.Vector2(0, 0)
        self.radius = PLAYER_RADIUS
        self.speed = PLAYER_SPEED
        self.hp = float(PLAYER_MAX_HP)
        self.shoot_cooldown = 0.0
        self.shoot_timer = 0.0  # Timer for shooting animation display
        self.pain_timer: float = 0.0  # Seconds until HUD pain flash ends
        self.current_weapon: str = "pistol"
        self.weapons_inventory: set[str] = {"pistol"}  # Start with pistol

        # Load sprites and create animation instance
        self.sprites = _load_sprites()
        self.animation = Animation(
            frame_count=PLAYER_FRAME_COUNT, fps=PLAYER_ANIMATION_FPS
        )

    def update(self, dt: float, obstacles: list | None = None) -> None:
        """Update player movement.

        Args:
            dt: Delta time in seconds.
            obstacles: List of Obstacle instances for collision resolution.
        """
        keys = pygame.key.get_pressed()
        self.vel.x = 0
        self.vel.y = 0

        # WASD movement
        if keys[pygame.K_a]:
            self.vel.x = -self.speed
        if keys[pygame.K_d]:
            self.vel.x = self.speed
        if keys[pygame.K_w]:
            self.vel.y = -self.speed
        if keys[pygame.K_s]:
            self.vel.y = self.speed

        # Normalize diagonal movement
        if self.vel.length() > 0:
            self.vel = self.vel.normalize() * self.speed

        # Update position
        self.pos += self.vel * dt

        # Clamp to screen bounds
        self.pos.x = max(self.radius, min(WIDTH - self.radius, self.pos.x))
        self.pos.y = max(self.radius, min(HEIGHT - self.radius, self.pos.y))

        # Obstacle push-out
        if obstacles:
            self.pos = resolve_entity_vs_obstacles(self.pos, self.radius, obstacles)
            # Re-clamp after obstacle resolution
            self.pos.x = max(self.radius, min(WIDTH - self.radius, self.pos.x))
            self.pos.y = max(self.radius, min(HEIGHT - self.radius, self.pos.y))

        # Update animation based on current velocity
        self.animation.update(dt, self.vel)

        # Decrement cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt

        # Decrement shoot timer
        if self.shoot_timer > 0:
            self.shoot_timer -= dt

        # Decrement pain flash timer
        if self.pain_timer > 0:
            self.pain_timer -= dt

    def shoot(self, target_pos: pygame.Vector2) -> list[Bullet]:
        """Shoot bullets toward target if cooldown ready.

        Args:
            target_pos: Target position to shoot toward.

        Returns:
            List of Bullet instances (empty if on cooldown).
        """
        if self.shoot_cooldown > 0:
            return []

        direction = target_pos - self.pos
        if direction.length() == 0:
            return []

        # Get weapon stats
        weapon = WEAPON_STATS[self.current_weapon]
        fire_rate = weapon["fire_rate"]
        bullet_count = int(weapon["bullet_count"])
        spread_angle = weapon["spread_angle"]

        # Set cooldown based on weapon fire rate
        self.shoot_cooldown = fire_rate
        self.shoot_timer = PLAYER_SHOOT_DURATION  # Trigger shooting animation

        # Single bullet (pistol, SMG)
        if bullet_count == 1:
            return [Bullet(self.pos, direction)]

        # Multiple bullets with spread (shotgun)
        bullets = []
        base_angle = math.atan2(direction.y, direction.x)

        # Spread bullets evenly across the spread angle
        for i in range(bullet_count):
            # Calculate angle offset from center
            if bullet_count > 1:
                # Evenly distribute across spread range
                t = i / (bullet_count - 1)  # 0.0 to 1.0
                angle_offset = math.radians(spread_angle) * (t - 0.5)
            else:
                angle_offset = 0

            bullet_angle = base_angle + angle_offset
            bullet_direction = pygame.Vector2(
                math.cos(bullet_angle), math.sin(bullet_angle)
            )
            bullets.append(Bullet(self.pos, bullet_direction))

        return bullets

    def add_weapon(self, weapon_type: str) -> None:
        """Add a weapon to inventory.

        Args:
            weapon_type: Type of weapon to add (pistol, shotgun, smg).
        """
        self.weapons_inventory.add(weapon_type)

    def switch_weapon(self, weapon_type: str) -> bool:
        """Switch to a different weapon if it's in inventory.

        Args:
            weapon_type: Type of weapon to switch to.

        Returns:
            True if switch successful, False if weapon not in inventory.
        """
        if weapon_type in self.weapons_inventory:
            self.current_weapon = weapon_type
            return True
        return False

    def take_damage(self, amount: float) -> None:
        """Apply damage and trigger HUD pain flash.

        Args:
            amount: HP to subtract (positive value; 0 is a no-op).
        """
        if amount > 0:
            from game.core.constants import HUD_PAIN_FLASH_DURATION

            self.hp -= amount
            self.pain_timer = HUD_PAIN_FLASH_DURATION

    def draw(self, screen: pygame.Surface) -> None:
        """Draw player to screen.

        Args:
            screen: Pygame surface to draw on.
        """
        # Get current direction from animation
        direction = self.animation.get_current_direction()

        # Select sprite based on shooting state
        if self.shoot_timer > 0:
            # Display shooting sprite (4th sprite in list: index 3)
            sprite = self.sprites[direction][PLAYER_FRAME_COUNT]
        else:
            # Display walk animation sprite
            frame_index = self.animation.get_current_frame_index()
            sprite = self.sprites[direction][frame_index]

        # Center sprite on player position
        sprite_rect = sprite.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        screen.blit(sprite, sprite_rect)
