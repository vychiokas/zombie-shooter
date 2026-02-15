# Directional Animated Zombie Models

## Problem Statement

The zombie shooter currently renders zombies as simple green circles, providing no visual feedback about movement direction or state. This creates a lifeless, static feel that reduces player engagement and makes the game feel less polished and immersive. Players cannot intuitively understand zombie behavior through visual cues alone.

## Evidence

- **Current state**: Zombies rendered as 16px radius green circles with no animation or directional indication
- **Developer feedback**: "I need animated enemies, it's more exciting, more alive realistic feel"
- **Technical observation**: Zombie entity is only 44 lines with `pygame.draw.circle()` rendering - minimal visual feedback
- **Performance baseline**: Max 50 zombies at 60 FPS with simple circle rendering
- **Market validation**: Pygame shooters like PyArena use 4-direction sprite animation as standard for enemy feedback
- **Assumption**: Directional sprites will improve perceived quality and gameplay feel - needs playtesting validation

## Proposed Solution

Implement a lightweight directional sprite animation system for zombie entities with 4-direction support (up, down, left, right). Each zombie will display a 2-4 frame walk cycle animation that updates based on their velocity vector, creating smooth visual feedback that matches movement direction. The system will use delta-time based frame cycling and support static frames when zombies are stationary.

**Why this approach**: Leverages existing velocity tracking, integrates cleanly with current entity pattern, uses proven 4-direction system (simpler than 8-direction), requires minimal architectural changes, and keeps performance impact low through asset reuse.

## Key Hypothesis

We believe **adding directional sprite animations to zombies** will **create a more engaging and polished gameplay experience** for **developers and players of the zombie shooter**.

We'll know we're right when **zombies visually face their movement direction with smooth looping animations, and the game maintains stable performance with 50 zombies**.

## What We're NOT Building

- **Player animations** - Player remains placeholder circle (out of scope)
- **Death animations** - Zombies disappear instantly on kill (no fade/death sequence)
- **Attack animations** - No special animation for zombie attacks/contact damage
- **8-direction sprites** - Using simpler 4-direction system (N/S/E/W)
- **Arbitrary angle rotation** - Snap to 4 cardinal directions, no smooth rotation
- **High-fidelity art** - Placeholder sprite sheets acceptable (artistic polish deferred)
- **Animation blending** - Instant direction changes, no transition smoothing
- **Idle vs walk states** - Single animation type, just loops or shows first frame when stopped
- **Asset pipeline** - No asset generation tools, manual sprite sheet creation

## Success Metrics

| Metric | Target | How Measured |
|--------|--------|--------------|
| Visual direction accuracy | 100% | Zombie sprite faces direction of velocity vector within one frame |
| Animation smoothness | No stutter | Walk cycle loops without visible frame skips or timing issues |
| Performance stability | 60 FPS maintained | `python -m game.main` with 50 zombies shows no FPS degradation |
| Code quality | Pass | `pytest -q` passes all tests, `ruff check` passes |
| Integration integrity | No regression | Existing gameplay (collisions, spawning, movement) works unchanged |

## Open Questions

- [ ] Should zombies show animation when moving slowly vs full speed?
- [ ] Should first frame be neutral stance or mid-walk frame?
- [ ] What sprite dimensions work best (16x16, 32x32)?
- [ ] Should animation speed scale with zombie speed?
- [ ] How to handle diagonal movement in 4-direction system (choose nearest cardinal)?

---

## Users & Context

**Primary User**
- **Who**: Developer (initially), future players (secondary)
- **Current behavior**: Observes zombies as green circles moving toward player with no visual personality
- **Trigger**: Gameplay feels flat and placeholder-like after initial implementation phase
- **Success state**: Zombies appear animated and alive, direction changes are visually obvious, game feels more polished

**Job to Be Done**
When **observing zombie enemies during gameplay**, I want to **see animated sprites showing movement direction**, so I can **experience a more engaging and realistic game feel**.

