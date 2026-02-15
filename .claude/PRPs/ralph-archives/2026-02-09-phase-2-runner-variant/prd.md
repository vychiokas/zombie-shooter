# Special Zombie Variants

## Problem Statement

The zombie shooter currently features only one basic zombie type (green animated sprites, 140 speed, 16 radius) that simply walks toward the player. After a few playthroughs, combat becomes monotonous and predictable with no tactical variety or strategic decision-making required. Players can use the same kiting strategy indefinitely without adapting their approach, resulting in boring, static gameplay that lacks movement challenges and strategic depth.

## Evidence

- **Developer feedback**: "Current zombies are boring, they just run towards me"
- **Observation**: Single zombie behavior pattern (seek player, no variance)
- **Gameplay analysis**: No forced adaptation - same strategy works for entire 60-second session
- **Comparison**: Existing weapon system provides tactical variety (pistol/shotgun/smg), but enemies don't match this depth
- **Market validation**: 2024 top-down zombie shooters commonly feature enemy variants with different types and equipment to force strategic adaptation

## Proposed Solution

Implement 4 special zombie variants with distinct behaviors, visual appearance (unique sprites), and gameplay implications that force players to adapt movement and prioritize targets. Each variant introduces specific tactical challenges:

1. **Runner Zombie** - Fast (2x speed: 280px/s), normal HP (1 shot), red sprites, forces quick reaction and aim tracking
2. **Tank Zombie** - Slow (0.7x speed: 98px/s), high HP (3 shots), larger (24 radius), blue/gray sprites, creates blocking threat and bullet economy pressure
3. **Exploder Zombie** - Normal speed (140px/s), normal HP, orange/yellow sprites, explodes on death dealing AoE damage (80px radius) to player AND other zombies, creates risk/reward tactical decisions
4. **Spitter Zombie** - Slow (100px/s), ranged attacks (300px range), green toxic sprites, shoots acid projectiles at player, forces target prioritization and breaks pure kiting patterns

Variants spawn with weighted probability mixed with normal zombies. Each maintains existing gore effects (blood particles, corpses, blood decals) on death. Exploder AoE damage creates emergent "use exploders to clear crowds" strategy.

**Why this approach**: Leverages existing weapon variant pattern (WEAPON_STATS dict), reuses animation/collision systems, introduces complementary tactical challenges (speed, HP, range, AoE), and creates emergent gameplay through exploder mechanics.

## Key Hypothesis

We believe **adding 4 distinct zombie variants with different movement speeds, HP values, and special abilities** will **create more dynamic, movement-focused gameplay requiring strategic adaptation** for **the developer/player**.

We'll know we're right when **all 4 variants spawn during gameplay, behave distinctly, are visually identifiable at a glance, and force the player to change tactics mid-game (dodging runners, focusing tanks, using exploders strategically, prioritizing spitters)**.

## What We're NOT Building

- **Variant-specific death animations** - All variants use existing death system (corpse + blood pool)
- **Different blood colors per variant** - All use standard red blood effects
- **Variant evolution/mutation** - Zombies don't change type during gameplay
- **Player abilities to counter variants** - No new dash/shield mechanics (movement challenges only)
- **Difficulty ramping of spawn rates** - Spawn probability stays constant across session
- **Weapon effectiveness variance** - All weapons deal same damage to all variants (except Tank HP)
- **Variant sound effects** - Visual distinction only, no unique audio
- **Boss variants** - Standard enemy types only, no special encounters

## Success Metrics

| Metric | Target | How Measured |
|--------|--------|--------------|
| Variant spawning | 100% | All 4 variants spawn during 60s gameplay session |
| Behavioral distinction | 100% | Each variant exhibits correct behavior (speed, HP, special ability) |
| Visual clarity | 100% | Player can identify variant type from sprite at a glance |
| Gore integration | 100% | Blood effects work for all variants (particles, corpses, decals) |
| Performance stability | 60 FPS | Game maintains target framerate with 50 mixed zombies |
| Tactical adaptation | Qualitative | Player changes strategy based on zombie composition (observed during playtesting) |

## Open Questions

- [ ] Should Spitter projectiles have different visuals than player bullets (different color, size)?
- [ ] Should Tank zombies provide more kill score/points than normal zombies?
- [ ] Should Exploder give visual warning before explosion (pulse, change color)?
- [ ] Should variant spawn probability change over time (more special variants late game)?
- [ ] Should Exploder explosion have friendly fire radius falloff or flat damage?
- [ ] Should dead Exploders trigger chain reactions if hit by another explosion?

---

## Users & Context

