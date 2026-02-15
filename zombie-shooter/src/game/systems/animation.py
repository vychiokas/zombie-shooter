"""Animation system for directional sprite cycling."""

from __future__ import annotations

import math

import pygame


class Animation:
    """Manages directional animation state and frame cycling.

    Detects movement direction from velocity vector (4 cardinal directions)
    and cycles through animation frames using delta-time accumulation.
    """

    def __init__(self, frame_count: int, fps: float) -> None:
        """Initialize animation.

        Args:
            frame_count: Number of frames per direction animation.
            fps: Animation frames per second (frame duration = 1/fps).
        """
        self.frame_count = frame_count
        self.frame_duration = 1.0 / fps  # seconds per frame
        self.frame_timer = 0.0
        self.current_frame = 0
        self.current_direction: str = "down"  # Default facing down

    def update(self, dt: float, velocity: pygame.Vector2) -> None:
        """Update animation state based on elapsed time and velocity.

        Args:
            dt: Delta time in seconds.
            velocity: Current velocity vector for direction detection.
        """
        # Detect direction from velocity
        if velocity.length() > 0.1:  # Moving threshold
            self.current_direction = self._get_direction_from_velocity(velocity)

            # Advance frame timer
            self.frame_timer += dt
            if self.frame_timer >= self.frame_duration:
                self.frame_timer -= self.frame_duration
                self.current_frame = (self.current_frame + 1) % self.frame_count
        else:
            # Stationary - show first frame of current direction
            self.current_frame = 0

    def get_current_frame_index(self) -> int:
        """Get current animation frame index.

        Returns:
            Frame index (0 to frame_count-1).
        """
        return self.current_frame

    def get_current_direction(self) -> str:
        """Get current facing direction.

        Returns:
            Direction string: "up", "down", "left", or "right".
        """
        return self.current_direction

    def _get_direction_from_velocity(self, velocity: pygame.Vector2) -> str:
        """Determine cardinal direction from velocity vector.

        Args:
            velocity: Velocity vector (must be non-zero length).

        Returns:
            Direction string: "up", "down", "left", or "right".
        """
        # Calculate angle in radians (-pi to pi)
        angle = math.atan2(velocity.y, velocity.x)

        # Convert to 4 cardinal directions
        # Right: -45° to 45° (or -π/4 to π/4)
        # Down: 45° to 135° (or π/4 to 3π/4)
        # Left: 135° to -135° (or 3π/4 to -3π/4)
        # Up: -135° to -45° (or -3π/4 to -π/4)

        if -math.pi / 4 <= angle < math.pi / 4:
            return "right"
        elif math.pi / 4 <= angle < 3 * math.pi / 4:
            return "down"
        elif angle >= 3 * math.pi / 4 or angle < -3 * math.pi / 4:
            return "left"
        else:  # -3π/4 <= angle < -π/4
            return "up"
