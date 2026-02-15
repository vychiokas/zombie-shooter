# Feature: Phase 1 - Weapon Data Model

## Summary

Establish the foundational weapon type system by adding weapon statistics configuration to constants, adding current weapon state tracking to the Player class, and defining pickup spawn parameters. This phase creates the data model foundation that subsequent phases (pickup entities, weapon behaviors) will build upon.

## User Story

As a player
I want the game to support different weapon types with distinct characteristics
So that I can experience varied tactical gameplay based on weapon choice

## Problem Statement

The game currently hardcodes shooting behavior (0.15s cooldown, single bullet) in Player class and constants. To support multiple weapons with different fire rates, bullet counts, and spread patterns, we need a flexible weapon configuration system and player state tracking for the currently equipped weapon.

## Solution Statement

Add a typed dictionary structure (`WEAPON_STATS`) to `constants.py` containing weapon configurations (pistol, shotgun, SMG) with fire_rate, bullet_count, and spread_angle parameters. Extend the Player class to track the `current_weapon` attribute. Define pickup spawn timing and collision radius constants to support future pickup spawning logic.

## Metadata

| Field            | Value                              |
| ---------------- | ---------------------------------- |
| Type             | NEW_CAPABILITY                     |
| Complexity       | LOW                                |
| Systems Affected | constants, player entity           |
| Dependencies     | pygame>=2.6.0 (already satisfied)  |
| Estimated Tasks  | 4                                  |

---

## UX Design

### Before State
```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌─────────────┐         ┌─────────────┐         ┌─────────────┐            ║
║   │   Player    │ ──────► │   Shoots    │ ──────► │   Bullet    │            ║
║   │   Entity    │         │  (hardcoded)│         │  (single)   │            ║
║   └─────────────┘         └─────────────┘         └─────────────┘            ║
║                                                                               ║
║   DATA_FLOW:                                                                  ║
║   - SHOOT_COOLDOWN = 0.15 (constant)                                          ║
║   - Player.shoot() returns single Bullet | None                               ║
║   - No weapon state tracking                                                  ║
║   - No weapon variation possible                                              ║
║                                                                               ║
║   PAIN_POINT:                                                                 ║
║   - Cannot support different weapon types                                     ║
║   - Fire rate and bullet count are hardcoded                                  ║
║   - No extensibility for future weapons                                       ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌─────────────┐         ┌─────────────┐         ┌─────────────┐            ║
║   │   Player    │ ──────► │   Shoots    │ ──────► │   Bullets   │            ║
║   │   Entity    │         │ (from stats)│         │  (variable) │            ║
║   └──────┬──────┘         └─────────────┘         └─────────────┘            ║
║          │                                                                    ║
║          │ current_weapon: str = "pistol"                                     ║
║          │                                                                    ║
║          ▼                                                                    ║
║   ┌─────────────┐                                                             ║
║   │ WEAPON_STATS│  ◄── {"pistol": {fire_rate, bullet_count, spread_angle}}   ║
║   │    dict     │  ◄── {"shotgun": {...}}                                    ║
║   │             │  ◄── {"smg": {...}}                                         ║
║   └─────────────┘                                                             ║
║                                                                               ║
║   DATA_FLOW:                                                                  ║
║   - Player has current_weapon attribute ("pistol" default)                    ║
║   - WEAPON_STATS[weapon_name] provides configuration                          ║
║   - Fire rate, bullet count, spread are data-driven                           ║
║   - Pickup spawn rate and radius defined                                      ║
║                                                                               ║
║   VALUE_ADD:                                                                  ║
║   - Weapon system is now extensible                                           ║
║   - Future phases can read weapon stats to vary behavior                      ║
║   - Player state tracks which weapon is equipped                              ║
║   - New weapons can be added by extending WEAPON_STATS dict                   ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes
| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| `constants.py` | Single `SHOOT_COOLDOWN` constant | `WEAPON_STATS` dict with 3 weapons + pickup params | Centralized weapon configuration |
| `Player.__init__()` | No weapon state | `current_weapon: str = "pistol"` attribute | Player tracks equipped weapon |
| Future weapon logic | Impossible to vary behavior | Can read `WEAPON_STATS[player.current_weapon]` | Enables dynamic weapon behavior |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `zombie-shooter/src/game/core/constants.py` | 1-34 | Pattern to MIRROR exactly - constant naming, organization, no type hints on scalars |
| P0 | `zombie-shooter/src/game/entities/player.py` | 21-32 | Pattern to MIRROR exactly - `__init__` attribute initialization with type hints |
| P1 | `zombie-shooter/src/game/entities/player.py` | 69-86 | Current `shoot()` implementation - Phase 3 will modify this |
| P1 | `zombie-shooter/tests/test_collisions.py` | 1-25 | Test pattern to FOLLOW - pytest structure, docstrings, imports |

**External Documentation:**
| Source | Section | Why Needed |
|--------|---------|------------|
| [Python TypedDict - PEP 589](https://peps.python.org/pep-0589/) | TypedDict basics | Optional: For understanding nested dict type hints (can use `dict[str, dict[str, float]]` for simplicity) |
| [Pygame Vector2 docs v2.6.0](https://www.pygame.org/docs/ref/math.html?highlight=vector) | Vector2.rotate() method | Phase 3 will use this for shotgun spread - context for spread_angle parameter |

---

## Patterns to Mirror

### NAMING_CONVENTION - Constants Module

**SOURCE:** `zombie-shooter/src/game/core/constants.py:1-34`

**COPY THIS PATTERN:**
```python
"""Game constants for zombie shooter."""