**Primary User**
- **Who**: Developer/player creating zombie shooter for personal use and presentation
- **Current behavior**: Plays 60-second survival sessions, shoots zombies with weapon variants, kites enemies in circles
- **Trigger**: After a few playthroughs, gameplay feels boring and static - no challenge variety or need to adapt strategy
- **Success state**: Faces mixed zombie compositions requiring tactical decisions (dodge runners, focus-fire tanks, position around exploders, prioritize spitters), feels "more dynamic and involving"

**Job to Be Done**
When **playing the 60-second survival mode**, I want to **face diverse enemy threats requiring different movement and targeting strategies**, so I can **experience engaging, dynamic gameplay that pushes me to dodge, prioritize, and think strategically rather than using the same kiting pattern**.

**Non-Users**
- Players wanting pure aim-skill challenges with no strategic elements
- Players preferring realistic zombie behavior (shambling, no special abilities)
- Players expecting deep progression systems or meta-game unlocks
- Mobile/touch-screen players (desktop pygame only)

---

## Solution Detail

### Core Capabilities (MoSCoW)

| Priority | Capability | Rationale |
|----------|------------|-----------|
| Must | Runner zombie (2x speed, 1 HP) | Forces aim tracking and quick reaction, breaks slow kiting patterns |
| Must | Tank zombie (0.7x speed, 3 HP) | Creates blocking threats, bullet economy pressure, requires focus-fire |
| Must | Exploder zombie (AOE damage on death) | Risk/reward decisions, emergent crowd control, damages player AND zombies |
| Must | Spitter zombie (ranged projectiles) | Forces target prioritization, breaks pure melee kiting, adds dodging challenge |
| Must | Unique sprites per variant | Visual distinction at a glance, player must identify threats quickly |
| Must | Weighted spawn probability | Mix of normal + special variants (not overwhelming, not too rare) |
| Must | Zombie HP system | Tank requires multi-hit, foundation for variant differentiation |
| Must | Exploder AOE damage to zombies | Enables strategic explosion usage, creates emergent gameplay |
| Must | Spitter projectile system | Ranged attacks with collision detection, movement prediction |
| Should | Visual feedback on Tank hit | Show when Tank takes damage but doesn't die (HP indicator or sprite flash) |
| Should | Exploder warning visual | Brief pulse/glow before explosion to signal danger |
| Should | Variant spawn balancing | Tuned probabilities to ensure good mix without overwhelming player |
| Could | Spitter projectile trail effect | Visual clarity for dodging acid shots |
| Could | Chain reaction exploders | Explosions trigger nearby exploders for cascading effects |
| Could | Variant-specific corpse sprites | Dead variants look different (currently reuse living sprite) |
| Won't | Variant-specific animations | All variants use 4-direction walk cycle, no unique moves |
| Won't | Adaptive spawn rates | Spawn probability stays constant (no difficulty ramping by variant) |
| Won't | Player abilities | No dash/shield/special moves to counter variants |

### MVP Scope

**Minimum viable feature set:**
1. ZOMBIE_VARIANTS dict in constants.py with stats (speed, HP, radius, color) for all 5 types (normal + 4 variants)
2. Zombie class modified to accept `variant` parameter, initialize from variant stats
3. HP system added to Zombie class (default 1 for normal/runner/exploder, 3 for tank)
4. Collision handling refactored to reduce HP instead of instant kill
5. Unique sprite sets for each variant (4 directions × 3 frames each = 12 sprites per variant)
6. Spawner.choose_variant() method with weighted random selection
7. Exploder explosion logic on death (AOE damage to player + zombies within radius)
8. Spitter update logic (shoot projectiles at player at interval)
9. Acid projectile entity class (reuse bullet collision system)
10. Visual distinction clear in all variants (different colors, sizes where applicable)

**Placeholder visuals (initial implementation):**
- Can use color-tinted versions of existing zombie sprites if unique sprites not ready
- Tank: 1.5x scale of normal sprite + blue tint
- Runner: red tint
- Exploder: orange/yellow tint
- Spitter: green tint

### User Flow

**Critical path (60-second survival session):**
1. Game starts, spawner begins creating zombies
2. First 10-15 seconds: mostly normal zombies (70% probability)
3. Around 15s mark: first Runner appears (fast red zombie)
4. Player notices increased speed, must adjust aim tracking
5. Around 20s: Tank spawns (slow blue zombie, larger)
6. Player shoots Tank once - zombie continues advancing
7. Player realizes need for focus-fire (3 shots to kill)
8. Around 25s: Exploder spawns (orange zombie)
9. Player shoots Exploder at distance - explosion damages nearby zombies
10. Player learns to position Exploders near zombie clusters
11. Around 30s: Spitter spawns (green zombie, stays at distance)
12. Spitter shoots acid projectile at player
13. Player must prioritize Spitter or dodge projectiles
14. Mid-game (30-45s): Mixed composition creates tactical decisions:
    - Dodge Runners while tracking them
    - Focus-fire Tanks before they block escape routes
    - Position Exploders strategically
    - Prioritize Spitters to reduce projectile spam
