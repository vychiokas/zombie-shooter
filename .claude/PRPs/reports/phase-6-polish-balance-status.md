# Phase 6: Visual Polish & Balance - Manual Completion Guide

**Status**: Ready for Manual Playtesting
**PRD**: .claude/PRPs/prds/004_special-zombie-variants.prd.md
**Date**: 2026-02-09

## Summary

All 5 zombie variants (Normal, Runner, Tank, Exploder, Spitter) are fully implemented, tested, and visually distinct. Phase 6 requires **manual playtesting** to validate balance and tune spawn weights. This document provides a checklist for completing Phase 6.

---

## Automated Validation Complete ✅

| Check | Status | Details |
|-------|--------|---------|
| All variants implemented | ✅ COMPLETE | Normal, Runner, Tank, Exploder, Spitter all working |
| Tests passing | ✅ COMPLETE | 118/118 tests (100% pass rate) |
| Linting passing | ✅ COMPLETE | 0 errors, 0 warnings (ruff) |
| Visual distinction | ✅ COMPLETE | Green (normal/spitter), Red (runner), Blue (tank), Orange (exploder) |
| Unique behaviors | ✅ COMPLETE | Speed, HP, ranged, explosion - all distinct |

---

## Manual Playtesting Required ⚠️

### Step 1: Performance Validation

**Goal**: Verify game maintains 60 FPS with all variants active

**How to Test**:
1. Start game: `python zombie-shooter/src/game/main.py`
2. Let game run for full 60 seconds
3. Observe FPS counter (if available) or visual smoothness
4. Check for frame drops when many zombies spawn (~50 zombies)
5. Test with all variants spawning simultaneously

**Success Criteria**:
- [ ] Game maintains smooth 60 FPS throughout session
- [ ] No performance degradation with 50+ zombies
- [ ] Explosions don't cause lag spikes
- [ ] Acid projectiles don't slow down game

**If Performance Issues**:
- Reduce `MAX_ZOMBIES` in constants.py (currently 50)
- Optimize particle counts (reduce EXPLODER_PARTICLE_COUNT)
- Profile with `cProfile` to identify bottlenecks

---

### Step 2: Spawn Weight Balance Testing

**Goal**: Verify spawn mix feels balanced and engaging

**Current Spawn Weights**:
```python
# zombie-shooter/src/game/core/constants.py:66-97
"normal":   weight=7.0   (63.6% spawn rate)
"runner":   weight=1.5   (13.6% spawn rate)
"tank":     weight=1.5   (13.6% spawn rate)
"exploder": weight=1.0   (9.1% spawn rate)
"spitter":  weight=1.0   (9.1% spawn rate)
```

**How to Test**: Play 10+ full sessions (60 seconds each) and observe:
- [ ] Do you see a good mix of all variants?
- [ ] Are there too many specials (overwhelming)?
- [ ] Are there too few specials (boring)?
- [ ] Do certain variants feel over/underpowered?

**Tuning Guidelines**:
- **Too many Runners**: Reduce runner weight (1.5 → 1.0)
- **Too many Tanks**: Reduce tank weight (1.5 → 1.0)
- **Not enough variety**: Reduce normal weight (7.0 → 5.0)
- **Too chaotic**: Increase normal weight (7.0 → 8.0)

**How to Adjust**:
```bash
# Edit constants.py and modify weight values:
vim zombie-shooter/src/game/core/constants.py
# Change ZOMBIE_VARIANTS weights, then test again
```

---

### Step 3: Tactical Depth Validation

**Goal**: Verify player must adapt tactics for different variants

**Test Each Variant**:

**Runner (Fast, 2x speed)**:
- [ ] Forces aim tracking and quick reactions
- [ ] Punishes slow movement
- [ ] Clear visual distinction (red color)

**Tank (Slow, 3 HP)**:
- [ ] Requires focus-fire (3 shots to kill)
- [ ] Creates bullet economy pressure
- [ ] Larger hitbox noticeable (24px radius)
- [ ] Clear visual distinction (blue/gray color)

**Exploder (Explosion on death)**:
- [ ] Player considers positioning before killing
- [ ] Chain reactions occur when Exploders cluster
- [ ] Risk/reward trade-off clear (damage vs crowd control)
- [ ] Clear visual distinction (orange/yellow color)

**Spitter (Ranged attacks)**:
- [ ] Forces target prioritization
- [ ] Projectiles are visible and dodge-able
- [ ] Breaks pure kiting patterns
- [ ] Clear visual distinction (green toxic color)

**Success Criteria**:
- [ ] Each variant requires different tactical response
- [ ] Player must prioritize threats dynamically
- [ ] No "one strategy wins all" patterns emerge
- [ ] Variant mix creates engaging combat

---

### Step 4: Edge Case Testing

**Test Extreme Compositions**:

**All Exploders**:
```python
# Temporarily modify constants.py:
ZOMBIE_VARIANTS = {
    "exploder": {"speed": 140, "hp": 1, "radius": 16, "weight": 10},
    # Set all others to weight: 0
}
```
- [ ] Chain reactions work correctly
- [ ] Game doesn't crash from recursion
- [ ] Performance remains stable

