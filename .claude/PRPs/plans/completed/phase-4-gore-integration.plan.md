# Feature: Gore Integration (Wire All Gore Systems)

## Summary

Integrate DeadZombie and BloodDecal entities into PlayScene's collision handler, update loop, and draw loop to complete the gore system. Blood particles are already wired from Phase 1, so this phase adds corpse and blood pool spawning on zombie death, updates their TTL counters, and establishes correct rendering order (blood decals → dead zombies → live zombies → blood particles) to create the complete DOOM-style gore experience.

## User Story

As a player
I want to see complete gore effects when I kill zombies (blood splash + corpse + blood pool)
So that I feel visceral satisfaction and see impactful visual feedback for my actions

## Problem Statement

Gore entities (BloodParticle, DeadZombie, BloodDecal) exist and are tested, but only BloodParticle is integrated. When zombies die, blood particles spray but corpses and blood pools don't appear, reducing the gore impact. The complete gore system needs all three entities spawned, updated, and rendered in correct order.

## Solution Statement

Add `dead_zombies` and `blood_decals` entity lists to PlayScene.__init__(), modify the collision handler to spawn DeadZombie and BloodDecal alongside existing BloodParticle spawning, add update loops for both new entity types, and reorganize the draw() method to render in correct order: blood decals first (underneath), then dead zombies, then live zombies, then blood particles on top.

## Metadata

| Field            | Value                                             |
| ---------------- | ------------------------------------------------- |
| Type             | ENHANCEMENT                                       |
| Complexity       | MEDIUM                                            |
| Systems Affected | PlayScene (collision, update, draw)               |
| Dependencies     | pygame, BloodParticle, DeadZombie, BloodDecal     |
| Estimated Tasks  | 5                                                 |

---

## UX Design

### Before State
```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌─────────────┐         ┌─────────────┐         ┌─────────────┐            ║
║   │   Player    │ ──────► │   Shoots    │ ──────► │   Zombie    │            ║
║   │   Shoots    │         │   Zombie    │         │   Dies      │            ║
║   └─────────────┘         └─────────────┘         └─────────────┘            ║
║                                                           │                   ║
║                                                           ▼                   ║
║                                                  ┌─────────────┐              ║
║                                                  │ Blood spray │              ║
║                                                  │   (0.8s)    │              ║
║                                                  └─────────────┘              ║
║                                                                               ║
║   USER_FLOW: Kill zombie → blood spray → particles fade → clean floor        ║
║   PAIN_POINT: No corpse, no blood pool - partial gore only                   ║
║   DATA_FLOW: Collision → spawn blood particles → zombie removed              ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌─────────────┐         ┌─────────────┐         ┌─────────────┐            ║
║   │   Player    │ ──────► │   Shoots    │ ──────► │   Zombie    │            ║
║   │   Shoots    │         │   Zombie    │         │   Dies      │            ║
║   └─────────────┘         └─────────────┘         └─────────────┘            ║
║                                                           │                   ║
║                                                           ▼                   ║
║                                                  ┌─────────────┐              ║
║                                                  │ Blood spray │              ║
║                                                  │   (0.8s)    │              ║
║                                                  └─────────────┘              ║
║                                                           │                   ║
║                                                           ▼                   ║
║                                                  ┌─────────────┐              ║
║                                                  │ Blood Pool  │              ║
║                                                  │   (decal)   │              ║
║                                                  └─────────────┘              ║
║                                                           │                   ║
║                                                           ▼                   ║
║                                                  ┌─────────────┐              ║
║                                                  │  Corpse on  │              ║
║                                                  │  blood pool │              ║
║                                                  │    (10s)    │              ║
║                                                  └─────────────┘              ║
║                                                                               ║
║   USER_FLOW: Kill zombie → blood spray + pool + corpse → persist 10s         ║
║   VALUE_ADD: Complete gore experience, visceral satisfaction                 ║
║   DATA_FLOW: Collision → spawn all 3 entities → update TTLs → render layers  ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location        | Before          | After              | User_Action | Impact                    |
| --------------- | --------------- | ------------------ | ----------- | ------------------------- |
| Play scene      | Blood spray only | Blood + corpse + pool | Kill zombie | Complete gore feedback |
| Battlefield     | Particles fade → clean | Corpses + pools persist 10s | Look around | Battlefield history visible |
| Rendering       | Particles on top only | Layered: pool → corpse → zombie → particles | Visual | Correct depth sorting |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `zombie-shooter/src/game/scenes/play.py` | 39-244 | Current PlayScene state - integration target |
| P0 | `zombie-shooter/src/game/entities/blood_particle.py` | 1-83 | BloodParticle already integrated (reference) |
| P0 | `zombie-shooter/src/game/entities/dead_zombie.py` | 1-75 | DeadZombie to integrate |
| P0 | `zombie-shooter/src/game/entities/blood_decal.py` | 1-67 | BloodDecal to integrate |
| P1 | `.claude/PRPs/reports/phase-1-blood-particle-system-report.md` | all | Phase 1 integration patterns |

**External Documentation:**

N/A - all patterns already established in codebase

---

## Patterns to Mirror

**ENTITY_LIST_INITIALIZATION:**
```python
# SOURCE: zombie-shooter/src/game/scenes/play.py:50-53
# COPY THIS PATTERN:
self.bullets: list[Bullet] = []
self.zombies: list[Zombie] = []
self.pickups: list[Pickup] = []
self.blood_particles: list[BloodParticle] = []
```

**COLLISION_HANDLER_SPAWNING:**
```python
# SOURCE: zombie-shooter/src/game/scenes/play.py:167-172
# COPY THIS PATTERN:
for b_idx, z_idx in bullet_zombie_hits:
    zombie = self.zombies[z_idx]  # Get zombie before removal
    self.spawn_blood_splash(zombie.pos)  # Spawn blood particles
    bullets_to_remove.add(b_idx)
    zombies_to_remove.add(z_idx)
    self.kills += 1
