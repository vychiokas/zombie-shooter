# Environment: Ground Textures & Solid Obstacles

## Problem Statement

The game world is a featureless dark gray void. No environmental identity, no tactical depth,
no visual atmosphere. Players and zombies move through an empty space with nothing to navigate
around, hide behind, or react to. The game feels unfinished and lacks the post-apocalyptic
tension the zombie theme demands.

## Evidence

- `play.py` draw method line 326: `screen.fill((40, 40, 40))` — the entire world is one flat color
- Zero obstacle entities in codebase — collision system only handles entity-to-entity
- Zombie AI does straight-line pursuit with no awareness of world geometry
- No tile, zone, or map data structure exists anywhere in the codebase

## Proposed Solution

Add a fixed hand-crafted map with coherent ground zones (asphalt path, grass, dirt) rendered
as a pre-baked surface, plus a set of scattered solid obstacles (trees, ponds, cars, houses,
burning barrels) drawn with pygame shapes at varied saturations. Both player and zombies are
pushed out of solid obstacles via axis-by-axis collision resolution. Bullets pass through
everything. Layout is intentional — path through the center, landmarks in corners, spacing
prevents clustering.

## Key Hypothesis

We believe a visually coherent hand-crafted environment with solid collidable obstacles will
make the game feel like an actual post-apocalyptic world rather than a tech demo. We'll know
we're right when the map has clear readable zones, obstacles feel intentionally placed, and
60fps is maintained with 50 zombies active.

## What We're NOT Building

- Procedural map generation — same map every run, full control over aesthetics
- A* pathfinding for zombies — axis-by-axis push-out is sufficient for v1
- Sprite/pixel art assets for obstacles — pygame.draw shapes with varied colors
- Bullet collision with obstacles — bullets pass through everything
- A camera/scrolling system — map stays at 1280×720 fixed viewport
- Destructible obstacles — all obstacles are permanently solid

## Success Metrics

| Metric | Target | How Measured |
|--------|--------|--------------|
| Frame rate | Stable 60fps with 50 zombies | pygame Clock.get_fps() |
| Ground coherence | No single-pixel biome transitions | Visual inspection |
| Obstacle distribution | No cluster of >3 same-type obstacles in proximity | Visual inspection |
| Collision correctness | Player and zombie slide along obstacle edges | Manual playtesting |
| Aesthetic | Map reads as "abandoned post-apocalyptic" | Visual inspection |

## Open Questions

- [ ] Should burning barrels have an animated flicker effect (color oscillation)?
- [ ] Should ponds slow movement rather than fully block it (future enhancement)?
- [ ] Should houses have interior-implied openings (doorways) or be fully solid rectangles?

---

## Users & Context

**Primary User**
- **Who**: Developer building a top-down zombie shooter for a programming presentation
- **Current behavior**: Plays on a blank gray screen with no environmental context
- **Trigger**: The game works mechanically but looks like a prototype
- **Success state**: Map feels like a believable abandoned town that players instinctively
  navigate around

**Job to Be Done**
When playing the zombie shooter, I want environmental obstacles and varied ground to navigate
around, so I can experience tactical gameplay and feel immersed in a post-apocalyptic world.

**Non-Users**
Not targeting players who want procedurally generated maps or realistic physics — this is a
focused arcade-feel implementation.

---

## Solution Detail

### Core Capabilities (MoSCoW)

| Priority | Capability | Rationale |
|----------|------------|-----------|
| Must | Pre-baked ground surface with zones (path, grass, dirt) | Foundation — replaces flat gray |
| Must | Obstacle class with rect/circle shape + solid flag | Enables all obstacle types |
| Must | Player push-out collision vs obstacles (axis-by-axis) | Core gameplay constraint |
| Must | Zombie push-out collision vs obstacles (axis-by-axis) | Consistent world rules |
| Must | Fixed hand-crafted obstacle layout | Intentional aesthetic, no clustering |
| Must | Trees, ponds, crashed cars, houses, burning barrels | Full obstacle variety |
| Should | Varied saturation per obstacle instance | Prevents visual monotony |
| Should | Burning barrel color oscillation (flicker effect) | Post-apocalyptic atmosphere |
| Could | Pond with slightly different movement speed | Future tactical depth |
| Won't | Sprite art for obstacles | Out of scope — shapes are intentional |
| Won't | Destructible obstacles | Out of scope for v1 |

### MVP Scope

Fixed map with coherent ground zones + all 5 obstacle types + push-out collision for player
and zombies. Everything renders at 60fps.

### User Flow / Rendering Pipeline

```
Game start
  → Generate ground surface (once, pre-baked)
  → Place obstacle list (fixed layout, defined in constants)

Each frame:
  1. Blit pre-baked ground surface (O(1))
  2. Draw obstacle shapes (pygame.draw per obstacle)
  3. Draw blood decals
  4. Draw dead zombies
  5. Draw player
  6. Draw bullets
  7. Draw living zombies
  8. Draw pickups / acid projectiles
  9. Draw particles
  10. Draw HUD
```

