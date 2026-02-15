# Rambo Player Sprite & Animations

## Problem Statement

The player character is currently rendered as a plain blue circle (18px radius), which looks mundane and breaks immersion in an otherwise polished game with detailed animated zombie sprites (48x48 pixels, 3-frame walk cycles, 5 variants). Players cannot see movement (legs walking), action (gun shooting), or thematic character design (muscular action hero), making gameplay feel unpolished despite having high-quality enemy sprites.

## Evidence

- **Developer observation**: "Current circle is mundane, now it feels like good time and place [after completing zombie variants]"
- **Visual mismatch**: Zombies have detailed 48x48 sprites with animations; player has primitive circle rendering
- **Immersion gap**: Player stated "once I see that player sprite is running, using legs, has a gun that shoots and has shooting animation - I am happy"
- **Timing**: All 5 zombie variants complete (Phases 1-6 of zombie PRD), natural progression to player visual polish

## Proposed Solution

Implement animated player character sprites using programmatic pixel art generation (pygame-based) matching the zombie sprite system architecture (48x48 pixels, horizontal sprite sheets, Animation class integration). Create Rambo-like action hero appearance with visible headband, muscular physique, and gun, featuring 4-direction walk animations (3 frames each) and 4-direction shooting poses (1 frame each, shared across all weapons).

**Why programmatic vs hand-drawn**: Constraints require AI-generated sprites; programmatic approach using pygame allows complete implementation without external assets while maintaining consistency with existing 48x48 sprite system.

## Key Hypothesis

We believe replacing the blue circle player rendering with animated Rambo-like sprite (walk + shoot animations in 4 directions) will make gameplay feel immersive and thematic for players. We'll know we're right when the player character visually matches the zombie sprite quality with visible movement (legs walking) and shooting animations (gun extended) during gameplay.

## What We're NOT Building

- **Multiple character skins/variants** - Single Rambo character only, no customization
- **Per-weapon unique animations** - One shooting animation shared across pistol/shotgun/SMG (constraint specified)
- **Hand-crafted detailed pixel art** - Using programmatic generation for feasibility
- **Idle animation** - Reusing walk cycle frame 0 for idle stance
- **Reload animation** - Not in MVP scope
- **Damage/hit animation** - Player damage handled by HP counter only
- **Death animation** - Game over screen handles player death
- **Character customization** - No skin/outfit changes

## Success Metrics

| Metric | Target | How Measured |
|--------|--------|--------------|
| Visual quality match | Sprites match zombie aesthetic | Side-by-side comparison of player vs zombie sprite quality (48x48, clear silhouette, distinct from circle) |
| Animation visibility | Walk/shoot animations clearly visible | Manual gameplay test - can observer see legs moving and gun extending when shooting |
| Performance | 60 FPS maintained | FPS counter with player sprite rendering (should match current circle performance) |
| Code integration | Zero test regressions | All 118 existing tests still pass after player sprite implementation |

## Open Questions

- [ ] Color scheme for Rambo character (green camo body? brown? red headband?)
- [ ] Gun appearance style (pistol-like extended arm? rifle silhouette?)
- [ ] Shooting animation behavior - does it pause walking or overlay on walk cycle?
- [ ] Should shooting animation show muzzle flash pixels or just extended gun pose?

---

## Users & Context

**Primary User**
- **Who**: Player of the zombie shooter game (developer/presenter initially, demo audience later)
- **Current behavior**: Plays game controlling blue circle with WASD movement and mouse shooting
- **Trigger**: Playing the game and seeing polished animated zombies contrasted with primitive player rendering
- **Success state**: Player sees animated character with legs walking, gun visible, shooting animation when firing

**Job to Be Done**
When playing the zombie shooter game, I want to see my player character animated with visible movement and weapon, so I can feel immersed in the action and enjoy a polished visual experience matching the zombie sprite quality.

**Non-Users**
- Players expecting realistic 3D graphics (this is retro pixel art)
- Players who want multiple character options/customization (single character implementation)
- Users wanting professional hand-drawn pixel art quality (using programmatic generation)

---

## Solution Detail

### Core Capabilities (MoSCoW)

