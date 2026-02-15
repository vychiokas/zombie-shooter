# Feature: Phase 5 - Gore System Testing & Polish

## Summary

Validate the complete gore system (blood particles, corpses, blood pools) through comprehensive testing, performance verification, and visual polish. This phase ensures the gore integration from Phase 4 works correctly, maintains 60 FPS with 50+ zombies, has accurate 10-second TTL timers, correct rendering order, and provides satisfying visceral feedback. Includes unit tests for edge cases, integration validation, manual playtesting, and minor visual/timing adjustments.

## User Story

As a developer/player
I want to verify the gore system works correctly and feels satisfying
So that zombie kills provide visceral visual feedback without bugs or performance issues

## Problem Statement

The gore system (Phases 1-4) has been implemented but needs validation to ensure: (1) all three gore entities (blood particles, corpses, blood pools) spawn correctly on kills, (2) 10-second persistence timers are accurate, (3) rendering layering is correct (pools under corpses under living zombies), (4) performance maintains 60 FPS with high entity counts, (5) visual feedback feels satisfying and visceral, (6) no regressions in existing gameplay.

## Solution Statement

Create comprehensive test coverage for gore entity edge cases, integration tests for PlayScene gore spawning/cleanup, manual playtesting procedures, performance benchmarking with FPS monitoring, visual tuning based on playtesting feedback, and validation that all success metrics from the PRD are met. This ensures production-readiness and confirms the hypothesis that gore effects create visceral satisfaction.

## Metadata

| Field            | Value                                             |
| ---------------- | ------------------------------------------------- |
| Type             | ENHANCEMENT                                       |
| Complexity       | LOW                                               |
| Systems Affected | Gore entities, PlayScene, Test suite             |
| Dependencies     | pytest (existing), pygame (existing)              |
| Estimated Tasks  | 8                                                 |

---

## UX Design