**All Tanks**:
```python
# Temporarily modify constants.py:
ZOMBIE_VARIANTS = {
    "tank": {"speed": 98, "hp": 3, "radius": 24, "weight": 10},
    # Set all others to weight: 0
}
```
- [ ] Bullet economy creates challenge
- [ ] No HP tracking bugs
- [ ] Performance remains stable

**All Spitters**:
```python
# Temporarily modify constants.py:
ZOMBIE_VARIANTS = {
    "spitter": {"speed": 100, "hp": 1, "radius": 16, "weight": 10},
    # Set all others to weight: 0
}
```
- [ ] Projectile spam doesn't crash game
- [ ] Projectiles clean up correctly (TTL)
- [ ] Performance remains stable

**Restore normal weights after testing!**

---

### Step 5: Optional Visual Polish

**Tank Hit Feedback** (optional enhancement):
- Add sprite flash when Tank takes damage but survives
- Or spawn small particle burst on hit
- Helps player track partially-damaged Tanks

**Exploder Warning Pulse** (optional enhancement):
- Add brief pulse/glow 0.5s before explosion
- Gives player warning to move away
- Increases tactical decision window

**Implementation**: These are optional polish features. If balance feels good without them, skip this step.

---

## Final Validation Checklist

Before marking Phase 6 complete:

- [ ] **Performance**: Game maintains 60 FPS with all variants (Step 1)
- [ ] **Balance**: Spawn mix feels engaging (Step 2)
- [ ] **Tactics**: Each variant requires adaptation (Step 3)
- [ ] **Edge Cases**: Extreme compositions don't break game (Step 4)
- [ ] **Tests**: All tests still passing: `pytest zombie-shooter/tests/` (should be 118/118)
- [ ] **Linting**: No errors: `ruff check zombie-shooter/src/`

---

## Completion Report Template

After completing manual testing, create final report:

```markdown
# Phase 6: Visual Polish & Balance - COMPLETE

**Playtesting Sessions**: {number} sessions completed
**Performance**: {FPS observed, any issues?}
**Spawn Balance**: {weights adjusted? final values?}
**Tactical Depth**: {does each variant create different challenges?}
**Edge Cases**: {any issues found?}

## Final Spawn Weights
- Normal: {weight} ({percentage}%)
- Runner: {weight} ({percentage}%)
- Tank: {weight} ({percentage}%)
- Exploder: {weight} ({percentage}%)
- Spitter: {weight} ({percentage}%)

## Recommended Adjustments (if any)
- {List any balance changes needed}

## PRD Status
All 6 phases COMPLETE ✅
```

---

## How to Mark PRD Complete

Once all manual testing is done:

1. **Update PRD status**:
   ```bash
   vim .claude/PRPs/prds/004_special-zombie-variants.prd.md
   # Change Phase 6 status from "pending" to "complete"
   ```

2. **Create final report**:
   ```bash
   vim .claude/PRPs/reports/phase-6-polish-balance-report.md
   # Document playtesting findings and final state
   ```

3. **Celebrate!** 🎉
   All zombie variants implemented, tested, and balanced!

---

## Current Spawn Weights (Baseline)

These are the current spawn weights to use as starting point for tuning:

```python
# Total weight: 7 + 1.5 + 1.5 + 1.0 + 1.0 = 12

ZOMBIE_VARIANTS = {
    "normal": {
        "speed": 140,
        "hp": 1,
        "radius": 16,
        "weight": 7,  # 63.6% (7/11)
    },
    "runner": {
        "speed": 280,
        "hp": 1,
        "radius": 16,
        "weight": 1.5,  # 13.6% (1.5/11)
    },
    "tank": {
        "speed": 98,
        "hp": 3,
        "radius": 24,
        "weight": 1.5,  # 13.6% (1.5/11)
    },
    "exploder": {
        "speed": 140,
        "hp": 1,
        "radius": 16,
        "weight": 1.0,  # 9.1% (1.0/11)
    },
    "spitter": {
        "speed": 100,
        "hp": 1,
        "radius": 16,
        "weight": 1.0,  # 9.1% (1.0/11)
    },
}
```

These weights have been chosen based on:
- **Normal (63.6%)**: Majority should be basic enemies for baseline threat
- **Runner/Tank (13.6% each)**: Moderate spawn rate for tactical variety
- **Exploder/Spitter (9.1% each)**: Lower spawn rate to avoid overwhelming player

**Tuning Philosophy**: Start conservative (lower special weights), increase if gameplay feels too easy/boring.

---

## Quick Start: Play and Observe

**Fastest path to Phase 6 completion**:

1. **Play the game**:
   ```bash
   cd zombie-shooter
   python src/game/main.py
   ```

2. **Observe for 10 sessions**:
   - Do all variants spawn?
   - Is the mix engaging?
   - 60 FPS maintained?
   - Any crashes or bugs?

3. **Adjust weights if needed** (edit constants.py)

4. **Run tests** to ensure no regressions:
   ```bash
   export PYTHONPATH="src"
   pytest tests/ -v
   ```

5. **Mark Phase 6 complete** in PRD

**That's it!** Phase 6 is primarily validation that all the hard work from Phases 1-5 comes together smoothly.