| Priority | Capability | Rationale |
|----------|------------|-----------|
| Must | 4-direction walk animations (3 frames each, 48x48 pixels) | Core movement visibility - player needs to see legs moving when using WASD |
| Must | 4-direction shooting poses (1 frame each, gun extended) | Core action feedback - player needs to see weapon when firing |
| Must | Rambo-like appearance (headband, muscular, visible gun) | Thematic character design matching "action hero zombie shooter" aesthetic |
| Must | Integration with existing Animation system | Reuse proven zombie sprite architecture for consistency |
| Should | Distinct visual appearance from zombies | Player sprite should be immediately identifiable (different color scheme/build) |
| Could | Muzzle flash pixels on shooting frame | Visual juice for shooting feedback |
| Could | Idle animation (dedicated frames) | Currently using walk frame 0, dedicated idle could improve polish |
| Won't | Per-weapon animation variants | Constraint: one animation for all guns to limit scope |
| Won't | Character customization/skins | Single character implementation only |

### MVP Scope

**Minimum to validate hypothesis:**
1. Programmatic sprite generation script creating 16 sprite files (4 directions × 4 animation types)
   - Walk: down/up/left/right (3 frames each = 12 files)
   - Shoot: down/up/left/right (1 frame each = 4 files)
2. Player class modified to load sprites (mirror zombie pattern)
3. Animation instance integrated into player update loop
4. Drawing method replaced (circle → sprite rendering)
5. Shooting animation triggered on weapon fire

**Success signal**: Player runs game, sees animated Rambo character walk with WASD and extend gun when shooting, visually matching zombie sprite quality.

### User Flow

**Critical path - shortest journey to value:**

1. **Game Launch**
   - Player starts game → PlayScene initializes
   - Player entity loads Rambo sprites instead of drawing circle
   - Default idle/down stance visible

2. **Movement (WASD)**
   - Player presses W → character walks up (3-frame animation cycles)
   - Player presses A → character walks left (3-frame animation cycles)
   - Animation direction auto-detected from velocity (existing system)
   - Player releases keys → character shows idle stance (frame 0)

3. **Shooting (Mouse Click)**
   - Player clicks to shoot → shooting animation frame displays
   - Gun visibly extends in current facing direction
   - Animation returns to walk/idle after shot
   - Works with all weapons (pistol/shotgun/SMG)

**Data flow:**
- Input (WASD) → Player.vel updated → Animation.update(dt, vel) detects direction → frame cycles
- Input (Mouse) → Shoot action → Display shoot sprite → Return to walk sprite
- Player.draw() → Get current animation frame → Blit sprite at player.pos

---

## Technical Approach

**Feasibility**: **HIGH**

**Architecture Notes**

**Sprite Generation (Programmatic)**
- Python script using pygame to draw pixels programmatically
- Generate 48x48 pixel sprites with geometric shapes:
  - Body: Rectangles for torso/limbs, tan/brown skin tone
  - Headband: Red 4px band across forehead
  - Clothing: Green/brown pixels for action outfit
  - Gun: L-shaped black pixels extending from hand
  - Legs: Shifting pixels frame-to-frame for walk cycle
- Output: PNG files in `/src/assets/players/` directory
  - `walk_down.png` (144×48, 3 frames horizontal)
  - `walk_up.png` (144×48, 3 frames horizontal)
  - `walk_left.png` (144×48, 3 frames horizontal)
  - `walk_right.png` (144×48, 3 frames horizontal)
  - `shoot_down.png` (48×48, 1 frame)
  - `shoot_up.png` (48×48, 1 frame)
  - `shoot_left.png` (48×48, 1 frame)
  - `shoot_right.png` (48×48, 1 frame)

**Player Class Integration (Mirror Zombie Pattern)**
- Add module-level sprite loading: `_load_player_sprites()`
- Add Animation instance to `Player.__init__()`: `self.animation = Animation(3, 10)`
- Add animation update in `Player.update()`: `self.animation.update(dt, self.vel)`
- Replace `Player.draw()` circle rendering with sprite blit (copy zombie pattern)
- Add shooting animation state: `self.is_shooting` flag toggled on weapon fire

**Shooting Animation Logic**
- Track shooting state in Player class
- When `shoot()` called: set `self.is_shooting = True` for brief duration (0.1s)
- In `draw()`: check `is_shooting` → use shoot sprite, else use walk sprite
- Shooting animation shows gun extended in current facing direction

**Constants**
```python
# Add to constants.py
PLAYER_SPRITE_SIZE = 48  # Match zombie size
PLAYER_WALK_FRAME_COUNT = 3  # Match zombie walk cycle
PLAYER_SHOOT_FRAME_COUNT = 1  # Single shooting pose per direction
PLAYER_ANIMATION_FPS = 10  # Match zombie animation speed
PLAYER_SHOOT_DURATION = 0.1  # Seconds to display shooting sprite
```

