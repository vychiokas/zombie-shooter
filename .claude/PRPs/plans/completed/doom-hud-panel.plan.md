# Feature: Doom HUD Panel (Phase 1)

## Summary

Replace the four white-text overlays with a Doom-inspired bottom-center HUD panel: a procedurally drawn pixel-art face whose expression degrades through 5 HP states (with a 0.4s pain-flash override when hit), flanked by weapon icon slots that gray out unowned guns and highlight the active one. Top-screen timer/kills text remains. All drawing is pure `pygame.draw` — no external assets, consistent with the obstacle/terrain art style already established.

## User Story

As a player
I want to glance at the bottom of the screen and instantly know my health state and weapon loadout
So that I can make tactical decisions without reading numbers mid-fight

## Problem Statement

Current HUD = 4 `font.render()` calls (HP top-left, timer top-center, kills top-right, weapon bottom-left). Zero immersion: no visual damage feedback, no weapon inventory display. Player cannot tell at a glance if they are healthy or dying. Weapon text says "Weapon: Shotgun" — no icon, no inventory view.

## Solution Statement

Add `pain_timer` + `take_damage()` to `Player`. Add HUD helper functions to `play.py` (`_get_face_state`, `_draw_hud_face`, `_build_weapon_icons`, `_draw_weapon_icons`). Replace `_draw_hud()` body with a centered bottom panel (440×88px) containing: weapon icon strip left, face portrait center, HP display right. Pre-build weapon icon surfaces once in `PlayScene.__init__` (like ground tiles).

## Metadata

| Field | Value |
|-------|-------|
| Type | NEW_CAPABILITY |
| Complexity | MEDIUM |
| Systems Affected | `constants.py`, `player.py`, `play.py`, `tests/test_hud.py` |
| Dependencies | pygame 2.6 (already installed) |
| Estimated Tasks | 6 |

---

## UX Design

### Before State

```
┌──────────────────────────────────────────────────────────────────────────┐
│ HP: 73                 Survived: 12.4s                     Kills: 5      │
│                                                                          │
│                       [game world]                                       │
│                                                                          │
│                                                                          │
│ Weapon: Shotgun                                                          │
└──────────────────────────────────────────────────────────────────────────┘
USER_FLOW: Player is hit → hp number decreases → player must read number
PAIN_POINT: No visceral damage feedback; no weapon inventory visible
DATA_FLOW: player.hp → font.render() → white text at fixed pixel coords
```

### After State

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        Survived: 12.4s                     Kills: 5     │
│                                                                          │
│                       [game world]                                       │
│                                                                          │
│          ┌─────────────────────────────────────────────┐                │
│          │ [🔫PISTOL] [☆SHOTGUN] [☆SMG] │ 😐 │ HP 73  │                │
│          └─────────────────────────────────────────────┘                │
└──────────────────────────────────────────────────────────────────────────┘
USER_FLOW: Player is hit → face flashes grimace (0.4s) → face degrades w/ HP
VALUE_ADD: Immediate visceral feedback; weapon inventory visible at a glance
DATA_FLOW: player.hp + player.pain_timer + player.weapons_inventory →
           _get_face_state() → _draw_hud_face() / _draw_weapon_icons()
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| `play.py:_draw_hud` | 4 text labels | Panel + face + icons | HUD looks like Doom |
| `play.py:421` | `HP: 73` text top-left | HP number inside panel right | Cleaner layout |
| `play.py:447` | `Weapon: Shotgun` text | Removed, replaced by icon | Icon-based inventory |
| `player.py` | Direct `hp -=` | `take_damage()` resets pain_timer | Pain flash on any hit |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `zombie-shooter/src/game/scenes/play.py` | 421-447 | `_draw_hud()` to REPLACE |
| P0 | `zombie-shooter/src/game/scenes/play.py` | 168-194 | `PlayScene.__init__` — add `_weapon_icons` here |
| P0 | `zombie-shooter/src/game/entities/player.py` | 44-64 | Player.__init__ — add `pain_timer` here |
| P0 | `zombie-shooter/src/game/entities/player.py` | 66-114 | Player.update() — add pain_timer decrement |
| P0 | `zombie-shooter/src/game/scenes/play.py` | 240-247 | explosion damage — change to take_damage() |
| P0 | `zombie-shooter/src/game/scenes/play.py` | 371-396 | `_process_player_damage()` — change to take_damage() |
| P1 | `zombie-shooter/src/game/core/constants.py` | 1-30 | Pattern for adding constants (no pygame imports!) |
| P1 | `zombie-shooter/src/game/scenes/play.py` | 58-130 | Ground tile helper functions — MIRROR this pattern for HUD helpers |
| P2 | `zombie-shooter/tests/test_obstacle.py` | 1-50 | Test structure to FOLLOW |

