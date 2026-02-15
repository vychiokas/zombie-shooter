"""Blood particle entity for gore effects."""

from __future__ import annotations

import pygame

from game.core.constants import BLOOD_PARTICLE_LIFETIME, BLOOD_PARTICLE_RADIUS


class BloodParticle:
    """Blood particle that sprays from zombie death."""

    def __init__(self, pos: pygame.Vector2, velocity: pygame.Vector2) -> None:
        """Initialize blood particle.

        Args:
            pos: Starting position.
            velocity: Initial velocity vector.
        """
        self.pos = pos.copy()  # Copy to avoid reference issues
        self.vel = velocity
        self.lifetime = BLOOD_PARTICLE_LIFETIME  # Seconds
        self.max_lifetime = BLOOD_PARTICLE_LIFETIME
        self.radius = BLOOD_PARTICLE_RADIUS
        self.color = (180, 0, 0)  # Dark red

    def update(self, dt: float) -> bool:
        """Update particle position and lifetime.

        Args:
            dt: Delta time in seconds.

        Returns:
            True if particle is still alive, False if should be removed.
        """
        self.pos += self.vel * dt  # Physics update
        self.lifetime -= dt  # Countdown
        return self.is_alive()

    def is_alive(self) -> bool:
        """Check if particle should still exist.

        Returns:
            True if lifetime > 0, False otherwise.
        """
        return self.lifetime > 0

    def get_alpha(self) -> int:
        """Calculate alpha transparency based on remaining lifetime.

        Returns:
            Alpha value (0-255), fades from 255 to 0.
        """
        ratio = self.lifetime / self.max_lifetime
        return int(255 * ratio)

    def draw(self, screen: pygame.Surface) -> None:
        """Render blood particle with fade effect.

        Args:
            screen: Pygame surface to draw on.
        """
        # Create temporary surface for alpha blending
        temp_surface = pygame.Surface(
            (self.radius * 2, self.radius * 2), pygame.SRCALPHA
        )
        alpha = self.get_alpha()
        color_with_alpha = (*self.color, alpha)

        # Draw circle on temp surface
        pygame.draw.circle(
            temp_surface,
            color_with_alpha,
            (self.radius, self.radius),  # Center of temp surface
            self.radius,
        )

        # Blit temp surface to screen
        screen.blit(
            temp_surface,
            (int(self.pos.x) - self.radius, int(self.pos.y) - self.radius),
        )
