# Feature: Phase 5 - HUD Integration (Weapon Name Display)

## Summary

Add weapon name display to the game HUD so players can see which weapon they currently have equipped. This enhancement adds a single text line "Weapon: [name]" at the bottom-left of the screen, following the existing HUD rendering pattern used for HP, Timer, and Kills.

## User Story

As a player
I want to see my current weapon name displayed on screen
So that I know which weapon I'm using and can adapt my tactics accordingly

## Problem Statement

Players cannot see which weapon they currently have equipped after picking up weapon pickups. This leads to confusion about why firing behavior changes (shotgun spread vs SMG rapid fire) and requires players to test-fire to identify their weapon.

## Solution Statement

Add a fourth HUD element displaying "Weapon: [weapon_name]" at the bottom-left of the screen. The weapon name (pistol, shotgun, or smg) will be capitalized and rendered in white text using the existing HUD font, updating automatically when the player collects a pickup.

## Metadata

| Field            | Value                                             |
| ---------------- | ------------------------------------------------- |
| Type             | ENHANCEMENT |
| Complexity       | LOW |
| Systems Affected | PlayScene rendering (HUD display) |
| Dependencies     | pygame 2.6.1, Player.current_weapon (Phase 1) |
| Estimated Tasks  | 2 |

---

## UX Design

### Before State
```
╔═══════════════════════════════════════════════════════════════╗
║  GAME SCREEN                                                  ║
║                                                               ║
║  HP: 100        Time: 23.5 / 60         Kills: 15            ║
║                                                               ║
║                        [Player]                               ║
║         [Zombie]                    [Zombie]                  ║
║                   [Pickup]                                    ║
║              [Bullets]                                        ║
║                                                               ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

DATA_FLOW: player.current_weapon exists internally but NOT displayed
PAIN_POINT: Player must test fire to know which weapon equipped
```

### After State
```
╔═══════════════════════════════════════════════════════════════╗
║  GAME SCREEN                                                  ║
║                                                               ║
║  HP: 100        Time: 23.5 / 60         Kills: 15            ║
║                                                               ║
║                        [Player]                               ║
║         [Zombie]                    [Zombie]                  ║
║                   [Pickup]                                    ║
║              [Bullets]                                        ║
║                                                               ║
║  Weapon: Shotgun   ◄──── NEW: Weapon name display            ║
╚═══════════════════════════════════════════════════════════════╝

DATA_FLOW: player.current_weapon → render text → blit to screen
VALUE_ADD: Instant visual feedback on weapon changes
```

### Interaction Changes
| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| Bottom-left HUD | No weapon display | "Weapon: [name]" in white | Player sees equipped weapon |
| Pickup collection | No visual feedback | HUD updates immediately | Confirms weapon swap |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `zombie-shooter/src/game/scenes/play.py` | 179-193 | HUD rendering pattern to MIRROR exactly |
| P1 | `zombie-shooter/src/game/scenes/play.py` | 54 | Font initialization pattern |
| P2 | `zombie-shooter/src/game/scenes/play.py` | 119 | Player.current_weapon access example |

