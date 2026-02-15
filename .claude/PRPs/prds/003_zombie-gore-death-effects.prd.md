# Zombie Gore & Death Effects

## Problem Statement

The zombie shooter currently provides zero visual feedback when zombies are killed - they simply vanish from the screen instantly. This creates an unsatisfying, arcade-like experience that lacks the visceral impact and excitement expected from a gory zombie game. Players receive no visual reward for successful kills, reducing engagement and the overall fun factor.

## Evidence

- **Developer feedback**: "Not fun, no visual feedback" when zombies disappear
- **Current implementation**: Zombies removed from `self.zombies` list at collision (play.py:135-151) with no death animation or effect
- **Inspiration**: Classic DOOM provides visceral, gory kills with blood effects that feel satisfying
- **Game feel observation**: Instant disappearance feels cheap and unrewarding compared to games with death animations and persistence

## Proposed Solution

Implement a multi-layered gore system that triggers on zombie death: (1) blood particle splash that sprays outward from impact point, (2) zombie transitions to "dead" state with corpse sprite/fallen animation, (3) blood pool decal appears underneath the corpse, (4) corpse and blood persist for 10 seconds before removal. This creates DOOM-style visceral feedback with visual reward for kills and battlefield persistence that shows player impact.

**Why this approach**: Leverages existing collision detection system, uses proven particle + decal pattern from classic shooters, requires minimal architectural changes (add dead zombie entity type), and provides layered visual feedback (immediate splash + persistent corpse).

## Key Hypothesis

We believe **adding gore effects with blood splash, corpse persistence, and blood pools** will **create visceral satisfaction and excitement on zombie kills** for **the player/developer**.

We'll know we're right when **every zombie kill produces visible blood splash particles, corpses fall and remain visible with blood pools underneath for 10 seconds, and the game feels more exciting and satisfying to play**.

## What We're NOT Building

- **Different death animations per weapon type** - All zombies die the same way regardless of weapon
- **Physics-based ragdoll** - No complex physics simulation for falling bodies
- **Blood trails/dripping over time** - Blood appears once, doesn't animate or spread
- **Gore sound effects** - Visual only, no audio feedback
- **Screen shake on kill** - No camera effects
- **Dismemberment or body parts** - Corpses stay intact, no gibbing
- **Variable blood amounts** - Same blood effect for all kills
- **Blood permanence** - Blood disappears after 10 seconds, doesn't stay forever
- **Weapon-specific gore** - Shotgun vs pistol produce same blood effect

## Success Metrics

| Metric | Target | How Measured |
|--------|--------|--------------|
| Blood splash visual feedback | 100% of kills | Every bullet-zombie collision spawns blood particles |
| Corpse persistence | 10 seconds ±0.5s | Dead zombie entities remain visible for exactly 10 seconds |
| Blood pool appearance | 100% of kills | Blood decal renders under every corpse |
| Performance stability | 60 FPS maintained | Game maintains target framerate with 50 zombies + blood effects |
| Visual satisfaction | Subjective "feels good" | Developer playtesting confirms kills feel visceral and satisfying |

## Open Questions

- [ ] Should blood particles have gravity and fade over time, or disappear instantly?
- [ ] Should corpses use rotated zombie sprite or dedicated death sprite?
- [ ] Should blood pool size vary, or be constant for all kills?
- [ ] Should old blood pools stack/overlap visually, or be limited in count?
- [ ] Should there be a max number of visible corpses (e.g., oldest fade if 20+ on screen)?

---

## Users & Context

**Primary User**
- **Who**: Developer/player creating zombie shooter presentation/demo
- **Current behavior**: Shoots zombies and sees them vanish instantly, feels unrewarding
- **Trigger**: Every successful bullet-zombie collision that results in a kill
- **Success state**: Sees blood splash, zombie falls down with blood pool, feels visceral satisfaction

