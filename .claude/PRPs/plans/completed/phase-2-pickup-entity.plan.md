# Feature: Phase 2 - Pickup Entity

## Summary

Create the Pickup entity class that represents collectible weapon pickups on the game map. The Pickup class follows the established entity pattern (pos, radius, update, draw) with TTL-based lifecycle management like bullets. Pickups render as colored rectangles (different colors for pistol/shotgun/SMG), have collision radius for player interaction, and automatically despawn after a time-to-live period. This phase establishes the visual representation of pickups before Phase 4 adds spawning logic.

## User Story

As a player
I want to see weapon pickups appear on the game map
So that I can visually identify different weapon types and navigate to collect them

## Problem Statement

The game currently has no visual representation for weapon pickups. Players need to see collectible items on the map with distinct visual identifiers for different weapon types (pistol, shotgun, SMG). The Pickup entity must follow existing entity patterns for consistency and integrate cleanly with the collision detection system.

## Solution Statement

Create `entities/pickup.py` implementing the Pickup class with standard entity methods (update, draw). Use the TTL-based lifecycle pattern from Bullet (update returns bool for alive/dead state). Render pickups as colored rectangles using pygame.draw.rect() with weapon-specific colors (yellow for pistol, red for shotgun, green for SMG). Initialize with position, weapon_type, and use PICKUP_RADIUS constant for collision detection.

## Metadata

| Field            | Value                              |
| ---------------- | ---------------------------------- |
| Type             | NEW_CAPABILITY                     |
| Complexity       | LOW                                |
| Systems Affected | entities module                    |
| Dependencies     | pygame>=2.6.0 (already satisfied), Phase 1 complete (WEAPON_STATS, PICKUP_RADIUS) |
| Estimated Tasks  | 5                                  |

---

## UX Design

### Before State
```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌──────────┐                                                                ║
║   │  Player  │  ◄── shoots, moves, avoids zombies                             ║
║   └──────────┘                                                                ║
║        ▲                                                                      ║
║        │  chased by                                                           ║
║        │                                                                      ║
║   ┌──────────┐                                                                ║
║   │ Zombies  │  ◄── spawn, seek player                                        ║
║   └──────────┘                                                                ║
║                                                                               ║
║   MISSING: No pickup entities exist                                           ║
║   PAIN_POINT: Cannot visualize weapon pickups on map                          ║
║   DATA_FLOW: Weapon pickups have no visual representation                     ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌──────────┐                    ┌──────────┐                                ║
║   │  Player  │  ◄── shoots, moves │ Pickups  │  ◄── NEW: Visible on map      ║
║   └──────────┘                    └──────────┘                                ║
║        ▲                                │                                     ║
║        │  chased by                     │  weapon_type: str                   ║
║        │                                │  pos: Vector2                       ║
║   ┌──────────┐                          │  radius: float                      ║
║   │ Zombies  │                          │  ttl: float                         ║
║   └──────────┘                          │                                     ║
║                                         ▼                                     ║
║                              Draw as colored rectangles:                      ║
║                              🟨 Yellow = Pistol                                ║
║                              🟥 Red = Shotgun                                  ║
║                              🟦 Cyan = SMG                                     ║
║                                                                               ║
║   USER_FLOW:                                                                  ║
║   1. Pickup spawned at position (future: Phase 4)                             ║
║   2. Pickup rendered as colored rectangle                                     ║
║   3. Pickup updates TTL each frame                                            ║
║   4. Pickup despawns when TTL expires                                         ║
║                                                                               ║
║   VALUE_ADD:                                                                  ║
║   - Players can see pickups on map                                            ║
║   - Color coding identifies weapon type                                       ║
║   - Collision radius enables player interaction (future: Phase 4)             ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes
| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| Game map | No visible pickups | Colored rectangles appear | Can see where weapons are |
| Pickup lifecycle | N/A | TTL-based despawn | Pickups don't last forever |
| Visual identification | N/A | Yellow/Red/Cyan colors | Can identify weapon type at a glance |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `zombie-shooter/src/game/entities/bullet.py` | 10-59 | Pattern to MIRROR - TTL lifecycle with bool return from update() |
| P0 | `zombie-shooter/src/game/entities/player.py` | 18-98 | Entity structure pattern - __init__, type hints, Google docstrings |
| P1 | `zombie-shooter/src/game/entities/zombie.py` | 10-44 | Additional entity pattern reference |
| P1 | `zombie-shooter/src/game/core/constants.py` | 22-43 | WEAPON_STATS dict and PICKUP_RADIUS already defined |
| P2 | `zombie-shooter/tests/test_weapon_constants.py` | 1-43 | Test pattern to FOLLOW - pytest structure |

**External Documentation:**
| Source | Section | Why Needed |
|--------|---------|------------|
| [Pygame draw.rect() v2.6.0](https://www.pygame.org/docs/ref/draw.html#pygame.draw.rect) | pygame.draw.rect() | Drawing rectangles for pickup visuals |
| [Pygame Rect v2.6.0](https://www.pygame.org/docs/ref/rect.html) | pygame.Rect | Creating Rect objects for positioning |

---

## Patterns to Mirror

### ENTITY_CLASS_STRUCTURE - Complete Pattern

**SOURCE:** `zombie-shooter/src/game/entities/bullet.py:10-59`

**COPY THIS PATTERN:**
```python
"""Bullet entity for zombie shooter."""