---

## Patterns to Mirror

**HELPER_FUNCTIONS (module-level in play.py):**
```python
# SOURCE: zombie-shooter/src/game/scenes/play.py:61-77
# COPY THIS PATTERN — module-level helper, returns Surface, called once:
def _make_grass_tile() -> pygame.Surface:
    """Generate a 16×16 pixel art grass tile with blade detail."""
    import random as _r
    rng = _r.Random(0xBEEF_CAFE)
    tile = pygame.Surface((_TILE_SIZE, _TILE_SIZE))
    tile.fill((38, 52, 28))
    ...
    return tile
```

**PRE-BUILD PATTERN (in __init__):**
```python
# SOURCE: zombie-shooter/src/game/scenes/play.py:191-194
# COPY THIS PATTERN — build once, store as self._xxx:
self._ground = _build_ground_surface()
self._obstacles: list[Obstacle] = build_obstacles()
```

**CONSTANTS (no pygame imports):**
```python
# SOURCE: zombie-shooter/src/game/core/constants.py:129-144
# COPY THIS PATTERN — plain ints/tuples only, no pygame:
GROUND_GRASS_COLOR: tuple[int, int, int] = (42, 58, 32)
GROUND_PATH_H: tuple[int, int, int, int] = (0, 310, 1280, 100)
```

**TEST STRUCTURE:**
```python
# SOURCE: zombie-shooter/tests/test_obstacle.py:21-29
# COPY THIS PATTERN — pytest functions, pygame.init() at module top:
pygame.init()

def test_obstacle_rect_init() -> None:
    """Obstacle initializes with correct attributes."""
    obs = Obstacle(...)
    assert obs.attribute == expected
```

**PLAYER INIT FIELD:**
```python
# SOURCE: zombie-shooter/src/game/entities/player.py:54-58
# ADD pain_timer alongside existing timer fields:
self.hp = float(PLAYER_MAX_HP)
self.shoot_cooldown = 0.0
self.shoot_timer = 0.0  # existing
self.pain_timer = 0.0   # ADD HERE — same pattern
self.current_weapon: str = "pistol"
```

**PLAYER UPDATE TIMER DECREMENT:**
```python
# SOURCE: zombie-shooter/src/game/entities/player.py:109-114
# COPY THIS PATTERN for pain_timer:
if self.shoot_cooldown > 0:
    self.shoot_cooldown -= dt
if self.shoot_timer > 0:
    self.shoot_timer -= dt
# ADD:
if self.pain_timer > 0:
    self.pain_timer -= dt
```

---

## Files to Change

| File | Action | Justification |
|------|--------|---------------|
| `zombie-shooter/src/game/core/constants.py` | UPDATE | Add HUD dimension/timing constants |
| `zombie-shooter/src/game/entities/player.py` | UPDATE | Add `pain_timer`, `take_damage()` |
| `zombie-shooter/src/game/scenes/play.py` | UPDATE | Add HUD helpers, replace `_draw_hud()`, update damage calls, pre-build icons |
| `zombie-shooter/tests/test_hud.py` | CREATE | Unit tests for face state logic and player damage tracking |

---

## NOT Building (Scope Limits)

- Animated face sprite sheets — procedural pygame.draw only
- Ammo counter — infinite ammo by design
- Full-width Doom-style bar — centered 440×88px panel fits 1280×720 better
- Sound on damage — no audio system
- Phase 2 (pickup sprites) — separate parallel phase, separate plan

---

## Step-by-Step Tasks

### Task 1: UPDATE `constants.py` — add HUD constants

- **ACTION**: ADD a `# ─── HUD ───` section at the end of constants.py
- **IMPLEMENT**: Add these constants (plain ints/tuples only — NO pygame imports):
  ```python
  # ─── HUD ─────────────────────────────────────────────────────────────────────
  HUD_PANEL_W = 440          # Width of bottom HUD panel in pixels
  HUD_PANEL_H = 88           # Height of bottom HUD panel in pixels
  HUD_FACE_SIZE = 60         # Face portrait diameter in pixels
  HUD_ICON_W = 52            # Weapon icon width in pixels
  HUD_ICON_H = 30            # Weapon icon height in pixels
  HUD_PAIN_FLASH_DURATION = 0.4  # Seconds pain flash face lasts after hit
  ```
- **MIRROR**: `constants.py:129-144` — same style, plain tuples/ints, no pygame
- **GOTCHA**: NEVER import pygame in constants.py — will break tests that import constants without pygame display
- **VALIDATE**: `make lint`