**Non-Users**
- Players expecting high-fidelity AAA-quality animations
- Developers wanting complex animation state machines
- Projects requiring 8-direction or free rotation systems
- Mobile/web platforms (desktop pygame only)

---

## Solution Detail

### Core Capabilities (MoSCoW)

| Priority | Capability | Rationale |
|----------|------------|-----------|
| Must | 4-direction sprite system (N/S/E/W) | Simplest proven approach, covers all movement cases |
| Must | 2-4 frame walk cycle per direction | Minimum for smooth animation feel |
| Must | Delta-time based frame cycling | Frame-rate independent, matches existing dt pattern |
| Must | Direction detection from velocity vector | Reuses existing `self.vel` calculation |
| Must | Sprite sheet loading and storage | Assets loaded once, reused for all zombies |
| Must | Animation helper class | Encapsulates frame timing and direction logic |
| Must | Static frame when not moving | Shows direction even when stationary |
| Should | Placeholder sprite sheets | Developer can test without artistic assets |
| Should | Animation speed configuration | Tunable via constants (frames per second) |
| Should | Asset organization in `assets/zombies/` | Clear directory structure |
| Could | Animation pause/resume | Currently just loops continuously |
| Could | Frame interpolation | Visual smoothing between frames |
| Won't | 8-direction sprites | Added complexity without significant value |
| Won't | Rotation/flip fallbacks | 4 directions sufficient, no need for transforms |
| Won't | Animation events/callbacks | Not needed for walk cycles |

### MVP Scope

**Minimum viable feature set:**
1. Animation helper class with direction detection (4 cardinal directions from Vector2)
2. Frame cycling using delta-time accumulator
3. Sprite sheet loading for zombie walk cycles (4 directions × 2-4 frames)
4. Zombie entity integration (replace `draw()` circle with animated sprite)
5. Direction updated each frame based on `self.vel`
6. First frame shown when velocity is zero

**Placeholder visuals:**
- 16x16 or 32x32 pixel sprites
- 4 directions: down (south), up (north), right (east), left (west)
- 2-4 frames per direction
- Simple pixel art acceptable (colored rectangles with direction indicator)
- Stored as sprite sheet PNG files in `assets/zombies/`

### User Flow

**Critical path:**
1. Game loads zombie sprite sheets once at initialization
2. Each Zombie entity creates Animation instance with sprite sheet reference
3. During gameplay, zombie moves toward player (velocity vector updated)
4. Animation detects direction from velocity (e.g., vel.x > 0 → "right")
5. Frame timer accumulates dt and cycles through frames for that direction
6. `Zombie.draw()` renders current frame sprite at zombie position
7. Direction changes immediately update to new direction's animation frames
8. When zombie stops (velocity ~= 0), animation shows first frame of last direction
9. Process repeats for all zombies every frame with no performance degradation

---

## Technical Approach

**Feasibility**: **HIGH**

**Architecture Notes**
- **Animation class**: Lightweight helper managing frame timing and direction mapping
  - Attributes: `current_direction`, `frame_index`, `frame_timer`, `sprite_sheets`
  - Methods: `update(dt, velocity)`, `get_current_frame()`, `set_direction(direction)`
- **Asset loading**: Load sprite sheets once in `Zombie.__init__()` or asset manager
- **Direction detection**: Calculate angle from `velocity.angle_to()` or compare x/y components
- **Frame cycling**: Accumulate `dt`, advance frame when timer exceeds threshold (e.g., 0.1s per frame)
- **Sprite rendering**: Replace `pygame.draw.circle()` with `screen.blit(sprite, pos)`
- **Constants**: Add `ZOMBIE_ANIMATION_FPS`, `ZOMBIE_SPRITE_SIZE` to constants.py
- **Asset structure**: `assets/zombies/walk_down.png`, `walk_up.png`, `walk_left.png`, `walk_right.png`

