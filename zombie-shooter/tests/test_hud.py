"""Tests for HUD face state logic and player pain timer."""

from __future__ import annotations

import pygame

from game.entities.player import Player
from game.scenes.play import _get_face_state

# Initialize pygame for Vector2 and Surface usage (matches test_obstacle.py pattern)
pygame.init()


def test_face_state_normal() -> None:
    """HP >= 80 and no pain flash returns normal."""
    assert _get_face_state(100.0, 0.0) == "normal"
    assert _get_face_state(80.0, 0.0) == "normal"


def test_face_state_hurt() -> None:
    """HP in [60, 80) returns hurt."""
    assert _get_face_state(79.9, 0.0) == "hurt"
    assert _get_face_state(60.0, 0.0) == "hurt"


def test_face_state_injured() -> None:
    """HP in [40, 60) returns injured."""
    assert _get_face_state(59.9, 0.0) == "injured"
    assert _get_face_state(40.0, 0.0) == "injured"


def test_face_state_critical() -> None:
    """HP in [20, 40) returns critical."""
    assert _get_face_state(39.9, 0.0) == "critical"
    assert _get_face_state(20.0, 0.0) == "critical"


def test_face_state_dying() -> None:
    """HP < 20 returns dying."""
    assert _get_face_state(19.9, 0.0) == "dying"
    assert _get_face_state(0.0, 0.0) == "dying"


def test_face_state_pain_flash_overrides_hp() -> None:
    """pain_timer > 0 overrides HP-based state at any HP level."""
    assert _get_face_state(100.0, 0.1) == "pain_flash"
    assert _get_face_state(10.0, 0.01) == "pain_flash"


def test_face_state_no_flash_when_timer_zero() -> None:
    """pain_timer == 0.0 uses HP-based state."""
    assert _get_face_state(90.0, 0.0) == "normal"


def test_player_pain_timer_initial_zero() -> None:
    """Player pain_timer starts at 0."""
    player = Player(pygame.Vector2(100, 100))
    assert player.pain_timer == 0.0


def test_take_damage_sets_pain_timer() -> None:
    """take_damage() sets pain_timer to HUD_PAIN_FLASH_DURATION."""
    from game.core.constants import HUD_PAIN_FLASH_DURATION

    player = Player(pygame.Vector2(100, 100))
    player.take_damage(10.0)
    assert player.pain_timer == HUD_PAIN_FLASH_DURATION


def test_take_damage_reduces_hp() -> None:
    """take_damage() subtracts the correct amount from HP."""
    from game.core.constants import PLAYER_MAX_HP

    player = Player(pygame.Vector2(100, 100))
    player.take_damage(25.0)
    assert player.hp == PLAYER_MAX_HP - 25.0


def test_take_damage_zero_does_not_set_timer() -> None:
    """take_damage(0) does not trigger pain flash."""
    player = Player(pygame.Vector2(100, 100))
    player.take_damage(0.0)
    assert player.pain_timer == 0.0


def test_pain_timer_decrements_in_update() -> None:
    """pain_timer decrements during player update."""
    player = Player(pygame.Vector2(100, 100))
    player.pain_timer = 0.4
    player.update(0.1)
    assert abs(player.pain_timer - 0.3) < 1e-6