from __future__ import annotations

import pygame

from game.core.constants import BULLET_RADIUS, BULLET_SPEED, BULLET_TTL


class Bullet:
    """Bullet entity with directional movement and TTL."""

    def __init__(self, pos: pygame.Vector2, direction: pygame.Vector2) -> None:
        """Initialize bullet.

        Args:
            pos: Starting position as Vector2.
            direction: Direction vector to travel.
        """
        self.pos = pos.copy()  # Copy to avoid reference issues
        self.vel = direction.normalize() * BULLET_SPEED
        self.radius = BULLET_RADIUS
        self.ttl = BULLET_TTL

    def update(self, dt: float) -> bool:
        """Update bullet position and TTL.

        Args:
            dt: Delta time in seconds.

        Returns:
            True if bullet is still alive, False if should be removed.
        """
        self.pos += self.vel * dt
        self.ttl -= dt
        return self.is_alive()

    def is_alive(self) -> bool:
        """Check if bullet is still alive.

        Returns:
            True if TTL > 0, False otherwise.
        """
        return self.ttl > 0

    def draw(self, screen: pygame.Surface) -> None:
        """Draw bullet to screen.

        Args:
            screen: Pygame surface to draw on.
        """
        # Draw yellow circle
        pygame.draw.circle(
            screen, (255, 255, 0), (int(self.pos.x), int(self.pos.y)), self.radius
        )
```

**Phase 2 applies:**
- Follow same structure: docstring, imports, class, __init__, update, is_alive, draw
- Use `pos.copy()` to avoid reference issues
- update() returns `bool` (TTL lifecycle)
- Add is_alive() helper method
- Use Google-style docstrings

---

### DRAWING_PATTERN - Pygame Shapes

**SOURCE:** `zombie-shooter/src/game/entities/player.py:89-98` (circle example)

**COPY THIS PATTERN:**
```python
def draw(self, screen: pygame.Surface) -> None:
    """Draw player to screen.

    Args:
        screen: Pygame surface to draw on.
    """
    # Draw blue circle
    pygame.draw.circle(
        screen, (50, 100, 255), (int(self.pos.x), int(self.pos.y)), self.radius
    )
