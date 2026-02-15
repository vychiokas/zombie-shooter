"""Tests for weapon constants and data model."""

from __future__ import annotations

from game.core.constants import PICKUP_RADIUS, PICKUP_SPAWN_RATE, WEAPON_STATS


def test_weapon_stats_structure() -> None:
    """Test that WEAPON_STATS has all required weapons."""
    assert "pistol" in WEAPON_STATS
    assert "shotgun" in WEAPON_STATS
    assert "smg" in WEAPON_STATS


def test_weapon_stats_pistol_default() -> None:
    """Test that pistol has expected default values."""
    pistol = WEAPON_STATS["pistol"]
    assert pistol["fire_rate"] == 0.15
    assert pistol["bullet_count"] == 1
    assert pistol["spread_angle"] == 0.0


def test_weapon_stats_shotgun() -> None:
    """Test that shotgun has spread and multiple bullets."""
    shotgun = WEAPON_STATS["shotgun"]
    assert shotgun["fire_rate"] == 0.5
    assert shotgun["bullet_count"] == 5
    assert shotgun["spread_angle"] == 30.0


def test_weapon_stats_smg() -> None:
    """Test that SMG has rapid fire rate."""
    smg = WEAPON_STATS["smg"]
    assert smg["fire_rate"] == 0.08
    assert smg["bullet_count"] == 1
    assert smg["spread_angle"] == 0.0


def test_pickup_constants_defined() -> None:
    """Test that pickup spawn constants exist."""
    assert PICKUP_SPAWN_RATE > 0
    assert PICKUP_RADIUS > 0