**Technical Risks**

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Programmatic sprites look too basic/geometric | MEDIUM | Use references from zombie sprites for style consistency; iterate on sprite generation script with color/shading |
| Shooting animation timing feels wrong (too fast/slow) | LOW | PLAYER_SHOOT_DURATION is tunable constant (0.1s default) |
| Animation system doesn't handle shooting state | LOW | Proven Animation class works for zombies; shooting is simple state flag addition |
| Sprite generation script complexity | LOW | Reuse pygame primitives (draw.rect, draw.circle); start simple and iterate |
| Performance regression with sprite rendering | VERY LOW | Zombie sprite rendering already proven at 50+ entities, player is 1 entity |

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
| 1 | Player sprite asset generation | Create programmatic sprite generation script, generate 8 sprite files (4 walk + 4 shoot) | complete | - | - | [phase-1-player-sprite-asset-generation.plan.md](../plans/completed/phase-1-player-sprite-asset-generation.plan.md) |
| 2 | Player animation system integration | Add sprite loading, Animation instance, update player draw method to use sprites | complete | - | 1 | [phase-2-player-animation-system-integration.plan.md](../plans/completed/phase-2-player-animation-system-integration.plan.md) |
| 3 | Shooting animation integration | Add shooting state tracking, trigger shoot sprites on weapon fire, timing logic | complete | - | 2 | [phase-3-shooting-animation-integration.plan.md](../plans/completed/phase-3-shooting-animation-integration.plan.md) |
| 4 | Testing & polish | Manual gameplay validation, sprite appearance tuning, performance check | pending | - | 3 | - |

### Phase Details

**Phase 1: Player sprite asset generation**
- **Goal**: Generate Rambo-like player sprites programmatically
- **Scope**:
  - Create Python script using pygame: `create_player_sprites.py`
  - Generate 4 walk animations (down/up/left/right, 3 frames each)
    - Frame 0: Neutral stance, both legs together
    - Frame 1: Left leg forward step
    - Frame 2: Right leg forward step
  - Generate 4 shooting poses (down/up/left/right, 1 frame each)
    - Extended gun arm in facing direction
  - Rambo appearance: red headband, muscular build, tan skin, green/brown outfit, black gun
  - Output PNG files to `src/assets/players/` directory
  - Walk sprites: horizontal sheets (144×48 = 3 frames × 48px)
  - Shoot sprites: single frames (48×48)
- **Success signal**: 8 PNG files exist, sprites visually show Rambo character with walk cycle and gun visible

**Phase 2: Player animation system integration**
- **Goal**: Replace circle rendering with sprite-based rendering
- **Scope**:
  - Add `load_player_sprites()` function to `loader.py` (mirror `load_zombie_sprites()` pattern)
  - Add module-level sprite caching to `player.py`: `_player_sprites` dict
  - Add `Animation` instance to `Player.__init__()`: `self.animation = Animation(PLAYER_WALK_FRAME_COUNT, PLAYER_ANIMATION_FPS)`
  - Add animation update in `Player.update()`: `self.animation.update(dt, self.vel)`
  - Replace `Player.draw()` circle rendering with sprite blit:
    ```python
    direction = self.animation.get_current_direction()
    frame_index = self.animation.get_current_frame_index()
    sprite = self.sprites["walk"][direction][frame_index]
    sprite_rect = sprite.get_rect(center=(int(self.pos.x), int(self.pos.y)))
    screen.blit(sprite, sprite_rect)
    ```
  - Add constants: `PLAYER_SPRITE_SIZE`, `PLAYER_WALK_FRAME_COUNT`, `PLAYER_ANIMATION_FPS`
- **Success signal**: Player character shows animated walk sprite when moving with WASD, direction changes correctly, animation cycles smoothly

**Phase 3: Shooting animation integration**
- **Goal**: Display shooting sprite when player fires weapon
- **Scope**:
  - Add `self.is_shooting` flag and `self.shoot_timer` to Player class
  - Modify `Player.shoot()` method (or shooting logic in PlayScene) to set shooting state:
    ```python
    self.is_shooting = True
    self.shoot_timer = PLAYER_SHOOT_DURATION
    ```
  - Add timer decrement in `Player.update()`:
    ```python
    if self.shoot_timer > 0:
        self.shoot_timer -= dt
    else:
        self.is_shooting = False
    ```
  - Modify `Player.draw()` to check shooting state:
    ```python
    if self.is_shooting:
        # Use shoot sprite
        direction = self.animation.get_current_direction()
        sprite = self.sprites["shoot"][direction]
    else:
        # Use walk sprite (existing code)
        direction = self.animation.get_current_direction()
        frame_index = self.animation.get_current_frame_index()
        sprite = self.sprites["walk"][direction][frame_index]
    ```
  - Add constant: `PLAYER_SHOOT_DURATION = 0.1`
