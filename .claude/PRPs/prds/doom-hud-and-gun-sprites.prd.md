# Doom-Style HUD & Pixel-Art Weapon Sprites

## Problem Statement

The game's current HUD is four lines of white text (HP, timer, kills, weapon name) that provides no immersion or visual feedback. Weapon pickups are plain colored squares on the ground with no identity. Players have no visceral sense of their health state, no visual weapon inventory, and no satisfaction from picking up weapons. The game feels like a prototype, not a finished experience.

## Evidence

- Current HUD: 4 `font.render()` calls; no icons, no face, no weapon strip (`play.py:421-447`)
- Weapon pickups: `pygame.draw.rect()` with flat color — yellow square = pistol, red = shotgun, cyan = SMG (`pickup.py:52-69`)
- Player has `hp`, `current_weapon`, `weapons_inventory` — all damage feedback data exists, nothing is visualized (`player.py:54-58`)
- Doom's HUD (1993) set the gold standard: face reacting to damage + weapon icons = instant situational awareness

## Proposed Solution

Replace the text HUD with a Doom-inspired HUD panel at the bottom-center of the screen: a procedurally drawn pixel-art face whose expression degrades as HP drops (with a brief pain-flash on hit), flanked by weapon icon slots that gray out unowned guns and highlight the active one. In parallel, replace the flat-color weapon pickup squares with recognizable pixel-art gun silhouettes so players know at a glance what they're picking up.

## Key Hypothesis

We believe a reactive face portrait + weapon icon strip will make health management and weapon collection feel satisfying and readable. We'll know we're right when a player can glance at the HUD and immediately know their HP state and weapon without reading any text.

## What We're NOT Building

- Animated sprite sheets for the face (too complex) — procedural `pygame.draw` only, consistent with existing obstacle/ground art style
- Ammo counter — weapon system has infinite ammo by design
- Minimap — out of scope
- Sound effects tied to damage states — audio system doesn't exist yet

## Success Metrics

| Metric | Target | How Measured |
|--------|--------|--------------|
| HUD renders at 60fps | No frame-time regression | `make run` timing |
| Face state matches HP | 5 distinct states visible | Manual visual test |
| All 3 weapon icons show in HUD | Grayed/normal/highlighted all visible | Manual test |
| Pickup sprites identifiable | Each weapon looks distinct | Manual test |
| All existing tests pass | 153/154 (pre-existing failure stays) | `make test` |

## Open Questions

- [ ] HUD panel width/position — full-width bar vs centered panel (Doom used full-width; centered panel fits 1280×720 better)
- [ ] Should the timer/kills text move to the HUD panel or stay as overlays?

---

## Users & Context

**Primary User**
- **Who**: The developer building a top-down zombie shooter for a presentation demo
- **Current behavior**: Glances at top-left corner for HP number; has no weapon inventory view
- **Trigger**: Taking damage, picking up a weapon, switching weapons
- **Success state**: Can read game state at a glance from the bottom HUD without reading text

**Job to Be Done**
When fighting zombies and taking damage, I want to feel the urgency of my health state visually and know my weapon loadout at a glance, so I can make tactical decisions without interrupting gameplay flow.

**Non-Users**
Not targeting players who need accessibility accommodations — pure visual aesthetic decision.

---

## Solution Detail

### Core Capabilities (MoSCoW)

| Priority | Capability | Rationale |
|----------|------------|-----------|
| Must | Face portrait with 5 HP-based expression states | Core Doom HUD identity; instant health readout |
| Must | Pain-flash state (brief grimace on hit) | Feedback that damage landed |
| Must | Weapon icon strip (3 slots: pistol/shotgun/smg) | Shows inventory + active weapon |
| Must | Grayed-out icons for unowned weapons | Communicates lock/unlock progression |
| Must | Highlight/border on active weapon icon | Shows what's equipped |
| Must | Pixel-art gun sprites for pickups on the map | Replaces plain colored squares |
| Should | HUD panel background (dark bar) | Visual separation from game world |
| Should | HP number shown in HUD panel | Keeps numeric precision alongside face |
| Could | Face briefly looks toward damage direction | More faithful to Doom; complex to add |
| Won't | Full sprite-sheet face animations | Too many frames for marginal gain |

### MVP Scope

HUD panel at bottom-center with: face portrait (5 states + pain flash) + weapon icon strip (3 slots, grayed/normal/highlighted) + HP display. Plus pixel-art gun pickup sprites for all 3 weapon types.

### User Flow

```
Player takes damage → HP drops → face expression updates immediately
                    → if hit in last 0.4s → pain-flash face shown instead
Player picks up shotgun → shotgun icon lights up in HUD; becomes highlighted as active
Player presses 2 (switch to shotgun) → shotgun icon gains selection highlight
Player presses 1 (switch to pistol) → pistol icon highlighted, shotgun reverts to normal
```

---

## Technical Approach

**Feasibility**: HIGH — all required data already exists on `player.py`; drawing is pure `pygame.draw`; no new game logic needed.

**Architecture Notes**