**Key technical decisions:**
1. **Direction system**: 4-direction (N/S/E/W) rather than 8-direction (simpler, standard pattern)
2. **Asset format**: Individual PNG files per direction (simpler than single sprite sheet with indexing)
3. **Animation ownership**: Each Zombie has its own Animation instance (independent timing)
4. **Direction threshold**: Use velocity magnitude check (e.g., `> 5`) to detect movement vs stationary
5. **Frame timing**: Fixed frame duration (0.1s) rather than speed-scaled (simpler, consistent feel)

**Technical Risks**

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Asset loading slows initialization | Low | Load once, cache in Zombie class variable, reuse across instances |
| Animation timing drifts at variable FPS | Low | Use dt accumulator, already proven in existing systems |
| Direction changes create visual stutter | Medium | Instant direction change acceptable, test with playtesters |
| Sprite rendering slower than circles | Low | Blitting is optimized in pygame, 50 sprites negligible at 60 FPS |
| Diagonal movement direction ambiguous | Medium | Choose nearest cardinal direction (e.g., velocity.x > velocity.y → horizontal) |
| Collision radius doesn't match sprite | Medium | Keep existing radius-based collision, sprite is visual only |

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
| 1 | Animation system foundation | Create Animation helper class with direction detection and frame cycling | complete | - | - | [phase-1-animation-system-foundation.plan.md](../../plans/phase-1-animation-system-foundation.plan.md) |
| 2 | Asset structure and loading | Define asset directory, create placeholder sprites, implement loading | complete | with 1 | - | [phase-2-asset-structure-and-loading.plan.md](../../plans/phase-2-asset-structure-and-loading.plan.md) |
| 3 | Zombie integration | Replace circle rendering with animated sprite, wire up velocity-based direction | complete | - | 1, 2 | [phase-3-zombie-integration.plan.md](../../plans/phase-3-zombie-integration.plan.md) |
| 4 | Testing & validation | Add tests, verify performance, fix bugs, manual playtest | complete | - | 3 | [phase-4-testing-and-validation-report.md](../../reports/phase-4-testing-and-validation-report.md) |

### Phase Details

**Phase 1: Animation system foundation**
- **Goal**: Create reusable animation system for directional sprite cycling
- **Scope**:
  - Create `game/systems/animation.py` with `Animation` class
  - Implement `update(dt, velocity: Vector2)` for direction detection and frame timing
  - Implement `get_current_frame() -> pygame.Surface` for current sprite retrieval
  - Add direction detection logic (4 cardinal directions from Vector2)
  - Add frame timer with dt accumulator
  - Add constants: `ZOMBIE_ANIMATION_FPS = 10` (0.1s per frame)
- **Success signal**: Animation class exists, direction detection works, frame cycling works in isolation

**Phase 2: Asset structure and loading**
- **Goal**: Establish asset organization and loading mechanism
- **Scope**:
  - Create `assets/zombies/` directory structure
  - Create placeholder sprite sheets (can use colored rectangles):
    - `walk_down.png` (2-4 frames, 16x16 or 32x32 each)
    - `walk_up.png`
    - `walk_left.png`
    - `walk_right.png`
  - Add sprite loading function (pygame.image.load)
  - Cache loaded sprites as class variable or module-level dict
  - Add error handling for missing assets
- **Success signal**: Sprites load without errors, visually distinguishable directions

**Phase 3: Zombie integration**
- **Goal**: Replace circle rendering with animated sprites
- **Scope**:
  - Modify `Zombie.__init__()` to create Animation instance
  - Update `Zombie.update(dt, player_pos)` to call `animation.update(dt, self.vel)`
  - Replace `Zombie.draw()` circle with sprite blit:
    ```python
    sprite = self.animation.get_current_frame()
    screen.blit(sprite, sprite.get_rect(center=(int(self.pos.x), int(self.pos.y))))
    ```
  - Verify collision detection still works (uses pos/radius, not sprite bounds)
  - Test direction changes during gameplay
- **Success signal**: Zombies render as sprites, animation loops, direction matches movement