---

### Task 2: UPDATE `player.py` — add `pain_timer` field and `take_damage()` method

- **ACTION**: THREE changes to player.py
- **CHANGE A**: In `__init__` (line 54-58 area), add `self.pain_timer: float = 0.0` after `self.shoot_timer`:
  ```python
  self.shoot_timer = 0.0   # existing line
  self.pain_timer: float = 0.0   # ADD — seconds until pain flash ends
  ```
- **CHANGE B**: In `update()` (line 109-114 area), add decrement after shoot_timer:
  ```python
  if self.shoot_timer > 0:
      self.shoot_timer -= dt   # existing
  if self.pain_timer > 0:      # ADD
      self.pain_timer -= dt    # ADD
  ```
- **CHANGE C**: Add new method `take_damage()` after `switch_weapon()` (after line 188):
  ```python
  def take_damage(self, amount: float) -> None:
      """Apply damage to player and trigger pain flash.

      Args:
          amount: HP to subtract (positive value).
      """
      from game.core.constants import HUD_PAIN_FLASH_DURATION
      if amount > 0:
          self.hp -= amount
          self.pain_timer = HUD_PAIN_FLASH_DURATION
  ```
  - **IMPORTS**: `HUD_PAIN_FLASH_DURATION` imported inside the method body to avoid circular import risk (safe pattern already used in play.py line 401)
  - **GOTCHA**: Import inside method body (see existing `from game.scenes.game_over import GameOverScene` pattern at play.py:401)
- **MIRROR**: `player.py:109-114` for decrement pattern; `player.py:168-188` for method pattern
- **VALIDATE**: `make lint`

---

### Task 3: UPDATE `play.py` — replace direct `hp -=` with `take_damage()`

- **ACTION**: Change THREE direct hp mutation sites to use `self.player.take_damage()`
- **CHANGE A**: `_process_player_damage()` line 381:
  - OLD: `self.player.hp -= CONTACT_DPS * dt * len(colliding_zombies)`
  - NEW: `self.player.take_damage(CONTACT_DPS * dt * len(colliding_zombies))`
- **CHANGE B**: `_process_player_damage()` line 389:
  - OLD: `self.player.hp -= projectile.damage`
  - NEW: `self.player.take_damage(projectile.damage)`
- **CHANGE C**: `apply_explosion()` line 247:
  - OLD: `self.player.hp -= EXPLODER_EXPLOSION_DAMAGE_TO_PLAYER`
  - NEW: `self.player.take_damage(EXPLODER_EXPLOSION_DAMAGE_TO_PLAYER)`
- **GOTCHA**: The `if colliding_zombies:` guard is already there — `take_damage` will get a positive value; no divide-by-zero risk
- **VALIDATE**: `make lint && make test` — all 153 passing tests must still pass

---

### Task 4: ADD HUD helpers to `play.py` — face state, face drawing, weapon icons

Add four module-level functions **before** the `PlayScene` class definition (after `_tile_region` / `_build_ground_surface`).

- **ACTION**: ADD these four functions to `play.py` at module level

**Function A — `_get_face_state(hp, pain_timer)`**:
```python
def _get_face_state(hp: float, pain_timer: float) -> str:
    """Return face expression state string based on HP and pain timer.

    Args:
        hp: Current player HP (0–100).
        pain_timer: Seconds remaining in pain flash (0 = no flash).

    Returns:
        One of: "pain_flash", "normal", "hurt", "injured", "critical", "dying".
    """
    if pain_timer > 0:
        return "pain_flash"
    if hp >= 80:
        return "normal"
    if hp >= 60:
        return "hurt"
    if hp >= 40:
        return "injured"
    if hp >= 20:
        return "critical"
    return "dying"
```