from __future__ import annotations

# Comment section header
CONSTANT_NAME = value  # Inline comment if needed

# Another section
ANOTHER_CONSTANT = value
```

**Phase 1 applies:**
- Add `# Weapons` section header
- Use ALL_UPPERCASE naming for constants
- No type hints on scalar constants (int/float)
- Add inline comments for clarity

---

### PLAYER_INITIALIZATION - Entity Attribute Setup

**SOURCE:** `zombie-shooter/src/game/entities/player.py:21-32`

**COPY THIS PATTERN:**
```python
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
```

**Phase 1 applies:**
- Add `self.current_weapon: str = "pistol"` after `self.shoot_cooldown = 0.0`
- Use type hint inline: `self.current_weapon: str`
- Initialize to default value `"pistol"`
- Google-style docstring unchanged (no new constructor params)

---

### TYPE_HINTS - Modern Python Syntax

**SOURCE:** Used throughout codebase, e.g., `player.py:69`

**COPY THIS PATTERN:**
```python
from __future__ import annotations  # At top of every file

def shoot(self, target_pos: pygame.Vector2) -> Bullet | None:
    # Modern union syntax, not Optional[Bullet]
```

**Phase 1 applies:**
- `from __future__ import annotations` already present in files (no change)
- Use `dict[str, dict[str, float]]` for WEAPON_STATS type hint (optional, but recommended)
- Use `str` for current_weapon attribute

---

### TEST_STRUCTURE - Pytest Pattern

**SOURCE:** `zombie-shooter/tests/test_collisions.py:1-25`

**COPY THIS PATTERN:**
```python
"""Tests for [module description]."""

from __future__ import annotations

import pygame

from game.core.constants import SOME_CONSTANT
from game.entities.player import Player


def test_something_specific_scenario() -> None:
    """Test that [specific behavior] works correctly."""
    # Arrange
    pos = pygame.Vector2(0, 0)

    # Act
    result = some_function(pos)

    # Assert
    assert result is True
```

**Phase 1 applies:**
- Test file: `tests/test_weapon_constants.py`
- Test function names: `test_weapon_stats_structure()`, `test_weapon_stats_pistol_default()`
- Descriptive docstrings
- Use `assert` statements

---

## Files to Change