15. Late game (45-60s): High zombie count + variant mix creates intense tactical challenge
16. Victory at 60s requires constant adaptation based on composition

**Emergent gameplay patterns:**
- Using Exploder explosions to clear Runner swarms
- Kiting Tanks to create safe zones (they're slow blockers)
- Prioritizing Spitters when surrounded (reduce ranged pressure)
- Letting Exploders get close to clusters before shooting

---

## Technical Approach

**Feasibility**: **HIGH**

**Architecture Notes**
- **Variant stats system**: Add ZOMBIE_VARIANTS dict to constants.py mirroring WEAPON_STATS pattern
  ```python
  ZOMBIE_VARIANTS: dict[str, dict[str, Any]] = {
      "normal": {"speed": 140, "hp": 1, "radius": 16, "color": (100, 200, 100)},
      "runner": {"speed": 280, "hp": 1, "radius": 16, "color": (255, 100, 100)},
      "tank": {"speed": 98, "hp": 3, "radius": 24, "color": (100, 100, 200)},
      "exploder": {"speed": 140, "hp": 1, "radius": 16, "color": (255, 200, 100)},
      "spitter": {"speed": 100, "hp": 1, "radius": 16, "color": (100, 255, 100)},
  }
  ```
- **Zombie class refactor**: Add variant parameter to `__init__`, load variant stats
  ```python
  def __init__(self, pos: Vector2, variant: str = "normal"):
      self.variant = variant
      self.hp = ZOMBIE_VARIANTS[variant]["hp"]
      self.speed = ZOMBIE_VARIANTS[variant]["speed"]
      self.radius = ZOMBIE_VARIANTS[variant]["radius"]
      self.sprites = load_zombie_sprites(variant)  # Load variant-specific sprites
  ```
- **HP system**: Add self.hp attribute, refactor collision to reduce HP instead of instant removal
- **Spawner integration**: Add choose_variant() method with weighted random
  ```python
  def choose_variant(self) -> str:
      return random.choices(
          ["normal", "runner", "tank", "exploder", "spitter"],
          weights=[50, 15, 15, 10, 10],  # 50% normal, 50% variants total
      )[0]
  ```
- **Exploder explosion**: On zombie death, if variant == "exploder", spawn AOE damage
  ```python
  if zombie.hp <= 0:
      if zombie.variant == "exploder":
          self.spawn_explosion(zombie.pos, radius=80)
      # Normal death effects...
  ```
- **Spitter projectiles**: Add shoot_timer to Zombie, create AcidProjectile entities
  ```python
  # In Zombie.update() for spitter variant
  if self.variant == "spitter":
      if distance_to_player < 300 and self.shoot_timer <= 0:
          direction = (player_pos - self.pos).normalize()
          projectiles.append(AcidProjectile(self.pos, direction))
          self.shoot_timer = 2.0  # 2 second cooldown
  ```
- **Asset loading**: Extend loader.py to load variant sprite folders
  ```python
  def load_zombie_sprites(variant: str) -> dict:
      zombies_dir = ASSETS_DIR / "zombies" / variant
      # Load walk_up.png, walk_down.png, walk_left.png, walk_right.png
  ```

**Key technical decisions:**
1. **Single Zombie class with variant parameter** (not inheritance) - matches weapon pattern, simpler maintenance
2. **Weighted random spawning** - ensures mix without overwhelming with specials
3. **Reuse bullet collision for acid projectiles** - avoid duplicating collision logic
4. **HP-based damage system** - foundation for future weapon damage variance if needed
5. **Explosion as separate function** - reusable for potential future explosive weapons

**Technical Risks**

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Exploder AOE needs zombie-to-zombie collision | Medium | Reuse check_bullet_zombie_collisions pattern, iterate zombies in radius |
| 50 mixed zombies degrade performance | Low | Variants reuse same systems, only behavioral differences (tested at 50 normal zombies at 60 FPS) |
| Unique sprites increase asset loading time | Low | Module-level caching already implemented, load once per variant |
| Tank multi-hit feels unresponsive (no feedback) | Medium | Add visual feedback (sprite flash, particle burst on hit) |
| Spitter projectiles hard to see/dodge | Medium | Use distinct color (green/yellow), optional trail effect, test visibility |
| Variant balance creates frustrating compositions | High | Tune spawn weights through playtesting, adjust probabilities |

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
| 1 | Core variant system & HP | Add ZOMBIE_VARIANTS dict, HP system, refactor collision for HP reduction | complete | - | - | [phase-1-core-variant-system-hp.plan.md](../plans/completed/phase-1-core-variant-system-hp.plan.md) |
| 2 | Runner variant | Implement fast zombie with unique sprites | complete | with 3 | 1 | - |
| 3 | Tank variant | Implement slow, high-HP zombie with larger hitbox and unique sprites | pending | with 2 | 1 | - |
| 4 | Exploder variant | Implement explosion on death with AOE damage to player and zombies | pending | - | 1, 2, 3 | - |
| 5 | Spitter variant | Implement ranged zombie with acid projectile attacks | pending | - | 1 | - |
| 6 | Visual polish & balance | Tune spawn weights, add hit feedback, test variant compositions | pending | - | 2, 3, 4, 5 | - |

### Phase Details

**Phase 1: Core variant system & HP**
- **Goal**: Establish foundation for variant differentiation
- **Scope**:
  - Add ZOMBIE_VARIANTS dict to constants.py with stats for all 5 types
  - Modify Zombie.__init__() to accept variant parameter, load variant stats
  - Add self.hp attribute to Zombie class
  - Refactor collision handling in PlayScene to reduce HP instead of instant kill
  - Only remove zombie when hp <= 0
  - Add Spawner.choose_variant() with weighted random (50% normal, 50% variants)
  - Update PlayScene to pass variant to Zombie constructor
- **Success signal**: Can spawn zombies with different speeds/HP, Tank takes 3 shots to kill, Runner/Normal take 1 shot

**Phase 2: Runner variant**
- **Goal**: Add fast-moving zombie that forces aim tracking
- **Scope**:
  - Create assets/zombies/runner/ directory with red-tinted sprites (4 directions × 3 frames)
  - Set Runner speed to 280 (2x normal) in ZOMBIE_VARIANTS
  - Verify spawner includes Runner in random selection
  - Test Runner movement and collision
- **Success signal**: Red zombies spawn, move 2x faster, die in 1 hit, visually distinct

**Phase 3: Tank variant**
- **Goal**: Add slow, tanky zombie that creates blocking threats
- **Scope**:
  - Create assets/zombies/tank/ directory with blue/gray sprites (4 directions × 3 frames)
  - Set Tank speed to 98 (0.7x), HP to 3, radius to 24 in ZOMBIE_VARIANTS
  - Update collision handling to show Tank continues after first hit
  - Optional: Add visual feedback on hit (sprite flash or particle burst)
- **Success signal**: Blue zombies spawn, move slowly, require 3 hits, larger collision radius, visually distinct

**Phase 4: Exploder variant**
- **Goal**: Add explosive zombie with AOE damage to player and other zombies
- **Scope**:
  - Create assets/zombies/exploder/ directory with orange/yellow sprites
  - Add explosion logic to PlayScene death handler:
    - Check if zombie.variant == "exploder"
    - Spawn explosion visual effect (particle burst)
    - Apply AOE damage to player (reduce HP if within 80px)
    - Apply AOE damage to zombies (iterate, reduce HP if within 80px)
  - Add EXPLODER_AOE_RADIUS = 80 and EXPLODER_DAMAGE = 1 to constants
  - Optional: Add warning visual (pulse) 0.5s before explosion
- **Success signal**: Orange zombies explode on death, damage player and nearby zombies within radius, creates tactical opportunity

**Phase 5: Spitter variant**
- **Goal**: Add ranged zombie that shoots acid projectiles
- **Scope**:
  - Create assets/zombies/spitter/ directory with green toxic sprites
  - Create AcidProjectile entity class (similar to Bullet):
    - Attributes: pos, vel, radius (6px), lifetime (2s), color (green/yellow)
    - Update: move by velocity, decrement lifetime
    - Draw: render acid blob with trail effect
  - Add shoot_timer to Zombie class (default 0)
  - Modify Zombie.update() for Spitter:
    - Check if distance to player < 300 and shoot_timer <= 0
    - Create AcidProjectile toward player position
    - Set shoot_timer = 2.0 (cooldown)
  - Add player-acid collision detection in PlayScene (reuse bullet collision pattern)
  - Add SPITTER_RANGE = 300, SPITTER_COOLDOWN = 2.0 to constants
- **Success signal**: Green zombies spawn, stay at distance, shoot acid projectiles at player, player takes damage from projectiles

**Phase 6: Visual polish & balance**
- **Goal**: Ensure variants feel good and spawn in good mix
- **Scope**:
  - Playtest 10+ full sessions, observe variant compositions
  - Tune spawn weights if too many/few specials (adjust Spawner.choose_variant() probabilities)
  - Add hit feedback for Tank if needed (sprite flash or particle burst)
  - Verify all variants have distinct silhouettes and colors
  - Check performance with 50 mixed zombies (should maintain 60 FPS)
  - Test edge cases: all exploders, all tanks, all spitters
  - Adjust explosion radius, spitter range, Tank HP if balance feels off
  - Run pytest to ensure no regressions
- **Success signal**: Variants spawn in good mix, player must adapt tactics, no performance issues, all tests pass

### Parallelism Notes

Phases 2 and 3 can run in parallel as they implement independent variants:
- Phase 2 (Runner) modifies zombie speed parameter and adds fast variant sprites
- Phase 3 (Tank) modifies HP/radius and adds slow variant sprites

Both depend on Phase 1 (core variant system + HP) but are otherwise independent. They can be implemented in separate branches or by different developers.

Phase 5 (Spitter) can also run in parallel with Phases 2-4 if projectile system is developed independently, though it shares the Phase 1 dependency.

---

## Decisions Log

| Decision | Choice | Alternatives | Rationale |
|----------|--------|--------------|-----------|
| Variant implementation | Single Zombie class with variant parameter | Inheritance hierarchy (TankZombie, RunnerZombie classes) | Matches existing weapon system pattern, simpler to maintain, easier to add new variants |
| Visual distinction | Unique sprite assets per variant | Color tinting only | User requirement: "unique sprites", clearer visual distinction at a glance |
| HP system approach | Add HP attribute to Zombie class | Create HealthComponent system | Simpler, matches player HP pattern, sufficient for variant needs |
| Exploder damage targets | Damages player AND zombies | Damages player only | Creates emergent "use exploders to clear crowds" strategy, more dynamic gameplay |
| Spawn probability | Weighted random (50% normal, 50% variants) | Equal probability all types | Ensures normal zombies remain base threat, specials feel special not overwhelming |
| Spitter projectile | Reuse bullet collision system | Create separate projectile collision | Avoid code duplication, proven collision detection, simpler maintenance |
| Tank HP value | 3 hits | 5 hits, scaling HP | 3 hits feels significant but not bullet-sponge, testable, tunable later |
| Variant spawn timing | Constant probability throughout session | Ramp up special variants over time | Simpler implementation, defer difficulty tuning to later iteration |
| Asset loading | Extend existing loader with variant parameter | Create new variant asset manager | Leverages existing module-level caching, consistent pattern |

---

## Research Summary

**Market Context**
- Top-down zombie shooters in 2024 commonly feature enemy variants with different types and equipment to force tactical adaptation
- Common patterns: mixing shooting with tactical positioning, resource management, and preparation for hordes
- Games use variants to create different player strategies - some enemies linear/predictable, others randomized
- Dash mechanics are common for movement-focused gameplay (not in scope for this feature)
- Successful variants create complementary challenges: speed (runners), tanking (high HP), area denial (exploders), range (spitters)

**Technical Context**
- Codebase has clean architecture with well-separated entities, systems, and constants
- Weapon system provides exact template for variant implementation (WEAPON_STATS dict, variant parameter pattern)
- Player already has HP system that can be copied to zombies
- Module-level sprite caching already implemented for efficient asset reuse
- Pygame supports color tinting via BLEND modes (used in blood particle system)
- Collision handling is clean and refactorable (currently one-shot kill, needs HP reduction)
- Spawner has perfect integration point: `self.zombies.append(Zombie(spawn_pos))`
- Animation system supports variant sprites through asset loader extension
- Performance baseline: 50 zombies at 60 FPS with current systems

**Technical Feasibility**
- Runner: VERY EASY (trivial speed parameter change)
- Tank: EASY (HP system + size adjustment)
- Exploder: MODERATE (AOE damage logic new, but pattern exists in collision system)
- Spitter: MODERATE (projectile entity new, but similar to existing Bullet class)
- Overall: HIGH feasibility with estimated 6-8 hours total implementation time

**Key Insight**: The weapon variant system (pistol/shotgun/smg) implemented in PRD-001 provides the exact architectural template for zombie variants. Both use the same pattern: stats dict + variant parameter + specialized behavior. This significantly de-risks implementation.

---

*Generated: 2026-02-09*
*Status: DRAFT - ready for implementation*