### Before State
```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌────────────────┐                                                         ║
║   │  Implemented   │  ──────► No validation yet                              ║
║   │  Gore System   │          (Phases 1-4 complete)                           ║
║   │  (Phase 4)     │                                                          ║
║   └────────────────┘                                                         ║
║                                                                               ║
║   STATUS: Gore integration complete but untested for:                         ║
║   - Edge cases (multiple simultaneous kills, max entities)                    ║
║   - Performance (FPS with 50+ zombies)                                        ║
║   - Timer accuracy (10-second persistence)                                    ║
║   - Rendering order (visual layering)                                         ║
║   - Visual satisfaction (subjective feel)                                     ║
║                                                                               ║
║   RISK: Bugs or performance issues may exist undetected                       ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌────────────────┐         ┌──────────────┐         ┌──────────────┐       ║
║   │  Gore System   │ ──────► │  Validated   │ ──────► │ Production-  │       ║
║   │  (Phase 4)     │         │  & Tested    │         │   Ready      │       ║
║   └────────────────┘         └──────────────┘         └──────────────┘       ║
║                                      │                         │              ║
║                                      ▼                         ▼              ║
║                              ┌───────────────┐       ┌──────────────┐        ║
║                              │ Test Coverage │       │   Polished   │        ║
║                              │ Edge Cases    │       │    Visuals   │        ║
║                              │ Performance   │       │   & Timing   │        ║
║                              └───────────────┘       └──────────────┘        ║
║                                                                               ║
║   STATUS: Gore system validated for:                                          ║
║   ✅ Edge cases tested (simultaneous kills, entity limits)                    ║
║   ✅ Performance verified (60 FPS with 50+ zombies)                           ║
║   ✅ Timer accuracy confirmed (10.0s ±0.5s)                                   ║
║   ✅ Rendering order correct (decals → corpses → zombies → particles)        ║
║   ✅ Visual satisfaction validated (feels visceral and satisfying)            ║
║   ✅ All existing tests passing (no regressions)                              ║
║                                                                               ║
║   VALUE: Confidence in production deployment, no surprises                    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes
| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| Codebase confidence | Gore system integrated but not validated | Gore system tested and production-ready | Developer can deploy confidently |
| Kill feedback | Implemented but not verified for bugs | Validated correct spawning, cleanup, layering | Player gets consistent, bug-free gore effects |
| Performance | Unknown if 60 FPS maintained with gore | Verified 60 FPS with 50+ zombies + gore | Smooth gameplay guaranteed |
| Visual polish | Gore effects at default parameters | Tuned for optimal visual satisfaction | Enhanced visceral impact |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `zombie-shooter/tests/test_blood_particle.py` | all | Existing gore entity test patterns to MIRROR |
| P0 | `zombie-shooter/tests/test_dead_zombie.py` | all | TTL countdown test patterns to FOLLOW |
| P0 | `zombie-shooter/tests/test_blood_decal.py` | all | Entity lifecycle test patterns to COPY |
| P1 | `zombie-shooter/tests/test_zombie_integration.py` | all | Integration test patterns for multi-system validation |
| P1 | `zombie-shooter/tests/test_pickup_spawning.py` | all | Scene integration patterns (PlayScene entity management) |
| P1 | `zombie-shooter/tests/test_animation.py` | 73-107 | Timing precision test patterns (frame cycling, dt accuracy) |
| P2 | `zombie-shooter/src/game/scenes/play.py` | 207-264 | Draw order to VALIDATE (rendering layers) |
| P2 | `zombie-shooter/src/game/core/constants.py` | 1-72 | Gore constants to VERIFY (CORPSE_PERSISTENCE, BLOOD_PARTICLE_LIFETIME) |

**External Documentation:**
| Source | Section | Why Needed |
|--------|---------|------------|
| N/A | N/A | All patterns established in existing codebase |

---

## Patterns to Mirror

**INITIALIZATION_TEST_PATTERN:**
```python
// SOURCE: zombie-shooter/tests/test_blood_particle.py:13-24
// COPY THIS PATTERN:
def test_blood_particle_initialization() -> None:
    """Test that BloodParticle initializes with correct attributes."""
    pos = pygame.Vector2(100, 200)
    vel = pygame.Vector2(50, -30)

    particle = BloodParticle(pos, vel)

    assert particle.pos.x == 100
    assert particle.pos.y == 200
    assert particle.vel.x == 50
    assert particle.vel.y == -30
    assert particle.lifetime > 0
    assert particle.radius == 3
    assert particle.is_alive() is True
```

**TTL_COUNTDOWN_TEST_PATTERN:**
```python
// SOURCE: zombie-shooter/tests/test_dead_zombie.py:26-34
// COPY THIS PATTERN:
def test_dead_zombie_update_decreases_lifetime() -> None:
    """Test that update() decreases lifetime."""
    corpse = DeadZombie(pygame.Vector2(0, 0))
    initial_lifetime = corpse.lifetime

    is_alive = corpse.update(0.2)

    assert corpse.lifetime == initial_lifetime - 0.2
    assert is_alive is True
```

**TIMING_PRECISION_TEST_PATTERN:**
```python
// SOURCE: zombie-shooter/tests/test_animation.py:73-98
// COPY THIS PATTERN:
def test_animation_cycles_frames_with_time() -> None:
    """Test that frames advance based on frame duration."""
    anim = Animation(frame_count=4, fps=10)  # 0.1s per frame
    velocity = pygame.Vector2(100, 0)

    # Start at frame 0
    assert anim.get_current_frame_index() == 0

    # Advance 0.05s - not enough to change frame
    anim.update(0.05, velocity)
    assert anim.get_current_frame_index() == 0

    # Advance another 0.05s - total 0.1s, should advance to frame 1
    anim.update(0.05, velocity)
    assert anim.get_current_frame_index() == 1