| File                             | Action | Justification                            |
| -------------------------------- | ------ | ---------------------------------------- |
| `zombie-shooter/src/game/core/constants.py` | UPDATE | Add WEAPON_STATS dict and pickup constants |
| `zombie-shooter/src/game/entities/player.py` | UPDATE | Add current_weapon attribute to Player class |
| `zombie-shooter/tests/test_weapon_constants.py` | CREATE | Test weapon stats structure and values |

---

## NOT Building (Scope Limits)

Explicit exclusions to prevent scope creep:

- **Weapon behavior implementation** - Phase 3 will modify Player.shoot() to use WEAPON_STATS. Phase 1 only defines the data model.
- **Pickup entity** - Phase 2 will create the Pickup class. Phase 1 only defines pickup spawn constants.
- **HUD display** - Phase 5 will render weapon name. Phase 1 only tracks current_weapon state.
- **Actual shooting with different weapons** - Player.shoot() remains unchanged in Phase 1. Only the data model is added.

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: UPDATE `zombie-shooter/src/game/core/constants.py`

**ACTION**: ADD weapon statistics dictionary and pickup spawn parameters

**IMPLEMENT**:
```python
# Weapons (ADD THIS SECTION after SHOOT_COOLDOWN line ~line 19)
WEAPON_STATS: dict[str, dict[str, float]] = {
    "pistol": {
        "fire_rate": 0.15,       # seconds between shots
        "bullet_count": 1,       # bullets per shot
        "spread_angle": 0.0,     # degrees spread for multi-shot
    },
    "shotgun": {
        "fire_rate": 0.5,        # slower fire rate
        "bullet_count": 5,       # 5 pellets per shot
        "spread_angle": 30.0,    # ±30° spread total
    },
    "smg": {
        "fire_rate": 0.08,       # rapid fire
        "bullet_count": 1,       # single bullet
        "spread_angle": 0.0,     # no spread
    },
}

# Pickups
PICKUP_SPAWN_RATE = 15.0  # seconds between pickup spawns
PICKUP_RADIUS = 20        # collision radius for pickups
```

**MIRROR**: `constants.py:1-34` - section headers, naming, inline comments

**IMPORTS**: None needed (dict and float are built-in)

**GOTCHA**:
- Use `dict[str, dict[str, float]]` type hint (requires `from __future__ import annotations` - already present)
- Keep spread_angle in degrees (pygame Vector2.rotate uses degrees)
- Values must be float for consistency (even bullet_count, for future flexibility)

**VALIDATE**:
```bash
cd zombie-shooter && python -m py_compile src/game/core/constants.py
```
Expected: No output (successful compilation)

---

### Task 2: UPDATE `zombie-shooter/src/game/entities/player.py`

**ACTION**: ADD current_weapon attribute to Player class

**IMPLEMENT**:
In `__init__` method after line 32 (`self.shoot_cooldown = 0.0`), add:
```python
self.current_weapon: str = "pistol"
```

**MIRROR**: `player.py:21-32` - attribute initialization pattern with inline type hint

**IMPORTS**:
Add to imports section (around line 5-10):
```python
from game.core.constants import (
    PLAYER_MAX_HP,
    PLAYER_RADIUS,
    PLAYER_SPEED,
    SHOOT_COOLDOWN,
    WEAPON_STATS,  # ADD THIS LINE
)
```

**GOTCHA**:
- Place after `shoot_cooldown` to maintain logical grouping (shooting-related attributes)
- Use inline type hint: `self.current_weapon: str`
- Default to `"pistol"` (must match WEAPON_STATS key exactly)
- Do NOT modify `__init__` docstring (no new constructor parameters)

**VALIDATE**:
```bash
cd zombie-shooter && ruff check src/game/entities/player.py && python -m py_compile src/game/entities/player.py
```
Expected: No errors or warnings

---

### Task 3: CREATE `zombie-shooter/tests/test_weapon_constants.py`

**ACTION**: CREATE unit tests for weapon stats structure

**IMPLEMENT**:
```python
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
```

**MIRROR**: `tests/test_collisions.py:1-25` - pytest structure, docstrings, imports