**Job to Be Done**
When **I shoot and kill a zombie**, I want to **see blood splash particles, the corpse fall and persist with a blood pool underneath**, so I can **feel visceral satisfaction and visual feedback that my shot connected and had deadly impact**.

**Non-Users**
- Players preferring non-violent or clean aesthetic games
- Young audiences (due to gore content)
- Performance-critical contexts where visual effects must be minimal
- Players wanting realistic medical accuracy in blood physics

---

## Solution Detail

### Core Capabilities (MoSCoW)

| Priority | Capability | Rationale |
|----------|------------|-----------|
| Must | Blood particle splash on zombie death | Immediate visual feedback, core to visceral impact |
| Must | Zombie corpse entity that persists for 10 seconds | Visual reward and battlefield persistence |
| Must | Blood pool decal under corpse | Reinforces death, adds gore element |
| Must | Corpse + blood removal after 10 second timer | Prevents memory/performance issues |
| Must | Particles spawn at collision point with outward velocity | Creates dynamic splash effect |
| Should | Particle fade-out animation | Smoother than instant disappearance |
| Should | Multiple blood particle sizes/shades | Visual variety and depth |
| Should | Corpse sprite distinct from living zombie | Clear visual distinction between alive/dead |
| Could | Blood pool size variation based on impact | More dynamic visual |
| Could | Particle velocity variation | Less uniform, more organic splash |
| Could | Max corpse limit with oldest-first removal | Performance safety net |
| Won't | Weapon-specific gore effects | Adds complexity without major value |
| Won't | Physics-based ragdoll | Too complex for 2D top-down |
| Won't | Permanent blood stains | Memory leak risk, visual clutter |

### MVP Scope

**Minimum viable gore system:**
1. Particle system class with position, velocity, lifetime, color
2. Blood particle spawner (5-10 red particles with random outward velocity)
3. Dead zombie entity class (position, sprite, 10-second timer)
4. Blood decal entity class (position, sprite, 10-second timer)
5. Modified collision handler: spawn particles + create dead zombie + create blood pool instead of removing zombie
6. Rendering order: blood decals → dead zombies → live zombies
7. Update loop: tick timers on dead zombies and blood decals, remove when expired

**Placeholder visuals:**
- Blood particles: Small red circles (2-4 pixels)
- Corpse sprite: Rotated/fallen version of zombie sprite OR simple "X" shape
- Blood pool: Red ellipse/circle (24-32 pixels diameter)

### User Flow

**Critical path (every zombie kill):**
1. Bullet collides with zombie (existing collision detection at play.py:135-151)
2. **NEW**: Spawn 5-10 blood particles at zombie position with random outward velocities
3. **NEW**: Remove zombie from `self.zombies` list (existing)
4. **NEW**: Create DeadZombie entity at zombie's last position, add to `self.dead_zombies` list
5. **NEW**: Create BloodDecal entity at same position, add to `self.blood_decals` list
6. Increment kill counter (existing)
7. Particles update each frame: move by velocity, decrement lifetime, fade alpha
8. Particles removed when lifetime <= 0 (after ~0.5-1 second)
9. Dead zombie and blood decal update: decrement 10-second timer
10. When timer expires: remove from `self.dead_zombies` and `self.blood_decals` lists
11. Rendering draws blood decals first (underneath), then dead zombies, then live zombies on top

**Edge case: Multiple kills**
- Each kill spawns independent particles, dead zombie, and blood pool
- All corpses/blood pools track own timers independently
- No limit on simultaneous corpses (unless performance degrades)

---

## Technical Approach

**Feasibility**: **HIGH**

**Architecture Notes**
- **Particle system**: Lightweight class with `pos`, `vel`, `lifetime`, `alpha` attributes
  - List of active particles: `self.blood_particles: list[BloodParticle]`
  - Update: `pos += vel * dt`, `lifetime -= dt`, fade `alpha`
  - Draw: `pygame.draw.circle()` with alpha via temporary surface