```

**SCENE_INTEGRATION_TEST_PATTERN:**
```python
// SOURCE: zombie-shooter/tests/test_pickup_spawning.py:11-17
// COPY THIS PATTERN:
def test_play_scene_initializes_pickups() -> None:
    """Test that PlayScene initializes with empty pickups list."""
    game = MagicMock()  # Mock game instance
    scene = PlayScene(game)
    assert scene.pickups == []
    assert scene.pickup_spawn_timer == 0.0
```

**DRAW_SAFETY_TEST_PATTERN:**
```python
// SOURCE: zombie-shooter/tests/test_blood_particle.py:80-84
// COPY THIS PATTERN:
def test_blood_particle_draw_no_error() -> None:
    """Test that draw() executes without errors."""
    particle = BloodParticle(pygame.Vector2(100, 100), pygame.Vector2(0, 0))
    screen = pygame.Surface((800, 600))

    particle.draw(screen)  # Should not raise exception
```

**EDGE_CASE_TEST_PATTERN:**
```python
// SOURCE: zombie-shooter/tests/test_weapon_behavior.py:95-109
// COPY THIS PATTERN:
def test_pistol_single_shot_on_cooldown() -> None:
    """Test that weapons respect cooldown."""
    player = Player(pygame.Vector2(100, 100))
    target = pygame.Vector2(200, 200)

    # First shot should work
    bullets = player.shoot(target)
    assert len(bullets) == 1

    # Second shot immediately should fail (on cooldown)
    bullets = player.shoot(target)
    assert len(bullets) == 0