- HUD drawn in `_draw_hud()` in `play.py` — replace text with panel + face + icon strip
- Face state computed from `self.player.hp` and a new `self.player.pain_timer` float (decremented in `player.update()`)
- `pain_timer` set to `0.4` whenever `player.hp` decreases (tracked via `prev_hp` in PlayScene or on Player)
- Face drawn procedurally: `pygame.draw.circle/rect/polygon` — same approach as obstacles
- Weapon icons: small `pygame.Surface` per weapon, pre-built once (like ground tile), drawn with state coloring
- Pickup sprites: replace `pygame.draw.rect()` in `pickup.py` with pixel-art gun shape per `weapon_type`
- HUD constants added to `constants.py` (no pygame imports — plain ints/tuples)

**Technical Risks**

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Pain timer tracking: where does hp delta get detected? | M | Add `prev_hp` to Player; check delta in Player.update() or PlayScene._process_player_damage() |
| HUD panel overlapping game elements at bottom edge | L | HUD panel is 90px tall; spawn zone stays within HEIGHT-90 with SPAWN_MARGIN already at 100px |
| 60fps maintained with procedural face drawing | L | Face is ~20 draw calls; negligible vs obstacle rendering |

---

## Implementation Phases

| # | Phase | Description | Status | Parallel | Depends | PRP Plan |
|---|-------|-------------|--------|----------|---------|----------|
| 1 | Doom HUD Panel | Face portrait + weapon icon strip replacing text HUD | in-progress | with 2 | - | `.claude/PRPs/plans/doom-hud-panel.plan.md` |
| 2 | Weapon Pickup Sprites | Pixel-art gun models replacing flat-color squares | pending | with 1 | - | - |

### Phase Details

**Phase 1: Doom HUD Panel**
- **Goal**: Replace text HUD with Doom-style bottom-center panel: face (5 HP states + pain flash) + weapon icon strip (3 slots: gray/normal/highlighted)
- **Scope**:
  - Add `HUD_*` constants to `constants.py`
  - Add `pain_timer: float = 0.0` to `Player.__init__`; update in `Player.update()` when HP drops
  - Replace `_draw_hud()` in `play.py` with panel background + `_draw_face()` + `_draw_weapon_icons()` helpers
  - Face states: `normal` (HP≥80), `hurt` (HP≥60), `injured` (HP≥40), `critical` (HP≥20), `dying` (HP<20); overridden by `pain_flash` if `pain_timer > 0`
  - Weapon icon slots pre-built as `pygame.Surface` objects (32×20px each), colored per state
  - Keep HP number + timer + kills text as overlays (top of screen) — just enhance the bottom HUD
- **Success signal**: Face visibly changes expression as HP crosses thresholds; weapon icons correctly show inventory state; `make test` still passes

**Phase 2: Weapon Pickup Sprites**
- **Goal**: Replace flat `pygame.draw.rect()` in `pickup.py` with per-weapon pixel-art gun silhouettes
- **Scope**:
  - Update `pickup.py draw()` only — no other files change
  - Pistol: compact handgun shape (barrel, grip, trigger guard)
  - Shotgun: long barrel, pump handle, stock
  - SMG: boxy body, short barrel, magazine
  - Colors: match existing palette (pistol yellow-gold, shotgun red-brown, SMG cyan-blue)
  - Size stays within 40×40px collision radius
- **Success signal**: Three visually distinct gun shapes on map; each identifiable at a glance; existing pickup collision tests pass

### Parallelism Notes

Phases 1 and 2 are fully independent — Phase 1 touches `play.py`, `player.py`, `constants.py`; Phase 2 touches only `pickup.py`. They can be implemented in parallel in separate worktrees or sequentially by the same developer.

---

## Decisions Log

| Decision | Choice | Alternatives | Rationale |
|----------|--------|--------------|-----------|
| Face drawing approach | Procedural pygame.draw | Sprite sheet PNG | Consistent with existing pixel-art obstacle style; no asset loading |
| HUD panel position | Bottom-center, 400×90px | Full-width bar | Centered panel doesn't obscure corner UI; matches 1280×720 aspect |
| Pain timer source | `pain_timer` on Player, decremented in update() | Track in PlayScene | Keeps damage feedback self-contained in Player entity |
| Weapon icons | Pre-built Surfaces per weapon | Draw every frame | Pre-building surfaces is fast; avoids per-frame branch on weapon type |
| Pickup sprite approach | Procedural draw in pickup.py | New sprite file | Single file change; consistent with no-asset-loading codebase style |

---

## Research Summary

**Market Context**
Doom (1993) HUD: full-width bottom bar, face in center changing between ~5 states (OK → oof → pain → heavy pain → death), weapon numbers 1-7 shown as colored numbers. Doom II kept same design. This is the reference. Our 3-weapon system maps cleanly to 3 icon slots.

**Technical Context**
- Player already tracks `hp` (float, max 100), `current_weapon` (str), `weapons_inventory` (set) — `player.py:54-58`
- No pain flash mechanism exists yet — needs `pain_timer` float + HP delta detection
- Existing draw pipeline: ground → obstacles → decals → corpses → player → bullets → zombies → pickups → acid → particles → HUD (`play.py:449-493`)
- Pixel-art precedent established: 16×16 tiles in `play.py`, detailed obstacles in `obstacle.py`
- No external asset loading in codebase — pure procedural drawing throughout

---

*Generated: 2026-02-28*
*Status: DRAFT - needs validation*
