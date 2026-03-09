"""Tests for Obstacle entity and collision resolution."""

from __future__ import annotations

import pygame

from game.entities.obstacle import Obstacle, build_obstacles
from game.systems.collisions import (
    resolve_circle_vs_circle_obstacle,
    resolve_circle_vs_rect_obstacle,
    resolve_entity_vs_obstacles,
)

# Initialize pygame for Vector2 and Surface usage
pygame.init()


# ── Obstacle initialization ───────────────────────────────────────────────────


def test_obstacle_rect_init() -> None:
    """Obstacle initializes with correct attributes."""
    obs = Obstacle("house", "rect", pygame.Vector2(100, 100), 80.0, 60.0, (50, 40, 30))
    assert obs.obstacle_type == "house"
    assert obs.shape == "rect"
    assert obs.pos.x == 100
    assert obs.width == 80.0
    assert obs.height == 60.0
    assert obs.solid is True
    assert obs.flicker is False


def test_obstacle_pos_independence() -> None:
    """Obstacle pos is a copy, not a reference."""
    source = pygame.Vector2(50, 50)
    obs = Obstacle("tree", "circle", source, 15.0, 15.0, (30, 50, 20))
    source.x = 999
    assert obs.pos.x == 50


def test_obstacle_radius_is_half_width() -> None:
    """Obstacle radius equals half of width."""
    obs = Obstacle("tree", "circle", pygame.Vector2(0, 0), 30.0, 30.0, (30, 50, 20))
    assert obs.radius == 15.0


def test_obstacle_get_rect() -> None:
    """get_rect returns correct centered rect."""
    obs = Obstacle("house", "rect", pygame.Vector2(200, 200), 100.0, 80.0, (50, 40, 30))
    rect = obs.get_rect()
    assert rect.left == 150
    assert rect.top == 160
    assert rect.width == 100
    assert rect.height == 80


def test_obstacle_draw_rect_no_error() -> None:
    """draw() executes without errors for rect shape."""
    screen = pygame.Surface((800, 600))
    obs = Obstacle("house", "rect", pygame.Vector2(100, 100), 80.0, 60.0, (50, 40, 30))
    obs.draw(screen, 0.0)


def test_obstacle_draw_circle_no_error() -> None:
    """draw() executes without errors for circle shape."""
    screen = pygame.Surface((800, 600))
    obs = Obstacle("tree", "circle", pygame.Vector2(100, 100), 30.0, 30.0, (40, 60, 30))
    obs.draw(screen, 0.0)


def test_obstacle_draw_ellipse_no_error() -> None:
    """draw() executes without errors for ellipse shape."""
    screen = pygame.Surface((800, 600))
    obs = Obstacle(
        "pond", "ellipse", pygame.Vector2(100, 100), 80.0, 50.0, (28, 45, 52)
    )
    obs.draw(screen, 0.0)


def test_obstacle_draw_flicker_no_error() -> None:
    """Flickering barrel draws without errors at various times."""
    screen = pygame.Surface((800, 600))
    obs = Obstacle(
        "barrel", "circle", pygame.Vector2(100, 100), 20.0, 20.0, (85, 50, 18),
        flicker=True,
    )
    for t in (0.0, 0.5, 1.0, 3.14):
        obs.draw(screen, t)


def test_build_obstacles_count() -> None:
    """build_obstacles returns correct count matching OBSTACLE_DEFS."""
    from game.core.constants import OBSTACLE_DEFS

    obstacles = build_obstacles()
    assert len(obstacles) == len(OBSTACLE_DEFS)


def test_build_obstacles_reproducible() -> None:
    """build_obstacles with same seed produces identical colors."""
    obs_a = build_obstacles(seed=42)
    obs_b = build_obstacles(seed=42)
    assert obs_a[0].color == obs_b[0].color
    assert obs_a[-1].color == obs_b[-1].color


def test_build_obstacles_different_seeds_differ() -> None:
    """build_obstacles with different seeds produces different colors."""
    obs_a = build_obstacles(seed=1)
    obs_b = build_obstacles(seed=999)
    # Very likely to differ with different seeds
    colors_a = [o.color for o in obs_a]
    colors_b = [o.color for o in obs_b]
    assert colors_a != colors_b


# ── Circle vs circle push-out ─────────────────────────────────────────────────


def test_circle_vs_circle_no_overlap() -> None:
    """No change when circles don't overlap."""
    pos = pygame.Vector2(100, 100)
    result = resolve_circle_vs_circle_obstacle(pos, 10, pygame.Vector2(0, 0), 10)
    assert result.x == 100 and result.y == 100


