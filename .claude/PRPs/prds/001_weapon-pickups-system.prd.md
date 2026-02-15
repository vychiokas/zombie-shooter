# Weapon Pickups System

## Problem Statement

The zombie shooter currently offers only a single weapon type, leading to monotonous gameplay with no tactical variety or progression. Players experience repetitive combat encounters with no opportunity to adapt their playstyle or discover new mechanics during a 60-second survival session.

## Evidence

- **Current state**: Single weapon type (basic shooting) with fixed 0.15s cooldown
- **Observation**: No pickups or items exist in the game currently - clean slate for implementation
- **Market validation**: PyArena and similar pygame shooters demonstrate that weapon variety (Pistol/Shotgun/SMG) is a core engagement mechanic for top-down shooters
- **Assumption**: Needs playtesting to validate engagement improvement

## Proposed Solution

Implement a weapon pickup system with three distinct weapon types (Pistol, Shotgun, SMG), each with unique fire patterns and rates. Pickups spawn periodically (~15 seconds) on the map, can be collected by player contact, and replace the currently equipped weapon. A HUD element displays the active weapon name to provide clear feedback.

**Why this approach**: Leverages existing clean Scene/Entity/System architecture, uses proven game design patterns (weapon spawning, instant swap on pickup), and requires minimal UI (text-only HUD).

## Key Hypothesis

We believe **adding weapon variety with distinct behaviors** will **increase gameplay engagement and tactical depth** for **players of the zombie shooter**.

We'll know we're right when **playtesting shows players actively seeking pickups and adapting tactics based on weapon type**.

## What We're NOT Building

- **Ammo system** - Weapons have infinite ammo to keep gameplay simple
- **Weapon inventory/switching** - Only one weapon equipped at a time, pickups replace current weapon
- **Weapon sprites** - Using placeholder shapes (rectangles/circles) only
- **Weapon upgrades/levels** - Single tier per weapon type
- **Damage variation** - All weapons deal same damage (1-shot zombies), differentiation is via fire pattern/rate
- **Pickup choice UI** - Automatic swap on contact, no "press E to pick up"

## Success Metrics

| Metric | Target | How Measured |
|--------|--------|--------------|
| Feature completeness | 100% | All weapons spawn, can be picked up, fire correctly |
| Visual feedback | 100% | HUD displays current weapon name |
| Code quality | Pass | `pytest -q` passes all tests |
| Runtime stability | No crashes | `python -m game.main` runs 60s without errors |

## Open Questions

- [ ] Should pickups despawn after X seconds if not collected?
- [ ] Should pickup spawn rate increase with difficulty/time?
- [ ] What happens if player walks over same weapon type already equipped?
- [ ] Should there be visual/audio feedback on weapon swap?

---

## Users & Context

**Primary User**
- **Who**: Player (developer/tester initially, potential end users later)
- **Current behavior**: Survives 60 seconds shooting zombies with single weapon, focuses on movement and positioning
- **Trigger**: Gameplay becomes repetitive after first few sessions
- **Success state**: Player adapts tactics based on available weapons (kiting with pistol, holding position with shotgun, aggressive with SMG)

**Job to Be Done**
When **playing survival mode**, I want to **discover and use different weapons**, so I can **experience varied combat encounters and adapt my strategy**.

**Non-Users**
- Players expecting realistic weapon mechanics (reloading, magazine management)
- Players wanting complex inventory systems
- Mobile/touch-screen players (desktop pygame only)

---

## Solution Detail

### Core Capabilities (MoSCoW)

| Priority | Capability | Rationale |
|----------|------------|-----------|
| Must | Pistol (default weapon) | Baseline weapon, player starts with this |
| Must | Shotgun pickup (spread fire) | Provides area-denial, close-range tactical option |
| Must | SMG pickup (fast fire rate) | Provides high-DPS, aggressive playstyle option |
| Must | Pickup spawning (~15s intervals) | Ensures weapons appear during 60s gameplay window |
| Must | Player-pickup collision detection | Core mechanic - must be able to collect weapons |
| Must | Weapon swapping on pickup | Replaces current weapon with new one |
| Must | HUD weapon display | Player must know current weapon |
| Must | Weapon-specific fire behavior | Shotgun spreads, SMG fires faster, pistol baseline |
| Should | Visual distinction for pickups | Different shapes/colors per weapon type |
| Should | Pickup spawn location variety | Spawn at random positions (not just center) |
| Could | Pickup glow/pulse animation | Polish - helps visibility |
| Could | Weapon swap sound effect | Feedback improvement |
| Won't | Ammo system | Deferred - adds complexity without core value |
| Won't | Weapon damage variation | Deferred - fire pattern differentiation is sufficient |