```

---

## Files to Change

| File                                      | Action | Justification                            |
| ----------------------------------------- | ------ | ---------------------------------------- |
| `tests/test_gore_integration.py`          | CREATE | Integration tests for PlayScene gore spawning/cleanup |
| `tests/test_gore_edge_cases.py`           | CREATE | Edge case tests (simultaneous kills, entity limits) |
| `tests/test_gore_timing.py`               | CREATE | Timing precision tests for TTL accuracy |
| `src/game/core/constants.py`              | UPDATE | Minor tuning if needed (optional based on playtesting) |

---

## NOT Building (Scope Limits)

Explicit exclusions to prevent scope creep:

- **Automated FPS benchmarking** - Manual observation sufficient for MVP
- **Visual regression testing** - No snapshot/image comparison framework
- **Sound effect testing** - Gore is visual-only per PRD
- **Performance profiling tools** - Simple FPS observation via manual testing
- **Automated playtesting bot** - Manual playtesting sufficient
- **Gore effect variations** - No weapon-specific gore per PRD
- **Blood pool stacking limits** - Not required per PRD Phase 5 scope

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: CREATE `tests/test_gore_integration.py`

- **ACTION**: CREATE integration tests for PlayScene gore system
- **IMPLEMENT**: Test gore entity spawning on zombie kill, cleanup after TTL, entity list management
- **MIRROR**: `tests/test_pickup_spawning.py:1-139` - Scene integration pattern with MagicMock
- **TESTS**:
  - `test_play_scene_initializes_gore_lists()` - Verify empty blood_particles, dead_zombies, blood_decals lists
  - `test_gore_spawns_on_zombie_kill()` - Kill zombie, verify 1 blood decal + 1 dead zombie + N blood particles spawned
  - `test_gore_entities_cleanup_after_ttl()` - Fast-forward time, verify entities removed after CORPSE_PERSISTENCE seconds
  - `test_multiple_simultaneous_kills()` - Kill 5 zombies in same frame, verify 5 decals + 5 corpses + N particles
- **IMPORTS**: `from unittest.mock import MagicMock`, `from game.scenes.play import PlayScene`
- **GOTCHA**: Use `scene.pickup_spawn_timer = 0.0` to prevent unwanted pickups during test
- **VALIDATE**: `PYTHONPATH=zombie-shooter/src .venv/bin/pytest tests/test_gore_integration.py -v`

### Task 2: CREATE `tests/test_gore_edge_cases.py`

- **ACTION**: CREATE edge case tests for gore system boundary conditions
- **IMPLEMENT**: Empty collection handling, max entity scenarios, rapid spawn/despawn cycles
- **MIRROR**: `tests/test_collisions.py:1-62` - Edge case coverage pattern
- **TESTS**:
  - `test_gore_update_with_empty_lists()` - Update PlayScene with no gore entities, no errors
  - `test_gore_draw_with_empty_lists()` - Draw PlayScene with no gore entities, no errors
  - `test_multiple_corpses_at_same_position()` - Kill 3 zombies at identical position, verify no overlap bugs
  - `test_rapid_kill_spawn_cycle()` - Kill 10 zombies in 0.1s, verify correct entity counts
  - `test_gore_entities_beyond_ttl()` - Manually set lifetime to negative, verify safe removal
- **VALIDATE**: `PYTHONPATH=zombie-shooter/src .venv/bin/pytest tests/test_gore_edge_cases.py -v`

### Task 3: CREATE `tests/test_gore_timing.py`

- **ACTION**: CREATE timing precision tests for TTL accuracy
- **IMPLEMENT**: Verify CORPSE_PERSISTENCE (10.0s), BLOOD_PARTICLE_LIFETIME (0.8s) accuracy within ±0.05s
- **MIRROR**: `tests/test_animation.py:73-107` - Incremental dt timing pattern
- **TESTS**:
  - `test_corpse_ttl_accuracy()` - Update corpse 100 times with dt=0.1s, verify removal at 10.0s ±0.05s
  - `test_blood_decal_ttl_accuracy()` - Update decal 100 times with dt=0.1s, verify removal at 10.0s ±0.05s
  - `test_blood_particle_ttl_accuracy()` - Update particle 8 times with dt=0.1s, verify removal at 0.8s ±0.05s
  - `test_gore_ttl_synchronized()` - Kill zombie, verify corpse and decal have identical lifetime values
- **VALIDATE**: `PYTHONPATH=zombie-shooter/src .venv/bin/pytest tests/test_gore_timing.py -v`

### Task 4: Run full test suite validation

- **ACTION**: VALIDATE no regressions in existing 81 tests
- **IMPLEMENT**: Run pytest on all tests, verify all pass
- **VALIDATE**: `PYTHONPATH=zombie-shooter/src .venv/bin/pytest tests/ -v`
- **EXPECT**: All 81+ tests passing (81 existing + new gore tests)
- **GOTCHA**: If any existing tests fail, investigate before proceeding

### Task 5: Manual playtesting - Gore spawning validation

- **ACTION**: MANUAL TEST - Launch game, kill 10+ zombies, observe gore effects
- **PROCEDURE**:
  1. Launch game: `PYTHONPATH=zombie-shooter/src .venv/bin/python -m game.main`
  2. Start PlayScene (click "Start")
  3. Kill 10 zombies (shoot until 10 kills registered in HUD)
  4. Observe for each kill:
     - ✅ Blood particles spray outward (8 red dots)
     - ✅ Blood pool appears at death position (dark red ellipse)
     - ✅ Corpse appears at death position (rotated zombie sprite)
  5. Visual layer order check:
     - ✅ Blood pool underneath corpse (visible as corpse rests on pool)
     - ✅ Corpse underneath living zombies (living zombies walk over corpses)
     - ✅ Blood particles fly over everything
- **VALIDATE**: All 5 checkmarks observed, gore spawns consistently
- **DOCUMENT**: Note any visual glitches, missing effects, or layering issues

### Task 6: Manual playtesting - Timer accuracy validation

- **ACTION**: MANUAL TEST - Verify 10-second persistence timer
- **PROCEDURE**:
  1. Kill a single zombie
  2. Start timer (use phone/stopwatch)
  3. Observe when corpse + blood pool disappear
  4. Record time
  5. Repeat for 3 more kills, average the times
- **VALIDATE**: Average time = 10.0s ±0.5s (9.5s - 10.5s acceptable)
- **DOCUMENT**: Record actual times (e.g., "9.8s, 10.1s, 10.2s, 9.9s → avg 10.0s")

### Task 7: Manual playtesting - Performance validation

- **ACTION**: MANUAL TEST - Verify 60 FPS with high entity count
- **PROCEDURE**:
  1. Survive 30+ seconds (many zombies spawned)
  2. Kill 10+ zombies rapidly (create 10 corpses + 10 pools + 80 particles)
  3. Observe for frame drops, stuttering, lag
  4. Move around battlefield with all gore entities visible
- **VALIDATE**:
  - ✅ No visible frame drops or stuttering
  - ✅ Game feels smooth (subjective but important)
  - ✅ Movement responsive with 20+ entities on screen
- **DOCUMENT**: Note any performance issues, FPS drops, or lag

### Task 8: Visual tuning (OPTIONAL - only if playtesting reveals issues)

- **ACTION**: UPDATE constants if visual feedback unsatisfying
- **TUNING OPTIONS** (only adjust if needed):
  - `BLOOD_PARTICLE_COUNT` - Increase if splash feels weak (try 10-12)
  - `BLOOD_PARTICLE_SPEED` - Increase if splash feels slow (try 180-200)
  - `BLOOD_POOL_SIZE` - Increase if pool too small (try 32-36)
  - `CORPSE_PERSISTENCE` - Decrease if battlefield too cluttered (try 8.0s)
- **MIRROR**: `src/game/core/constants.py:1-72` - Constant definition pattern
- **VALIDATE**: Re-run manual playtest after each adjustment
- **GOTCHA**: Only change if playtesting feedback demands it (don't over-tune)

---

## Testing Strategy

### Unit Tests to Write

| Test File                                | Test Cases                 | Validates      |
| ---------------------------------------- | -------------------------- | -------------- |
| `tests/test_gore_integration.py` | Scene initialization, spawning, cleanup, multi-kill | PlayScene gore lifecycle |
| `tests/test_gore_edge_cases.py`  | Empty lists, same position, rapid cycles, negative TTL | Boundary conditions |
| `tests/test_gore_timing.py` | TTL accuracy for corpse, decal, particle, synchronization | Timer precision |

### Edge Cases Checklist

- [x] Empty gore entity lists (no crashes on update/draw)
- [x] Multiple corpses at same position (no visual artifacts)
- [x] Rapid simultaneous kills (correct entity counts)
- [x] Negative lifetime values (safe removal)
- [x] Gore entities beyond TTL (cleanup works)
- [x] Zero dt update (no division by zero)

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
.venv/bin/ruff check zombie-shooter/tests/test_gore_*.py
```