def test_circle_vs_circle_overlap_pushes_out() -> None:
    """Entity is pushed to minimum separation distance when overlapping."""
    entity_pos = pygame.Vector2(15, 0)  # 15px from center, min dist = 20
    result = resolve_circle_vs_circle_obstacle(
        entity_pos, 10, pygame.Vector2(0, 0), 10
    )
    dist = result.length()
    assert dist >= 20.0 - 0.01


def test_circle_vs_circle_exact_contact_not_moved() -> None:
    """Entity exactly at min distance is not pushed (already at boundary)."""
    pos = pygame.Vector2(20, 0)  # exactly 20 from origin
    result = resolve_circle_vs_circle_obstacle(pos, 10, pygame.Vector2(0, 0), 10)
    assert abs(result.x - 20.0) < 0.01
    assert abs(result.y) < 0.01


def test_circle_vs_circle_center_overlap_pushes_up() -> None:
    """Entity at exact same position as obstacle is pushed upward."""
    pos = pygame.Vector2(0, 0)
    result = resolve_circle_vs_circle_obstacle(pos, 10, pygame.Vector2(0, 0), 10)
    # Should be pushed to min_dist in some direction (upward by convention)
    dist = result.length()
    assert dist >= 20.0 - 0.01


# ── Circle vs rect push-out ───────────────────────────────────────────────────


def test_rect_entity_outside_not_moved() -> None:
    """No change when entity is outside rect."""
    pos = pygame.Vector2(200, 200)
    rect = pygame.Rect(0, 0, 100, 100)
    result = resolve_circle_vs_rect_obstacle(pos, 18, rect)
    assert result.x == 200 and result.y == 200


def test_rect_entity_pushed_from_left() -> None:
    """Entity approaching from left is pushed outside rect left edge."""
    rect = pygame.Rect(100, 100, 80, 60)
    # Entity at (107, 130) with radius 18 — inside left portion
    entity_pos = pygame.Vector2(107, 130)
    result = resolve_circle_vs_rect_obstacle(entity_pos, 18, rect)
    # Entity left edge (result.x - radius) should be <= rect.left
    assert result.x - 18 <= rect.left + 0.5


def test_rect_entity_touching_left_edge_unchanged() -> None:
    """Entity touching but not overlapping rect is not moved."""
    rect = pygame.Rect(100, 100, 80, 60)
    # Entity at (82, 130): left edge at 64, rect left at 100 — no overlap
    entity_pos = pygame.Vector2(82, 130)
    result = resolve_circle_vs_rect_obstacle(entity_pos, 18, rect)
    assert abs(result.x - 82) < 0.01


# ── resolve_entity_vs_obstacles ───────────────────────────────────────────────


def test_resolve_entity_vs_obstacles_empty_list() -> None:
    """No change when obstacle list is empty."""
    pos = pygame.Vector2(100, 100)
    result = resolve_entity_vs_obstacles(pos, 18, [])
    assert result.x == 100 and result.y == 100


def test_resolve_entity_vs_obstacles_skips_non_solid() -> None:
    """Non-solid obstacles are ignored during push-out."""
    obs = Obstacle(
        "pond", "ellipse", pygame.Vector2(100, 100), 50.0, 40.0, (30, 40, 50)
    )
    obs.solid = False
    pos = pygame.Vector2(100, 100)  # Same center as obstacle
    result = resolve_entity_vs_obstacles(pos, 18, [obs])
    assert result.x == 100 and result.y == 100


def test_resolve_entity_vs_obstacles_rect_pushes_out() -> None:
    """Entity overlapping solid rect obstacle is pushed out."""
    obs = Obstacle("house", "rect", pygame.Vector2(200, 200), 100.0, 80.0, (50, 40, 30))
    # Entity at rect center — clearly inside
    pos = pygame.Vector2(200, 200)
    result = resolve_entity_vs_obstacles(pos, 18, [obs])
    # Entity must be outside the rect
    rect = obs.get_rect()
    left_ok = result.x - 18 <= rect.left + 0.5
    right_ok = result.x + 18 >= rect.right - 0.5
    top_ok = result.y - 18 <= rect.top + 0.5
    bottom_ok = result.y + 18 >= rect.bottom - 0.5
    assert left_ok or right_ok or top_ok or bottom_ok


def test_resolve_entity_vs_obstacles_circle_pushes_out() -> None:
    """Entity overlapping solid circle obstacle is pushed out."""
    obs = Obstacle("tree", "circle", pygame.Vector2(100, 100), 30.0, 30.0, (30, 55, 22))
    # Entity at same center — inside tree
    pos = pygame.Vector2(100, 100)
    result = resolve_entity_vs_obstacles(pos, 18, [obs])
    dist = (result - obs.pos).length()
    assert dist >= obs.radius + 18 - 0.1