- **Dead zombie entity**: New class mirroring Zombie but stationary
  - Attributes: `pos`, `sprite`, `timer` (counts down from 10.0)
  - No AI/movement, just draws sprite and ticks timer
- **Blood decal entity**: Simple sprite or shape at position
  - Attributes: `pos`, `sprite/color`, `timer` (10.0 seconds)
  - Drawn before dead zombies (render order)
- **Modified collision handler** (play.py:135-151):
  ```python
  for b_idx, z_idx in bullet_zombie_hits:
      zombie = self.zombies[z_idx]
      # NEW: Spawn blood particles
      self.spawn_blood_splash(zombie.pos)
      # NEW: Create dead zombie and blood pool
      self.dead_zombies.append(DeadZombie(zombie.pos, zombie.animation.get_current_frame()))
      self.blood_decals.append(BloodDecal(zombie.pos))
      # Existing: Remove zombie
      zombies_to_remove.add(z_idx)
      self.kills += 1
  ```
- **Rendering order** (play.py:173-189):
  ```python
  # Background
  # Blood decals (NEW - drawn first, underneath everything)
  for decal in self.blood_decals:
      decal.draw(screen)
  # Dead zombies (NEW)
  for corpse in self.dead_zombies:
      corpse.draw(screen)
  # Player
  # Bullets
  # Live zombies
  # Pickups
  # Blood particles (NEW - drawn on top for splash visibility)
  for particle in self.blood_particles:
      particle.draw(screen)
  # HUD
  ```
- **New entity files**:
  - `game/entities/blood_particle.py` - Particle class
  - `game/entities/dead_zombie.py` - DeadZombie class
  - `game/entities/blood_decal.py` - BloodDecal class
- **Constants** (add to constants.py):
  - `BLOOD_PARTICLE_COUNT = 8` - Particles per death
  - `BLOOD_PARTICLE_SPEED = 150` - Initial velocity magnitude
  - `BLOOD_PARTICLE_LIFETIME = 0.8` - Seconds before fade
  - `CORPSE_PERSISTENCE = 10.0` - Seconds corpse/blood remains
  - `BLOOD_POOL_SIZE = 28` - Pixel diameter of blood pool

**Key technical decisions:**
1. **Particle approach**: Simple position + velocity + lifetime (no physics library needed)
2. **Corpse sprite**: Reuse zombie's last animation frame, optionally rotate 90° for "fallen" look
3. **Blood pool**: Static red ellipse sprite/shape (no animation)
4. **Timer approach**: Countdown float in entity, remove when <= 0
5. **Alpha blending**: Use `pygame.SRCALPHA` surfaces for particle fade and blood pool transparency
6. **Performance**: Max 50 zombies × 8 particles = 400 particles briefly, then fade - negligible impact

**Technical Risks**

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Too many particles degrade FPS | Low | Particles fade quickly (0.8s), max 50 zombies, tested at 60 FPS |
| Corpse buildup slows game over time | Low | 10-second removal, max 50 zombies spawned per session, corpses are static (no AI) |
| Blood pool rendering stacks poorly | Medium | Use alpha blending, or limit max decals (e.g., 100 cap with FIFO removal) |
| Particle alpha blending expensive | Low | Simple circle draw with alpha surface, pygame handles efficiently |
| Collision detection unchanged breaks | Very Low | Only adding entities after collision, not modifying collision logic |

---

## Implementation Phases

<!--
  STATUS: pending | in-progress | complete
  PARALLEL: phases that can run concurrently (e.g., "with 3" or "-")
  DEPENDS: phases that must complete first (e.g., "1, 2" or "-")
  PRP: link to generated plan file once created
-->