---

## Technical Approach

**Feasibility**: HIGH

The codebase is clean, well-separated, and ready for extension. No architectural changes needed —
add a map module, an Obstacle dataclass, update the draw order in `play.py`, and hook collision
into the existing update loop.

### Ground Zone System

Pre-bake a `pygame.Surface` once at scene initialization:

```
Zones (draw order — painter's algorithm):
  1. Base layer: Grass (#3a4a2a) — fill entire surface
  2. Dirt patches: irregular rect regions (#5a4a30) at specific coordinates
  3. Main path: horizontal strip + vertical strip (#2a2a2a asphalt) through center
  4. Path edge noise: slightly lighter/darker rects along path borders (#333333)
```

No per-pixel operations. All zones are simple filled rects or polygons.
Zone boundaries are wide enough that transitions look deliberate, not accidental.

### Obstacle System

**Data model** — new file `src/game/entities/obstacle.py`:

```python
@dataclass
class Obstacle:
    pos: pygame.Vector2      # center position
    shape: Literal["rect", "circle", "ellipse"]
    width: float             # for rect/ellipse
    height: float            # for rect/ellipse
    radius: float            # for circle
    color: tuple[int,int,int]
    obstacle_type: str       # "tree", "pond", "car", "house", "barrel"
    solid: bool = True
    flicker: bool = False    # for barrels
```

**Collision shape**: rect-based AABB for cars/houses, circle for trees/barrels, ellipse-bounding-rect for ponds.

**Push-out algorithm** (axis-by-axis separation):
```
For each solid obstacle:
  1. Compute overlap on X axis
  2. Compute overlap on Y axis
  3. Push entity out along the axis with smaller overlap
  → Entity slides along obstacle edge naturally
```

Applied to both Player and Zombie in their respective `update()` methods.

### Fixed Map Layout

Map designed for 1280×720. Zones and obstacle placement:

```
┌─────────────────────────────────────────────────────────┐
│ [HOUSE]  grass/dirt         │         grass  [HOUSE]    │
│          [TREE][TREE]       │    [TREE]                 │
│                             │                           │
│─────────────── ASPHALT PATH ───────────────────────────│  ← horizontal center strip
│          [CAR]──[CAR]       │   [BARREL][BARREL]        │
│                    │                                     │
│                    │  VERTICAL PATH                      │
│                    │                                     │
│ [POND]   [TREE]    │         [CAR]      [TREE]          │
│                    │                                     │
│ [HOUSE]  [BARREL]  │                   [HOUSE]          │
└─────────────────────────────────────────────────────────┘
```

Obstacle placement rules:
- **Houses**: 4 corners, large (80×80 to 120×80 rects), dark desaturated brown/gray
- **Trees**: Scattered in grass zones only, circles r=12–18, varied dark greens
- **Cars**: On or near path only, rects ~50×25, varied dark grays/rust (desaturated reds)
- **Ponds**: Grass zones, ellipses, muted dark blue-green
- **Barrels**: Near houses/walls, small circles r=10, dark orange-brown, some flickering

**Saturation rule**: Each obstacle instance gets a slight random offset to its base color
(±15 on each channel) at map generation time, seeded for reproducibility. No two look identical
but they stay in the same family.

### Performance Notes

- Ground: pre-baked Surface → single `blit()` per frame, near-zero cost
- Obstacles: ~25–35 total → `pygame.draw` is fast, well within budget
- Zombie obstacle collision: 50 zombies × 35 obstacles = 1,750 AABB checks/frame → trivial
- No spatial partitioning needed at this scale

### Technical Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Zombie push-out causes jitter against corners | M | Clamp push-out magnitude; prefer smallest-overlap axis |
| Ground surface memory too large | L | 1280×720 RGBA = ~3.5MB — negligible |
| Obstacle placement blocks zombie spawn paths | M | Spawns are at screen edges; ensure edge strips stay clear |
| Burning barrel flicker tanks fps | L | Simple `sin(time)` color lerp, no surface recreation |

---

## Implementation Phases