```

**Phase 2 applies:**
- Use `pygame.draw.rect()` instead of `pygame.draw.circle()`
- Colors as RGB tuples: `(R, G, B)` where 0-255
- Convert position to int: `int(self.pos.x)`, `int(self.pos.y)`
- Create pygame.Rect for rectangle positioning

**Rectangle drawing pattern:**
```python
pygame.draw.rect(
    screen,
    color_tuple,
    pygame.Rect(
        int(self.pos.x) - self.radius,  # Left edge
        int(self.pos.y) - self.radius,  # Top edge
        self.radius * 2,                # Width
        self.radius * 2,                # Height
    ),
)
```

---

### TYPE_HINTS - Modern Python Syntax

**SOURCE:** Used throughout codebase, e.g., `bullet.py:13-23`

**COPY THIS PATTERN:**
```python
from __future__ import annotations  # At top of every file

import pygame

def __init__(self, pos: pygame.Vector2, direction: pygame.Vector2) -> None:
    """Initialize bullet."""
    self.pos: pygame.Vector2 = pos.copy()
    self.radius: float = BULLET_RADIUS
    self.ttl: float = BULLET_TTL

def update(self, dt: float) -> bool:
    """Update with delta time, return alive status."""
```

**Phase 2 applies:**
- `from __future__ import annotations` enables modern syntax
- Type hint all parameters: `pos: pygame.Vector2`, `weapon_type: str`
- Type hint return types: `-> None`, `-> bool`
- Attribute type hints optional but recommended for clarity

---

### TEST_STRUCTURE - Pytest Pattern

**SOURCE:** `zombie-shooter/tests/test_weapon_constants.py:1-43`

**COPY THIS PATTERN:**
```python
"""Tests for weapon constants and data model."""

from __future__ import annotations

from game.core.constants import PICKUP_RADIUS, PICKUP_SPAWN_RATE, WEAPON_STATS


def test_weapon_stats_structure() -> None:
    """Test that WEAPON_STATS has all required weapons."""
    assert "pistol" in WEAPON_STATS
    assert "shotgun" in WEAPON_STATS
    assert "smg" in WEAPON_STATS
```

**Phase 2 applies:**
- Test file: `tests/test_pickup.py`
- Import Pickup class and pygame
- Test function names: `test_pickup_<scenario>()`
- Google-style docstrings describing test purpose
- Use assert statements

---

## Files to Change

| File                             | Action | Justification                            |
| -------------------------------- | ------ | ---------------------------------------- |
| `zombie-shooter/src/game/core/constants.py` | UPDATE | Add PICKUP_TTL constant (time-to-live for pickups) |
| `zombie-shooter/src/game/entities/pickup.py` | CREATE | Main Pickup entity class implementation |
| `zombie-shooter/tests/test_pickup.py` | CREATE | Unit tests for Pickup entity |

---

## NOT Building (Scope Limits)

Explicit exclusions to prevent scope creep:

- **Pickup spawning logic** - Phase 4 will add timer-based spawning to PlayScene. Phase 2 only creates the entity class.
- **Player-pickup collision handling** - Phase 4 will implement collision detection and weapon swapping. Phase 2 establishes the collision radius.
- **Integration with PlayScene** - Phase 4 will add pickup list management to PlayScene. Phase 2 only defines the entity.
- **HUD weapon display** - Phase 5 will render current weapon name. Phase 2 doesn't touch UI.
- **Weapon behavior changes** - Phase 3 will modify shooting to use WEAPON_STATS. Phase 2 is purely visual.

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: UPDATE `zombie-shooter/src/game/core/constants.py`

**ACTION**: ADD PICKUP_TTL constant after PICKUP_RADIUS

**IMPLEMENT**:
Add after line 43 (PICKUP_RADIUS):
```python
PICKUP_TTL = 30.0  # time to live in seconds for pickups
```

**MIRROR**: `constants.py:16-20` - follow constant naming and inline comment pattern

**IMPORTS**: None needed

**GOTCHA**:
- Use float value (30.0 not 30) for consistency with other time constants
- Place after PICKUP_RADIUS in the "# Pickups" section

**VALIDATE**:
```bash
python -m py_compile zombie-shooter/src/game/core/constants.py
```
Expected: No output (successful compilation)

---

### Task 2: CREATE `zombie-shooter/src/game/entities/pickup.py`

**ACTION**: CREATE Pickup entity class with full implementation

**IMPLEMENT**:
```python
"""Pickup entity for zombie shooter."""

