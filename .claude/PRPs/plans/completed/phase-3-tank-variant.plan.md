# Feature: Phase 3 - Tank Zombie Variant

## Summary

Implement the Tank zombie variant - a slow-moving (98 px/s, 0.7x normal speed), high-HP enemy (3 hits to kill) with a larger collision hitbox (24px radius vs 16px). This variant creates blocking threats and forces players to commit resources (3 bullets vs 1) while managing other zombies. Tank uses the same HP system from Phase 1 but is the first variant to meaningfully test multi-hit gameplay. Visual distinction comes from blue/gray-tinted sprites.

## User Story

As a player
I want to face slow but durable zombies that absorb damage
So that I must make tactical decisions about focus-fire, bullet economy, and escape route management

## Problem Statement

Current zombie variants (Normal, Runner, Spitter) all die in 1 hit, creating a binary threat model: "hit = dead". There's no sustained threat or resource commitment required. Players don't need to track partially-damaged enemies or make focus-fire decisions. The HP system from Phase 1 exists but isn't meaningfully tested beyond 1-shot kills.

**Testable Success**: Blue tank zombies spawn, move at 98 px/s (0.7x normal), require exactly 3 bullet hits to kill, have 24px collision radius (larger hitbox), and remain visually distinct during gameplay.

## Solution Statement