| # | Phase | Description | Status | Parallel | Depends | PRP Plan |
|---|-------|-------------|--------|----------|---------|----------|
| 1 | Blood particle system | Create particle entity class with spawn, update, fade, draw logic | complete | - | - | [phase-1-blood-particle-system-report.md](../../reports/phase-1-blood-particle-system-report.md) |
| 2 | Dead zombie entity | Create dead zombie class with timer and rendering | complete | with 1 | - | [phase-2-dead-zombie-entity-report.md](../reports/phase-2-dead-zombie-entity-report.md) |
| 3 | Blood decal entity | Create blood pool decal class with timer | complete | with 1, 2 | - | [phase-3-blood-decal-entity-report.md](../reports/phase-3-blood-decal-entity-report.md) |
| 4 | Gore integration | Wire up collision handler to spawn particles, dead zombies, and blood pools | complete | - | 1, 2, 3 | [phase-4-gore-integration-report.md](../reports/phase-4-gore-integration-report.md) |
| 5 | Testing & polish | Verify timers, rendering order, performance, visual feel | complete | - | 4 | [phase-5-testing-polish-report.md](../reports/phase-5-testing-polish-report.md) |

### Phase Details

**Phase 1: Blood particle system**
- **Goal**: Create reusable particle system for blood splash effects
- **Scope**:
  - Create `game/entities/blood_particle.py` with `BloodParticle` class
  - Attributes: `pos: Vector2`, `vel: Vector2`, `lifetime: float`, `max_lifetime: float`, `radius: int`, `color: tuple`
  - Method: `update(dt)` - move particle, decrement lifetime, calculate fade alpha
  - Method: `draw(screen)` - render circle with alpha based on lifetime ratio
  - Add `spawn_blood_splash(pos)` helper in PlayScene to create 8 particles with random outward velocities
  - Add constants: `BLOOD_PARTICLE_COUNT`, `BLOOD_PARTICLE_SPEED`, `BLOOD_PARTICLE_LIFETIME`
- **Success signal**: Can spawn blood particles at a point, they fly outward and fade over 0.8 seconds

**Phase 2: Dead zombie entity**
- **Goal**: Create corpse entity that persists with timer
- **Scope**:
  - Create `game/entities/dead_zombie.py` with `DeadZombie` class
  - Attributes: `pos: Vector2`, `sprite: Surface`, `timer: float` (starts at 10.0)
  - Method: `update(dt)` - decrement timer
  - Method: `draw(screen)` - blit sprite at position (optionally rotated 90° for fallen effect)
  - Add `CORPSE_PERSISTENCE = 10.0` constant
- **Success signal**: Dead zombie sprite renders at position and removes after 10 seconds

**Phase 3: Blood decal entity**
- **Goal**: Create blood pool visual under corpses
- **Scope**:
  - Create `game/entities/blood_decal.py` with `BloodDecal` class
  - Attributes: `pos: Vector2`, `size: int`, `color: tuple`, `timer: float` (10.0 seconds)
  - Method: `update(dt)` - decrement timer
  - Method: `draw(screen)` - draw red ellipse/circle with alpha transparency
  - Add `BLOOD_POOL_SIZE = 28` constant
- **Success signal**: Red blood pool appears under corpse position, persists 10 seconds

**Phase 4: Gore integration**
- **Goal**: Connect gore system to zombie death collision
- **Scope**:
  - Add entity lists to PlayScene: `self.blood_particles = []`, `self.dead_zombies = []`, `self.blood_decals = []`
  - Modify collision handler (play.py:135-151):
    - On zombie hit: spawn blood particles, create dead zombie, create blood decal
    - Remove zombie from live list (existing behavior)
  - Update PlayScene.update():
    - Update all blood particles, remove if lifetime <= 0
    - Update dead zombies, remove if timer <= 0
    - Update blood decals, remove if timer <= 0
  - Modify PlayScene.draw() rendering order:
    - Draw blood decals first (underneath)
    - Draw dead zombies
    - Draw live zombies on top
    - Draw blood particles last (on top of everything except HUD)
- **Success signal**: Zombie deaths trigger blood splash, corpse appears with blood pool, both disappear after 10 seconds

