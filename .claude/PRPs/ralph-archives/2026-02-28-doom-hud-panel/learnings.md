# Implementation Report

**Plan**: `.claude/PRPs/plans/doom-hud-panel.plan.md`
**Completed**: 2026-02-28
**Iterations**: 1

## Summary

Replaced the 4-text-label HUD with a Doom-inspired bottom-center panel (440×88px). Added a reactive procedural face portrait (6 states: normal/hurt/injured/critical/dying/pain_flash) + weapon icon strip (3 slots: gray when locked, normal when owned, gold-bordered when active). Added `take_damage()` to Player for pain flash triggering. All drawing is pure `pygame.draw`.

## Tasks Completed

- [x] Task 1: HUD constants added to `constants.py`
- [x] Task 2: `pain_timer` field + `take_damage()` method in `player.py`
- [x] Task 3: All 3 direct `hp -=` sites in `play.py` changed to `take_damage()`
- [x] Task 4: `_get_face_state`, `_draw_hud_face`, `_build_weapon_icons`, `_draw_weapon_icons` added to `play.py`
- [x] Task 5: `_draw_hud()` replaced; `_weapon_icons` pre-built in `PlayScene.__init__`
- [x] Task 6: `tests/test_hud.py` — 12 tests written and passing

## Validation Results

| Check | Result | Notes |
|-------|--------|-------|
| Lint (`make lint`) | PASS | 0 errors |
| New HUD tests | PASS | 12/12 |
| Full suite (`make test`) | PASS | 165/166 (1 pre-existing failure) |
| Game runs (`make run`) | PASS | No crash |

## Codebase Patterns Discovered

- `pygame.BLEND_RGB_MULT` on SRCALPHA surface: `fill((r,g,b,0), special_flags=...)` multiplies only RGB channels; alpha 0 prevents touching the alpha channel
- Module-level `_WEAPON_ORDER` tuple defined in play.py (not constants.py) — rendering concern, not game balance
- `take_damage()` uses late import `from game.core.constants import HUD_PAIN_FLASH_DURATION` inside method body — same pattern as `GameOverScene` import at play.py:401
- Face state function `_get_face_state` is importable directly from `play` module without instantiating PlayScene — useful for tests

## Deviations from Plan

- `hurt` state: plan used two separate squint lines per eye; implementation used `my` variable for the neutral mouth line (same fix applied as E501 lint fix)
- One E501 lint error caught and fixed: `(cx - r // 4, cy + r // 4)` repeated twice on one line → extracted `my = cy + r // 4`