```

**ENTITY_UPDATE_LOOP:**
```python
# SOURCE: zombie-shooter/src/game/scenes/play.py:119
# COPY THIS PATTERN:
self.bullets = [b for b in self.bullets if b.update(dt)]
```

**ENTITY_DRAW_LOOP:**
```python
# SOURCE: zombie-shooter/src/game/scenes/play.py:207-217
# COPY THIS PATTERN:
for bullet in self.bullets:
    bullet.draw(screen)

for zombie in self.zombies:
    zombie.draw(screen)

for pickup in self.pickups:
    pickup.draw(screen)
```

---

## Files to Change

| File                             | Action | Justification                            |
| -------------------------------- | ------ | ---------------------------------------- |
| `zombie-shooter/src/game/scenes/play.py` | UPDATE | Add entity lists, wire collision/update/draw |

---

## NOT Building (Scope Limits)

Explicit exclusions to prevent scope creep:

- **Corpse collision**: Dead zombies don't block movement or bullets (visual only)
- **Blood pool stacking**: Multiple pools can overlap, no special handling
- **Performance limits**: No max corpse count (10s TTL is sufficient)
- **Variable gore**: All kills produce same effects (no weapon-specific variations)
- **Sound effects**: Visual only, no audio
- **Screen shake**: No camera effects
- **New constants**: Use existing constants from Phases 1-3

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: UPDATE `zombie-shooter/src/game/scenes/play.py` - Add imports

- **ACTION**: ADD imports for DeadZombie and BloodDecal
- **IMPLEMENT**: Add to import section at top of file (around line 23-27)
- **IMPORTS**:
  ```python
  from game.entities.blood_decal import BloodDecal
  from game.entities.dead_zombie import DeadZombie
  ```
- **PLACEMENT**: After `from game.entities.blood_particle import BloodParticle` (line 23)
- **MIRROR**: `zombie-shooter/src/game/scenes/play.py:22-27` (existing import block)
- **GOTCHA**: Alphabetical order for entity imports
- **VALIDATE**: `cd zombie-shooter && .venv/bin/ruff check src/game/scenes/play.py`

### Task 2: UPDATE `zombie-shooter/src/game/scenes/play.py` - Add entity lists

- **ACTION**: ADD `self.dead_zombies` and `self.blood_decals` lists to __init__
- **IMPLEMENT**: Add after `self.blood_particles` list (line 53)
  ```python
  self.dead_zombies: list[DeadZombie] = []
  self.blood_decals: list[BloodDecal] = []
  ```
- **MIRROR**: `zombie-shooter/src/game/scenes/play.py:50-53` (existing entity lists)
- **PLACEMENT**: After line 53 (`self.blood_particles`)
- **GOTCHA**: Type hints required (list[EntityType])
- **VALIDATE**: `cd zombie-shooter && .venv/bin/ruff check src/game/scenes/play.py`

### Task 3: UPDATE `zombie-shooter/src/game/scenes/play.py` - Modify collision handler

- **ACTION**: ADD DeadZombie and BloodDecal spawning to collision handler
- **IMPLEMENT**: Add two lines after `self.spawn_blood_splash(zombie.pos)` (line 169)
  ```python
  self.blood_decals.append(BloodDecal(zombie.pos))  # Spawn blood pool
  self.dead_zombies.append(DeadZombie(zombie.pos))  # Spawn corpse
  ```
- **MIRROR**: `zombie-shooter/src/game/scenes/play.py:169` (existing blood particle spawning)
- **PLACEMENT**: Lines 170-171 (right after spawn_blood_splash call)
- **ORDER**: Blood decal first (renders underneath), then dead zombie
- **GOTCHA**: Use same `zombie.pos` for all spawns (captured before removal)
- **VALIDATE**: `cd zombie-shooter && .venv/bin/ruff check src/game/scenes/play.py`

### Task 4: UPDATE `zombie-shooter/src/game/scenes/play.py` - Add update loops

- **ACTION**: ADD update loops for dead_zombies and blood_decals
- **IMPLEMENT**: Add after blood particle update loop (line 122)
  ```python
  # Update dead zombies and remove expired ones
  self.dead_zombies = [d for d in self.dead_zombies if d.update(dt)]

  # Update blood decals and remove expired ones
  self.blood_decals = [b for b in self.blood_decals if b.update(dt)]
  ```
- **MIRROR**: `zombie-shooter/src/game/scenes/play.py:122` (blood particle update)
- **PLACEMENT**: After line 122 (`self.blood_particles = [...]`)
- **PATTERN**: List comprehension filtering with `entity.update(dt)` returning bool
- **GOTCHA**: Same pattern as blood_particles (not separate loops)
- **VALIDATE**: `cd zombie-shooter && .venv/bin/ruff check src/game/scenes/play.py`

### Task 5: UPDATE `zombie-shooter/src/game/scenes/play.py` - Reorganize draw order

- **ACTION**: REORGANIZE draw() method for correct rendering order
- **IMPLEMENT**: Reorder drawing sections (lines 201-221)
  ```python
  # Dark gray background
  screen.fill((40, 40, 40))

  # Draw blood decals first (underneath everything)
  for decal in self.blood_decals:
      decal.draw(screen)

  # Draw dead zombies (on top of blood pools)
  for corpse in self.dead_zombies:
      corpse.draw(screen)

  # Draw player
  self.player.draw(screen)

  # Draw bullets
  for bullet in self.bullets:
      bullet.draw(screen)

  # Draw live zombies (on top of corpses)
  for zombie in self.zombies:
      zombie.draw(screen)

  # Draw pickups
  for pickup in self.pickups:
      pickup.draw(screen)

  # Draw blood particles (on top of everything except HUD)
  for particle in self.blood_particles:
      particle.draw(screen)
  ```
- **MIRROR**: `zombie-shooter/src/game/scenes/play.py:201-221` (existing draw loops)
- **ORDER**: Decals → corpses → player → bullets → zombies → pickups → particles → HUD
- **RATIONALE**: Blood decals under corpses, corpses under live zombies, particles on top
- **GOTCHA**: Keep HUD drawing at end (lines 223-243), don't move it
- **VALIDATE**: `cd zombie-shooter && .venv/bin/ruff check src/game/scenes/play.py && .venv/bin/ruff format src/game/scenes/play.py`

---

## Testing Strategy

### Unit Tests to Write

No new unit tests needed - all entity classes already have comprehensive tests from Phases 1-3. Integration testing will be manual via gameplay.

### Edge Cases Checklist

- [ ] Multiple simultaneous kills (all spawn correctly)
- [ ] Rapid kills (50+ corpses/pools briefly)
- [ ] Blood decals/corpses auto-remove after 10 seconds
- [ ] Rendering order correct (pools under corpses under zombies)
- [ ] No memory leaks (entities removed when dead)
- [ ] Performance maintained (60 FPS with max zombies)

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
cd zombie-shooter
.venv/bin/ruff check .
.venv/bin/ruff format .
```