**Phase 4: Testing & validation**
- **Goal**: Ensure feature works reliably and meets success metrics
- **Scope**:
  - Add unit tests for Animation direction detection
  - Add unit tests for frame cycling logic
  - Manual playtest: run `python -m game.main` for 60 seconds
  - Verify smooth animation with 50 zombies
  - Verify direction accuracy (move zombies in all 4 directions)
  - Check performance: FPS counter, no stuttering
  - Run `pytest -q` and `ruff check` to ensure quality
  - Fix any bugs discovered
- **Success signal**: All tests pass, gameplay smooth, animations match movement direction

### Parallelism Notes

Phases 1 and 2 can run in parallel as they touch different domains:
- Phase 1 (Animation system) creates Python code in `game/systems/animation.py`
- Phase 2 (Asset structure) creates PNG files in `assets/zombies/` and loading logic

Both are independent until Phase 3 (integration) which requires both to be complete.

---

## Decisions Log

| Decision | Choice | Alternatives | Rationale |
|----------|--------|--------------|-----------|
| Direction system | 4-direction (N/S/E/W) | 8-direction, free rotation | Simpler implementation, standard for pygame, sufficient visual feedback |
| Frame count | 2-4 frames per direction | 1 frame (static), 6+ frames (complex) | Minimum for smooth walk cycle feel without excessive asset creation |
| Animation timing | Delta-time based | Frame-based (update every N frames) | Matches existing dt pattern, frame-rate independent |
| Direction detection | Velocity vector angle | Mouse position, player position | Matches actual movement, more realistic |
| Asset format | Individual PNGs per direction | Single sprite sheet atlas | Simpler loading logic, easier to create placeholder assets |
| Sprite ownership | Each Zombie has Animation instance | Global Animation manager | Independent timing per zombie, simpler state management |
| Static behavior | Show first frame when stopped | Continue animation, show blank | Preserves direction feedback even when stationary |
| Animation speed | Fixed 10 FPS (0.1s/frame) | Speed-scaled, configurable per zombie | Consistent feel, simpler implementation |

---

## Research Summary

**Market Context**
- Top-down pygame shooters commonly use 4-direction sprite systems for enemies
- PyArena demonstrates 4-direction with 2-4 frame walk cycles as standard
- Common patterns: velocity-based direction detection, dt-based frame timing, cached sprite loading
- Animation frame rates typically 8-12 FPS for retro/pixel art feel
- Sprite dimensions commonly 16x16 or 32x32 for small enemies

**Technical Context**
- Codebase uses clean Scene/Entity/System architecture - animation system fits naturally
- Zombie entity already tracks velocity vector (`self.vel`) - perfect for direction detection
- Delta-time pattern used consistently (`update(dt)`) - animation timing integrates seamlessly
- Current rendering is simple circle - easy to replace with sprite blit
- Collision system uses `pos` and `radius` - sprite rendering won't affect collision detection
- Max 50 zombies at 60 FPS - sprite rendering performance impact should be negligible
- Assets directory exists but empty - ready for sprite sheet population

**Pygame Animation Patterns**
- `pygame.image.load()` for asset loading
- `Surface.blit(sprite, rect)` for rendering
- `get_rect(center=pos)` for sprite positioning
- Frame cycling via timer accumulation: `timer += dt; if timer > threshold: next_frame()`
- Direction detection via `Vector2.angle_to()` or component comparison

**Sources:**
- [Pygame Animation Tutorial - Real Python](https://realpython.com/pygame-a-primer/#sprites)
- [Top-Down Character Animation - GameDev.net](https://www.gamedev.net/forums/topic/587596-weapon-system-in-top-down-shooter/)
- [PyArena Pygame Project](https://www.pygame.org/project-pyarena-484-.html)
- [Sprite Animation Techniques - Pygame Docs](https://www.pygame.org/docs/tut/SpriteIntro.html)

---

*Generated: 2026-01-27*
*Status: DRAFT - needs implementation and playtesting validation*