**EXPECT**: Exit 0, no errors or warnings

### Level 2: UNIT_TESTS (New Gore Tests)

```bash
PYTHONPATH=zombie-shooter/src .venv/bin/pytest zombie-shooter/tests/test_gore_integration.py -v
PYTHONPATH=zombie-shooter/src .venv/bin/pytest zombie-shooter/tests/test_gore_edge_cases.py -v
PYTHONPATH=zombie-shooter/src .venv/bin/pytest zombie-shooter/tests/test_gore_timing.py -v
```

**EXPECT**: All new tests pass

### Level 3: FULL_SUITE (Regression Check)

```bash
PYTHONPATH=zombie-shooter/src .venv/bin/pytest zombie-shooter/tests/ -v
```

**EXPECT**: All 81+ tests pass (no regressions)

### Level 4: MANUAL_VALIDATION (Playtesting)

**Task 5: Gore Spawning**
```bash
PYTHONPATH=zombie-shooter/src .venv/bin/python -m game.main
# Kill 10 zombies, observe blood particles + pools + corpses
```

**Task 6: Timer Accuracy**
```bash
# Kill zombie, time with stopwatch until corpse/pool disappear
# Target: 10.0s ±0.5s
```

**Task 7: Performance**
```bash
# Survive 30s, kill 10+ rapidly, observe for frame drops
# Target: Smooth 60 FPS, no stuttering
```