**EXPECT**: Exit 0, no errors or warnings

### Level 2: UNIT_TESTS

```bash
cd zombie-shooter
PYTHONPATH=src .venv/bin/pytest -v
```

**EXPECT**: All 81 tests pass (no new tests, just verify no regressions)

### Level 3: FULL_SUITE

```bash
cd zombie-shooter
PYTHONPATH=src .venv/bin/pytest -v
```

**EXPECT**: All tests pass

### Level 4: DATABASE_VALIDATION

N/A - no database changes

### Level 5: BROWSER_VALIDATION

N/A - not a web application

### Level 6: MANUAL_VALIDATION

**Launch game and test gore system:**

```bash
cd zombie-shooter
PYTHONPATH=src .venv/bin/python -m game.main
```

**Test checklist:**
1. Kill a zombie → verify blood spray + blood pool + corpse all appear
2. Wait 1 second → blood spray fades (0.8s lifetime)
3. Wait 10 seconds → blood pool + corpse disappear together
4. Kill multiple zombies rapidly → all effects spawn correctly
5. Check rendering order → blood pools under corpses, corpses under live zombies
6. Verify performance → 60 FPS maintained with many zombies
7. Check no crashes → play for 2+ minutes with heavy combat

---

## Acceptance Criteria

- [ ] `dead_zombies` and `blood_decals` entity lists added to PlayScene.__init__
- [ ] DeadZombie and BloodDecal imports added
- [ ] Collision handler spawns all 3 gore entities (particles, decal, corpse)
- [ ] Update loops filter dead entities for dead_zombies and blood_decals
- [ ] Draw order correct: decals → corpses → player → bullets → zombies → pickups → particles → HUD
- [ ] Manual testing shows complete gore effects (blood + corpse + pool)
- [ ] Blood pools appear under corpses (rendering order)
- [ ] Blood pools and corpses persist 10 seconds then auto-remove
- [ ] No regressions in existing tests (81/81 passing)
- [ ] Level 1-3 validation passes
- [ ] Performance maintained (60 FPS)