Tank variant leverages the existing HP system (Phase 1) with HP=3, combined with reduced speed (0.7x) and increased collision radius (24px). No new systems needed - just parameter tuning. The challenge: Tank must survive 2 hits without visual feedback (currently, there's no "damaged state" indication). Optional enhancement: add hit feedback (sprite flash or particle burst) to show Tank taking damage but surviving.

## Metadata

| Field            | Value                                    |
| ---------------- | ---------------------------------------- |
| Type             | NEW_CAPABILITY                           |
| Complexity       | LOW                                      |
| Systems Affected | constants, assets, optional: zombie.py   |
| Dependencies     | pygame>=2.6.0, Python 3.11+              |
| Estimated Tasks  | 3 (core) + 1 (optional visual feedback)  |

---

## UX Design

### Before State
```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌─────────────┐                                                             ║
║   │   Player    │ shoots → zombie dies (1 hit)                                ║
║   │  (center)   │                                                             ║
║   └─────────────┘                                                             ║
║         ▲                                                                     ║
║         │                                                                     ║
║    ┌────┴────┐                                                                ║
║    │ Normal  │ HP=1, 1 shot kills                                             ║
║    │ Zombie  │                                                                ║
║    └─────────┘                                                                ║
║         │                                                                     ║
║    ┌────▼────┐                                                                ║
║    │ Runner  │ HP=1, 1 shot kills (fast)                                      ║
║    │ Zombie  │                                                                ║
║    └─────────┘                                                                ║
║                                                                               ║
║   USER_FLOW: See zombie → shoot once → zombie dies → move on                  ║
║   PAIN_POINT: No sustained threats, no resource commitment, binary outcomes   ║
║   DATA_FLOW: Bullet hits zombie → HP-=1 → HP<=0 → remove zombie              ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌─────────────┐                                                             ║
║   │   Player    │ shoots Tank → Tank continues advancing                      ║
║   │  (center)   │ shoots again → Tank still coming                            ║
║   └─────────────┘ shoots 3rd time → Tank dies                                 ║
║         ▲                                                                     ║
║         │                                                                     ║
║    ┌────┴────┐                                                                ║
║    │  TANK   │ HP=3, requires 3 shots (slow, large hitbox)                    ║
║    │ (Blue)  │ Speed: 98px/s (0.7x), Radius: 24px (1.5x)                     ║
║    └─────────┘                                                                ║
║         │                                                                     ║
║         ├─── Shot 1: HP=3→2 (Tank survives, keeps advancing)                  ║
║         ├─── Shot 2: HP=2→1 (Tank survives, keeps advancing)                  ║
║         └─── Shot 3: HP=1→0 (Tank dies, spawns gore)                          ║
║                                                                               ║
║   USER_FLOW:                                                                  ║
║   1. Tank spawns → moves slowly toward player                                 ║
║   2. Player shoots → Tank shrugs off hit, continues                           ║
║   3. Player realizes need for focus-fire (commit 3 shots)                     ║
║   4. Tactical decision: "Do I finish this Tank or switch to nearby Runner?"   ║
║   5. Larger hitbox makes Tank easier to hit but harder to avoid               ║
║                                                                               ║
║   VALUE_ADD:                                                                  ║
║   - Bullet economy pressure (3 shots vs 1)                                    ║
║   - Focus-fire decisions (commit to Tank or switch targets?)                  ║
║   - Blocking threat (slow but durable, creates escape route pressure)         ║
║   - Hitbox variety (24px radius = 1.5x normal, easier to collide)            ║
║                                                                               ║
║   DATA_FLOW:                                                                  ║
║   Bullet hits Tank → HP-=1 → HP=2 (survives) → Tank continues                 ║
║   Bullet hits Tank → HP-=1 → HP=1 (survives) → Tank continues                 ║
║   Bullet hits Tank → HP-=1 → HP=0 → remove Tank, spawn gore                   ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location              | Before                     | After                                  | User Impact                             |
| --------------------- | -------------------------- | -------------------------------------- | --------------------------------------- |
| Zombie spawning       | Normal/Runner/Spitter only | Tanks spawn at 15% rate                | Player sees slow blue zombies appearing |
| Bullet collision      | 1 hit = kill               | Tank takes 3 hits to kill              | Must commit 3 shots per tank            |
| Movement pressure     | Normal/Runner speeds only  | Tank moves slowly (0.7x)               | Easier to kite but creates blockage     |
| Collision avoidance   | All 16px radius            | Tank has 24px radius (50% larger)      | Harder to avoid, easier to hit          |
| Resource management   | No bullet economy pressure | Tank = 3x bullet cost                  | Must decide: finish Tank or switch?     |
| Tactical depth        | Simple priority            | Focus-fire vs target switching tension | More strategic depth                    |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File                                                                                | Lines   | Why Read This                                    |
| -------- | ----------------------------------------------------------------------------------- | ------- | ------------------------------------------------ |
| P0       | `/zombie-shooter/src/game/core/constants.py`                                        | 56-87   | ZOMBIE_VARIANTS structure - pattern to follow    |
| P0       | `/zombie-shooter/.claude/PRPs/ralph-archives/2026-02-09-phase-2-runner-variant/`   | all     | Runner implementation - exact pattern for Tank   |
| P1       | `/zombie-shooter/src/assets/zombies/runner/`                                        | all     | Sprite tinting pattern to copy for blue tint     |
| P2       | `/zombie-shooter/tests/test_zombie_integration.py`                                  | all     | Test patterns for variant attributes             |

**External Documentation:**
| Source | Section | Why Needed |
|--------|---------|------------|
| [Pygame Docs v2.6 - BLEND modes](https://www.pygame.org/docs/ref/surface.html#pygame.Surface.blit) | BLEND_RGBA_ADD | Color tinting sprites |

---

## Patterns to Mirror

**VARIANT CONSTANTS PATTERN:**
```python
# SOURCE: /zombie-shooter/src/game/core/constants.py:56-74
# COPY THIS PATTERN FOR TANK:
ZOMBIE_VARIANTS: dict[str, dict[str, int | float]] = {
    "normal": {
        "speed": 140,
        "hp": 1,
        "radius": 16,
        "weight": 7,  # 70% spawn rate
    },
    "runner": {
        "speed": 280,  # 2x speed
        "hp": 1,
        "radius": 16,
        "weight": 1.5,  # 15% spawn rate
    },
    # ADD TANK HERE with speed=98, hp=3, radius=24, weight=1.5
}
```

**SPRITE TINTING PATTERN:**
```python
# SOURCE: Phase 2 Runner implementation (from archives)
# COPY THIS PATTERN BUT CHANGE TO BLUE:
tinted = original.copy()
red_overlay = pygame.Surface(original.get_size()).convert_alpha()
red_overlay.fill((255, 80, 80, 0))  # For runner (red tint)
tinted.blit(red_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

# FOR TANK: Use blue tint instead
# blue_overlay.fill((80, 120, 255, 0))  # Blue tint
```

**HP SYSTEM (ALREADY EXISTS):**
```python
# SOURCE: /zombie-shooter/src/game/entities/zombie.py:51
# NO CHANGES NEEDED - HP system already implemented in Phase 1:
self.hp = float(variant_stats["hp"])

# SOURCE: /zombie-shooter/src/game/scenes/play.py:193
# Collision already handles multi-hit:
zombie.hp -= 1  # Reduce HP instead of instant kill
if zombie.hp <= 0:
    # Only remove zombie when HP depleted
```

**VARIANT SPRITE LOADING (ALREADY EXISTS):**
```python
# SOURCE: /zombie-shooter/src/game/assets/loader.py:74-119
# NO CHANGES NEEDED - loader already handles variant parameter:
def load_zombie_sprites(
    sprite_size: int = 32, frame_count: int = 3, variant: str = "normal"
) -> dict[str, list[pygame.Surface]]:
    # Variant-specific directory handling already implemented
    if variant == "normal":
        zombies_dir = ASSETS_DIR / "zombies"
    else:
        zombies_dir = ASSETS_DIR / "zombies" / variant
```

**TEST STRUCTURE:**
```python
# SOURCE: /zombie-shooter/tests/test_zombie_integration.py
# COPY THIS PATTERN FOR TANK TESTS:
def test_zombie_has_correct_variant_stats() -> None:
    """Test that zombie initializes with variant-specific stats."""
    # For tank: should have HP=3, speed=98, radius=24
    zombie = Zombie(pygame.Vector2(100, 100), variant="tank")
    assert zombie.hp == 3
    assert zombie.speed == 98
    assert zombie.radius == 24
```

---

## Files to Change

| File                                                         | Action | Justification                                  |
| ------------------------------------------------------------ | ------ | ---------------------------------------------- |
| `zombie-shooter/src/game/core/constants.py`                  | UPDATE | Enable tank variant (change weight from 0 to 1.5) |
| `zombie-shooter/src/assets/zombies/tank/walk_down.png`       | CREATE | Blue-tinted tank sprite (down direction)      |
| `zombie-shooter/src/assets/zombies/tank/walk_up.png`         | CREATE | Blue-tinted tank sprite (up direction)        |
| `zombie-shooter/src/assets/zombies/tank/walk_left.png`       | CREATE | Blue-tinted tank sprite (left direction)      |
| `zombie-shooter/src/assets/zombies/tank/walk_right.png`      | CREATE | Blue-tinted tank sprite (right direction)     |

---

## NOT Building (Scope Limits)

Explicit exclusions to prevent scope creep:

- **Hit visual feedback** - Tank taking damage shows no visual indication (sprite flash, particle burst, etc.). This is optional and can be added in Phase 6 polish if needed.
- **Different death animations** - Tank uses same gore effects as other zombies (blood particles, corpse, blood pool).
- **Armor mechanics** - No damage reduction or penetration system. Tank just has 3 HP.
- **Dynamic HP scaling** - Tank always has 3 HP, doesn't scale with time or difficulty.
- **Weapon effectiveness variance** - All weapons deal 1 damage per hit to Tank (3 pistol shots = 3 shotgun pellets = 3 SMG bullets).
- **Tank charge/slam attacks** - Tank is purely defensive (high HP), no special attacks.
- **Size scaling** - Tank sprite size stays same as normal zombies, only hitbox (radius) changes.
- **Tank-specific sounds** - No unique audio for Tank footsteps or death.

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: UPDATE `zombie-shooter/src/game/core/constants.py`

- **ACTION**: ENABLE tank variant by changing weight from 0 to 1.5
- **IMPLEMENT**:
  ```python
  "tank": {
      "speed": 98,  # 0.7x speed (98/140 = 0.7)
      "hp": 3,  # Requires 3 hits
      "radius": 24,  # Larger hitbox (24/16 = 1.5x)
      "weight": 1.5,  # 15% spawn rate (enabled in Phase 3)
  },
  ```
- **MIRROR**: Existing ZOMBIE_VARIANTS structure (lines 56-87)
- **LOCATION**: Update line 83 - change weight from 0 to 1.5
- **GOTCHA**: Tank stats already exist in constants (from Phase 1), just need to enable spawning
- **VALIDATE**:
  ```bash
  /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/.venv/bin/python -m ruff check zombie-shooter/src/game/core/constants.py
  ```

### Task 2: CREATE tank zombie sprites

- **ACTION**: CREATE blue-tinted sprite assets for tank variant
- **IMPLEMENT**: Python script to generate blue-tinted sprites from normal zombie sprites
  ```python
  """Generate blue-tinted tank zombie sprites."""
  from pathlib import Path
  import pygame

  pygame.init()
  pygame.display.set_mode((1, 1))

  script_dir = Path(__file__).resolve().parent
  assets_dir = script_dir / "src/assets/zombies"
  tank_dir = script_dir / "src/assets/zombies/tank"
  tank_dir.mkdir(parents=True, exist_ok=True)

  directions = ["walk_down", "walk_up", "walk_left", "walk_right"]

  for direction in directions:
      original_path = assets_dir / f"{direction}.png"
      original = pygame.image.load(str(original_path))

      # Create blue-tinted version
      tinted = original.copy()
      blue_overlay = pygame.Surface(original.get_size()).convert_alpha()
      blue_overlay.fill((80, 120, 255, 0))  # Blue tint (tank armor color)
      tinted.blit(blue_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

      # Optional: Add gray tint for "armored" look
      gray_overlay = pygame.Surface(original.get_size()).convert_alpha()
      gray_overlay.fill((60, 60, 60, 0))  # Slight gray for metallic look
      tinted.blit(gray_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

      # Save
      output_path = tank_dir / f"{direction}.png"
      pygame.image.save(tinted, str(output_path))
      print(f"Created {output_path}")

  print("Tank sprites created successfully!")
  ```
- **MIRROR**: Phase 2 runner sprite generation (exact same pattern, different color)
- **RUN**:
  ```bash
  /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/.venv/bin/python zombie-shooter/create_tank_sprites.py
  ```
- **VALIDATE**: Check files exist
  ```bash
  ls -la zombie-shooter/src/assets/zombies/tank/
  ```
- **EXPECTED OUTPUT**: 4 sprite files (walk_down.png, walk_up.png, walk_left.png, walk_right.png)

### Task 3: CREATE `zombie-shooter/tests/test_tank_variant.py`

- **ACTION**: CREATE integration tests for tank variant behavior
- **IMPLEMENT**:
  ```python
  """Tests for tank zombie variant."""

  from __future__ import annotations

  import pygame

  from game.core.constants import ZOMBIE_VARIANTS
  from game.entities.zombie import Zombie

  pygame.init()


  def test_tank_variant_has_correct_stats() -> None:
      """Test that tank zombie initializes with correct variant stats."""
      tank = Zombie(pygame.Vector2(100, 100), variant="tank")

      assert tank.variant == "tank"
      assert tank.hp == 3  # Requires 3 hits
      assert tank.speed == 98  # 0.7x normal speed (140 * 0.7 = 98)
      assert tank.radius == 24  # Larger hitbox (16 * 1.5 = 24)


  def test_tank_variant_survives_one_hit() -> None:
      """Test that tank survives first hit (HP reduces but tank lives)."""
      tank = Zombie(pygame.Vector2(100, 100), variant="tank")

      initial_hp = tank.hp
      tank.hp -= 1  # Simulate bullet hit

      assert tank.hp == initial_hp - 1
      assert tank.hp == 2  # Still alive with 2 HP


  def test_tank_variant_survives_two_hits() -> None:
      """Test that tank survives second hit."""
      tank = Zombie(pygame.Vector2(100, 100), variant="tank")

      tank.hp -= 1  # First hit
      tank.hp -= 1  # Second hit

      assert tank.hp == 1  # Still alive with 1 HP


  def test_tank_variant_dies_after_three_hits() -> None:
      """Test that tank dies after third hit."""
      tank = Zombie(pygame.Vector2(100, 100), variant="tank")

      tank.hp -= 1  # First hit: 3→2
      tank.hp -= 1  # Second hit: 2→1
      tank.hp -= 1  # Third hit: 1→0

      assert tank.hp <= 0  # Dead


  def test_tank_variant_moves_slower_than_normal() -> None:
      """Test that tank moves slower than normal zombie."""
      tank = Zombie(pygame.Vector2(100, 100), variant="tank")
      normal = Zombie(pygame.Vector2(200, 200), variant="normal")

      assert tank.speed < normal.speed
      assert tank.speed == 98
      assert normal.speed == 140


  def test_tank_variant_has_larger_hitbox() -> None:
      """Test that tank has larger collision radius than normal zombie."""
      tank = Zombie(pygame.Vector2(100, 100), variant="tank")
      normal = Zombie(pygame.Vector2(200, 200), variant="normal")

      assert tank.radius > normal.radius
      assert tank.radius == 24
      assert normal.radius == 16


  def test_tank_variant_loads_unique_sprites() -> None:
      """Test that tank loads variant-specific sprites."""
      tank = Zombie(pygame.Vector2(100, 100), variant="tank")

      # Should have sprites for all 4 directions
      assert "down" in tank.sprites
      assert "up" in tank.sprites
      assert "left" in tank.sprites
      assert "right" in tank.sprites

      # Each direction should have 3 frames
      for direction in ["down", "up", "left", "right"]:
          assert len(tank.sprites[direction]) == 3


  def test_tank_variant_constants_defined() -> None:
      """Test that tank variant is properly defined in constants."""
      assert "tank" in ZOMBIE_VARIANTS

      tank_stats = ZOMBIE_VARIANTS["tank"]
      assert tank_stats["speed"] == 98
      assert tank_stats["hp"] == 3
      assert tank_stats["radius"] == 24
      assert tank_stats["weight"] == 1.5  # 15% spawn rate
  ```
- **MIRROR**: `/zombie-shooter/tests/test_zombie_integration.py` - test structure and patterns
- **IMPORTS**: Import Zombie, ZOMBIE_VARIANTS, pygame
- **VALIDATE**:
  ```bash
  export PYTHONPATH="zombie-shooter/src" && /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/.venv/bin/python -m pytest zombie-shooter/tests/test_tank_variant.py -v
  ```

---

## Testing Strategy

### Unit Tests to Write

| Test File                          | Test Cases                                            | Validates                |
| ---------------------------------- | ----------------------------------------------------- | ------------------------ |
| `tests/test_tank_variant.py`       | stats, multi-hit survival, death, speed, hitbox, sprites | Tank variant behavior    |

### Edge Cases Checklist

- [ ] Tank spawns with correct stats (HP=3, speed=98, radius=24)
- [ ] Tank survives 1 bullet hit (HP=3→2)
- [ ] Tank survives 2 bullet hits (HP=3→2→1)
- [ ] Tank dies after 3 bullet hits (HP=3→2→1→0)
- [ ] Tank moves slower than normal zombies
- [ ] Tank has larger collision radius (easier to hit, harder to avoid)
- [ ] Tank loads unique blue sprites
- [ ] Tank spawns at 15% rate (weight=1.5)
- [ ] Tank death spawns same gore effects as other zombies
- [ ] Multiple tanks can coexist and be tracked independently

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
/Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/.venv/bin/python -m ruff check zombie-shooter/src/
```

**EXPECT**: Exit 0, no errors or warnings

### Level 2: UNIT_TESTS

```bash
export PYTHONPATH="zombie-shooter/src" && /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/.venv/bin/python -m pytest zombie-shooter/tests/ -v
```

**EXPECT**: All tests pass (101 existing + 8 new tank tests = 109 total)

### Level 3: FULL_SUITE

```bash
export PYTHONPATH="zombie-shooter/src" && /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/.venv/bin/python -m pytest zombie-shooter/tests/ && /Users/Vytautas/repositories/personal/presentation/top_down_zombie_shooter/zombie-shooter/.venv/bin/python -m ruff check zombie-shooter/src/
```

**EXPECT**: All tests pass, linting passes, exit 0

### Level 4: MANUAL_VALIDATION

1. **Start game**: `python zombie-shooter/src/game/main.py`
2. **Verify tank spawning**: Wait 10-15 seconds, look for slow blue zombies
3. **Verify multi-hit**:
   - Shoot tank once → tank continues advancing
   - Shoot tank twice → tank still advancing
   - Shoot tank three times → tank dies, spawns gore
4. **Verify speed**: Tank should move noticeably slower than normal zombies (0.7x)
5. **Verify hitbox**: Tank should be easier to hit (larger radius)
6. **Verify visual distinction**: Blue/gray color clearly distinguishes tank from other variants
7. **Check performance**: Game maintains 60 FPS with multiple tanks

---

## Acceptance Criteria

- [ ] All specified functionality implemented per user story
- [ ] Level 1-3 validation commands pass with exit 0
- [ ] Unit tests cover tank variant behavior (multi-hit, stats, sprites)
- [ ] Code changes minimal (only constants update + sprites)
- [ ] No regressions in existing tests (101/101 still pass + 8 new = 109/109)
- [ ] Tank sprites created and loaded correctly (blue-tinted, 4 directions)
- [ ] Tank spawns at 15% rate when enabled (weight=1.5)
- [ ] Tank requires exactly 3 hits to kill (HP system working)
- [ ] Tank moves at 98 px/s (0.7x normal speed)
- [ ] Tank has 24px radius (1.5x normal, larger hitbox)
- [ ] Performance stable (60 FPS with multiple tanks)

---

## Completion Checklist

- [ ] Task 1: Constants updated (tank weight 0→1.5)
- [ ] Task 2: Tank sprites created (blue-tinted, 4 directions)
- [ ] Task 3: Unit tests written and passing
- [ ] Level 1: Linting passes (ruff check)
- [ ] Level 2: Unit tests pass (pytest)
- [ ] Level 3: Full suite passes (tests + lint)
- [ ] Level 4: Manual validation passed (gameplay testing)
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk                              | Likelihood | Impact | Mitigation                                                                 |
| --------------------------------- | ---------- | ------ | -------------------------------------------------------------------------- |
| Tank too easy/hard to kill        | MEDIUM     | MEDIUM | HP=3 is tunable in Phase 6 if needed (adjust to 2 or 4)                   |
| Tank feels too slow/boring        | LOW        | MEDIUM | 0.7x speed creates blocking threat, tested in design                       |
| No visual feedback confusing      | MEDIUM     | LOW    | Players see HP bar (if implemented) or just shoot until dead               |
| Larger hitbox too easy to hit     | LOW        | LOW    | 1.5x radius is modest increase, still requires aim                         |
| Blue tint not distinct enough     | LOW        | MEDIUM | Use both blue (80, 120, 255) and gray (60, 60, 60) overlays for "armored" |
| Tank spawn rate feels unbalanced  | MEDIUM     | MEDIUM | 15% weight (1.5) matches Runner, tune in Phase 6 if needed                |

---

## Notes

**Design Decisions:**

1. **HP=3 is optimal**: 2 hits feels too weak, 4+ feels bullet-sponge. 3 hits creates meaningful commitment without frustration.

2. **0.7x speed (98 px/s)**: Slow enough to kite easily, but creates blocking/positioning challenges when combined with faster zombies.

3. **1.5x radius (24px)**: Larger hitbox makes tank easier to hit (pro) but also harder to squeeze past (con). Balanced trade-off.

4. **No hit feedback initially**: Keeps Phase 3 scope minimal. Can add sprite flash/particle burst in Phase 6 polish if playtesting shows it's needed.

5. **Blue + gray tint**: Blue alone might not look "armored". Adding subtle gray overlay creates metallic/tank aesthetic.

6. **15% spawn weight**: Matches Runner (1.5), creates balanced mix. Normal=70%, Runner=15%, Tank=15%, Spitter=10% (total: 7+1.5+1.5+1.0=11, weights are relative).

**Pattern Reuse from Phase 2 (Runner)**:
- Sprite tinting: Exact same technique, just different color
- Constants update: One-line weight change
- Sprite loading: Already implemented, just needs sprites to exist
- HP system: Already working from Phase 1

**Why Phase 3 is LOW Complexity**:
- No new systems (HP, sprites, spawning all exist)
- No new entity types (just parameter tuning)
- No new collision logic (radius change is transparent)
- Only real work: create 4 sprite files + enable in constants

**Future Enhancements (Phase 6)**:
- Hit feedback: Sprite flash when tank takes damage
- HP bar: Visual indicator of remaining HP
- Armor particles: Metallic spark on hit
- Death animation: Heavier thud sound or larger gore burst

**Phase 3 → Phase 4 Transition**:
After Phase 3, Phase 4 (Exploder) depends on Phases 1, 2, 3 all being complete. Tank completes the prerequisites for Exploder (which needs all basic variants for AOE testing).