| # | Phase | Description | Status | Parallel | Depends | PRP Plan |
|---|-------|-------------|--------|----------|---------|----------|
| 1 | Ground Zones | Pre-baked surface with path/grass/dirt zones | in-progress | - | - | `.claude/PRPs/plans/environment-obstacles-textures.plan.md` |
| 2 | Obstacle Model | Obstacle dataclass + fixed layout definition in constants | in-progress | with 1 | - | `.claude/PRPs/plans/environment-obstacles-textures.plan.md` |
| 3 | Obstacle Rendering | Draw obstacles each frame in correct z-order | in-progress | - | 1, 2 | `.claude/PRPs/plans/environment-obstacles-textures.plan.md` |
| 4 | Player Collision | Axis-by-axis push-out for player vs all solid obstacles | in-progress | - | 2 | `.claude/PRPs/plans/environment-obstacles-textures.plan.md` |
| 5 | Zombie Collision | Axis-by-axis push-out for all zombies vs all solid obstacles | in-progress | with 4 | 2 | `.claude/PRPs/plans/environment-obstacles-textures.plan.md` |
| 6 | Polish & Tuning | Barrel flicker, color variation seeding, layout tweaks, perf check | in-progress | - | 3, 4, 5 | `.claude/PRPs/plans/environment-obstacles-textures.plan.md` |

### Phase Details

**Phase 1: Ground Zones**
- **Goal**: Replace flat gray with coherent ground zones
- **Scope**: `src/game/scenes/play.py` — generate ground Surface at `__init__`, blit in `draw()`; zone rects defined in `constants.py`
- **Success signal**: Game renders grass/path/dirt zones, no visual seams, 60fps maintained

**Phase 2: Obstacle Model**
- **Goal**: Define all obstacles as data, placed in fixed positions
- **Scope**: New `src/game/entities/obstacle.py` dataclass; `OBSTACLE_LAYOUT` list in `constants.py` with all ~30 obstacle definitions including type, shape, position, base color
- **Success signal**: Import resolves, obstacle list instantiates correctly

**Phase 3: Obstacle Rendering**
- **Goal**: All obstacles drawn at correct z-layer with varied colors
- **Scope**: `play.py` draw method — add obstacle draw pass between ground and blood decals; barrel flicker via sin-based color shift on `obstacle.flicker == True`
- **Success signal**: All obstacle types visible, visually varied, no clustering, barrels animate

**Phase 4: Player Collision**
- **Goal**: Player cannot walk through solid obstacles, slides along edges
- **Scope**: `player.py` update() — after position update, iterate obstacles, compute AABB/circle overlap, apply push-out; also update boundary clamp to use obstacle-aware logic
- **Success signal**: Player slides smoothly along house walls, tree trunks, cars

**Phase 5: Zombie Collision**
- **Goal**: Zombies cannot walk through solid obstacles, slide along edges
- **Scope**: `zombie.py` update() — same push-out logic as player; obstacles passed into update() or accessed via module-level list
- **Success signal**: Zombies navigate around obstacles (may bunch at corners — acceptable for v1)

**Phase 6: Polish & Tuning**
- **Goal**: Everything looks and feels right at 60fps
- **Scope**: Seed random color variation per obstacle instance; verify spawner doesn't place zombies inside obstacles; adjust obstacle positions that feel wrong in play; performance profiling
- **Success signal**: Stable 60fps with 50 zombies, map reads clearly as abandoned town

### Parallelism Notes

Phase 1 (ground) and Phase 2 (obstacle model) can run in parallel — they touch different files
and have no dependencies on each other. Phase 4 (player) and Phase 5 (zombie) can run in
parallel — they touch different entity files.

---

## Decisions Log

| Decision | Choice | Alternatives | Rationale |
|----------|--------|--------------|-----------|
| Ground rendering | Pre-baked Surface, blit once | Per-frame fill with rects | Pre-bake = O(1) per frame, no performance cost |
| Obstacle visuals | pygame.draw shapes | Sprite pixel art assets | Fast to implement, fits retro aesthetic deliberately |
| Map layout | Fixed hand-crafted | Procedural generation | Full control over aesthetic, no clustering, intentional composition |
| Zombie avoidance | Axis-by-axis push-out | A* pathfinding | Proportional to complexity; zombies sliding is acceptable and fast |
| Bullet collision | Pass through obstacles | Block at obstacle | Keeps gameplay fast-paced; simplifies implementation |
| Color variation | Per-instance random offset (seeded) | Uniform colors | Prevents monotony without requiring art assets |
| Obstacle collision shape | AABB rect for rect obstacles, circle for round | Per-pixel or polygon | Simple, fast, good enough for game feel |

---

## Research Summary

**Technical Context**
- Codebase is pure Pygame 2.6+, Python 3.11+, 60fps target
- No existing tile/map/obstacle system — greenfield implementation
- Collision system in `systems/collisions.py` uses circle distance² — obstacle collision will use AABB separately
- Player boundary clamping in `player.py` update() — natural place to add obstacle push-out
- Zombie AI in `zombie.py` seeks player via direct vector each frame — push-out added after velocity application
- Pre-baked surface approach is standard Pygame pattern for static backgrounds
- Axis-by-axis AABB resolution is a well-established 2D game collision technique (used in countless top-down games)
- 50 zombies × 35 obstacles = 1,750 checks/frame at O(1) per check — well within budget

---

*Generated: 2026-02-26*
*Status: DRAFT*