from __future__ import annotations

import pygame

from game.core.constants import PICKUP_RADIUS, PICKUP_TTL


class Pickup:
    """Collectible pickup entity with weapon type and TTL."""

    def __init__(self, pos: pygame.Vector2, weapon_type: str) -> None:
        """Initialize pickup.

        Args:
            pos: Starting position as Vector2.
            weapon_type: Type of weapon ("pistol", "shotgun", or "smg").
        """
        self.pos = pos.copy()  # Copy to avoid reference issues
        self.radius = PICKUP_RADIUS
        self.weapon_type = weapon_type
        self.ttl = PICKUP_TTL

    def update(self, dt: float) -> bool:
        """Update pickup TTL.

        Args:
            dt: Delta time in seconds.

        Returns:
            True if pickup is still alive, False if should be removed.
        """
        self.ttl -= dt
        return self.is_alive()

    def is_alive(self) -> bool:
        """Check if pickup is still alive.

        Returns:
            True if TTL > 0, False otherwise.
        """
        return self.ttl > 0

    def draw(self, screen: pygame.Surface) -> None:
        """Draw pickup to screen as colored rectangle.

        Args:
            screen: Pygame surface to draw on.
        """
        # Color mapping for weapon types
        colors = {
            "pistol": (255, 200, 100),   # Yellow/orange
            "shotgun": (255, 100, 100),  # Red
            "smg": (100, 200, 255),      # Cyan
        }
        color = colors.get(self.weapon_type, (200, 200, 200))  # Gray fallback

        # Draw rectangle centered on position
        pygame.draw.rect(
            screen,
            color,
            pygame.Rect(
                int(self.pos.x) - self.radius,  # Left edge
                int(self.pos.y) - self.radius,  # Top edge
                self.radius * 2,                # Width (square)
                self.radius * 2,                # Height (square)
            ),
        )
```

**MIRROR**:
- `bullet.py:10-59` - Overall structure, TTL pattern, is_alive() helper
- `player.py:89-98` - Drawing pattern with pygame.draw

**IMPORTS**:
- `pygame` for Vector2 and drawing
- `PICKUP_RADIUS`, `PICKUP_TTL` from constants

**GOTCHA**:
- Use `pos.copy()` NOT `pos` directly (avoids reference issues like Bullet)
- Rectangle positioned by top-left corner, so subtract radius to center
- `colors.get()` with fallback handles invalid weapon_type gracefully
- Width/height both use `radius * 2` for square shape

**VALIDATE**:
```bash
python -m py_compile zombie-shooter/src/game/entities/pickup.py && zombie-shooter/.venv/bin/ruff check zombie-shooter/src/game/entities/pickup.py
```
Expected: Compilation succeeds, ruff passes with 0 errors

---

### Task 3: CREATE `zombie-shooter/tests/test_pickup.py`

**ACTION**: CREATE unit tests for Pickup entity

**IMPLEMENT**:
```python
"""Tests for Pickup entity."""

from __future__ import annotations

import pygame

from game.entities.pickup import Pickup


def test_pickup_initialization() -> None:
    """Test that Pickup initializes with correct attributes."""
    pos = pygame.Vector2(100, 200)
    weapon_type = "shotgun"

    pickup = Pickup(pos, weapon_type)

    assert pickup.pos.x == 100
    assert pickup.pos.y == 200
    assert pickup.weapon_type == "shotgun"
    assert pickup.radius == 20  # PICKUP_RADIUS
    assert pickup.ttl > 0