**PATTERN**:
- One test per weapon type + structure test
- Descriptive function names: `test_<what>_<scenario>()`
- Google-style docstrings
- Use `assert` statements with explicit comparisons

**VALIDATE**:
```bash
cd zombie-shooter && pytest tests/test_weapon_constants.py -v
```
Expected: 5 tests passed

---

### Task 4: RUN full validation suite

**ACTION**: Verify all changes integrate correctly with existing codebase

**IMPLEMENT**: Run comprehensive validation commands

**VALIDATE**:
```bash
cd zombie-shooter && ruff format . && ruff check --fix . && pytest -q
```

Expected:
- `ruff format .`: Reformats code (may show files changed)
- `ruff check --fix .`: No errors or warnings
- `pytest -q`: All tests pass (existing + 5 new weapon tests)

**GOTCHA**:
- If ruff changes files, review changes to ensure they're formatting-only
- If pytest fails on existing tests, Phase 1 changes should NOT have broken them - investigate
- New tests should add exactly 5 passing tests to the suite

---

## Testing Strategy

### Unit Tests to Write

| Test File                                | Test Cases                 | Validates      |
| ---------------------------------------- | -------------------------- | -------------- |
| `tests/test_weapon_constants.py` | weapon_stats_structure | All 3 weapons defined |
| `tests/test_weapon_constants.py` | weapon_stats_pistol_default | Pistol values correct |
| `tests/test_weapon_constants.py` | weapon_stats_shotgun | Shotgun spread & count |
| `tests/test_weapon_constants.py` | weapon_stats_smg | SMG rapid fire rate |
| `tests/test_weapon_constants.py` | pickup_constants_defined | Pickup params exist |

### Edge Cases Checklist

- [ ] WEAPON_STATS keys are strings (not enums or ints)
- [ ] WEAPON_STATS values are dicts with required keys
- [ ] Fire rates are positive floats
- [ ] Bullet counts are positive (can be 1 or more)
- [ ] Spread angles are non-negative floats (0° = no spread)
- [ ] Player.current_weapon defaults to "pistol" (valid WEAPON_STATS key)
- [ ] PICKUP_SPAWN_RATE is positive (spawning makes sense)
- [ ] PICKUP_RADIUS is positive (collision detection requires it)

---

## Validation Commands

### Level 1: STATIC_ANALYSIS
```bash
cd zombie-shooter && ruff format . && ruff check --fix .
```
**EXPECT**: Exit 0, no lint errors or warnings

### Level 2: UNIT_TESTS
```bash
cd zombie-shooter && pytest tests/test_weapon_constants.py -v
```
**EXPECT**: 5 tests pass (weapon_stats_structure, pistol_default, shotgun, smg, pickup_constants_defined)

### Level 3: FULL_SUITE
```bash
cd zombie-shooter && pytest -q
```
**EXPECT**: All existing tests + 5 new tests pass

### Level 4: TYPE_CHECK (Optional but recommended)
```bash
cd zombie-shooter && python -m mypy src/game/core/constants.py src/game/entities/player.py --strict
```
**EXPECT**: No type errors (note: mypy not in pyproject.toml, so this is optional)

### Level 5: MANUAL_VALIDATION
```bash
cd zombie-shooter && python -m game.main
```
**EXPECT**:
- Game launches successfully
- No crashes or errors related to new attributes
- Player can still shoot (behavior unchanged in Phase 1)
- Game plays for 60 seconds without issues

---

## Acceptance Criteria

- [ ] WEAPON_STATS dict added to constants.py with pistol, shotgun, SMG configurations
- [ ] Each weapon has fire_rate, bullet_count, spread_angle keys (all float values)
- [ ] PICKUP_SPAWN_RATE and PICKUP_RADIUS constants defined
- [ ] Player class has current_weapon attribute (default "pistol")
- [ ] All 5 unit tests pass (weapon stats structure and values)
- [ ] Level 1-3 validation commands pass with exit 0
- [ ] Existing tests still pass (no regressions)
- [ ] Code follows ruff formatting and linting standards
- [ ] Type hints follow modern syntax (dict[str, dict[str, float]])
- [ ] Game runs without errors (manual validation level 5)