### MVP Scope

**Minimum viable feature set:**
1. Three weapon types with distinct stats (fire rate, bullet count, spread)
2. Pickup entity spawns every ~15 seconds at random map position
3. Player collision with pickup triggers weapon swap
4. HUD text shows "Weapon: [name]"
5. Weapons fire according to their stats (shotgun = 5 bullets spread, SMG = 0.08s cooldown, pistol = 0.15s cooldown)

**Placeholder visuals:**
- Pistol pickup: Small yellow rectangle
- Shotgun pickup: Medium red rectangle
- SMG pickup: Small green rectangle
- No particle effects or animations

### User Flow

**Critical path:**
1. Player starts game with pistol equipped
2. HUD displays "Weapon: Pistol" (top-left or top-center)
3. After ~15 seconds, pickup spawns at random location (e.g., shotgun)
4. Player navigates toward pickup while avoiding zombies
5. On collision with pickup, weapon swaps instantly
6. HUD updates to "Weapon: Shotgun"
7. Player shoots - 5 bullets fire in spread pattern
8. Process repeats with new pickups spawning every ~15s

---

## Technical Approach

**Feasibility**: **HIGH**

**Architecture Notes**
- **Entity pattern**: Create `Pickup` class following existing pattern (pos, radius, update, draw)
- **Weapon stats**: Add `WEAPON_STATS` dict to `constants.py` with fire rate, spread, bullet count
- **Player state**: Add `current_weapon: str` attribute to Player class
- **Collision reuse**: Leverage existing `check_collision_circle()` for player-pickup detection
- **Spawning**: Add `PickupSpawner` or integrate into PlayScene with timer-based spawning
- **HUD integration**: Extend existing HUD rendering with weapon text line
- **Multi-bullet firing**: Modify `Player.shoot()` to return `list[Bullet]` for shotgun spread

**Key technical decisions:**
1. **Weapon data structure**: Use dict-based config in constants rather than weapon classes (simpler, data-driven)
2. **Pickup spawning**: Timer-based in PlayScene rather than separate spawner system (fewer moving parts)
3. **Bullet modification**: Extend Bullet class with optional `lifetime` or keep existing TTL approach

**Technical Risks**

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Shotgun spread creates too many bullets | Medium | Limit spread to 5 bullets, test performance |
| Pickup collision feels unresponsive | Low | Use radius of 25-30 pixels for generous hitbox |
| HUD text overlaps with existing UI | Low | Place weapon text in top-center or dedicated corner |
| Weapon swap loses player position | Low | Swap only changes weapon state, not position/velocity |

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
| 1 | Weapon data model | Define weapon stats in constants, add player weapon state | complete | - | - | [phase-1-weapon-data-model.plan.md](../../plans/phase-1-weapon-data-model.plan.md) |
| 2 | Pickup entity | Create Pickup class with rendering and collision | complete | - | 1 | [phase-2-pickup-entity.plan.md](../../plans/phase-2-pickup-entity.plan.md) |
| 3 | Weapon behavior | Implement fire patterns (spread, rate) for each weapon | complete | with 2 | 1 | - |
| 4 | Pickup spawning | Add timer-based pickup spawning to PlayScene | complete | - | 2 | [phase-4-pickup-spawning.plan.md](../../plans/phase-4-pickup-spawning.plan.md) |
| 5 | HUD integration | Display current weapon name in HUD | complete | - | 1 | [phase-5-hud-integration.plan.md](../../plans/phase-5-hud-integration.plan.md) |
| 6 | Testing & validation | Add tests, verify gameplay, fix bugs | complete | - | 3, 4, 5 | [phase-6-testing-validation.plan.md](../../plans/phase-6-testing-validation.plan.md) |

### Phase Details

**Phase 1: Weapon data model**
- **Goal**: Establish weapon type system and player weapon state
- **Scope**:
  - Add `WEAPON_STATS` dict to `constants.py` with fire_rate, bullet_count, spread_angle
  - Add `current_weapon: str = "pistol"` to Player class
  - Define constants for pickup spawn rate and radius
- **Success signal**: Constants defined, player has weapon attribute, tests pass

**Phase 2: Pickup entity**
- **Goal**: Create collectible pickup items that spawn on map
- **Scope**:
  - Create `entities/pickup.py` with Pickup class
  - Implement `update(dt)`, `draw(screen)` methods
  - Use placeholder shapes (rectangles, colored by weapon type)
  - Add `weapon_type` attribute
