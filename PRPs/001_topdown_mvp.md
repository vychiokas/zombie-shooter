# PRP-001 — Top-Down Zombie Shooter (MVP Vertical Slice)

**Project:** Zombie Shooter (Pygame)  
**PRP ID:** 001_topdown_mvp  
**Goal:** Build a playable vertical slice: move + aim + shoot + zombies + damage + win/lose + restart  
**Tech:** Python + Pygame  
**Graphics:** Placeholder shapes only (rects/circles), no external assets required  
**Target:** Smooth 60 FPS on a normal dev machine

---

## 1) Product Requirements (What “done” means)

### 1.1 Core Loop
- Game launches into **Menu** scene
- Press **ENTER** to start game
- **Play** scene:
  - Player moves
  - Player aims with mouse
  - Player shoots bullets
  - Zombies spawn and chase player
  - Bullets kill zombies
  - Player loses HP on contact with zombie
  - Win condition: **survive 60 seconds**
- End state:
  - If player HP reaches 0 → **Game Over**
  - If survival timer reaches 60 seconds → **You Win**
- End screens show:
  - Result (Game Over / You Win)
  - Final kills count
  - Press **R** to restart (back to Play)
  - Press **ESC** to go back to Menu / Quit

### 1.2 Controls
- Move: **WASD**
- Aim: **Mouse position**
- Shoot: **Left mouse button**
- Restart: **R**
- Quit: **ESC** or window close button

### 1.3 Gameplay Rules
- Player starts centered on screen
- Player has HP: **100**
- Zombie contact damage: **10 HP per second** (continuous while overlapping)
- Bullets:
  - Travel forward from the player toward the mouse aim direction
  - Destroy on leaving screen bounds or after TTL (e.g. 1.5s)
  - Kill zombie in 1 hit (MVP)
- Zombies:
  - Spawn at screen edges (random side)
  - Move toward player constantly
  - No complex pathfinding; just straight seek
- Spawn progression:
  - Starts easy and ramps up (e.g. spawn every 1.0s → down to 0.25s)
  - Cap max zombies alive for MVP (e.g. 50)

### 1.4 HUD (Minimum UI)
During Play:
- HP bar or HP number (top-left)
- Timer (top-center): `Time: 12.3 / 60`
- Kills count (top-right)

### 1.5 Performance & Feel Targets
- Fixed window resolution: **1280x720**
- Frame cap: **60 FPS**
- Movement should be **delta-time based** (not frame-dependent)
- “Good enough” feel:
  - Player speed: ~300 px/sec
  - Zombie speed: ~140 px/sec (slower than player)
  - Bullet speed: ~700 px/sec
  - Shooting cooldown: ~0.15 sec

---

## 2) Non-Goals (Explicitly out of scope)
Do **NOT** implement these in MVP:
- Sprite art, animations, sound effects
- Weapon upgrades, pickups, ammo
- Multiple enemy types
- Level generation, obstacles
- Particle effects / screen shake
- Multiplayer
- Save/load progression
- Complex UI framework

---

## 3) Architecture & Code Constraints

### 3.1 Folder Layout (Expected)
```
src/game/
  main.py
  core/
    game.py
    scene.py
    constants.py
  scenes/
    menu.py
    play.py
    game_over.py
  entities/
    player.py
    zombie.py
    bullet.py
  systems/
    collisions.py
    spawner.py
```

### 3.2 Scene Pattern
All scenes implement:

- `handle_event(event)`
- `update(dt: float)`
- `draw(screen)`

`Game` owns the active scene and can switch scenes.

### 3.3 Entities Pattern
All entities should be simple objects with:
- `pos: pygame.Vector2`
- `vel: pygame.Vector2` (optional)
- `radius` or `rect` for collision
- `update(dt)`
- `draw(screen)`

Avoid overengineering: no ECS.

### 3.4 Deterministic-ish Logic
- Use `dt` from `clock.tick(60) / 1000.0`
- Don’t hardcode movement per frame.

### 3.5 Collision Approach (MVP)
Use **circle collisions** for simplicity:
- Player: circle radius ~18
- Zombie: circle radius ~16
- Bullet: circle radius ~4