def test_pickup_position_copy() -> None:
    """Test that Pickup copies position to avoid reference issues."""
    pos = pygame.Vector2(100, 200)
    pickup = Pickup(pos, "pistol")

    # Modify original position
    pos.x = 500

    # Pickup position should be unchanged
    assert pickup.pos.x == 100


def test_pickup_update_decreases_ttl() -> None:
    """Test that update() decreases TTL."""
    pickup = Pickup(pygame.Vector2(0, 0), "smg")
    initial_ttl = pickup.ttl

    is_alive = pickup.update(1.0)  # 1 second elapsed

    assert pickup.ttl == initial_ttl - 1.0
    assert is_alive is True


def test_pickup_dies_when_ttl_expires() -> None:
    """Test that Pickup becomes not alive when TTL <= 0."""
    pickup = Pickup(pygame.Vector2(0, 0), "pistol")
    pickup.ttl = 0.5

    # Update with large dt to expire TTL
    is_alive = pickup.update(1.0)

    assert pickup.ttl <= 0
    assert is_alive is False


def test_pickup_is_alive() -> None:
    """Test is_alive() method."""
    pickup = Pickup(pygame.Vector2(0, 0), "shotgun")

    assert pickup.is_alive() is True

    pickup.ttl = 0
    assert pickup.is_alive() is False

    pickup.ttl = -1
    assert pickup.is_alive() is False


def test_pickup_weapon_types() -> None:
    """Test that all weapon types can be created."""
    for weapon in ["pistol", "shotgun", "smg"]:
        pickup = Pickup(pygame.Vector2(0, 0), weapon)
        assert pickup.weapon_type == weapon


def test_pickup_draw_no_error() -> None:
    """Test that draw() executes without errors."""
    pickup = Pickup(pygame.Vector2(100, 100), "pistol")
    screen = pygame.Surface((800, 600))

    # Should not raise exception
    pickup.draw(screen)