---

## Completion Checklist

- [ ] Task 1: Imports added
- [ ] Task 2: Entity lists added
- [ ] Task 3: Collision handler modified
- [ ] Task 4: Update loops added
- [ ] Task 5: Draw order reorganized
- [ ] Level 1: Static analysis passes
- [ ] Level 2: Unit tests pass (no regressions)
- [ ] Level 3: Full test suite passes
- [ ] Level 6: Manual validation passes (gore effects working)
- [ ] All acceptance criteria met
- [ ] Implementation report created
- [ ] PRD Phase 4 status updated to complete

---

## Risks and Mitigations

| Risk               | Likelihood   | Impact       | Mitigation                              |
| ------------------ | ------------ | ------------ | --------------------------------------- |
| Rendering order wrong | LOW | HIGH | Follow exact pattern: decals → corpses → zombies → particles |
| Memory leak from entities | LOW | HIGH | TTL auto-removal already tested in Phases 1-3 |
| Performance degradation | LOW | MEDIUM | 10s TTL limits max entities, all tested individually |
| Multiple spawns failing | LOW | MEDIUM | All use same `zombie.pos` captured before removal |
| Z-fighting (visual glitches) | LOW | LOW | Clear layer separation, tested in phases |

---

## Notes

**Design Decision - Rendering Order**: Blood decals drawn first (underneath), then dead zombies, then live zombies, then particles on top. This creates correct visual layering where blood pools are under corpses, and corpses are under live zombies walking over them.

**Design Decision - No New Tests**: Integration is tested manually via gameplay. All entity classes already have comprehensive unit tests (81 tests total). Adding integration tests would test game loop mechanics, which is better done via manual play.

**Design Decision - Spawn Order**: Blood decal spawned before dead zombie in collision handler to match draw order (decals first, corpses second). This maintains consistency between spawn order and render order.

**Phase 1 Already Done**: Blood particles are already integrated (spawn_blood_splash exists, blood_particles list exists, update/draw loops exist). This phase only adds the remaining two entity types.

**Performance Notes**: With 50 max zombies and 10-second persistence, maximum simultaneous gore entities is ~150 decals + 150 corpses + brief particle bursts. All tested individually and should have no performance impact.

**Implementation Highlight**: This is purely a wiring phase - no new entity logic, no new algorithms, just connecting existing tested components into the game loop. All entity classes are production-ready from Phases 1-3.

---

*Implementation plan complete. All three gore entities (BloodParticle, DeadZombie, BloodDecal) ready to wire into PlayScene for complete DOOM-style gore experience.*