**Phase 5: Testing & polish**
- **Goal**: Verify gore system works correctly and feels satisfying
- **Scope**:
  - Manual playtest: kill 10+ zombies, observe blood effects
  - Verify 10-second timer accuracy
  - Check rendering order (blood under corpses, corpses under live zombies)
  - Performance test: 50 zombies with rapid kills, confirm 60 FPS maintained
  - Visual tuning: adjust particle count, speed, lifetime, blood pool size for best feel
  - Edge case testing: multiple simultaneous kills, max zombie scenarios
  - Run `pytest` to ensure no regressions
- **Success signal**: All tests pass, gore effects feel visceral and satisfying, 60 FPS maintained

### Parallelism Notes

Phases 1, 2, and 3 can run in parallel as they create independent entity classes:
- Phase 1 creates `BloodParticle` class
- Phase 2 creates `DeadZombie` class
- Phase 3 creates `BloodDecal` class

None of these depend on each other until Phase 4 (integration) where all three are wired into the collision handler.

---

## Decisions Log

| Decision | Choice | Alternatives | Rationale |
|----------|--------|--------------|-----------|
| Particle system | Custom lightweight particles | Use PyIgnition library | Simpler, no external dependency, full control, sufficient for blood splash |
| Corpse sprite | Reuse zombie animation frame | Create new death sprite | Faster implementation, reuses existing assets |
| Blood pool rendering | Simple red ellipse/circle | Blood sprite asset | Programmer art acceptable for MVP, can upgrade later |
| Timer approach | Countdown float in entity | Global timer manager | Simpler per-entity state, easier to reason about |
| Persistence duration | 10 seconds | 5s / 15s / permanent | User requirement, balances visual feedback with performance |
| Particle count | 8 per death | 5 / 15 / 20+ | Balance visual impact with performance |
| Rendering order | Decals → dead zombies → live zombies → particles | All corpses on top | Blood under corpses looks more natural |
| Alpha blending | Yes for particles and blood pools | Solid colors only | More polished visual, worth minor perf cost |

---

## Research Summary

**Market Context**
- Classic DOOM and modern shooters use particle splash + corpse persistence for visceral kills
- PyIgnition and SPPE are established pygame particle libraries, but lightweight custom system is simpler for blood effects
- 2D blood sprite packs available on itch.io for visual polish if needed
- Common pattern: immediate particle splash (0.5-1s) + persistent corpse/decal (5-15s)

**Technical Context**
- Codebase has clean entity lifecycle: lists of entities updated/drawn each frame
- Collision detection at play.py:135-151 is perfect injection point for gore spawn
- No existing particle systems - clean slate for implementation
- Rendering order explicit in draw() method - easy to control layering
- Asset loading system supports adding new sprites (blood pools, death sprites)
- Performance target: 60 FPS with 50 zombies - blood effects should be negligible overhead

**Pygame Gore Patterns**
- Alpha blending via `pygame.SRCALPHA` surfaces
- Particle velocity: `pos += vel * dt`
- Fade effect: `alpha = 255 * (lifetime / max_lifetime)`
- Timer pattern: `timer -= dt; if timer <= 0: remove()`
- Temporary surface for alpha: `temp = pygame.Surface((w, h), pygame.SRCALPHA); pygame.draw.circle(temp, (r, g, b, alpha), ...); screen.blit(temp, pos)`

**Sources:**
- [PyIgnition - Pygame particle effects library](https://www.pygame.org/project-PyIgnition-1527-.html)
- [Simple Pygame Particle Engine](https://www.pygame.org/project-Simple+Pygame+Particle+Engine-2021-.html)
- [itch.io 2D blood game assets](https://itch.io/game-assets/tag-2d/tag-blood)
- [Adding Special Effects to Pygame Games: Particle Systems](https://www.makeuseof.com/pygame-games-special-effects-particle-systems-visual-enhancements/)

---

*Generated: 2026-02-02*
*Status: DRAFT - ready for implementation*