**Function B — `_draw_hud_face(screen, cx, cy, r, state)`**:
```python
def _draw_hud_face(
    screen: pygame.Surface,
    cx: int,
    cy: int,
    r: int,
    state: str,
) -> None:
    """Draw procedural pixel-art face portrait at (cx, cy) with radius r.

    Args:
        screen: Surface to draw on.
        cx: Center x coordinate.
        cy: Center y coordinate.
        r: Face radius in pixels (half of HUD_FACE_SIZE).
        state: Expression state from _get_face_state().
    """
    # Skin color degrades with HP
    skin = {
        "pain_flash": (230, 175, 120),
        "normal":     (220, 168, 112),
        "hurt":       (208, 155, 100),
        "injured":    (192, 142,  88),
        "critical":   (172, 124,  74),
        "dying":      (148, 104,  62),
    }[state]

    # Head circle
    pygame.draw.circle(screen, skin, (cx, cy), r)
    pygame.draw.circle(screen, (max(0, skin[0]-40), max(0, skin[1]-40), max(0, skin[2]-40)), (cx, cy), r, 2)

    # Eye positions
    ex_l = cx - r // 3
    ex_r = cx + r // 3
    ey   = cy - r // 5
    er   = max(3, r // 5)   # eye white radius

    if state == "pain_flash":
        # Wide-open eyes (shock), small O-mouth
        pygame.draw.circle(screen, (255, 255, 255), (ex_l, ey), er + 2)
        pygame.draw.circle(screen, (20, 20, 20), (ex_l, ey), er // 2)
        pygame.draw.circle(screen, (255, 255, 255), (ex_r, ey), er + 2)
        pygame.draw.circle(screen, (20, 20, 20), (ex_r, ey), er // 2)
        pygame.draw.circle(screen, (40, 30, 25), (cx, cy + r // 4), max(3, r // 6))

    elif state == "normal":
        # Normal round eyes, gentle upward mouth
        pygame.draw.circle(screen, (255, 255, 255), (ex_l, ey), er)
        pygame.draw.circle(screen, (30, 20, 15), (ex_l, ey), er // 2)
        pygame.draw.circle(screen, (255, 255, 255), (ex_r, ey), er)
        pygame.draw.circle(screen, (30, 20, 15), (ex_r, ey), er // 2)
        # Slight smile: two upward points from center
        mx = cx
        my = cy + r // 4
        pygame.draw.line(screen, (60, 35, 20), (mx - r//4, my+1), (mx, my-1), 2)
        pygame.draw.line(screen, (60, 35, 20), (mx, my-1), (mx + r//4, my+1), 2)

    elif state == "hurt":
        # Slightly squinted — flatten top of eye circle
        pygame.draw.circle(screen, (255, 255, 255), (ex_l, ey), er)
        pygame.draw.circle(screen, (30, 20, 15), (ex_l, ey), er // 2)
        pygame.draw.circle(screen, (255, 255, 255), (ex_r, ey), er)
        pygame.draw.circle(screen, (30, 20, 15), (ex_r, ey), er // 2)
        # Draw squint line over top half of each eye
        pygame.draw.line(screen, skin, (ex_l - er, ey - 1), (ex_l + er, ey - 1), 3)
        pygame.draw.line(screen, skin, (ex_r - er, ey - 1), (ex_r + er, ey - 1), 3)
        # Neutral flat mouth
        pygame.draw.line(screen, (55, 32, 18), (cx - r//4, cy + r//4), (cx + r//4, cy + r//4), 2)

    elif state == "injured":
        # Left eye X, right eye squinted
        pygame.draw.line(screen, (200, 40, 40), (ex_l - er, ey - er), (ex_l + er, ey + er), 2)
        pygame.draw.line(screen, (200, 40, 40), (ex_l + er, ey - er), (ex_l - er, ey + er), 2)
        pygame.draw.circle(screen, (255, 255, 255), (ex_r, ey), er)
        pygame.draw.circle(screen, (30, 20, 15), (ex_r, ey), er // 2)
        pygame.draw.line(screen, skin, (ex_r - er, ey - 1), (ex_r + er, ey - 1), 3)
        # Frown
        mx = cx
        my = cy + r // 4
        pygame.draw.line(screen, (60, 35, 20), (mx - r//4, my-1), (mx, my+2), 2)
        pygame.draw.line(screen, (60, 35, 20), (mx, my+2), (mx + r//4, my-1), 2)
        # Blood drop on left cheek
        pygame.draw.circle(screen, (180, 20, 20), (ex_l - 2, cy + r//3), 2)

    elif state == "critical":
        # Both eyes X
        for ex in (ex_l, ex_r):
            pygame.draw.line(screen, (200, 40, 40), (ex - er, ey - er), (ex + er, ey + er), 2)
            pygame.draw.line(screen, (200, 40, 40), (ex + er, ey - er), (ex - er, ey + er), 2)
        # Grimace — jagged line
        gmy = cy + r // 4
        pts = [
            (cx - r//4, gmy), (cx - r//8, gmy - 3),
            (cx,        gmy + 3), (cx + r//8, gmy - 3),
            (cx + r//4, gmy),
        ]
        pygame.draw.lines(screen, (55, 32, 18), False, pts, 2)
        # Blood marks both cheeks
        pygame.draw.circle(screen, (180, 20, 20), (ex_l - 2, cy + r//3), 2)
        pygame.draw.circle(screen, (180, 20, 20), (ex_r + 2, cy + r//3), 2)

    else:  # dying
        # Both eyes X (larger), heavy grimace, skin very pale handled via skin color above
        for ex in (ex_l, ex_r):
            pygame.draw.line(screen, (220, 40, 40), (ex - er, ey - er), (ex + er, ey + er), 3)
            pygame.draw.line(screen, (220, 40, 40), (ex + er, ey - er), (ex - er, ey + er), 3)
        # Droop — downturned heavy grimace
        gmy = cy + r // 4
        pts = [
            (cx - r//3, gmy - 2), (cx - r//6, gmy + 4),
            (cx,        gmy - 1), (cx + r//6, gmy + 4),
            (cx + r//3, gmy - 2),
        ]
        pygame.draw.lines(screen, (50, 28, 14), False, pts, 2)
        # Blood streak down from left eye
        pygame.draw.line(screen, (160, 15, 15), (ex_l, ey + er), (ex_l - 1, cy + r//2), 2)
        pygame.draw.circle(screen, (180, 20, 20), (ex_r + 2, cy + r//3), 2)
```

