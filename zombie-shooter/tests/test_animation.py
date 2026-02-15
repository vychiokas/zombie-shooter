"""Tests for animation system."""

from __future__ import annotations

import pygame

from game.systems.animation import Animation

# Initialize pygame once for all tests
pygame.init()


def test_animation_initializes_with_default_state() -> None:
    """Test that animation starts with frame 0, facing down."""
    anim = Animation(frame_count=4, fps=10)

    assert anim.get_current_frame_index() == 0
    assert anim.get_current_direction() == "down"


def test_animation_detects_right_direction() -> None:
    """Test direction detection for rightward velocity."""
    anim = Animation(frame_count=4, fps=10)
    velocity_right = pygame.Vector2(100, 0)  # Moving right

    anim.update(0.1, velocity_right)

    assert anim.get_current_direction() == "right"


def test_animation_detects_left_direction() -> None:
    """Test direction detection for leftward velocity."""
    anim = Animation(frame_count=4, fps=10)
    velocity_left = pygame.Vector2(-100, 0)  # Moving left

    anim.update(0.1, velocity_left)

    assert anim.get_current_direction() == "left"


def test_animation_detects_up_direction() -> None:
    """Test direction detection for upward velocity."""
    anim = Animation(frame_count=4, fps=10)
    velocity_up = pygame.Vector2(0, -100)  # Moving up (negative y)

    anim.update(0.1, velocity_up)

    assert anim.get_current_direction() == "up"


def test_animation_detects_down_direction() -> None:
    """Test direction detection for downward velocity."""
    anim = Animation(frame_count=4, fps=10)
    velocity_down = pygame.Vector2(0, 100)  # Moving down (positive y)

    anim.update(0.1, velocity_down)

    assert anim.get_current_direction() == "down"


def test_animation_detects_diagonal_as_nearest_cardinal() -> None:
    """Test that diagonal movement maps to nearest cardinal direction."""
    anim = Animation(frame_count=4, fps=10)

    # Down-right diagonal (more down than right)
    velocity_dr = pygame.Vector2(30, 70)
    anim.update(0.1, velocity_dr)
    assert anim.get_current_direction() == "down"

    # Right-down diagonal (more right than down)
    velocity_rd = pygame.Vector2(70, 30)
    anim.update(0.1, velocity_rd)
    assert anim.get_current_direction() == "right"


def test_animation_cycles_frames_with_time() -> None:
    """Test that frames advance based on frame duration."""
    anim = Animation(frame_count=4, fps=10)  # 0.1s per frame
    velocity = pygame.Vector2(100, 0)

    # Start at frame 0
    assert anim.get_current_frame_index() == 0

    # Advance 0.05s - not enough to change frame
    anim.update(0.05, velocity)
    assert anim.get_current_frame_index() == 0

    # Advance another 0.05s - total 0.1s, should advance to frame 1
    anim.update(0.05, velocity)
    assert anim.get_current_frame_index() == 1

    # Advance 0.1s - should advance to frame 2
    anim.update(0.1, velocity)
    assert anim.get_current_frame_index() == 2


def test_animation_loops_frames() -> None:
    """Test that frames loop back to 0 after reaching frame_count."""
    anim = Animation(frame_count=3, fps=10)  # 3 frames
    velocity = pygame.Vector2(100, 0)

    # Advance through all 3 frames
    anim.update(0.1, velocity)  # frame 1
    anim.update(0.1, velocity)  # frame 2
    assert anim.get_current_frame_index() == 2

    # Advance once more - should loop to frame 0
    anim.update(0.1, velocity)
    assert anim.get_current_frame_index() == 0


def test_animation_resets_to_first_frame_when_stationary() -> None:
    """Test that stationary entities show frame 0."""
    anim = Animation(frame_count=4, fps=10)
    velocity_moving = pygame.Vector2(100, 0)
    velocity_stopped = pygame.Vector2(0, 0)

    # Move and advance to frame 2
    anim.update(0.1, velocity_moving)
    anim.update(0.1, velocity_moving)
    assert anim.get_current_frame_index() == 2

    # Stop moving - should reset to frame 0
    anim.update(0.1, velocity_stopped)
    assert anim.get_current_frame_index() == 0


def test_animation_preserves_direction_when_stationary() -> None:
    """Test that direction is preserved when entity stops moving."""
    anim = Animation(frame_count=4, fps=10)
    velocity_right = pygame.Vector2(100, 0)
    velocity_stopped = pygame.Vector2(0, 0)

    # Move right
    anim.update(0.1, velocity_right)
    assert anim.get_current_direction() == "right"

    # Stop - should still face right
    anim.update(0.1, velocity_stopped)
    assert anim.get_current_direction() == "right"
    assert anim.get_current_frame_index() == 0  # First frame of right direction


def test_animation_handles_very_small_velocity() -> None:
    """Test that tiny velocities below threshold are treated as stationary."""
    anim = Animation(frame_count=4, fps=10)
    velocity_tiny = pygame.Vector2(0.05, 0.05)  # Length ~0.07, below 0.1 threshold

    # Should be treated as stationary
    anim.update(0.1, velocity_tiny)
    assert anim.get_current_frame_index() == 0
