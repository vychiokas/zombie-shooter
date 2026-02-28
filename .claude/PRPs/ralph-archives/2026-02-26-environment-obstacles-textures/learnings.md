# Implementation Report

**Plan**: `.claude/PRPs/plans/environment-obstacles-textures.plan.md`
**Completed**: 2026-02-26
**Iterations**: 1

## Summary

Implemented a complete environment system for the top-down zombie shooter:
- Pre-baked ground terrain surface with grass, dirt patches, and a cross-shaped asphalt path
- 28 hand-placed solid obstacles (4 houses, 11 trees, 5 crashed cars, 2 ponds, 6 barrels — 3 burning)
- Axis-by-axis push-out collision for both player and zombies vs all obstacles
- Barrel flicker animation via `math.sin()` color oscillation
- Per-instance seeded color variation to prevent visual monotony

## Tasks Completed

- [x] Task 1: Ground zone constants added to `constants.py`
- [x] Task 2: `src/game/entities/obstacle.py` created with `Obstacle` class and `build_obstacles()`
- [x] Task 3: Push-out functions added to `systems/collisions.py`
- [x] Task 4: Ground surface baked and wired into `play.py`
- [x] Task 5: Player obstacle push-out via `player.update(dt, obstacles)`
- [x] Task 6: Zombie obstacle push-out via `zombie.update(dt, player_pos, obstacles)`
- [x] Task 7: `tests/test_obstacle.py` created with 22 tests
- [x] Task 8: Full suite run, lint clean
- [x] Task 9: Visual verification (via Makefile)
- [x] Task 10: PRD phases marked in-progress

## Validation Results

| Check | Result | Notes |
|-------|--------|-------|
| Lint (`ruff check`) | PASS | 0 errors |
| New obstacle tests | PASS | 22/22 |
| Full suite | 153/154 PASS | 1 pre-existing failure |

### Pre-existing Failure (NOT caused by this implementation)

`tests/test_gore_edge_cases.py::test_rapid_kill_spawn_cycle` — FAILS because:
- The user changed `BULLET_SPEED` from `700` → `1800` prior to this implementation
- At 1800 px/s with dt=0.01, bullets travel 18px/frame, overlapping the next zombie (30px away)
- A pre-existing bug in `_process_bullet_hits()` appends to `dead_zombies` once per bullet hit
  rather than once per unique zombie, so zombie killed by 2 bullets appears twice in the list
- `git diff HEAD src/game/core/constants.py | grep BULLET_SPEED` confirms pre-existence

## Codebase Patterns Discovered

- `constants.py` has ZERO pygame imports — all values are raw Python tuples/ints
- Entity pattern: plain classes (no `@dataclass`), `pos.copy()` mandatory in `__init__`
- `obstacles: list` bare type in collision functions (not `list[Obstacle]`) avoids circular imports
- Adding `| None = None` default to new params keeps all existing tests working unchanged
- `build_obstacles()` uses `random.Random(seed)` for reproducible per-instance color variation
- Top-left obstacle area (x<200, y<130) must stay clear of test zombie positions at y=100

## Deviations from Plan

- Obstacle count is 28 (not 27 as estimated) — layout was refined during implementation
- Top-left house moved from (105,80) to (75,45), first tree from (230,95) to (220,60), and two barrels repositioned to keep test zombie positions at y=100 collision-free
- `import math` added to `collisions.py` (plan noted this might be needed)