**Function C — `_build_weapon_icons()`**:
```python
_WEAPON_ORDER = ("pistol", "shotgun", "smg")


def _build_weapon_icons() -> dict[str, pygame.Surface]:
    """Pre-build weapon icon surfaces for HUD (called once in PlayScene.__init__).

    Each icon is HUD_ICON_W × HUD_ICON_H pixels, drawn on a transparent surface.
    The base surface is always drawn bright; state coloring applied at blit time.

    Returns:
        Dict mapping weapon name to Surface with gun silhouette.
    """
    from game.core.constants import HUD_ICON_H, HUD_ICON_W

    icons: dict[str, pygame.Surface] = {}

    for weapon in _WEAPON_ORDER:
        surf = pygame.Surface((HUD_ICON_W, HUD_ICON_H), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 0))  # fully transparent

        w, h = HUD_ICON_W, HUD_ICON_H  # 52 × 30

        if weapon == "pistol":
            # Compact handgun: body center-right, short barrel right, grip below
            body_rect  = pygame.Rect(w//2 - 6, h//2 - 5, 20, 10)
            barrel_rect = pygame.Rect(w - 16, h//2 - 3, 16, 6)
            grip_rect  = pygame.Rect(w//2 - 2, h//2 + 5, 8, 14)
            trigger_x  = w//2 + 6
            for r in (body_rect, barrel_rect, grip_rect):
                pygame.draw.rect(surf, (200, 200, 200), r)
            # Trigger guard arc approximation
            pygame.draw.line(surf, (180, 180, 180), (trigger_x, h//2 + 4), (trigger_x + 4, h//2 + 10), 2)

        elif weapon == "shotgun":
            # Long pump shotgun: long barrel top, body center, pump on barrel, stock left
            barrel_rect = pygame.Rect(8, h//2 - 3, w - 10, 6)
            body_rect   = pygame.Rect(w//3, h//2 - 5, 18, 10)
            pump_rect   = pygame.Rect(w//2 - 2, h//2 - 5, 8, 4)
            stock_rect  = pygame.Rect(2, h//2 - 8, 12, 16)
            for r in (barrel_rect, body_rect, pump_rect, stock_rect):
                pygame.draw.rect(surf, (200, 200, 200), r)
            # Barrel tip circle
            pygame.draw.circle(surf, (180, 180, 180), (w - 4, h//2), 4)

        else:  # smg
            # Boxy SMG: body center, short barrel right, vertical mag below, small stock left
            body_rect   = pygame.Rect(w//4, h//2 - 5, 24, 10)
            barrel_rect = pygame.Rect(w//4 + 24, h//2 - 3, 12, 6)
            mag_rect    = pygame.Rect(w//4 + 8, h//2 + 5, 8, 14)
            stock_rect  = pygame.Rect(4, h//2 - 4, 10, 8)
            for r in (body_rect, barrel_rect, mag_rect, stock_rect):
                pygame.draw.rect(surf, (200, 200, 200), r)

        icons[weapon] = surf

    return icons
```