**External Documentation:**
| Source | Section | Why Needed |
|--------|---------|------------|
| [Pygame Font v2.6.1](https://www.pygame.org/docs/ref/font.html#pygame.font.Font.render) | font.render() | Text rendering syntax |
| [Pygame Surface v2.6.1](https://www.pygame.org/docs/ref/surface.html#pygame.Surface.blit) | blit() | Screen positioning |

---

## Patterns to Mirror

**HUD_RENDERING_PATTERN:**
```python
# SOURCE: zombie-shooter/src/game/scenes/play.py:179-191
# COPY THIS PATTERN:

# HUD - HP (top-left)
hp_text = self.font.render(f"HP: {int(self.player.hp)}", True, (255, 255, 255))
screen.blit(hp_text, (10, 10))

# HUD - Timer (top-center)
timer_text = self.font.render(
    f"Time: {self.timer:.1f} / 60", True, (255, 255, 255)
)
timer_rect = timer_text.get_rect(center=(WIDTH // 2, 25))
screen.blit(timer_text, timer_rect)

# HUD - Kills (top-right)
kills_text = self.font.render(f"Kills: {self.kills}", True, (255, 255, 255))
kills_rect = kills_text.get_rect(topright=(WIDTH - 10, 10))
screen.blit(kills_text, kills_rect)
```

**FONT_INITIALIZATION:**
```python
# SOURCE: zombie-shooter/src/game/scenes/play.py:54
# ALREADY EXISTS - REUSE:
self.font = pygame.font.Font(None, 36)
```

**PLAYER_STATE_ACCESS:**
```python
# SOURCE: zombie-shooter/src/game/scenes/play.py:119
# COPY THIS ACCESS PATTERN:
self.player.current_weapon  # Returns "pistol", "shotgun", or "smg"
```

**COLOR_CONVENTION:**
```python
# SOURCE: zombie-shooter/src/game/scenes/play.py:180,183,189
# USE THIS COLOR FOR HUD:
(255, 255, 255)  # White RGB tuple for all HUD text
```

**STRING_FORMATTING:**
```python
# PATTERN: Use f-string with capitalize()
f"Weapon: {self.player.current_weapon.capitalize()}"
# Result: "Weapon: Pistol" or "Weapon: Shotgun" or "Weapon: Smg"
```

---

## Files to Change

| File                             | Action | Justification                            |
| -------------------------------- | ------ | ---------------------------------------- |
| `zombie-shooter/src/game/scenes/play.py` | UPDATE | Add weapon text rendering to draw() method |

---

## NOT Building (Scope Limits)

Explicit exclusions to prevent scope creep:

- **Weapon icons/sprites**: Out of scope - text only per PRD Phase 5
- **Weapon stats display**: Out of scope - name only, not fire rate/damage
- **Colored text per weapon**: Out of scope - consistent white HUD text
- **Center screen positioning**: Out of scope - bottom-left mirrors HP pattern
- **Weapon hotkey display**: Out of scope - pickup-based system only

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: UPDATE `zombie-shooter/src/game/scenes/play.py` - Add weapon HUD display

- **ACTION**: ADD weapon text rendering to PlayScene.draw() method
- **LOCATION**: After kills text rendering (after line 191), before method ends
- **IMPLEMENT**:
  ```python
  # HUD - Weapon (bottom-left)
  weapon_text = self.font.render(
      f"Weapon: {self.player.current_weapon.capitalize()}", True, (255, 255, 255)
  )
  screen.blit(weapon_text, (10, HEIGHT - 50))
  ```
- **MIRROR**: `zombie-shooter/src/game/scenes/play.py:179-181` - follow HP rendering pattern exactly
- **PATTERN**:
  - Use `self.font.render()` (already initialized in __init__)
  - Format string: `f"Weapon: {name}"`
  - Capitalize weapon name: `.capitalize()`
  - Color: `(255, 255, 255)` - white
  - Antialias: `True`
  - Position: `(10, HEIGHT - 50)` - 10px from left, 50px from bottom
- **IMPORTS**: Verify `HEIGHT` is imported (should already be in constants import)
- **GOTCHA**: Must access `self.player.current_weapon` not just `player.current_weapon`
- **VALIDATE**:
  ```bash
  cd zombie-shooter
  PYTHONPATH=src .venv/bin/python -c "import sys; sys.path.insert(0, 'src'); from game.scenes.play import PlayScene; print('✅ PlayScene compiles')"
  ```

### Task 2: RUN manual validation - Verify HUD displays correctly

- **ACTION**: Launch game and verify weapon name appears
- **STEPS**:
  1. Launch game: `cd zombie-shooter && PYTHONPATH=src .venv/bin/python -m game.main`
  2. Check bottom-left corner shows "Weapon: Pistol" (default)
  3. Wait for pickup to spawn (~15 seconds)
  4. Collect pickup (walk over colored rectangle)
  5. Verify HUD updates to show new weapon name
  6. Test all three weapons: Pistol, Shotgun, SMG
  7. Confirm text is white, readable, and doesn't overlap with entities
- **VALIDATE**: All weapon names display correctly on pickup
- **EXPECTED**:
  - Start: "Weapon: Pistol"
  - After red pickup: "Weapon: Shotgun"
  - After cyan pickup: "Weapon: Smg"
  - After yellow pickup: "Weapon: Pistol"

---

## Testing Strategy

### Unit Tests to Write

No new unit tests required - this is a pure rendering change with no business logic.

### Edge Cases Checklist

- [x] Default weapon (pistol) displays on game start
- [x] Weapon name updates immediately on pickup collection
- [x] All three weapon names display correctly (Pistol, Shotgun, Smg)
- [x] Text doesn't overlap with game entities
- [x] Text remains visible throughout 60-second gameplay
- [x] Capitalization works correctly (lowercase "smg" → "Smg")

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
cd zombie-shooter
.venv/bin/ruff format .
.venv/bin/ruff check .
```

**EXPECT**: Exit 0, no errors or warnings

### Level 2: COMPILATION_CHECK

```bash
cd zombie-shooter
PYTHONPATH=src .venv/bin/python -c "import sys; sys.path.insert(0, 'src'); from game.scenes.play import PlayScene; print('✅ Compiles')"
```

**EXPECT**: "✅ Compiles" printed, no import errors

### Level 3: EXISTING_TESTS

```bash
cd zombie-shooter
PYTHONPATH=src .venv/bin/pytest tests -q
```

**EXPECT**: All existing tests pass (27 tests from previous phases)

### Level 4: MANUAL_GAME_LAUNCH

```bash
cd zombie-shooter
PYTHONPATH=src .venv/bin/python -m game.main
```

**EXPECT**: Game launches, HUD shows "Weapon: Pistol" at bottom-left

### Level 5: MANUAL_WEAPON_SWAP_TEST

**Steps**:
1. Launch game (Level 4 command)
2. Observe "Weapon: Pistol" at bottom-left
3. Wait for pickup spawn (~15 seconds)
4. Collect red rectangle (shotgun)
5. Observe HUD changes to "Weapon: Shotgun"
6. Test fire - verify 5-bullet spread matches weapon display
7. Collect cyan rectangle (SMG)
8. Observe HUD changes to "Weapon: Smg"
9. Test fire - verify rapid fire matches weapon display

**EXPECT**: HUD updates match weapon behavior

---

## Acceptance Criteria

- [ ] Weapon name displays at bottom-left in white text
- [ ] Format is "Weapon: [Name]" with capitalized weapon name
- [ ] Default weapon "Pistol" shows on game start
- [ ] HUD updates immediately when player collects pickup
- [ ] All three weapons display correctly (Pistol, Shotgun, Smg)
- [ ] Text doesn't overlap with game entities
- [ ] Level 1-3 validation commands pass with exit 0
- [ ] No regressions in existing 27 tests
- [ ] Manual testing confirms HUD updates match weapon behavior

---

## Completion Checklist

- [ ] Task 1: Weapon text rendering added to PlayScene.draw()
- [ ] Task 2: Manual validation completed successfully
- [ ] Level 1: ruff format + check passes
- [ ] Level 2: Compilation check passes
- [ ] Level 3: Existing test suite passes (27 tests)
- [ ] Level 4: Game launches successfully
- [ ] Level 5: Manual weapon swap test passes
- [ ] All acceptance criteria met
- [ ] No visual artifacts or overlapping text

---

## Risks and Mitigations

| Risk               | Likelihood   | Impact       | Mitigation                              |
| ------------------ | ------------ | ------------ | --------------------------------------- |
| Text overlaps with entities at bottom | LOW | LOW | Position at (10, HEIGHT - 50) with 50px margin |
| Capitalization looks wrong for "SMG" | LOW | LOW | Acceptable - "Smg" matches Python .capitalize() behavior |
| Text not visible on dark background | LOW | LOW | White (255,255,255) has high contrast vs dark gray (40,40,40) |

---

## Notes

**Design Decision**: Bottom-left positioning chosen to mirror HP display pattern and avoid center-screen obstruction during gameplay. This creates visual symmetry: HP (top-left) and Weapon (bottom-left).

**Capitalization**: Using Python's built-in `.capitalize()` method results in "Smg" not "SMG". This is acceptable for MVP and can be enhanced later with a weapon display name mapping if needed.

**Performance**: Adding one text render per frame is negligible - existing HUD already renders 3 text elements with no performance impact.

**Future Enhancement**: Could add weapon-colored text (yellow for pistol, red for shotgun, cyan for SMG) to match pickup colors, but this is explicitly out of scope for Phase 5.
