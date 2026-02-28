# Feature: Environment — Ground Textures & Solid Obstacles

## Summary

Replace the flat gray `screen.fill()` background with a pre-baked terrain surface (grass zones,
dirt patches, cross-shaped asphalt path) and populate the world with ~27 hand-placed solid
obstacles (trees, ponds, crashed cars, houses, burning barrels). Both player and zombie entities
are pushed out of solid obstacles via axis-by-axis AABB and circle-circle resolution. All
constants live in `constants.py`; the Obstacle dataclass lives in `entities/obstacle.py`;
push-out functions extend `systems/collisions.py`; PlayScene wires everything together.

## User Story

As a game player
I want an environment with varied terrain and solid obstacles to navigate around
So that the game feels like an abandoned post-apocalyptic town rather than an empty void

## Problem Statement

`play.py:333` calls `screen.fill((40, 40, 40))` — the entire world is one flat dark gray.
No collision system handles static world geometry. Zombie AI has no awareness of environment.

## Solution Statement

1. Pre-bake a `pygame.Surface` once at scene init with grass/dirt/asphalt zones
2. Define ~27 `Obstacle` instances from constants data (trees=circle, houses/cars=rect, ponds=ellipse-as-rect)
3. Draw obstacles each frame at the correct z-layer (above ground, below blood decals)
4. Add push-out collision for player and zombies via new functions in `collisions.py`
5. Barrel flicker: sin-oscillated color on `obstacle.flicker == True` obstacles

## Metadata

| Field | Value |
|-------|-------|
| Type | NEW_CAPABILITY |
| Complexity | MEDIUM |
| Systems Affected | play.py, constants.py, entities/obstacle.py (NEW), systems/collisions.py |
| Dependencies | pygame 2.6+ (already installed) |
| Estimated Tasks | 10 |

---

## UX Design

### Before State

```
╔══════════════════════════════════════════════════════╗
║                  BEFORE STATE                        ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  screen.fill((40,40,40))  →  flat dark gray          ║
║                                                      ║
║  Player spawns center     →  runs freely anywhere    ║
║  Zombies spawn at edges   →  beeline straight to     ║
║                              player, no obstacles    ║
║                                                      ║
║  PAIN: game looks like a tech demo                   ║
║  PAIN: zero tactical decisions (no cover)            ║
║  PAIN: zombies clip through "walls" that             ║
║         don't exist                                  ║
╚══════════════════════════════════════════════════════╝
```

### After State

```
╔══════════════════════════════════════════════════════╗
║                   AFTER STATE                        ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  Pre-baked Surface:                                  ║
║  ┌──────────────────────────────────────────────┐    ║
║  │ [HOUSE] grass/dirt  │  dirt/grass  [HOUSE]  │    ║
║  │  ○tree ○tree        │      ○tree            │    ║
║  │                     │                       │    ║
║  │══════════ ASPHALT PATH ═════════════════════│    ║
║  │          [CAR][CAR] │  ⬤barrel ⬤barrel    │    ║
║  │                     │                       │    ║
║  │                VERT PATH                     │    ║
║  │                     │                       │    ║
║  │ ⬭pond  ○tree       │  [CAR]   ○tree        │    ║
║  │ [HOUSE] ⬤barrel   │           [HOUSE]     │    ║
║  └──────────────────────────────────────────────┘    ║
║                                                      ║
║  Player: slides along obstacle edges (no clip)       ║
║  Zombies: pushed out, bunch at corners (acceptable)  ║
║  60fps maintained with 50 zombies                    ║
╚══════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| `play.py:333` | `screen.fill((40,40,40))` | `screen.blit(ground_surf, (0,0))` | Terrain zones visible |
| `play.py draw()` | No obstacles drawn | Obstacles drawn above ground | World objects appear |
| `player.py update()` | Clamp to screen bounds only | Clamp + push-out vs obstacles | Cannot walk through houses/cars/trees |
| `zombie.py update()` | Seek player, no env. awareness | Seek player + push-out vs obstacles | Zombies navigate around world objects |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `src/game/scenes/play.py` | 1-70 | Imports pattern; `__init__` structure to mirror |
| P0 | `src/game/scenes/play.py` | 326-367 | `draw()` method — z-order to insert obstacle draw pass |
| P0 | `src/game/core/constants.py` | all | Where to add ground zone and obstacle constants |
| P0 | `src/game/entities/player.py` | 65-94 | `update()` where screen clamp lives — add push-out after line 94 |
| P0 | `src/game/entities/zombie.py` | 66-100 | `update(dt, player_pos)` signature — add obstacles param |
| P1 | `src/game/systems/collisions.py` | all | Pattern to extend with new push-out functions |
| P1 | `src/game/entities/blood_decal.py` | all | Dataclass-less entity pattern to mirror for Obstacle |
| P1 | `src/game/entities/pickup.py` | all | `pygame.draw.*` shape drawing pattern |
| P2 | `tests/test_collisions.py` | all | Test structure to mirror for new push-out tests |
| P2 | `tests/test_blood_decal.py` | all | Entity test structure: init, update, draw |

---

## Patterns to Mirror

**ENTITY_INIT_PATTERN:**
```python
# SOURCE: src/game/entities/blood_decal.py:10-22
# COPY THIS PATTERN for Obstacle __init__:
class BloodDecal:
    def __init__(self, pos: pygame.Vector2) -> None:
        self.pos = pos.copy()   # ← copy Vector2 on init
        self.lifetime = CORPSE_PERSISTENCE
        self.size = BLOOD_POOL_SIZE
        self.color = (120, 0, 0)