**Function D — `_draw_weapon_icons(screen, panel_x, panel_y, icons, inventory, current)`**:
```python
def _draw_weapon_icons(
    screen: pygame.Surface,
    panel_x: int,
    panel_y: int,
    icons: dict[str, pygame.Surface],
    inventory: set[str],
    current: str,
) -> None:
    """Draw weapon icon slots on the HUD panel.

    Three fixed slots (pistol / shotgun / smg), left-to-right.
    - Not owned: gray silhouette, dark slot background
    - Owned, not active: normal silhouette, medium slot background
    - Active: bright silhouette, bright slot background + 2px yellow border

    Args:
        screen: Surface to draw on.
        panel_x: Left edge of the icons area.
        panel_y: Top edge of the icons area.
        icons: Pre-built icon surfaces from _build_weapon_icons().
        inventory: Set of owned weapon names.
        current: Currently equipped weapon name.
    """
    from game.core.constants import HUD_ICON_H, HUD_ICON_W

    slot_pad = 6  # pixels between slots

    for i, weapon in enumerate(_WEAPON_ORDER):
        sx = panel_x + i * (HUD_ICON_W + slot_pad)
        sy = panel_y
        slot_rect = pygame.Rect(sx, sy, HUD_ICON_W, HUD_ICON_H)

        owned   = weapon in inventory
        active  = weapon == current

        # Slot background
        if active:
            bg = (55, 48, 32)
        elif owned:
            bg = (35, 32, 28)
        else:
            bg = (22, 20, 18)
        pygame.draw.rect(screen, bg, slot_rect)

        # Selection border for active weapon
        if active:
            pygame.draw.rect(screen, (220, 190, 40), slot_rect, 2)
        else:
            pygame.draw.rect(screen, (55, 52, 48), slot_rect, 1)

        # Icon surface with colorization
        icon = icons.get(weapon)
        if icon is None:
            continue
        tinted = icon.copy()
        if not owned:
            # Gray out: multiply to dark gray
            tinted.fill((60, 60, 60, 0), special_flags=pygame.BLEND_RGB_MULT)
        elif active:
            # Brighten for active
            tinted.fill((255, 240, 180, 0), special_flags=pygame.BLEND_RGB_MULT)
        # else: normal — keep base (200,200,200) silhouette
        screen.blit(tinted, slot_rect)
```

- **IMPORTS needed at top of play.py** (add to existing import block):
  ```python
  from game.core.constants import (
      ...
      HUD_FACE_SIZE,
      HUD_ICON_H,
      HUD_ICON_W,
      HUD_PAIN_FLASH_DURATION,  # only needed if referenced outside player.py
      HUD_PANEL_H,
      HUD_PANEL_W,
      ...
  )
  ```
  - **GOTCHA**: Add all 5 HUD constants to the existing import tuple in play.py — do NOT import `HUD_PAIN_FLASH_DURATION` if it's only used inside `player.py`; only import what `play.py` actually uses
  - **GOTCHA**: `_WEAPON_ORDER` and functions D reference `HUD_ICON_W`/`HUD_ICON_H` — import from constants at module level, not inside functions, to keep it clean. However, the local imports inside `_build_weapon_icons` and `_draw_weapon_icons` are acceptable to avoid cluttering module-level import block — mirror the pattern at `play.py:401` where `GameOverScene` is imported locally
- **VALIDATE**: `make lint`

---

### Task 5: UPDATE `play.py` — replace `_draw_hud()`, wire icons in `__init__`

- **ACTION A**: Add `self._weapon_icons = _build_weapon_icons()` in `PlayScene.__init__` after `self._obstacles = build_obstacles()` (line 194)
- **ACTION B**: Replace entire `_draw_hud()` body (lines 421-447) with new implementation:

```python
def _draw_hud(self, screen: pygame.Surface) -> None:
    """Draw heads-up display: top overlays + Doom-style bottom panel."""
    # ── Top overlays ─────────────────────────────────────────────────────
    # Survival timer (top-center)
    timer_text = self.font.render(
        f"Survived: {self.timer:.1f}s", True, (255, 255, 255)
    )
    timer_rect = timer_text.get_rect(center=(WIDTH // 2, 25))
    screen.blit(timer_text, timer_rect)

    # Kills (top-right)
    kills_text = self.font.render(f"Kills: {self.kills}", True, (255, 255, 255))
    kills_rect = kills_text.get_rect(topright=(WIDTH - 10, 10))
    screen.blit(kills_text, kills_rect)

    # ── Bottom HUD panel ─────────────────────────────────────────────────
    panel_x = (WIDTH - HUD_PANEL_W) // 2
    panel_y = HEIGHT - HUD_PANEL_H - 4

    # Panel background + border
    pygame.draw.rect(
        screen, (20, 18, 16),
        pygame.Rect(panel_x, panel_y, HUD_PANEL_W, HUD_PANEL_H),
    )
    pygame.draw.rect(
        screen, (65, 60, 52),
        pygame.Rect(panel_x, panel_y, HUD_PANEL_W, HUD_PANEL_H), 2,
    )

    icon_area_w = len(_WEAPON_ORDER) * (HUD_ICON_W + 6) - 6  # 3 × (52+6) - 6 = 162

    # ── Weapon icons (left side) ─────────────────────────────────────────
    icons_x = panel_x + 10
    icons_y = panel_y + (HUD_PANEL_H - HUD_ICON_H) // 2
    _draw_weapon_icons(
        screen, icons_x, icons_y,
        self._weapon_icons,
        self.player.weapons_inventory,
        self.player.current_weapon,
    )

    # ── Face portrait (center) ────────────────────────────────────────────
    face_cx = panel_x + 10 + icon_area_w + (HUD_PANEL_W - 10 - icon_area_w - 80) // 2
    face_cy = panel_y + HUD_PANEL_H // 2
    face_r  = HUD_FACE_SIZE // 2
    face_state = _get_face_state(self.player.hp, self.player.pain_timer)
    _draw_hud_face(screen, face_cx, face_cy, face_r, face_state)

    # ── HP display (right side) ───────────────────────────────────────────
    hp_val = max(0, int(self.player.hp))
    hp_r   = min(255, max(60, 255 - int((100 - hp_val) * 2)))
    hp_g   = min(255, max(20, int(hp_val * 1.8)))
    hp_color = (hp_r, hp_g, 30)
    hp_text = self.font.render(f"HP {hp_val}", True, hp_color)
    hp_rect = hp_text.get_rect(
        midright=(panel_x + HUD_PANEL_W - 10, panel_y + HUD_PANEL_H // 2)
    )
    screen.blit(hp_text, hp_rect)
```

- **REMOVE**: The old bottom-left `Weapon: ...` text (previously at line 443-447) is gone — the weapon icon strip replaces it
- **KEEP**: The top-left `HP: {x}` text IS removed (HP now in panel). The top-center timer and top-right kills stay.
- **GOTCHA**: `HUD_PANEL_W`, `HUD_PANEL_H`, `HUD_FACE_SIZE`, `HUD_ICON_W`, `HUD_ICON_H` must all be in the `from game.core.constants import (...)` block at top of play.py
- **VALIDATE**: `make lint`

---

### Task 6: CREATE `tests/test_hud.py` — unit tests

- **ACTION**: CREATE `zombie-shooter/tests/test_hud.py`
- **MIRROR**: `tests/test_obstacle.py:1-50` — same structure: `pygame.init()` at top, plain `def test_xxx()` functions, no classes
- **IMPLEMENT**: These tests:

```python
"""Tests for HUD face state logic and player pain timer."""

from __future__ import annotations

import pygame

from game.scenes.play import _get_face_state

pygame.init()


def test_face_state_normal() -> None:
    """HP >= 80 and no pain flash → normal."""
    assert _get_face_state(100.0, 0.0) == "normal"
    assert _get_face_state(80.0, 0.0) == "normal"


def test_face_state_hurt() -> None:
    """HP in [60, 80) → hurt."""
    assert _get_face_state(79.9, 0.0) == "hurt"
    assert _get_face_state(60.0, 0.0) == "hurt"


def test_face_state_injured() -> None:
    """HP in [40, 60) → injured."""
    assert _get_face_state(59.9, 0.0) == "injured"
    assert _get_face_state(40.0, 0.0) == "injured"


def test_face_state_critical() -> None:
    """HP in [20, 40) → critical."""
    assert _get_face_state(39.9, 0.0) == "critical"
    assert _get_face_state(20.0, 0.0) == "critical"


def test_face_state_dying() -> None:
    """HP < 20 → dying."""
    assert _get_face_state(19.9, 0.0) == "dying"
    assert _get_face_state(0.0, 0.0) == "dying"


def test_face_state_pain_flash_overrides_hp() -> None:
    """pain_timer > 0 overrides HP-based state at any HP level."""
    assert _get_face_state(100.0, 0.1) == "pain_flash"
    assert _get_face_state(10.0, 0.01) == "pain_flash"


def test_face_state_no_flash_when_timer_zero() -> None:
    """pain_timer == 0 uses HP-based state."""
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
```

- **IMPORTS needed at top of test file**:
  ```python
  from game.entities.player import Player
  from game.scenes.play import _get_face_state
  ```
- **GOTCHA**: `pygame.init()` must be called before `Player()` because Player loads sprites; add at module level (see `tests/test_obstacle.py:15`)
- **GOTCHA**: `_get_face_state` is a module-level function in `play.py` — it can be imported directly without instantiating PlayScene
- **VALIDATE**: `make test tests/test_hud.py`

---

## Testing Strategy

### Unit Tests to Write