```

**MIRROR**: `test_weapon_constants.py:1-43` - Test structure, docstrings, imports

**PATTERN**:
- One test per behavior or edge case
- Descriptive function names: `test_pickup_<scenario>()`
- Google-style docstrings explaining test intent
- Use `assert` statements with explicit comparisons

**GOTCHA**:
- Must initialize pygame.Vector2 for position tests
- Need to create pygame.Surface for draw() test
- TTL tests use small values (0.5, 1.0) for fast execution

**VALIDATE**:
```bash
PYTHONPATH=zombie-shooter/src zombie-shooter/.venv/bin/python -m pytest zombie-shooter/tests/test_pickup.py -v
```
Expected: 8 tests pass

---

### Task 4: RUN static analysis

**ACTION**: Verify code formatting and linting

**IMPLEMENT**: Run ruff format and check

**VALIDATE**:
```bash
zombie-shooter/.venv/bin/ruff format zombie-shooter && zombie-shooter/.venv/bin/ruff check zombie-shooter
```

Expected:
- `ruff format`: May reformat files (acceptable)
- `ruff check`: All checks passed, 0 errors

**GOTCHA**:
- Ruff may adjust spacing/line breaks (this is expected)
- If F401 (unused import) errors, verify all imports are used

---

### Task 5: RUN full test suite

**ACTION**: Verify all tests pass (existing + new)

**IMPLEMENT**: Run pytest with full suite

**VALIDATE**:
```bash
PYTHONPATH=zombie-shooter/src zombie-shooter/.venv/bin/python -m pytest zombie-shooter -q
```

Expected: All tests pass (7 collision + 5 weapon constants + 8 pickup = 20 total)

**GOTCHA**:
- If import errors occur, check PYTHONPATH is set correctly
- If new tests fail, check Pickup implementation matches test expectations

---

## Testing Strategy

### Unit Tests to Write

| Test File                                | Test Cases                 | Validates      |
| ---------------------------------------- | -------------------------- | -------------- |
| `tests/test_pickup.py` | test_pickup_initialization | Constructor sets all attributes correctly |
| | test_pickup_position_copy | Position is copied (not referenced) |
| | test_pickup_update_decreases_ttl | TTL decreases by dt |
| | test_pickup_dies_when_ttl_expires | Returns False when TTL <= 0 |
| | test_pickup_is_alive | is_alive() method works correctly |
| | test_pickup_weapon_types | All weapon types supported |
| | test_pickup_draw_no_error | draw() executes without exceptions |

### Edge Cases Checklist

- [ ] Pickup initialized with valid weapon types ("pistol", "shotgun", "smg")
- [ ] Pickup initialized with invalid weapon type (should render gray fallback color)
- [ ] Pickup position is copied (modifying original pos doesn't affect pickup)
- [ ] Pickup TTL decreases correctly with various dt values
- [ ] Pickup returns False when TTL reaches 0
- [ ] Pickup returns False when TTL goes negative
- [ ] Pickup draw() handles edge positions (near screen bounds)
- [ ] Pickup radius is PICKUP_RADIUS (20 pixels)

---

## Validation Commands

### Level 1: STATIC_ANALYSIS
```bash
zombie-shooter/.venv/bin/ruff format zombie-shooter && zombie-shooter/.venv/bin/ruff check zombie-shooter
```
**EXPECT**: Exit 0, all checks passed

### Level 2: UNIT_TESTS
```bash
PYTHONPATH=zombie-shooter/src zombie-shooter/.venv/bin/python -m pytest zombie-shooter/tests/test_pickup.py -v
```
**EXPECT**: 8 tests pass (pickup initialization, position copy, TTL lifecycle, weapon types, draw)

### Level 3: FULL_SUITE
```bash
PYTHONPATH=zombie-shooter/src zombie-shooter/.venv/bin/python -m pytest zombie-shooter -q
```
**EXPECT**: All tests pass (20 total: 7 collision + 5 weapon constants + 8 pickup)

### Level 4: TYPE_CHECK (Optional)
```bash
zombie-shooter/.venv/bin/python -m mypy zombie-shooter/src/game/entities/pickup.py --strict
```
**EXPECT**: No type errors (mypy not in pyproject.toml, so optional)

### Level 5: MANUAL_VALIDATION
```bash
PYTHONPATH=zombie-shooter/src zombie-shooter/.venv/bin/python -c "from game.entities.pickup import Pickup; import pygame; pygame.init(); p = Pickup(pygame.Vector2(100, 100), 'shotgun'); print(f'Pickup created: pos={p.pos}, weapon={p.weapon_type}, radius={p.radius}, ttl={p.ttl}')"
```
**EXPECT**: Output shows pickup created successfully with correct attributes

---

## Acceptance Criteria

- [ ] PICKUP_TTL constant added to constants.py
- [ ] Pickup class created in entities/pickup.py
- [ ] Pickup has pos, radius, weapon_type, ttl attributes
- [ ] Pickup.update() returns bool (TTL lifecycle)
- [ ] Pickup.is_alive() helper method implemented
- [ ] Pickup.draw() renders colored rectangle (yellow/red/cyan by weapon)
- [ ] 8 unit tests written and passing
- [ ] Level 1-3 validation commands pass with exit 0
- [ ] Code follows ruff formatting and linting standards
- [ ] Type hints follow modern syntax (pygame.Vector2, str, bool)
- [ ] Google-style docstrings on all public methods

---

## Completion Checklist

- [ ] Task 1: PICKUP_TTL added to constants.py
- [ ] Task 2: Pickup entity class created in entities/pickup.py
- [ ] Task 3: test_pickup.py created with 8 tests
- [ ] Task 4: Static analysis passes (ruff format + check)
- [ ] Task 5: Full test suite passes (20 tests)
- [ ] Level 1: Static analysis passes
- [ ] Level 2: Unit tests pass (8/8 pickup tests)
- [ ] Level 3: Full suite passes (20 tests)
- [ ] Level 5: Manual validation passes
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk               | Likelihood   | Impact       | Mitigation                              |
| ------------------ | ------------ | ------------ | --------------------------------------- |
| Rectangle drawing offset incorrect | LOW | MEDIUM | Use `pos - radius` for top-left corner, test with visual inspection in Phase 4 |
| Position reference bug | LOW | HIGH | Use `pos.copy()` like Bullet entity (tested in test_pickup_position_copy) |
| Invalid weapon_type crashes draw() | LOW | MEDIUM | Use `colors.get()` with fallback gray color for unknown types |
| TTL too short/long | MEDIUM | LOW | PICKUP_TTL = 30.0 seconds balances visibility and map clutter (adjustable constant) |
| Test import failures | LOW | MEDIUM | Use `PYTHONPATH=zombie-shooter/src` for all pytest commands |

---

## Notes

**Design Decisions:**

1. **TTL-based lifecycle**: Pickups follow Bullet pattern with `update() -> bool` rather than Player/Zombie pattern (`update() -> None`). This allows PlayScene to filter pickups using list comprehension: `pickups = [p for p in pickups if p.update(dt)]`. This is essential for Phase 4 integration.

2. **Rectangle shape**: Phase 2 uses rectangles instead of circles to differentiate pickups from other entities (player/bullets/zombies are circles). This provides instant visual distinction.

3. **Color coding**:
   - Pistol: Yellow/orange (255, 200, 100) - warm, basic
   - Shotgun: Red (255, 100, 100) - aggressive, spread weapon
   - SMG: Cyan (100, 200, 255) - cool, rapid fire
   - Invalid: Gray fallback (defensive programming)

4. **PICKUP_TTL = 30 seconds**: Long enough for players to notice and reach pickups, short enough to prevent map clutter. Adjustable via constants.py without code changes.

5. **Square dimensions**: Both width and height use `radius * 2` creating 40x40 pixel squares (PICKUP_RADIUS = 20). This makes pickups larger than bullets (8px diameter) but smaller than player (36px diameter).

6. **Position copying**: Like Bullet, Pickup uses `pos.copy()` to avoid reference issues. Without this, modifying the spawn position would move the pickup.

**Integration with Future Phases:**

- **Phase 3 (Weapon behavior)**: No dependency - Phase 3 modifies Player.shoot(), Pickup is independent
- **Phase 4 (Pickup spawning)**: Will import Pickup class, create instances: `Pickup(pos, weapon_type)`, add to PlayScene.pickups list
- **Phase 4 (Collision)**: Will use check_collision_circle(player.pos, player.radius, pickup.pos, pickup.radius)
- **Phase 4 (Collection)**: Will read pickup.weapon_type and set player.current_weapon
- **Phase 5 (HUD)**: No direct dependency on Pickup entity

**Why Phase 2 Can Run Independently:**

Phase 2 creates the entity class but doesn't integrate it with PlayScene. The Pickup class can be:
- Instantiated in tests
- Drawn to surfaces
- Updated with delta time
- All without PlayScene integration

This means Phase 2 can be completed and tested in isolation before Phase 4 adds spawning/collection logic.

**Performance Considerations:**

- Pickup.update() is O(1) - just TTL decrement
- Pickup.draw() is O(1) - single pygame.draw.rect call
- No pathfinding or complex logic
- Expected max pickups on map: ~4-5 (60s game / 15s spawn rate)
- Negligible performance impact

---

**Sources:**
- [Pygame draw.rect() Documentation v2.6.0](https://www.pygame.org/docs/ref/draw.html#pygame.draw.rect) - Rectangle drawing API
- [Pygame Rect Documentation v2.6.0](https://www.pygame.org/docs/ref/rect.html) - Rect object creation