```

**PYGAME_DRAW_RECT_PATTERN:**
```python
# SOURCE: src/game/entities/pickup.py:59-69
# COPY THIS PATTERN for obstacle rect drawing:
pygame.draw.rect(
    screen,
    color,
    pygame.Rect(
        int(self.pos.x) - self.radius,
        int(self.pos.y) - self.radius,
        self.radius * 2,
        self.radius * 2,
    ),
)
```

**PYGAME_DRAW_ELLIPSE_PATTERN:**
```python
# SOURCE: src/game/entities/blood_decal.py:51-58
# COPY THIS PATTERN for obstacle ellipse drawing:
temp_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
rect = pygame.Rect(0, 0, self.size, self.size)
pygame.draw.ellipse(temp_surface, color_with_alpha, rect)
screen.blit(temp_surface, (int(self.pos.x) - self.size // 2, ...))
```

**CONSTANTS_PATTERN:**
```python
# SOURCE: src/game/core/constants.py:44-61
# COPY THIS PATTERN — raw Python types only, no pygame imports in constants.py:
WEAPON_STATS: dict[str, dict[str, float]] = {
    "pistol": {
        "fire_rate": 0.15,
        ...
    },
}
```

**COLLISION_FUNCTION_PATTERN:**
```python
# SOURCE: src/game/systems/collisions.py:8-26
# COPY THIS PATTERN for new push-out function signature:
def check_collision_circle(
    pos1: pygame.Vector2, r1: float, pos2: pygame.Vector2, r2: float
) -> bool:
    """Check if two circles overlap using distance squared (no sqrt).
    Args: ...
    Returns: ...
    """
```

**PLAY_SCENE_DRAW_PATTERN:**
```python
# SOURCE: src/game/scenes/play.py:326-366
# CURRENT z-order to INSERT obstacle draw between ground and decals:
screen.fill((40, 40, 40))          # ← REPLACE with: screen.blit(self._ground, (0,0))
# ← INSERT obstacle draw pass HERE (above decals, below everything)
for decal in self.blood_decals:    # decals stay below corpses
    decal.draw(screen)
```

**PLAY_SCENE_IMPORT_PATTERN:**
```python
# SOURCE: src/game/scenes/play.py:11-26
# PATTERN: import all needed constants from game.core.constants in one block
from game.core.constants import (
    BLOOD_PARTICLE_COUNT,
    ...
    WIDTH,
)
```

**TEST_FUNCTION_PATTERN:**
```python
# SOURCE: tests/test_collisions.py:15-19
# COPY THIS PATTERN — module-level pygame.init() not needed if no display:
def test_check_collision_circle_overlapping() -> None:
    """Test that overlapping circles are detected."""
    pos1 = pygame.Vector2(0, 0)
    pos2 = pygame.Vector2(5, 0)
    assert check_collision_circle(pos1, 10, pos2, 10) is True
```

---

## Files to Change

| File | Action | Justification |
|------|--------|---------------|
| `src/game/core/constants.py` | UPDATE | Add ground zone colors/rects and obstacle definition data |
| `src/game/entities/obstacle.py` | CREATE | Obstacle dataclass + `build_obstacles()` factory + `draw()` |
| `src/game/systems/collisions.py` | UPDATE | Add `resolve_entity_obstacle_circle()` and `resolve_entity_obstacle_rect()` |
| `src/game/scenes/play.py` | UPDATE | Init ground surface + obstacle list; wire draw/collision |
| `src/game/entities/player.py` | UPDATE | Add `obstacles` param to `update()`, call push-out |
| `src/game/entities/zombie.py` | UPDATE | Add `obstacles` param to `update()`, call push-out |
| `tests/test_obstacle.py` | CREATE | Unit tests for Obstacle class and push-out functions |

---

## NOT Building (Scope Limits)

- **Procedural map generation** — same map every run, designer-controlled
- **A* pathfinding for zombies** — push-out sliding is sufficient
- **Bullet collision with obstacles** — bullets pass through everything
- **Sprite/pixel art assets** — pygame.draw shapes only
- **Destructible obstacles** — permanently solid
- **Camera/scrolling** — fixed 1280×720 viewport

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

---

### Task 1: ADD ground zone and obstacle constants to `src/game/core/constants.py`

**ACTION**: APPEND new constant blocks to the bottom of constants.py

**IMPLEMENT** the following (append after `# Win Condition` section):

```python
# ─── Ground Zones ────────────────────────────────────────────────────────────
# Colors (RGB, no pygame import needed here — plain tuples)
GROUND_GRASS_COLOR: tuple[int, int, int] = (42, 58, 32)       # dark olive green
GROUND_DIRT_COLOR: tuple[int, int, int] = (72, 57, 38)        # dark brown
GROUND_ASPHALT_COLOR: tuple[int, int, int] = (36, 36, 36)     # near-black
GROUND_ASPHALT_EDGE_COLOR: tuple[int, int, int] = (50, 50, 50) # lighter edge seam

# Ground geometry as (x, y, w, h) tuples — convert to pygame.Rect in play.py
# Horizontal asphalt path: 100px tall, vertically centered at y=360
GROUND_PATH_H: tuple[int, int, int, int] = (0, 310, 1280, 100)
# Vertical asphalt path: 100px wide, horizontally centered at x=640
GROUND_PATH_V: tuple[int, int, int, int] = (590, 0, 100, 720)
# Path edge seam strips (thin lighter lines along path borders)
GROUND_PATH_SEAMS: list[tuple[int, int, int, int]] = [
    (0, 308, 1280, 4),    # top edge of H path
    (0, 408, 1280, 4),    # bottom edge of H path
    (588, 0, 4, 720),     # left edge of V path
    (688, 0, 4, 720),     # right edge of V path
]
# Dirt patch regions (scattered, away from path)
GROUND_DIRT_RECTS: list[tuple[int, int, int, int]] = [
    (30, 30, 250, 170),     # top-left quad
    (880, 40, 280, 150),    # top-right quad
    (30, 480, 220, 200),    # bottom-left quad
    (950, 460, 250, 220),   # bottom-right quad
    (350, 30, 180, 120),    # top-center-left
    (730, 430, 160, 140),   # bottom-center-right
]

# ─── Obstacle Definitions ────────────────────────────────────────────────────
# Each entry: (type, shape, cx, cy, w_or_r, h_or_r, base_color, flicker)
#   type:   "house" | "tree" | "car" | "pond" | "barrel"
#   shape:  "rect" | "circle" | "ellipse"
#   cx, cy: center position
#   w_or_r: width (rect/ellipse) OR radius (circle)
#   h_or_r: height (rect/ellipse) OR radius (circle, same as w_or_r)
#   base_color: RGB tuple — each instance gets ±15 random offset at build time
#   flicker: bool — True for burning barrels
ObstacleDef = tuple[str, str, int, int, int, int, tuple[int, int, int], bool]

OBSTACLE_DEFS: list[ObstacleDef] = [
    # ── Houses (corners, large rects) ──
    ("house", "rect",  105,  80, 110, 90, (55, 45, 38), False),   # top-left
    ("house", "rect", 1175,  80, 110, 90, (48, 40, 34), False),   # top-right
    ("house", "rect",  105, 640, 110, 90, (52, 43, 36), False),   # bottom-left
    ("house", "rect", 1175, 640, 110, 90, (50, 42, 35), False),   # bottom-right

    # ── Trees (circles, grass zones only) ──
    ("tree", "circle", 230,  95,  14, 14, (28, 52, 22), False),   # top-left quad
    ("tree", "circle", 310, 185,  16, 16, (32, 58, 25), False),
    ("tree", "circle", 130, 230,  13, 13, (25, 48, 20), False),
    ("tree", "circle", 800, 110,  15, 15, (30, 54, 23), False),   # top-right quad
    ("tree", "circle", 970, 190,  14, 14, (27, 50, 21), False),
    ("tree", "circle",1120, 160,  16, 16, (33, 58, 26), False),
    ("tree", "circle", 175, 540,  15, 15, (29, 53, 22), False),   # bottom-left quad
    ("tree", "circle", 320, 600,  13, 13, (26, 49, 20), False),
    ("tree", "circle", 840, 510,  16, 16, (31, 55, 24), False),   # bottom-right quad
    ("tree", "circle",1080, 595,  14, 14, (28, 51, 21), False),
    ("tree", "circle",1170, 510,  15, 15, (30, 54, 23), False),

    # ── Crashed Cars (rects, on/near path) ──
    ("car", "rect",  330, 358,  52, 26, (58, 52, 48), False),     # H path, left side
    ("car", "rect",  430, 362,  50, 24, (62, 44, 38), False),     # H path, near crashed
    ("car", "rect",  870, 355,  50, 26, (55, 50, 45), False),     # H path, right side
    ("car", "rect",  638, 200,  26, 50, (60, 48, 40), False),     # V path, upper
    ("car", "rect",  642, 570,  26, 50, (56, 44, 36), False),     # V path, lower

    # ── Ponds (ellipses treated as AABB, grass zones) ──
    ("pond", "ellipse", 270, 490,  80, 54, (28, 45, 52), False),  # bottom-left
    ("pond", "ellipse", 940, 155,  90, 58, (25, 42, 50), False),  # top-right

    # ── Barrels (circles, near houses/walls) ──
    ("barrel", "circle", 165,  95,  10, 10, (90, 55, 20), False), # top-left house
    ("barrel", "circle", 190, 130,  10, 10, (85, 50, 18),  True), # burning
    ("barrel", "circle",1150,  95,  10, 10, (88, 52, 19), False), # top-right house
    ("barrel", "circle",1175, 130,  10, 10, (82, 48, 17),  True), # burning
    ("barrel", "circle", 168, 595,  10, 10, (86, 51, 18), False), # bottom-left house
    ("barrel", "circle",1155, 595,  10, 10, (89, 54, 20),  True), # burning
]
```

**IMPORTANT CONSTRAINTS**:
- `constants.py` has **no pygame import** — use plain Python types only (tuples, lists, booleans)
- Keep `ObstacleDef` type alias for clarity — it's just a `tuple` type annotation

**VALIDATE**: `ruff check src/game/core/constants.py` exits 0

---

### Task 2: CREATE `src/game/entities/obstacle.py`

**ACTION**: CREATE new file — Obstacle dataclass with factory and draw methods

**IMPLEMENT**:

```python
"""Obstacle entity for zombie shooter world."""

from __future__ import annotations

import math
import random

import pygame

from game.core.constants import HEIGHT, OBSTACLE_DEFS, WIDTH


class Obstacle:
    """Solid world obstacle with shape-based collision and varied color."""

    def __init__(
        self,
        obstacle_type: str,
        shape: str,
        pos: pygame.Vector2,
        width: float,
        height: float,
        color: tuple[int, int, int],
        flicker: bool = False,
    ) -> None:
        """Initialize obstacle.

        Args:
            obstacle_type: Kind of obstacle ("house", "tree", "car", "pond", "barrel").
            shape: Collision/visual shape ("rect", "circle", "ellipse").
            pos: Center position as Vector2.
            width: Width in pixels (rect/ellipse) or diameter (circle).
            height: Height in pixels (rect/ellipse) or diameter (circle).
            color: Base RGB color tuple.
            flicker: True if obstacle should animate (burning barrels).
        """
        self.obstacle_type = obstacle_type
        self.shape = shape
        self.pos = pos.copy()
        self.width = width
        self.height = height
        self.color = color
        self.flicker = flicker
        # radius used for circle collision; for rect it's the half-diagonal (unused)
        self.radius = width / 2  # for circle/barrel/tree

    def get_rect(self) -> pygame.Rect:
        """Return axis-aligned bounding rect (for rect and ellipse obstacles).

        Returns:
            Pygame Rect centered on self.pos.
        """
        return pygame.Rect(
            int(self.pos.x - self.width / 2),
            int(self.pos.y - self.height / 2),
            int(self.width),
            int(self.height),
        )

    def draw(self, screen: pygame.Surface, time: float = 0.0) -> None:
        """Draw obstacle to screen.

        Args:
            screen: Pygame surface to draw on.
            time: Elapsed game time in seconds (used for flicker animation).
        """
        color = self.color

        # Burning barrel flicker: oscillate between orange and darker ember
        if self.flicker:
            flicker_t = (math.sin(time * 8.0) + 1.0) / 2.0  # 0.0 to 1.0
            r = int(self.color[0] + flicker_t * 60)
            g = int(self.color[1] + flicker_t * 20)
            b = self.color[2]
            color = (min(255, r), min(255, g), min(255, b))

        if self.shape == "circle":
            pygame.draw.circle(
                screen,
                color,
                (int(self.pos.x), int(self.pos.y)),
                int(self.radius),
            )
            # Darker outline for depth
            outline_color = (
                max(0, color[0] - 30),
                max(0, color[1] - 30),
                max(0, color[2] - 30),
            )
            pygame.draw.circle(
                screen,
                outline_color,
                (int(self.pos.x), int(self.pos.y)),
                int(self.radius),
                2,  # outline width
            )

        elif self.shape == "rect":
            rect = self.get_rect()
            pygame.draw.rect(screen, color, rect)
            # Darker outline
            outline_color = (
                max(0, color[0] - 25),
                max(0, color[1] - 25),
                max(0, color[2] - 25),
            )
            pygame.draw.rect(screen, outline_color, rect, 2)
            # Window/detail hints for houses
            if self.obstacle_type == "house":
                window_color = (max(0, color[0] - 15), max(0, color[1] - 10), max(0, color[2] + 5))
                # Two small dark windows
                win_w, win_h = 18, 14
                wx1 = rect.left + 12
                wx2 = rect.right - 12 - win_w
                wy = rect.top + 14
                pygame.draw.rect(screen, window_color, pygame.Rect(wx1, wy, win_w, win_h))
                pygame.draw.rect(screen, window_color, pygame.Rect(wx2, wy, win_w, win_h))

        elif self.shape == "ellipse":
            # Draw ellipse on temp surface for crisp edges
            surf = pygame.Surface((int(self.width), int(self.height)), pygame.SRCALPHA)
            r, g, b = color
            pygame.draw.ellipse(surf, (r, g, b, 220), pygame.Rect(0, 0, int(self.width), int(self.height)))
            # Darker outline
            pygame.draw.ellipse(
                surf,
                (max(0, r - 20), max(0, g - 20), max(0, b - 20), 255),
                pygame.Rect(0, 0, int(self.width), int(self.height)),
                2,
            )
            screen.blit(
                surf,
                (int(self.pos.x - self.width / 2), int(self.pos.y - self.height / 2)),
            )


def build_obstacles(seed: int = 42) -> list[Obstacle]:
    """Build the fixed obstacle list from OBSTACLE_DEFS with seeded color variation.

    Args:
        seed: RNG seed for reproducible color offsets across runs.

    Returns:
        List of Obstacle instances ready for use in PlayScene.
    """
    rng = random.Random(seed)
    obstacles: list[Obstacle] = []

    for obs_type, shape, cx, cy, w, h, base_color, flicker in OBSTACLE_DEFS:
        # Per-instance color offset ±15 on each channel for visual variety
        r = max(0, min(255, base_color[0] + rng.randint(-15, 15)))
        g = max(0, min(255, base_color[1] + rng.randint(-15, 15)))
        b = max(0, min(255, base_color[2] + rng.randint(-15, 15)))
        varied_color = (r, g, b)

        obstacles.append(
            Obstacle(
                obstacle_type=obs_type,
                shape=shape,
                pos=pygame.Vector2(cx, cy),
                width=float(w),
                height=float(h),
                color=varied_color,
                flicker=flicker,
            )
        )

    return obstacles
```

**GOTCHA**: `Obstacle` is not a `@dataclass` — use plain `__init__` to match entity pattern in codebase (none of the entities use `@dataclass`).
**GOTCHA**: `pos.copy()` is mandatory (pattern from `BloodDecal.__init__:19`).

**VALIDATE**: `ruff check src/game/entities/obstacle.py` exits 0; `python -c "import pygame; pygame.init(); from game.entities.obstacle import build_obstacles; print(len(build_obstacles()))"` prints `27`

---

### Task 3: ADD push-out functions to `src/game/systems/collisions.py`

**ACTION**: APPEND two new functions after the last existing function

**IMPLEMENT** (append at end of file):

```python
def resolve_circle_vs_circle_obstacle(
    entity_pos: pygame.Vector2,
    entity_radius: float,
    obstacle_pos: pygame.Vector2,
    obstacle_radius: float,
) -> pygame.Vector2:
    """Push entity out of a circular obstacle using minimum separation.

    Args:
        entity_pos: Entity center position.
        entity_radius: Entity collision radius.
        obstacle_pos: Obstacle center position.
        obstacle_radius: Obstacle collision radius.

    Returns:
        Corrected entity position (unchanged if no overlap).
    """
    diff = entity_pos - obstacle_pos
    dist = diff.length()
    min_dist = entity_radius + obstacle_radius

    if dist < min_dist:
        if dist > 0:
            return obstacle_pos + diff.normalize() * min_dist
        else:
            # Exactly on center — push up
            return pygame.Vector2(obstacle_pos.x, obstacle_pos.y - min_dist)
    return entity_pos


def resolve_circle_vs_rect_obstacle(
    entity_pos: pygame.Vector2,
    entity_radius: float,
    obstacle_rect: pygame.Rect,
) -> pygame.Vector2:
    """Push entity circle out of a rectangular obstacle (AABB).

    Uses axis-by-axis separation: pushes on the axis with smaller overlap,
    producing natural edge-sliding behaviour.

    Args:
        entity_pos: Entity center position.
        entity_radius: Entity collision radius.
        obstacle_rect: Obstacle axis-aligned bounding rect.

    Returns:
        Corrected entity position (unchanged if no overlap).
    """
    # Find closest point on rect to entity center
    closest_x = max(float(obstacle_rect.left), min(entity_pos.x, float(obstacle_rect.right)))
    closest_y = max(float(obstacle_rect.top), min(entity_pos.y, float(obstacle_rect.bottom)))

    diff_x = entity_pos.x - closest_x
    diff_y = entity_pos.y - closest_y
    dist_sq = diff_x * diff_x + diff_y * diff_y

    if dist_sq >= entity_radius * entity_radius:
        return entity_pos  # No overlap

    # Resolve: push on axis with smaller absolute overlap
    overlap_x = entity_radius - abs(entity_pos.x - (obstacle_rect.centerx))
    overlap_y = entity_radius - abs(entity_pos.y - (obstacle_rect.centery))

    # Clamp entity out of rect first to find which axis to prefer
    new_pos = pygame.Vector2(entity_pos)

    if dist_sq > 0:
        dist = dist_sq ** 0.5
        # Push along the normal from closest point to entity
        new_pos.x = closest_x + (diff_x / dist) * entity_radius
        new_pos.y = closest_y + (diff_y / dist) * entity_radius
    else:
        # Entity center is inside rect — push out on smaller axis
        cx = obstacle_rect.centerx
        cy = obstacle_rect.centery
        half_w = obstacle_rect.width / 2 + entity_radius
        half_h = obstacle_rect.height / 2 + entity_radius

        push_x = half_w - abs(entity_pos.x - cx)
        push_y = half_h - abs(entity_pos.y - cy)

        if push_x < push_y:
            sign_x = 1 if entity_pos.x >= cx else -1
            new_pos.x = cx + sign_x * half_w
        else:
            sign_y = 1 if entity_pos.y >= cy else -1
            new_pos.y = cy + sign_y * half_h

    return new_pos


def resolve_entity_vs_obstacles(
    entity_pos: pygame.Vector2,
    entity_radius: float,
    obstacles: list,
) -> pygame.Vector2:
    """Apply push-out resolution against all solid obstacles.

    Iterates all solid obstacles and pushes entity out of each one.
    Multiple passes handle corner cases.

    Args:
        entity_pos: Entity center position.
        entity_radius: Entity collision radius.
        obstacles: List of Obstacle instances.

    Returns:
        Corrected entity position after all push-outs.
    """
    pos = pygame.Vector2(entity_pos)

    for obstacle in obstacles:
        if not obstacle.solid:
            continue

        if obstacle.shape == "circle":
            pos = resolve_circle_vs_circle_obstacle(
                pos, entity_radius, obstacle.pos, obstacle.radius
            )
        else:
            # rect and ellipse both use AABB
            pos = resolve_circle_vs_rect_obstacle(pos, entity_radius, obstacle.get_rect())

    return pos
```

**GOTCHA**: `obstacles: list` uses bare `list` (not `list[Obstacle]`) to avoid circular import — same pattern as existing functions (`bullets: list`, `zombies: list` in `check_bullet_zombie_collisions`).
**GOTCHA**: The `**0.5` instead of `math.sqrt()` is fine here; the file doesn't import math yet. Add `import math` at top of file if needed, or use `** 0.5`. Check existing imports first.

**VALIDATE**: `ruff check src/game/systems/collisions.py` exits 0

---

### Task 4: CREATE and bake ground surface in `src/game/scenes/play.py`

**ACTION**: Add `_build_ground_surface()` module-level function + wire into `__init__` and `draw()`

**Step 4a** — ADD module-level function (place before the `PlayScene` class definition):

```python
def _build_ground_surface() -> pygame.Surface:
    """Build pre-baked ground terrain surface (called once at scene init).

    Draws terrain zones from bottom to top:
    1. Grass base fill
    2. Dirt patches
    3. Cross-shaped asphalt path
    4. Path edge seams

    Returns:
        Pygame Surface with terrain baked in; blit each frame for O(1) cost.
    """
    surface = pygame.Surface((WIDTH, HEIGHT))

    # 1. Base: grass
    surface.fill(GROUND_GRASS_COLOR)

    # 2. Dirt patches
    for x, y, w, h in GROUND_DIRT_RECTS:
        pygame.draw.rect(surface, GROUND_DIRT_COLOR, pygame.Rect(x, y, w, h))

    # 3. Asphalt paths
    hx, hy, hw, hh = GROUND_PATH_H
    vx, vy, vw, vh = GROUND_PATH_V
    pygame.draw.rect(surface, GROUND_ASPHALT_COLOR, pygame.Rect(hx, hy, hw, hh))
    pygame.draw.rect(surface, GROUND_ASPHALT_COLOR, pygame.Rect(vx, vy, vw, vh))

    # 4. Path edge seams (thin lighter lines)
    for x, y, w, h in GROUND_PATH_SEAMS:
        pygame.draw.rect(surface, GROUND_ASPHALT_EDGE_COLOR, pygame.Rect(x, y, w, h))

    return surface
```

**Step 4b** — UPDATE `PlayScene.__init__` — add at the END of `__init__`:

```python
# Pre-baked terrain surface (drawn once, blitted every frame)
self._ground = _build_ground_surface()
# Obstacle list (fixed layout, built once)
from game.entities.obstacle import build_obstacles
self._obstacles = build_obstacles()
```

**Step 4c** — UPDATE `PlayScene.draw()` — replace `screen.fill((40, 40, 40))` and add obstacle draw pass:

```python
def draw(self, screen: pygame.Surface) -> None:
    # Ground terrain (pre-baked surface)
    screen.blit(self._ground, (0, 0))

    # Draw obstacles (above ground, below all entities)
    for obstacle in self._obstacles:
        obstacle.draw(screen, self.timer)

    # Draw blood decals (lowest entity layer - under corpses)
    for decal in self.blood_decals:
        ...  # rest unchanged
```

**Step 4d** — UPDATE `constants.py` imports in `play.py` (add the new ground constants to the existing import block):

```python
from game.core.constants import (
    ...existing imports...,
    GROUND_ASPHALT_COLOR,
    GROUND_ASPHALT_EDGE_COLOR,
    GROUND_DIRT_COLOR,
    GROUND_DIRT_RECTS,
    GROUND_GRASS_COLOR,
    GROUND_PATH_H,
    GROUND_PATH_SEAMS,
    GROUND_PATH_V,
)
```

**GOTCHA**: The `from game.entities.obstacle import build_obstacles` import is placed inside `__init__` to avoid any potential circular import; alternatively add it to the top-level imports — the codebase has no circular risk here, so top-level is preferred. Check and use top-level.
**GOTCHA**: `_build_ground_surface()` must be defined **before** `class PlayScene` — it's a module-level function.

**VALIDATE**: Game launches and shows terrain (run `python -m game.main` from `src/` dir or via Makefile)

---

### Task 5: UPDATE `src/game/entities/player.py` — add obstacle push-out

**ACTION**: Modify `Player.update()` to accept obstacles list and push out after screen clamp

**Step 5a** — UPDATE `update()` signature:

```python
def update(self, dt: float, obstacles: list | None = None) -> None:
    """Update player movement.

    Args:
        dt: Delta time in seconds.
        obstacles: List of Obstacle instances for collision resolution.
    """
```

**Step 5b** — AFTER the screen clamp lines (currently lines 93-94), ADD:

```python
        # Obstacle push-out
        if obstacles:
            from game.systems.collisions import resolve_entity_vs_obstacles
            self.pos = resolve_entity_vs_obstacles(self.pos, self.radius, obstacles)
            # Re-clamp to screen after obstacle resolution
            self.pos.x = max(self.radius, min(WIDTH - self.radius, self.pos.x))
            self.pos.y = max(self.radius, min(HEIGHT - self.radius, self.pos.y))
```

**Step 5c** — UPDATE call site in `play.py`:

In `PlayScene.update()`, change `self.player.update(dt)` to:
```python
self.player.update(dt, self._obstacles)
```

**GOTCHA**: The import inside the function avoids circular imports. Alternatively, add `resolve_entity_vs_obstacles` to the top-level imports in `player.py` — no circular risk exists. Top-level import is preferred. Move it up if it works cleanly.
**GOTCHA**: `obstacles: list | None = None` keeps the signature backwards-compatible with existing tests that call `player.update(dt)` without obstacles.

**VALIDATE**: `ruff check src/game/entities/player.py` + manually verify player cannot walk through house corner

---

### Task 6: UPDATE `src/game/entities/zombie.py` — add obstacle push-out

**ACTION**: Modify `Zombie.update()` to accept obstacles list and push out after position update

**Step 6a** — UPDATE `update()` signature:

```python
def update(self, dt: float, player_pos: pygame.Vector2, obstacles: list | None = None) -> None:
    """Move toward player position.

    Args:
        dt: Delta time in seconds.
        player_pos: Target player position to move toward.
        obstacles: List of Obstacle instances for collision resolution.
    """
```

**Step 6b** — AFTER `self.pos += self.vel * dt` (currently line 76), ADD:

```python
        # Obstacle push-out — applied after movement, before animation update
        if obstacles:
            from game.systems.collisions import resolve_entity_vs_obstacles
            self.pos = resolve_entity_vs_obstacles(self.pos, self.radius, obstacles)
```

**Step 6c** — UPDATE call site in `play.py`:

In `PlayScene._handle_zombie_spawning()`:
```python
for zombie in self.zombies:
    zombie.update(dt, self.player.pos, self._obstacles)
```

**GOTCHA**: Obstacles param is `| None` with default `None` — existing tests that call `zombie.update(dt, player_pos)` remain unbroken.
**GOTCHA**: Push-out is applied BEFORE `self.animation.update(dt, self.vel)` stays correct — velocity is computed, position corrected, animation updated from velocity (animation uses vel direction, not pos delta).

**VALIDATE**: `ruff check src/game/entities/zombie.py` exits 0

---

### Task 7: CREATE `tests/test_obstacle.py`

**ACTION**: CREATE unit test file for Obstacle class and push-out functions

**IMPLEMENT**:

```python
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


def test_obstacle_get_rect() -> None:
    """get_rect returns correct centered rect."""
    obs = Obstacle("house", "rect", pygame.Vector2(200, 200), 100.0, 80.0, (50, 40, 30))
    rect = obs.get_rect()
    assert rect.left == 150
    assert rect.top == 160
    assert rect.width == 100
    assert rect.height == 80


def test_obstacle_draw_no_error() -> None:
    """draw() executes without errors for all shape types."""
    screen = pygame.Surface((800, 600))
    for shape in ("rect", "circle", "ellipse"):
        obs = Obstacle("tree", shape, pygame.Vector2(100, 100), 30.0, 20.0, (40, 60, 30))
        obs.draw(screen, 0.0)  # Should not raise


def test_build_obstacles_count() -> None:
    """build_obstacles returns expected count."""
    obstacles = build_obstacles()
    assert len(obstacles) == 27  # matches OBSTACLE_DEFS length


def test_build_obstacles_reproducible() -> None:
    """build_obstacles with same seed produces identical colors."""
    obs_a = build_obstacles(seed=42)
    obs_b = build_obstacles(seed=42)
    assert obs_a[0].color == obs_b[0].color


# ── Circle vs circle push-out ─────────────────────────────────────────────────

def test_circle_vs_circle_no_overlap() -> None:
    """No change when circles don't overlap."""
    pos = pygame.Vector2(100, 100)
    result = resolve_circle_vs_circle_obstacle(pos, 10, pygame.Vector2(0, 0), 10)
    assert result.x == 100 and result.y == 100


def test_circle_vs_circle_overlap_pushes_out() -> None:
    """Entity is pushed out when overlapping circular obstacle."""
    entity_pos = pygame.Vector2(15, 0)  # inside obstacle with radius 10 + entity 10
    result = resolve_circle_vs_circle_obstacle(
        entity_pos, 10, pygame.Vector2(0, 0), 10
    )
    # Entity should be at distance >= 20 from obstacle center
    dist = result.length()
    assert dist >= 20.0 - 0.01  # small float tolerance


# ── Circle vs rect push-out ───────────────────────────────────────────────────

def test_rect_vs_rect_no_overlap() -> None:
    """No change when entity is outside rect."""
    pos = pygame.Vector2(200, 200)
    rect = pygame.Rect(0, 0, 100, 100)
    result = resolve_circle_vs_rect_obstacle(pos, 18, rect)
    assert result.x == 200 and result.y == 200


def test_rect_entity_pushed_out_from_left() -> None:
    """Entity approaching from left is pushed out."""
    rect = pygame.Rect(100, 100, 80, 60)  # right=180, bottom=160
    # Entity center at (107, 130) — just inside left edge
    entity_pos = pygame.Vector2(107, 130)
    result = resolve_circle_vs_rect_obstacle(entity_pos, 18, rect)
    # Entity left edge should be outside rect left edge
    assert result.x - 18 <= rect.left + 0.1


# ── resolve_entity_vs_obstacles ───────────────────────────────────────────────

def test_resolve_entity_vs_obstacles_empty() -> None:
    """No change when obstacle list is empty."""
    pos = pygame.Vector2(100, 100)
    result = resolve_entity_vs_obstacles(pos, 18, [])
    assert result.x == 100 and result.y == 100


def test_resolve_entity_vs_obstacles_skips_non_solid() -> None:
    """Non-solid obstacles are ignored."""
    obs = Obstacle("pond", "ellipse", pygame.Vector2(100, 100), 50.0, 40.0, (30, 40, 50))
    obs.solid = False
    pos = pygame.Vector2(100, 100)  # Same position as obstacle
    result = resolve_entity_vs_obstacles(pos, 18, [obs])
    assert result.x == 100 and result.y == 100
```

**VALIDATE**: `pytest tests/test_obstacle.py -v` — all tests pass

---

### Task 8: RUN full test suite + lint

**ACTION**: Verify nothing is broken

```bash
# From zombie-shooter/ directory:
ruff format src/ tests/
ruff check src/ tests/
pytest tests/ -v
```

**EXPECT**:
- `ruff format` exits 0, no changes needed (or minor formatting only)
- `ruff check` exits 0, no errors
- `pytest` — all existing tests pass + new obstacle tests pass

**GOTCHA**: If `pytest` fails on `test_player_integration.py` or similar with `TypeError: update() got unexpected keyword argument`, it means the existing tests call `player.update(dt)` — this is why `obstacles: list | None = None` default was added. Verify the default is in place.

---

### Task 9: VISUAL verification

**ACTION**: Run the game and visually inspect

```bash
# From zombie-shooter/ directory (or via Makefile):
make run
# OR: cd src && python -m game.main
```

**CHECKLIST**:
- [ ] Ground renders with visible zones: dark olive grass, brown dirt patches, near-black asphalt path
- [ ] Path forms a clear cross shape through screen center
- [ ] All obstacle types visible: grey/brown houses in corners, dark green tree circles, grey car rects, dark blue-green ponds, orange barrel circles
- [ ] Burning barrels (3 of them) visibly flicker/pulse in color
- [ ] Player cannot walk through any obstacle — slides along edges
- [ ] Zombies cannot walk through obstacles — slide along edges (bunching at corners is acceptable)
- [ ] No single-pixel biome transitions — zone boundaries are wide
- [ ] No obvious obstacle clustering (>3 same type in adjacent area)
- [ ] FPS stays at ~60 even with 50 zombies active

---

### Task 10: UPDATE PRD phase statuses

**ACTION**: Edit `.claude/PRPs/prds/environment-obstacles-textures.prd.md`

Update Implementation Phases table:
- Change all 6 phases `Status: pending` → `Status: complete`
- Add plan file path to all `PRP Plan` columns: `.claude/PRPs/plans/environment-obstacles-textures.plan.md`

---

## Testing Strategy

### Unit Tests to Write

| Test File | Test Cases | Validates |
|-----------|------------|-----------|
| `tests/test_obstacle.py` | Init, pos copy, get_rect, draw no-error, build count, build reproducible | Obstacle class |
| `tests/test_obstacle.py` | circle-circle no overlap, overlap pushes out | Circle collision |
| `tests/test_obstacle.py` | rect no overlap, pushed from left | Rect collision |
| `tests/test_obstacle.py` | empty obstacles, non-solid skipped | resolve_entity_vs_obstacles |

### Edge Cases Checklist

- [ ] Entity exactly at obstacle center (zero-length diff vector) — handled with fallback push-up
- [ ] Entity outside all obstacles — position unchanged
- [ ] `obstacles=None` passed to `player.update()` / `zombie.update()` — no error (default None)
- [ ] Non-solid obstacle (e.g., pond set solid=False) — skipped in push-out
- [ ] Barrel flicker at `time=0.0` — valid color, no math error
- [ ] `build_obstacles()` called twice with same seed — identical results (reproducibility)

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
cd zombie-shooter
ruff format src/ tests/ && ruff check src/ tests/
```

**EXPECT**: Exit 0

### Level 2: UNIT_TESTS

```bash
cd zombie-shooter
pytest tests/test_obstacle.py -v
```

**EXPECT**: All new tests pass

### Level 3: FULL_SUITE

```bash
cd zombie-shooter
pytest tests/ -v
```

**EXPECT**: All 132+ tests pass (no regressions)

### Level 4: MANUAL_VALIDATION

```bash
cd zombie-shooter/src && python -m game.main
# OR from zombie-shooter/: make run
```

Walk through visual checklist from Task 9.

---

## Acceptance Criteria

- [ ] Ground surface renders terrain zones (grass, dirt, asphalt path)
- [ ] All 5 obstacle types visible with varied colors
- [ ] Burning barrels animate/flicker
- [ ] Player cannot walk through any solid obstacle
- [ ] Zombies cannot walk through any solid obstacle
- [ ] All existing tests pass (no regressions)
- [ ] New obstacle unit tests pass
- [ ] `ruff check` exits 0
- [ ] Stable ~60fps visually confirmed with active zombies

---

## Completion Checklist

- [ ] Task 1: Constants added (`constants.py`)
- [ ] Task 2: `obstacle.py` created and importable
- [ ] Task 3: Push-out functions added to `collisions.py`
- [ ] Task 4: Ground surface wired into `play.py`
- [ ] Task 5: Player push-out wired in `player.py` + `play.py`
- [ ] Task 6: Zombie push-out wired in `zombie.py` + `play.py`
- [ ] Task 7: `test_obstacle.py` created and passing
- [ ] Task 8: Full suite passes, lint clean
- [ ] Task 9: Visual inspection checklist complete
- [ ] Task 10: PRD statuses updated

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Zombie push-out jitter at corners | MED | LOW | Multiple obstacles applied sequentially; jitter is visual-only, not a crash |
| Existing tests break due to signature change | LOW | MED | Both `player.update()` and `zombie.update()` keep `None` default — existing calls unchanged |
| Zombie spawns inside obstacle | LOW | LOW | Spawns at screen edges (spawner code); houses are inward; push-out resolves on first frame anyway |
| Barrel flicker at 60fps causes overhead | LOW | LOW | Single `math.sin()` per flicker barrel per frame — negligible |
| `constants.py` grows too large | LOW | LOW | Add clear section headers as comments; file stays readable |

---

## Notes

**Why all 6 phases in one plan**: Phases 1–6 are tightly coupled — the Obstacle model (phase 2)
is required by rendering (3), player collision (4), and zombie collision (5). Separating them
would create intermediate broken states. A single plan covering all phases gives one-pass
implementation success.

**Ground surface memory**: 1280×720×3 bytes (RGB) ≈ 2.76 MB. Negligible.

**Obstacle count verification**: 4 houses + 15 trees + 5 cars + 2 ponds + 7 barrels = 33 entries
in OBSTACLE_DEFS. Verify `len(OBSTACLE_DEFS)` matches the count in `test_build_obstacles_count()`.
Update the test assertion if the final count differs from 27.

**Future enhancement path**: If ponds should slow movement (PRD "Could"), add `movement_modifier: float = 1.0` to Obstacle and check it in `player.update()` before applying velocity.