| Test File | Test Cases | Validates |
|-----------|------------|-----------|
| `tests/test_hud.py` | 12 tests covering face states + player pain timer | `_get_face_state()`, `Player.take_damage()`, `pain_timer` lifecycle |

### Edge Cases Checklist

- [x] HP exactly at boundary (80.0 → normal, 79.9 → hurt)
- [x] pain_timer = 0 (no flash)
- [x] pain_timer > 0 at any HP level overrides face state
- [x] take_damage(0) does NOT set pain_timer
- [x] pain_timer decrements in update()
- [ ] HUD panel renders without crash when `weapons_inventory = {"pistol"}` only
- [ ] HUD panel renders without crash when all 3 weapons owned
- [ ] HP color transitions: green at 100, red near 0

---

## Validation Commands

### Level 1: STATIC_ANALYSIS
```bash
make lint
```
**EXPECT**: Exit 0, 0 errors

### Level 2: UNIT_TESTS (new HUD tests)
```bash
cd zombie-shooter && PYTHONPATH=src python -m pytest tests/test_hud.py -v
```
**EXPECT**: 12/12 pass

### Level 3: FULL_SUITE
```bash
make test
```
**EXPECT**: 165/166 pass (12 new + 153 existing; 1 pre-existing failure remains)

### Level 4: MANUAL VALIDATION
```bash
make run
```
Verify visually:
- [ ] Bottom HUD panel visible, centered, dark background
- [ ] 3 weapon icon slots visible; only pistol lit (others grayed)
- [ ] Face shows "normal" at start (HP 100)
- [ ] Pick up shotgun → shotgun icon lights up, becomes highlighted as active
- [ ] Press 1 → pistol icon highlighted, shotgun normal
- [ ] Take zombie damage → face briefly grimaces (pain flash)
- [ ] Let HP drop to ~50 → face shows injured state
- [ ] Let HP drop below 20 → face shows dying state

---

## Acceptance Criteria

- [ ] Bottom center HUD panel rendered with dark background + border
- [ ] Weapon icon strip: grayed when not owned, normal when owned, highlighted border when active
- [ ] Face portrait: 5 HP-based expressions, pain flash overrides for 0.4s on any hit
- [ ] HP color in panel changes from green (full) → red (low)
- [ ] `make lint` exits 0
- [ ] `make test` passes 165/166 (12 new tests pass, 0 regressions)
- [ ] `make run` — visual check passes all manual validation points

---

## Completion Checklist

- [ ] Task 1: constants.py — HUD constants added
- [ ] Task 2: player.py — pain_timer field + take_damage() method
- [ ] Task 3: play.py — 3 damage sites use take_damage()
- [ ] Task 4: play.py — 4 HUD helper functions added at module level
- [ ] Task 5: play.py — _draw_hud() replaced; _weapon_icons in __init__
- [ ] Task 6: tests/test_hud.py — 12 tests written and passing
- [ ] make lint — exits 0
- [ ] make test — 165/166
- [ ] make run — manual visual verification passes

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Line-length lint failures in draw functions | HIGH | LOW | Keep each draw call on its own line; use intermediate variables for long Rect args |
| HUD panel overlaps player near bottom screen edge | LOW | MED | Player start pos is (WIDTH/2, HEIGHT/2); HUD is 88px tall + 4px margin = 92px from bottom; player radius 18px, so player must be within 92px of bottom to overlap — clamp is already `min(HEIGHT - self.radius, ...)` = 702px, HUD top is 636px, so possible overlap. Acceptable — same as Doom |
| `BLEND_RGB_MULT` flag zeroes transparent pixels | MED | LOW | Icon surface uses SRCALPHA; fill() with special_flags only affects RGB channels of non-transparent pixels — test visually |
| Importing `HUD_PAIN_FLASH_DURATION` inside `take_damage()` each call | LOW | LOW | Python caches module imports; no performance hit |

---

## Notes

- **Phase 2 (weapon pickup sprites) is fully independent** — touches only `pickup.py`, can be started in parallel immediately. Run `/prp-plan .claude/PRPs/prds/doom-hud-and-gun-sprites.prd.md` again after this plan is saved to generate the Phase 2 plan.
- The `_WEAPON_ORDER = ("pistol", "shotgun", "smg")` tuple is defined at module level in play.py (not in constants.py) because it's a rendering concern, not a game balance constant.
- `take_damage()` is intentionally minimal — it does NOT clamp `hp` to 0 because `_check_game_over()` handles the death condition, and tests may check exact hp values after damage.
- The HP color formula `hp_r = 255 - (100-hp)*2` gives: 100HP→green (55,255,30), 50HP→yellow (155,140,30), 0HP→red (255,20,30).