- **Success signal**: Pickup renders on screen, has collision radius

**Phase 3: Weapon behavior**
- **Goal**: Different weapons fire differently
- **Scope**:
  - Modify `Player.shoot()` to return `list[Bullet]` instead of `Bullet | None`
  - Implement pistol: single bullet, 0.15s cooldown
  - Implement shotgun: 5 bullets in spread pattern, 0.5s cooldown
  - Implement SMG: single bullet, 0.08s cooldown
  - Update PlayScene to handle list of bullets from single shot
- **Success signal**: Each weapon fires with distinct pattern when tested manually

**Phase 4: Pickup spawning**
- **Goal**: Pickups appear periodically during gameplay
- **Scope**:
  - Add `pickup_spawn_timer` to PlayScene
  - Spawn random weapon pickup every ~15 seconds
  - Spawn at random position (avoid edges)
  - Implement player-pickup collision check
  - On collision: set `player.current_weapon`, remove pickup
- **Success signal**: Pickups spawn automatically, player can collect them, weapon swaps

**Phase 5: HUD integration**
- **Goal**: Player sees current weapon name
- **Scope**:
  - Add weapon text rendering to `PlayScene.draw()`
  - Position in top-center or top-left
  - Format: "Weapon: [weapon_name]" in white text
- **Success signal**: HUD updates when weapon changes

**Phase 6: Testing & validation**
- **Goal**: Ensure feature works reliably
- **Scope**:
  - Add unit tests for weapon stats, pickup collision
  - Manual playtest: verify each weapon fires correctly
  - Run `python -m game.main` - play full 60s session
  - Run `pytest -q` - all tests pass
  - Fix any bugs discovered
- **Success signal**: Both validation commands pass, gameplay feels responsive

### Parallelism Notes

Phases 2 and 3 can run in parallel as they touch different domains:
- Phase 2 (Pickup entity) modifies `entities/pickup.py` (new file) and adds pickup rendering
- Phase 3 (Weapon behavior) modifies `entities/player.py` and `entities/bullet.py` shooting logic

Both depend on Phase 1 (weapon data model) being complete, but are otherwise independent.

---

## Decisions Log

| Decision | Choice | Alternatives | Rationale |
|----------|--------|--------------|-----------|
| Weapon swap behavior | Instant replace on contact | Hold to swap, inventory system | Keeps gameplay fast-paced, reduces UI complexity |
| Weapon differentiation | Fire pattern + rate | Damage + ammo + rate | Simpler balance, avoids ammo management complexity |
| Pickup spawn method | Timer-based (~15s) | Spawn on zombie kill | Predictable cadence ensures weapons appear in 60s window |
| Visual style | Placeholder shapes | Sprites/assets | Matches project constraint, faster iteration |
| Bullet return type | `list[Bullet]` | Keep single bullet, handle spread internally | Cleaner separation, PlayScene treats all bullets uniformly |
| Shotgun spread pattern | Fixed 5 bullets, ±30° spread | Random spread, more bullets | Consistent behavior, testable, reasonable performance |
| SMG fire rate | 0.08s (12.5 shots/sec) | 0.05s (20 shots/sec) | 2x pistol rate feels distinct without overwhelming screen |

---

## Research Summary

**Market Context**
- Top-down shooters commonly use class-based or data-driven weapon systems
- PyArena demonstrates the exact weapon set (Pistol/Shotgun/SMG) with differentiation via fire rate and spread
- Common patterns: pickups as world entities, instant swap on contact, visual/audio feedback for weapon change
- Weapon balance typically achieved through fire rate, spread/accuracy, and damage tradeoffs

**Technical Context**
- Codebase uses clean Scene/Entity/System architecture - well-suited for this feature
- Existing collision system (`check_collision_circle`) is efficient and reusable
- Player entity is self-contained - adding weapon state is isolated change
- No existing pickup system - clean slate implementation
- HUD uses simple pygame font rendering - weapon text integrates easily
- Game loop uses delta time consistently - weapon cooldowns integrate naturally

**Sources:**
- [TopDown Engine Weapons Documentation](https://topdown-engine-docs.moremountains.com/weapons.html)
- [Weapon System Design Patterns - GameDev.net](https://www.gamedev.net/forums/topic/587596-weapon-system-in-top-down-shooter/)
- [PyArena Pygame Project](https://www.pygame.org/project-pyarena-484-.html)
- [Pygame Weapons Source Code](https://scriptline-studios.itch.io/pygame-weapons-source-code)

---

*Generated: 2026-01-26*
*Status: DRAFT - needs playtesting validation*