- **Success signal**: Player sprite shows extended gun when shooting (mouse click), returns to walk animation after brief duration, works with all weapons

**Phase 4: Testing & polish**
- **Goal**: Validate visual quality and gameplay feel
- **Scope**:
  - Manual gameplay testing: walk in all directions, shoot while moving, shoot while idle
  - Verify sprite appearance matches zombie quality (clear silhouette, readable at game resolution)
  - Check performance: FPS maintained at 60 (no regression from circle rendering)
  - Validate all 118 existing tests still pass (no regressions)
  - Optional: Iterate on sprite generation script if appearance needs refinement
    - Adjust colors, proportions, gun style
    - Re-run generation script, reload sprites
  - Optional: Add muzzle flash pixels to shooting sprite for extra polish
- **Success signal**: Player sprite looks good during gameplay, animations feel smooth, no performance issues, all tests pass, sprite quality comparable to zombies

### Parallelism Notes

All phases are sequential (each depends on previous):
- Phase 1 creates assets needed by Phase 2
- Phase 2 integrates walk animations needed before Phase 3
- Phase 3 adds shooting on top of working walk system
- Phase 4 validates complete implementation

No parallel work possible due to dependencies.

---

## Decisions Log

| Decision | Choice | Alternatives | Rationale |
|----------|--------|--------------|-----------|
| Sprite generation method | Programmatic (pygame) | Hand-drawn pixel art, AI image generation, Asset store purchase | Constraint: AI must create sprites. Programmatic approach is feasible with pygame primitives and maintains control over output |
| Sprite resolution | 48×48 pixels | 32×32 (smaller), 64×64 (larger) | Match zombie sprite size (48×48) for visual consistency and reuse existing constants/systems |
| Walk animation frames | 3 frames per direction | 2 frames (simpler), 4+ frames (smoother) | Match zombie walk cycle (3 frames) - proven to work well, consistent aesthetic |
| Shooting animation | Shared across all weapons | Per-weapon animations (pistol/shotgun/SMG) | User constraint: "one animation for all guns" to limit scope; sufficient for MVP |
| Idle animation | Reuse walk frame 0 | Dedicated idle frames | Scope reduction - walk frame 0 is sufficient idle pose, can add dedicated idle later if needed |
| Animation FPS | 10 FPS | 8 FPS (choppier), 15 FPS (smoother) | Match zombie animation speed (10 FPS) for consistency |
| Shooting duration | 0.1 seconds | 0.05s (very brief), 0.2s (longer) | Balance between visible feedback and not interrupting movement feel; tunable constant |
| Character style | Rambo (headband, muscular, gun) | Generic soldier, Tactical operator, Survivor | User specified "Rambo-like" - iconic action hero aesthetic with headband and visible weapon |

---

## Research Summary

**Market Context**
- Industry standard for top-down shooters includes walk (4 directions), idle, and shoot animations ([OpenGameArt.org](https://opengameart.org/content/animated-top-down-survivor-player))
- 48×48 pixel sprites are common for retro pixel art top-down games
- Asset marketplaces ([CraftPix](https://craftpix.net/sets/top-down-shooter-pixel-art-collection/), [GameDev Market](https://www.gamedevmarket.net/asset/pixel-art-top-down-shooter)) show survivor characters with visible weapons as standard
- Top-down zombie shooters commonly feature armed survivor characters vs zombie hordes aesthetic

**Technical Context**
- **Current player rendering**: Simple blue circle (18px radius) in `player.py:146-155`
- **Zombie sprite system**: Proven architecture with 48×48 sprites, 3-frame walk cycles, 10 FPS animation
- **Animation class**: Fully functional, detects 4 cardinal directions from velocity vector, handles frame cycling
- **Sprite loading**: Module-level caching pattern (`_zombie_sprites`), loads horizontal sprite sheets, splits into frames
- **Integration points**: Player class already tracks `pos`, `vel`, `radius` - ready for sprite integration
- **Feasibility**: HIGH - zombie sprite system provides exact pattern to mirror for player sprites

**Key Technical Insight**: The zombie sprite infrastructure is the perfect foundation. All systems needed for player sprites already exist and are proven to work at scale (50+ animated zombies at 60 FPS).

---

*Generated: 2026-02-09T23:00:00Z*
*Status: DRAFT - ready for implementation*
