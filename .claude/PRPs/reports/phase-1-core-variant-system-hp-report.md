# Implementation Report: Phase 1 - Core Zombie Variant System & HP

**Plan**: `.claude/PRPs/plans/phase-1-core-variant-system-hp.plan.md`
**Completed**: 2026-02-09T21:25:00Z
**Iterations**: 1

## Summary

Successfully implemented the foundation for zombie variant differentiation by adding ZOMBIE_VARIANTS dictionary (mirroring WEAPON_STATS pattern), implementing HP system for zombies (copying player HP pattern), refactoring collision handling from instant-kill to HP-reduction, and adding weighted random variant selection to spawner. Phase 1 enables zombies with different speeds (Runner 2x, Tank 0.7x) and durability (Tank requires 3 hits), setting foundation for visual variants in Phase 2-5.

## Tasks Completed

- ✅ Task 1: Added ZOMBIE_VARIANTS dict to constants.py with 5 variants (normal/runner/tank/exploder/spitter with speed/hp/radius/weight)
- ✅ Task 2: Modified Zombie.__init__() to accept variant parameter, added self.hp attribute (float type), load variant-specific stats
- ✅ Task 3: Added Spawner.get_spawn_variant() method using random.choices() with weights
- ✅ Task 4: Updated PlayScene zombie creation to pass variant from spawner (lines 135-138)
- ✅ Task 5: Refactored bullet collision handler to reduce zombie HP and only spawn gore/remove on death (lines 175-189)
- ✅ Cleanup: Removed unused imports (ZOMBIE_RADIUS, ZOMBIE_SPEED) from zombie.py

## Validation Results

| Check | Result | Details |
|-------|--------|---------|
| Ruff check | ✅ PASS | All checks passed (after removing unused imports) |
| Type check (mypy) | ⏭️ SKIPPED | Not installed in venv |
| Unit tests | ✅ PASS | 94/94 tests passed in 0.53s |
| Variant distribution | ✅ PASS | 68.3% normal, 14.9% runner, 16.8% tank (over 1000 spawns) |
| Tank HP validation | ✅ PASS | Survives 2 hits, dies on 3rd hit as expected |

## Codebase Patterns Discovered

- **WEAPON_STATS dict pattern**: Perfect template for ZOMBIE_VARIANTS - same structure (dict[str, dict[str, float]]) worked flawlessly
- **Player HP system pattern**: Copying `self.hp = float(PLAYER_MAX_HP)` pattern to zombies worked correctly with damage reduction logic
- **Module-level sprite caching**: Existing `_zombie_sprites` global pattern continues to work with variant system (no changes needed)
- **Type annotations**: `dict[str, dict[str, int | float]]` union type handles mixed int/float values in variant stats
- **random.choices() with weights**: Returns list, requires [0] index to extract single element

## Learnings

### What Worked Well
1. **Pattern mirroring strategy**: WEAPON_STATS dict provided exact blueprint for ZOMBIE_VARIANTS, reducing implementation risk
2. **HP system integration**: Player HP pattern (float type, damage reduction, death check `<= 0`) transferred seamlessly to zombies
3. **Weighted spawning**: random.choices() with weights [7, 1.5, 1.5] produced desired 70/15/15 distribution without tuning
4. **Gore system preservation**: Deferred gore effects (blood splash, corpses, decals) until `hp <= 0` maintained existing visual quality
5. **Clean refactoring**: Changes isolated to 4 files with clear integration points, no unexpected side effects

### Gotchas Encountered
1. **Unused imports**: Initially imported ZOMBIE_RADIUS and ZOMBIE_SPEED but they became unused after variant system - ruff caught this
2. **random.choices() vs random.choice()**: Must use choices (with 's') for weighted selection, returns list not single value

### Performance Notes
- All tests passed (94/94) in 0.53s - no performance regression
- Variant distribution over 1000 spawns completed in <1s - negligible overhead
- HP reduction logic (`zombie.hp -= 1, check hp <= 0`) adds minimal computation

## Deviations from Plan

None - all tasks completed as specified in plan.

## Next Steps

**Phase 1 Complete** ✅ - Variant infrastructure ready.

**Ready for Phase 2-5** (can run in parallel):
- Phase 2: Runner variant (unique sprites, fast movement)
- Phase 3: Tank variant (unique sprites, slow movement, visual hit feedback)
- Phase 4: Exploder variant (explosion on death, AOE damage)
- Phase 5: Spitter variant (ranged acid projectile attacks)

To continue:
```bash
# Option 1: Implement next sequential phase
/prp-plan .claude/PRPs/prds/004_special-zombie-variants.prd.md

# Option 2: Run Phases 2+3 in parallel (separate worktrees)
git worktree add -b phase-2-runner ../zombie-shooter-phase-2 main
cd ../zombie-shooter-phase-2 && /prp-plan .claude/PRPs/prds/004_special-zombie-variants.prd.md
```

## Files Changed

- `src/game/core/constants.py`: Added ZOMBIE_VARIANTS dict (lines 55-88)
- `src/game/entities/zombie.py`: Added variant parameter to __init__, added self.hp, load variant stats (lines 7-14, 38-50)
- `src/game/systems/spawner.py`: Added get_spawn_variant() method (lines 72-81)
- `src/game/scenes/play.py`: Pass variant to Zombie(), refactor collision to HP reduction (lines 135-138, 175-189)

## Git Status

Modified files ready for commit:
```
M src/game/core/constants.py
M src/game/entities/zombie.py
M src/game/systems/spawner.py
M src/game/scenes/play.py
```

Suggested commit message:
```
feat(zombies): implement core variant system with HP tracking

Add ZOMBIE_VARIANTS dict with 5 types (normal/runner/tank/exploder/spitter)
- Zombies now spawn with variant-specific speed, HP, and radius
- Weighted random spawning (70% normal, 15% runner, 15% tank)
- Refactor collision to HP reduction instead of instant kill
- Tank zombies require 3 hits to kill (HP=3)
- Runner zombies move 2x faster (speed=280)

Phase 1 of Special Zombie Variants PRD complete.
Foundation ready for visual variants (Phase 2-5).

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```