Collision detection:
- overlap if distance squared <= (r1 + r2)^2

---

## 4) Implementation Plan (Milestones)

### Milestone 1 — Boot & Core Loop
- `main.py` runs the game module entrypoint
- `Game` initializes pygame, creates window, runs main loop
- Scene switching works (start in Menu)

**Done when:**
- Window opens, ESC exits, no exceptions

---

### Milestone 2 — Menu Scene
- Display title text: “Zombie Shooter”
- Instructions: “ENTER to Start, ESC to Quit”
- ENTER switches to Play

**Done when:**
- Menu displays and transitions correctly

---

### Milestone 3 — Play Scene Skeleton + Player Movement
- Play scene draws background and player placeholder circle
- WASD movement with dt
- Clamp player within screen

**Done when:**
- Player moves smoothly, stays on screen

---

### Milestone 4 — Aim + Shoot + Bullets
- Determine aim direction from mouse to player
- Spawn bullet on LMB with cooldown
- Bullets move, despawn offscreen/TTL

**Done when:**
- Can shoot bullets continuously, bullets fly toward mouse

---

### Milestone 5 — Zombie Spawning + Seek AI
- Spawn zombies periodically at screen edges
- Zombies seek player

**Done when:**
- Zombies appear and chase player

---

### Milestone 6 — Collisions, Damage, Kills
- Bullet hits zombie → remove zombie + increment kills
- Zombie touches player → drain HP at DPS rate (scaled by dt)
- If HP <= 0 → go to Game Over scene

**Done when:**
- Player can die; bullets kill zombies

---

### Milestone 7 — Win Condition + End Screens
- Survival timer counts up
- If time >= 60 → “You Win” end screen
- End screens show kills and restart instructions
- R restarts Play; ESC goes to Menu

**Done when:**
- Full MVP loop works from menu → play → end → restart

---

## 5) Validation & Test Plan (Must Run)

### 5.1 Manual Validation (Required)
- Launch game, start Play, move, shoot, kill zombie, die, restart
- Confirm FPS is stable and no input lag
- Confirm no entity list grows forever (bullets/zombies despawn)

### 5.2 Commands
From repo root:

Run game:
```bash
python -m game.main
```

Run tests:
```bash
pytest -q
```

Optional lint (if installed):
```bash
ruff check .
```

---

## 6) Suggested Constants (Keep in `constants.py`)
- `WIDTH = 1280`
- `HEIGHT = 720`
- `FPS = 60`

Player:
- `PLAYER_SPEED = 300`
- `PLAYER_RADIUS = 18`
- `PLAYER_MAX_HP = 100`
- `CONTACT_DPS = 10`

Bullets:
- `BULLET_SPEED = 700`
- `BULLET_RADIUS = 4`
- `BULLET_TTL = 1.5`
- `SHOOT_COOLDOWN = 0.15`

Zombies:
- `ZOMBIE_SPEED = 140`
- `ZOMBIE_RADIUS = 16`
- `MAX_ZOMBIES = 50`

Spawning:
- `SPAWN_INTERVAL_START = 1.0`
- `SPAWN_INTERVAL_MIN = 0.25`
- `SPAWN_RAMP_SECONDS = 45`

Win:
- `SURVIVE_SECONDS = 60`

---

## 7) Edge Cases & Quality Checklist
- [ ] Closing the window exits cleanly (no hang)
- [ ] ESC always works
- [ ] Player stays in bounds
- [ ] Bullet list doesn’t grow indefinitely
- [ ] Zombie list doesn’t grow indefinitely
- [ ] Damage is based on dt (no frame-rate dependence)
- [ ] Restart resets timer, HP, entities, kills
- [ ] Win screen triggers exactly once at 60s

---

## 8) Notes for Future PRPs (After MVP)
- Sprites + animation
- Multiple weapons and pickups
- Wave UI and difficulty curve tuning
- Obstacles + map boundaries
- Sound + music
- Particle effects / hit feedback
- Settings (volume, sensitivity)

---
**End of PRP-001**