---

## Completion Checklist

- [ ] Task 1: WEAPON_STATS and pickup constants added to constants.py
- [ ] Task 2: current_weapon attribute added to Player.__init__()
- [ ] Task 3: test_weapon_constants.py created with 5 tests
- [ ] Task 4: Full validation suite passes (ruff + pytest)
- [ ] Level 1: Static analysis passes (ruff format + check)
- [ ] Level 2: Unit tests pass (5/5 weapon tests)
- [ ] Level 3: Full test suite passes (all existing + new tests)
- [ ] Level 5: Manual validation passes (game runs 60s without error)
- [ ] All acceptance criteria met
- [ ] No regressions in existing functionality

---

## Risks and Mitigations

| Risk               | Likelihood   | Impact       | Mitigation                              |
| ------------------ | ------------ | ------------ | --------------------------------------- |
| Type hint breaks Python 3.11 | LOW | HIGH | Use `from __future__ import annotations` (already present) - enables modern dict[...] syntax |
| WEAPON_STATS keys typo | LOW | MEDIUM | Unit tests verify exact key names ("pistol", "shotgun", "smg") |
| Player.current_weapon invalid default | LOW | HIGH | Default to "pistol" which is guaranteed to exist in WEAPON_STATS dict |
| Existing tests break | LOW | MEDIUM | Phase 1 is purely additive (no behavior changes) - run full test suite to verify |
| PICKUP_RADIUS too small | LOW | LOW | Use 20 pixels (larger than player radius 18) - generous hitbox |
| Future phases can't find constants | LOW | HIGH | Use standard import pattern from game.core.constants - tested in unit tests |

---

## Notes

**Design Decisions:**

1. **Dict-based configuration over classes**: WEAPON_STATS uses a simple nested dict rather than Weapon classes. This is:
   - Simpler to implement and test
   - Easier to extend with new weapons (just add dict entry)
   - More flexible (can be loaded from JSON/YAML in future)
   - Follows data-driven game design patterns

2. **spread_angle in degrees**: Pygame's Vector2.rotate() method uses degrees, not radians. Storing spread_angle in degrees avoids conversion overhead in hot path (shooting).

3. **bullet_count as float**: While bullet count is logically an int, we use float for consistency with other weapon stats. This allows future fractional values (e.g., 1.5 bullets for balancing) and avoids type mixing in the dict.

4. **current_weapon as str**: Using weapon name string allows direct WEAPON_STATS key lookup. Alternative (enum) would add complexity without clear benefit at this scale.

5. **No weapon class hierarchy**: Player.shoot() will remain a single method that reads WEAPON_STATS rather than delegating to weapon objects. This keeps the design simple and follows the existing entity pattern.

**Future Phase Dependencies:**

- **Phase 2 (Pickup entity)**: Will read PICKUP_RADIUS and PICKUP_SPAWN_RATE from constants
- **Phase 3 (Weapon behavior)**: Will read WEAPON_STATS[player.current_weapon] to vary fire behavior
- **Phase 4 (Pickup spawning)**: Will set player.current_weapon when collision occurs
- **Phase 5 (HUD integration)**: Will read player.current_weapon to display weapon name

**Why Phase 1 Can Run Independently:**

Phase 1 is purely additive:
- Adds constants (never removed or modified)
- Adds player attribute (does not change existing behavior)
- No changes to game loop, shooting logic, or collision detection
- Tests verify data model structure only (not runtime behavior)

This means Phase 1 can be completed, tested, and merged without waiting for other phases.

---

**Sources:**
- [Pygame Vector2 Documentation v2.6.0](https://www.pygame.org/docs/ref/math.html?highlight=vector) - Vector2.rotate() method for spread calculations
- [PEP 589 - TypedDict](https://peps.python.org/pep-0589/) - Type hints for nested dictionaries
- [Python typing module](https://docs.python.org/3/library/typing.html) - Modern type hint syntax