---

## Acceptance Criteria

- [x] Integration tests cover PlayScene gore spawning/cleanup
- [x] Edge case tests cover boundary conditions
- [x] Timing tests verify TTL accuracy within ±0.05s
- [x] All existing tests pass (no regressions)
- [x] Manual playtesting confirms gore spawns on every kill
- [x] Manual playtesting confirms 10-second timer accuracy (±0.5s)
- [x] Manual playtesting confirms 60 FPS maintained with high entity count
- [x] Rendering layer order visually correct (decals → corpses → zombies → particles)
- [x] Gore effects feel visceral and satisfying (subjective but validated)

---

## Completion Checklist

- [ ] Task 1: `test_gore_integration.py` created with 4 tests
- [ ] Task 2: `test_gore_edge_cases.py` created with 5 tests
- [ ] Task 3: `test_gore_timing.py` created with 4 tests
- [ ] Task 4: Full test suite passes (81+ tests)
- [ ] Task 5: Manual playtest - Gore spawning validated
- [ ] Task 6: Manual playtest - Timer accuracy validated (10.0s ±0.5s)
- [ ] Task 7: Manual playtest - Performance validated (60 FPS)
- [ ] Task 8: Visual tuning complete (if needed)
- [ ] All acceptance criteria met
- [ ] PRD Phase 5 marked as complete
- [ ] Implementation report created

---

## Risks and Mitigations

| Risk               | Likelihood   | Impact       | Mitigation                              |
| ------------------ | ------------ | ------------ | --------------------------------------- |
| Test flakiness due to timing precision | Medium | Low | Use tolerance ranges (±0.05s) instead of exact equality |
| Manual playtest subjectivity (visual satisfaction) | Medium | Low | Use objective criteria (spawns on every kill, correct layering) + subjective "feels good" |
| Performance varies by system | Low | Medium | Test on development machine, document specs if issues arise |
| Edge cases missed | Low | Low | Cover common boundaries (empty, max, negative, zero) |
| Existing tests break during refactor | Very Low | Medium | Run full suite after each change, fix regressions immediately |

---

## Notes

**Phase 5 Focus:** This phase is about VALIDATION and POLISH, not new feature development. All gore entities (BloodParticle, DeadZombie, BloodDecal) and integration (PlayScene) were completed in Phases 1-4. Phase 5 confirms everything works correctly, performs well, and feels satisfying.

**Testing Philosophy:** Combination of automated unit/integration tests (repeatability, fast feedback) and manual playtesting (visual/performance validation, subjective feel). Automated tests catch regressions and bugs; manual tests validate user experience.

**Visual Tuning:** Only adjust constants (Task 8) if playtesting reveals issues. Don't over-optimize or change values speculatively. Trust the initial design (BLOOD_PARTICLE_COUNT=8, CORPSE_PERSISTENCE=10.0s, etc.) unless feedback demands changes.

**Success Metrics Validation:** This phase directly validates PRD success metrics:
- Blood splash visual feedback: 100% of kills (Task 5)
- Corpse persistence: 10 seconds ±0.5s (Task 6)
- Blood pool appearance: 100% of kills (Task 5)
- Performance stability: 60 FPS maintained (Task 7)
- Visual satisfaction: Subjective "feels good" (Tasks 5-7)

**After Phase 5:** Gore system is production-ready. All PRD phases complete (1-5). Next steps could include: additional polish passes, gore sound effects (out of scope per PRD), weapon-specific gore variations (out of scope per PRD), or moving to next PRD feature.
