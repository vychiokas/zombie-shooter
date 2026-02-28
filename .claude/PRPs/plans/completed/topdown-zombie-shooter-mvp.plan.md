# Feature: Top-Down Zombie Shooter MVP

## Summary

Build a playable vertical slice of a top-down zombie shooter game with complete game loop: menu → play (move, aim, shoot zombies, take damage) → win/lose screens → restart. Uses pygame with clean architecture patterns (Scene management, Entity system, collision detection), placeholder graphics (circles/rectangles), and delta-time based movement for 60 FPS performance. This serves as a learning project demonstrating production-quality Python game development patterns.

## User Story

As a Python developer learning game development
I want to implement a complete, well-architected pygame vertical slice
So that I can understand production game patterns and present clean code to colleagues/conferences

## Problem Statement

Most pygame tutorials provide either trivial single-file examples or overwhelming full-game codebases. There's a gap for intermediate developers who need a complete vertical slice demonstrating:
- Scene management pattern (menu/play/gameover)
- Entity architecture without over-engineering (no ECS)
- Delta-time based physics
- Collision systems
- Game state management
- Clean separation of concerns following Python best practices

## Solution Statement

Implement a 7-milestone zombie shooter MVP with:
- **Scene Pattern**: Base Scene class with handle_event/update/draw interface
- **Entity Pattern**: Simple objects with pos/vel/radius and update/draw methods
- **Game Loop**: Centralized Game class managing scene switching and delta-time
- **Systems**: Collision detection and zombie spawning as separate modules
- **Constants**: All magic numbers in dedicated constants.py
- **Testing**: Unit tests for collision system with edge case coverage

## Metadata

| Field            | Value                                                              |
| ---------------- | ------------------------------------------------------------------ |
| Type             | NEW_CAPABILITY                                                     |
| Complexity       | MEDIUM                                                             |
| Systems Affected | core, scenes, entities, systems                                    |
| Dependencies     | pygame>=2.6.0, pytest (dev), ruff (dev)                            |
| Estimated Tasks  | 18 tasks across 7 milestones                                       |

---

## UX Design

### Before State
```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌─────────────┐                                                             ║
║   │   Launch    │ ──────► Empty black window (800x600)                        ║
║   │   Game      │         - Only QUIT event works                             ║
║   └─────────────┘         - No gameplay                                       ║
║                           - No scenes                                         ║
║                           - No entities                                       ║
║                                                                               ║
║   USER_FLOW: Launch → see black screen → close window                         ║
║   PAIN_POINT: No game content, just pygame initialization skeleton            ║
║   DATA_FLOW: pygame.init() → main loop → pygame.quit()                        ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌─────────────┐         ┌─────────────┐         ┌─────────────┐            ║
║   │   Launch    │ ──────► │    Menu     │ ──────► │    Play     │            ║
║   │   Game      │  auto   │   Scene     │  ENTER  │   Scene     │            ║
║   └─────────────┘         └─────────────┘         └─────────────┘            ║
║                                  │                        │                   ║
║                                  │ ESC                    │ HP=0 OR time=60   ║
║                                  ▼                        ▼                   ║
║                           ┌─────────────┐         ┌─────────────┐            ║
║                           │    Quit     │         │  Game Over  │            ║
║                           │             │         │    Scene    │            ║
║                           └─────────────┘         └─────────────┘            ║
║                                                           │                   ║
║                                                           │ R (restart)       ║
║                                                           └──────┐            ║
║                                                                  │            ║
║                                                    ┌─────────────▼──────┐     ║
║                                                    │  Back to Play       │     ║
║                                                    │  (reset state)      │     ║
║                                                    └─────────────────────┘     ║
║                                                                               ║
║   PLAY SCENE MECHANICS:                                                        ║
║   ┌──────────────────────────────────────────────────────────────┐            ║
║   │  Player (circle) ◄──WASD──► moves with delta-time             │            ║
║   │       │                                                        │            ║
║   │       │ Left Click ───► Bullet spawns (with cooldown)         │            ║
║   │       │                    │                                  │            ║
║   │       │                    ▼                                  │            ║
║   │       │            Bullet travels toward mouse                │            ║
║   │       │                    │                                  │            ║
║   │       │                    ▼                                  │            ║
║   │       │            Hits Zombie ───► Zombie dies, kills++      │            ║
║   │       │                                                        │            ║
║   │       ▼ Zombie touches                                        │            ║
║   │   HP decreases (10 DPS * dt)                                  │            ║
║   │                                                                │            ║
║   │  Zombies spawn at edges → seek player position                │            ║
║   │  Spawn rate ramps up over time (1.0s → 0.25s)                 │            ║
║   │                                                                │            ║
║   │  HUD: HP (top-left) | Timer (top-center) | Kills (top-right) │            ║
║   └──────────────────────────────────────────────────────────────┘            ║
║                                                                               ║
║   USER_FLOW: Menu → Play → Survive/Die → See results → Restart/Quit          ║
║   VALUE_ADD: Complete game loop with polish, smooth movement, clear feedback  ║
║   DATA_FLOW: Scene switches → entity updates (dt) → collision checks →        ║
║              state changes → HUD rendering → scene transitions                ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location          | Before             | After                            | User Impact                       |
| ----------------- | ------------------ | -------------------------------- | --------------------------------- |
| `main.py`         | Direct pygame loop | Delegates to Game class          | Cleaner architecture              |
| Window            | 800x600            | 1280x720                         | Larger play area                  |
| Menu Scene        | N/A                | Title + instructions             | Clear entry point                 |
| Play Scene        | N/A                | Player + zombies + bullets + HUD | Full gameplay experience          |
| WASD              | No effect          | Player moves smoothly            | Responsive controls               |
| Mouse LMB         | No effect          | Shoots bullets toward mouse      | Interactive shooting              |
| Zombies           | N/A                | Spawn and chase player           | Challenge/threat                  |
| Collisions        | N/A                | Bullets kill zombies, HP drains  | Win/lose mechanics                |
| Timer             | N/A                | Counts to 60 seconds             | Win condition                     |
| Game Over Scene   | N/A                | Shows result + kills + controls  | Clear end state and restart flow  |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File                                                                 | Lines  | Why Read This                                       |
| -------- | -------------------------------------------------------------------- | ------ | --------------------------------------------------- |
| P0       | `zombie-shooter/src/game/main.py`                                    | 1-30   | Current pygame initialization pattern to MIRROR     |
| P0       | `zombie-shooter/pyproject.toml`                                      | all    | Type hints, ruff config, dependencies to FOLLOW     |
| P0       | `PRPs/001_topdown_mvp.md`                                            | all    | Complete specification - the source of truth        |
| P1       | `zombie-shooter/README.md`                                           | all    | Run commands and project structure overview         |

**External Documentation:**

| Source                                                                                                                             | Section                      | Why Needed                                            |
| ---------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- | ----------------------------------------------------- |
| [pygame.math docs](https://www.pygame.org/docs/ref/math.html)                                                                      | Vector2                      | Position/velocity with delta-time movement            |
| [Scene Manager Pattern](https://nerdparadise.com/programming/pygame/part7)                                                         | Centralized Scene Logic      | Scene switching architecture                          |
| [Delta Time Best Practices](https://coderivers.org/blog/delta-time-python/)                                                       | Frame-independent movement   | Ensure 60 FPS consistency                             |
| [Circle Collision Detection](https://github.com/Rabbid76/PyGameExamplesAndAnswers/blob/master/documentation/pygame/pygame_collision_and_intesection.md) | Distance squared optimization | Performance-optimized collision checks                |
| [Pygame Event Handling](https://www.pygame.org/docs/ref/event.html)                                                               | Event types                  | QUIT, KEYDOWN, MOUSEBUTTONDOWN patterns               |

---

## Patterns to Mirror

**TYPE_ANNOTATIONS:**
```python
# SOURCE: zombie-shooter/src/game/main.py:1-4
# COPY THIS PATTERN:
"""Main entry point for the zombie shooter game."""

from __future__ import annotations

import pygame


def main() -> None:
    """Launch the game."""
```

**PYGAME_INITIALIZATION:**
```python
# SOURCE: zombie-shooter/src/game/main.py:10-14
# COPY THIS PATTERN:
pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Zombie Shooter")
clock = pygame.time.Clock()
running = True
```

**GAME_LOOP:**
```python
# SOURCE: zombie-shooter/src/game/main.py:16-24
# COPY THIS PATTERN (but refactor to use Game class):
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    pygame.display.flip()
    clock.tick(60)
```

**DELTA_TIME_CALCULATION:**
```python
# RECOMMENDED PATTERN (from pygame best practices):
# Calculate delta time in seconds
dt = clock.tick(60) / 1000.0

# Use for movement (speed in pixels per second)
player.pos.x += player.vel.x * dt
```

**SCENE_INTERFACE:**
```python
# PATTERN TO IMPLEMENT (from PRP-001):
class Scene:
    """Base class for all game scenes."""

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle pygame events."""
        pass

    def update(self, dt: float) -> None:
        """Update scene logic (dt in seconds)."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Draw scene to screen."""
        pass
```

**ENTITY_INTERFACE:**
```python
# PATTERN TO IMPLEMENT (from PRP-001):
class Entity:
    """Base pattern for game entities."""

    def __init__(self, pos: pygame.Vector2) -> None:
        self.pos = pos
        self.vel = pygame.Vector2(0, 0)
        self.radius = 10  # for collision

    def update(self, dt: float) -> None:
        """Update entity (dt in seconds)."""
        self.pos += self.vel * dt

    def draw(self, screen: pygame.Surface) -> None:
        """Draw entity to screen."""
        pygame.draw.circle(screen, (255, 255, 255), (int(self.pos.x), int(self.pos.y)), self.radius)
```

**CIRCLE_COLLISION_CHECK:**
```python
# PATTERN TO IMPLEMENT (optimized, no square root):
def check_collision_circle(pos1: pygame.Vector2, r1: float,
                          pos2: pygame.Vector2, r2: float) -> bool:
    """Check if two circles overlap using distance squared."""
    # Calculate distance squared
    dx = pos2.x - pos1.x
    dy = pos2.y - pos1.y
    distance_squared = dx * dx + dy * dy

    # Compare with sum of radii squared
    radius_sum = r1 + r2
    return distance_squared <= radius_sum * radius_sum
```

**CONSTANTS_STRUCTURE:**
```python
# PATTERN TO IMPLEMENT (from PRP-001 Section 6):
"""Game constants for zombie shooter."""

from __future__ import annotations

# Window
WIDTH = 1280
HEIGHT = 720
FPS = 60

# Player
PLAYER_SPEED = 300  # pixels per second
PLAYER_RADIUS = 18
PLAYER_MAX_HP = 100
CONTACT_DPS = 10  # damage per second

# Bullets
BULLET_SPEED = 700
BULLET_RADIUS = 4
BULLET_TTL = 1.5  # time to live in seconds
SHOOT_COOLDOWN = 0.15

# Zombies
ZOMBIE_SPEED = 140
ZOMBIE_RADIUS = 16
MAX_ZOMBIES = 50

# Spawning
SPAWN_INTERVAL_START = 1.0
SPAWN_INTERVAL_MIN = 0.25
SPAWN_RAMP_SECONDS = 45

# Win Condition
SURVIVE_SECONDS = 60
```

---

## Files to Change

| File                                    | Action | Justification                                        |
| --------------------------------------- | ------ | ---------------------------------------------------- |
| `src/game/core/constants.py`            | CREATE | Centralize all game constants (PRP-001 Section 6)    |
| `src/game/core/scene.py`                | CREATE | Base Scene class with handle_event/update/draw       |
| `src/game/core/game.py`                 | CREATE | Game class managing scenes and main loop             |
| `src/game/main.py`                      | UPDATE | Refactor to delegate to Game class                   |
| `src/game/scenes/menu.py`               | CREATE | Menu scene (Milestone 2)                             |
| `src/game/entities/player.py`           | CREATE | Player entity with movement and shooting             |
| `src/game/scenes/play.py`               | CREATE | Play scene orchestrating gameplay (Milestone 3-6)    |
| `src/game/entities/bullet.py`           | CREATE | Bullet entity with TTL and movement                  |
| `src/game/entities/zombie.py`           | CREATE | Zombie entity with seeking AI                        |
| `src/game/systems/spawner.py`           | CREATE | Zombie spawning system with difficulty ramp          |
| `src/game/systems/collisions.py`        | CREATE | Collision detection using distance squared           |
| `src/game/scenes/game_over.py`          | CREATE | Game over scene showing results (Milestone 7)        |
| `tests/test_collisions.py`              | UPDATE | Unit tests for collision system                      |

---

## NOT Building (Scope Limits)

Explicit exclusions to prevent scope creep (from PRP-001 Section 2):

- **Sprite art/animations**: Only placeholder shapes (circles, rectangles) - no image assets
- **Sound effects/music**: Silent game - audio is out of scope for MVP
- **Weapon upgrades/pickups**: Single weapon type, no powerups
- **Multiple enemy types**: Only zombies, no variety
- **Level generation/obstacles**: Open arena, no walls or terrain
- **Particle effects/screen shake**: No visual polish effects
- **Multiplayer**: Single-player only
- **Save/load progression**: No persistence between runs
- **Complex UI framework**: Simple text rendering only, no UI library
- **Configuration menu**: Hardcoded settings (no volume, sensitivity controls)

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Milestone 1: Boot & Core Loop

#### Task 1: CREATE `src/game/core/constants.py`

- **ACTION**: CREATE constants file with all game parameters
- **IMPLEMENT**: All constants from PRP-001 Section 6 (window, player, bullets, zombies, spawning, win condition)
- **MIRROR**: Pattern shown in "CONSTANTS_STRUCTURE" section above
- **IMPORTS**: `from __future__ import annotations`
- **GOTCHA**: Use descriptive names (PLAYER_SPEED not SPEED), include units in comments (pixels per second, seconds)
- **VALIDATE**: `ruff check src/game/core/constants.py && python -c "from src.game.core.constants import WIDTH; print(WIDTH)"`

#### Task 2: CREATE `src/game/core/scene.py`

- **ACTION**: CREATE base Scene class defining the interface
- **IMPLEMENT**: Abstract base class with handle_event, update, draw methods
- **MIRROR**: Pattern shown in "SCENE_INTERFACE" section above
- **IMPORTS**: `from __future__ import annotations`, `import pygame`
- **PATTERN**: Empty implementations that raise NotImplementedError or pass (subclasses will override)
- **GOTCHA**: Use `pygame.event.Event` type hint for event parameter
- **VALIDATE**: `ruff check src/game/core/scene.py && python -c "from src.game.core.scene import Scene; print('Scene imported')"`

#### Task 3: CREATE `src/game/core/game.py`

- **ACTION**: CREATE Game class managing pygame lifecycle and scene switching
- **IMPLEMENT**:
  - `__init__()`: Initialize pygame, create window (WIDTH x HEIGHT from constants), create clock
  - `run()`: Main game loop with delta-time calculation and scene delegation
  - `change_scene(new_scene: Scene)`: Switch active scene
  - `quit()`: Set running flag to False
- **MIRROR**: Current main.py structure but encapsulated in class
- **IMPORTS**: `from __future__ import annotations`, `import pygame`, `from src.game.core.constants import WIDTH, HEIGHT, FPS`, `from src.game.core.scene import Scene`
- **PATTERN**:
  ```python
  def run(self) -> None:
      while self.running:
          dt = self.clock.tick(FPS) / 1000.0  # Convert to seconds

          for event in pygame.event.get():
              if event.type == pygame.QUIT:
                  self.running = False
              self.scene.handle_event(event)

          self.scene.update(dt)
          self.scene.draw(self.screen)
          pygame.display.flip()
  ```
- **GOTCHA**: Store scene as instance variable, initialize with a default scene (will be Menu)
- **VALIDATE**: `ruff check src/game/core/game.py`

#### Task 4: UPDATE `src/game/main.py`

- **ACTION**: Refactor to use Game class instead of direct pygame loop
- **IMPLEMENT**:
  - Import Game class
  - Import Menu scene (will implement next)
  - Create Game instance
  - Create initial Menu scene
  - Call game.run()
- **MIRROR**: Keep same entry point structure, same docstring style
- **IMPORTS**: `from src.game.core.game import Game`, `from src.game.scenes.menu import MenuScene`
- **PATTERN**:
  ```python
  def main() -> None:
      """Launch the game."""
      game = Game()
      game.change_scene(MenuScene(game))
      game.run()
  ```
- **GOTCHA**: Pass game instance to scene so scene can switch to other scenes
- **VALIDATE**: Code compiles but won't run yet (Menu not implemented) - `ruff check src/game/main.py`

---

### Milestone 2: Menu Scene

#### Task 5: CREATE `src/game/scenes/menu.py`

- **ACTION**: CREATE menu scene showing title and instructions
- **IMPLEMENT**:
  - Display "Zombie Shooter" title (centered, large font)
  - Display "Press ENTER to Start" (centered below title)
  - Display "Press ESC to Quit" (centered below)
  - ENTER key → switch to PlayScene
  - ESC key → quit game
- **MIRROR**: Scene base class pattern from Task 2
- **IMPORTS**: `from __future__ import annotations`, `import pygame`, `from src.game.core.scene import Scene`, `from src.game.core.constants import WIDTH, HEIGHT`
- **PATTERN**:
  ```python
  class MenuScene(Scene):
      def __init__(self, game) -> None:
          self.game = game
          self.font_large = pygame.font.Font(None, 74)
          self.font_small = pygame.font.Font(None, 36)

      def handle_event(self, event: pygame.event.Event) -> None:
          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_RETURN:
                  from src.game.scenes.play import PlayScene
                  self.game.change_scene(PlayScene(self.game))
              elif event.key == pygame.K_ESCAPE:
                  self.game.quit()

      def update(self, dt: float) -> None:
          pass  # No updates needed for static menu

      def draw(self, screen: pygame.Surface) -> None:
          screen.fill((0, 0, 0))  # Black background
          # Render text (centered)
  ```
- **GOTCHA**: Import PlayScene inside handle_event to avoid circular import, use `pygame.font.Font(None, size)` for default font
- **VALIDATE**: `ruff check src/game/scenes/menu.py && zombie-shooter/.venv/bin/python zombie-shooter/src/game/main.py` (should show menu, ESC exits, ENTER crashes because PlayScene not implemented)

---

### Milestone 3: Play Scene Skeleton + Player Movement

#### Task 6: CREATE `src/game/entities/player.py`

- **ACTION**: CREATE Player entity with WASD movement and screen bounds clamping
- **IMPLEMENT**:
  - `__init__(pos, speed, radius, max_hp)` with defaults from constants
  - `update(dt)`: Read WASD keys, set velocity, update position, clamp to screen
  - `draw(screen)`: Draw blue circle at position
  - `hp` property with getter/setter
- **MIRROR**: Entity interface pattern from "ENTITY_INTERFACE" section
- **IMPORTS**: `from __future__ import annotations`, `import pygame`, `from src.game.core.constants import PLAYER_SPEED, PLAYER_RADIUS, PLAYER_MAX_HP, WIDTH, HEIGHT`
- **PATTERN**:
  ```python
  class Player:
      def __init__(self, pos: pygame.Vector2) -> None:
          self.pos = pos
          self.vel = pygame.Vector2(0, 0)
          self.radius = PLAYER_RADIUS
          self.speed = PLAYER_SPEED
          self.hp = PLAYER_MAX_HP

      def update(self, dt: float) -> None:
          keys = pygame.key.get_pressed()
          self.vel.x = 0
          self.vel.y = 0

          if keys[pygame.K_a]:
              self.vel.x = -self.speed
          if keys[pygame.K_d]:
              self.vel.x = self.speed
          if keys[pygame.K_w]:
              self.vel.y = -self.speed
          if keys[pygame.K_s]:
              self.vel.y = self.speed

          # Normalize diagonal movement
          if self.vel.length() > 0:
              self.vel = self.vel.normalize() * self.speed

          # Update position
          self.pos += self.vel * dt

          # Clamp to screen
          self.pos.x = max(self.radius, min(WIDTH - self.radius, self.pos.x))
          self.pos.y = max(self.radius, min(HEIGHT - self.radius, self.pos.y))
  ```
- **GOTCHA**: Normalize velocity for diagonal movement (else player moves faster diagonally), clamp AFTER updating position
- **VALIDATE**: `ruff check src/game/entities/player.py`

#### Task 7: CREATE `src/game/scenes/play.py` (skeleton)

- **ACTION**: CREATE play scene with player rendering and movement (no zombies/bullets yet)
- **IMPLEMENT**:
  - Initialize Player at screen center
  - update(dt): Call player.update(dt)
  - draw(screen): Fill background, draw player, draw simple HUD (HP, Timer: 0.0, Kills: 0)
  - handle_event: Pass events through (will add shooting later)
- **MIRROR**: Scene pattern from Task 5
- **IMPORTS**: `from __future__ import annotations`, `import pygame`, `from src.game.core.scene import Scene`, `from src.game.core.constants import WIDTH, HEIGHT`, `from src.game.entities.player import Player`
- **PATTERN**:
  ```python
  class PlayScene(Scene):
      def __init__(self, game) -> None:
          self.game = game
          self.player = Player(pygame.Vector2(WIDTH / 2, HEIGHT / 2))
          self.timer = 0.0
          self.kills = 0
          self.font = pygame.font.Font(None, 36)

      def update(self, dt: float) -> None:
          self.timer += dt
          self.player.update(dt)

      def draw(self, screen: pygame.Surface) -> None:
          screen.fill((40, 40, 40))  # Dark gray background
          self.player.draw(screen)

          # HUD
          hp_text = self.font.render(f"HP: {self.player.hp}", True, (255, 255, 255))
          timer_text = self.font.render(f"Time: {self.timer:.1f} / 60", True, (255, 255, 255))
          kills_text = self.font.render(f"Kills: {self.kills}", True, (255, 255, 255))

          screen.blit(hp_text, (10, 10))
          screen.blit(timer_text, (WIDTH // 2 - 80, 10))
          screen.blit(kills_text, (WIDTH - 150, 10))
  ```
- **GOTCHA**: Start timer at 0.0, increment with dt each frame
- **VALIDATE**: `zombie-shooter/.venv/bin/python zombie-shooter/src/game/main.py` (Menu → ENTER → Play scene with moving player)

---

### Milestone 4: Aim + Shoot + Bullets

#### Task 8: CREATE `src/game/entities/bullet.py`

- **ACTION**: CREATE Bullet entity with directional movement and TTL
- **IMPLEMENT**:
  - `__init__(pos, direction, speed, radius, ttl)` with defaults from constants
  - `update(dt)`: Move in direction, decrement TTL, return True if alive
  - `draw(screen)`: Draw yellow circle
  - `is_alive()`: Check if TTL > 0 and in screen bounds
- **MIRROR**: Entity pattern from Task 6
- **IMPORTS**: `from __future__ import annotations`, `import pygame`, `from src.game.core.constants import BULLET_SPEED, BULLET_RADIUS, BULLET_TTL, WIDTH, HEIGHT`
- **PATTERN**:
  ```python
  class Bullet:
      def __init__(self, pos: pygame.Vector2, direction: pygame.Vector2) -> None:
          self.pos = pos.copy()  # Copy to avoid reference issues
          self.vel = direction.normalize() * BULLET_SPEED
          self.radius = BULLET_RADIUS
          self.ttl = BULLET_TTL

      def update(self, dt: float) -> bool:
          """Update bullet. Returns True if still alive."""
          self.pos += self.vel * dt
          self.ttl -= dt
          return self.is_alive()

      def is_alive(self) -> bool:
          """Check if bullet should be removed."""
          if self.ttl <= 0:
              return False
          if self.pos.x < 0 or self.pos.x > WIDTH:
              return False
          if self.pos.y < 0 or self.pos.y > HEIGHT:
              return False
          return True

      def draw(self, screen: pygame.Surface) -> None:
          pygame.draw.circle(screen, (255, 255, 0), (int(self.pos.x), int(self.pos.y)), self.radius)
  ```
- **GOTCHA**: `pos.copy()` to avoid sharing reference with player pos, normalize direction before multiplying by speed
- **VALIDATE**: `ruff check src/game/entities/bullet.py`

#### Task 9: UPDATE `src/game/entities/player.py` (add shooting)

- **ACTION**: Add shooting capability to Player
- **IMPLEMENT**:
  - Add `shoot_cooldown` timer (starts at 0)
  - Add `shoot(mouse_pos)` method that returns Bullet or None
  - Decrement cooldown in update(dt)
- **MIRROR**: Existing player structure
- **IMPORTS**: Add `from src.game.entities.bullet import Bullet`, `from src.game.core.constants import SHOOT_COOLDOWN`
- **PATTERN**:
  ```python
  def __init__(self, pos: pygame.Vector2) -> None:
      # ... existing code ...
      self.shoot_cooldown = 0.0

  def update(self, dt: float) -> None:
      # ... existing movement code ...

      # Decrement cooldown
      if self.shoot_cooldown > 0:
          self.shoot_cooldown -= dt

  def shoot(self, target_pos: pygame.Vector2) -> Bullet | None:
      """Shoot bullet toward target if cooldown ready. Returns Bullet or None."""
      if self.shoot_cooldown > 0:
          return None

      direction = target_pos - self.pos
      if direction.length() == 0:
          return None

      self.shoot_cooldown = SHOOT_COOLDOWN
      return Bullet(self.pos, direction)
  ```
- **GOTCHA**: Check `direction.length() == 0` to avoid division by zero when normalizing
- **VALIDATE**: `ruff check src/game/entities/player.py`

#### Task 10: UPDATE `src/game/scenes/play.py` (add bullet management)

- **ACTION**: Add bullet list and shooting logic to PlayScene
- **IMPLEMENT**:
  - Add `self.bullets: list[Bullet] = []`
  - In `handle_event`: Check for MOUSEBUTTONDOWN (left click), call player.shoot, append bullet
  - In `update`: Update all bullets, filter dead bullets
  - In `draw`: Draw all bullets
- **MIRROR**: Existing PlayScene structure
- **IMPORTS**: Add `from src.game.entities.bullet import Bullet`
- **PATTERN**:
  ```python
  def __init__(self, game) -> None:
      # ... existing code ...
      self.bullets: list[Bullet] = []

  def handle_event(self, event: pygame.event.Event) -> None:
      if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
          mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
          bullet = self.player.shoot(mouse_pos)
          if bullet:
              self.bullets.append(bullet)

  def update(self, dt: float) -> None:
      # ... existing code ...

      # Update bullets and remove dead ones
      self.bullets = [b for b in self.bullets if b.update(dt)]

  def draw(self, screen: pygame.Surface) -> None:
      # ... existing code ...

      # Draw bullets
      for bullet in self.bullets:
          bullet.draw(screen)
  ```
- **GOTCHA**: List comprehension filtering is cleaner than loop with remove()
- **VALIDATE**: `zombie-shooter/.venv/bin/python zombie-shooter/src/game/main.py` (can shoot bullets with LMB)

---

### Milestone 5: Zombie Spawning + Seek AI

#### Task 11: CREATE `src/game/entities/zombie.py`

- **ACTION**: CREATE Zombie entity that seeks player position
- **IMPLEMENT**:
  - `__init__(pos, speed, radius)` with defaults from constants
  - `update(dt, player_pos)`: Move toward player position
  - `draw(screen)`: Draw green circle
- **MIRROR**: Entity pattern from previous entities
- **IMPORTS**: `from __future__ import annotations`, `import pygame`, `from src.game.core.constants import ZOMBIE_SPEED, ZOMBIE_RADIUS`
- **PATTERN**:
  ```python
  class Zombie:
      def __init__(self, pos: pygame.Vector2) -> None:
          self.pos = pos
          self.radius = ZOMBIE_RADIUS
          self.speed = ZOMBIE_SPEED

      def update(self, dt: float, player_pos: pygame.Vector2) -> None:
          """Move toward player position."""
          direction = player_pos - self.pos
          if direction.length() > 0:
              self.vel = direction.normalize() * self.speed
              self.pos += self.vel * dt

      def draw(self, screen: pygame.Surface) -> None:
          pygame.draw.circle(screen, (0, 255, 0), (int(self.pos.x), int(self.pos.y)), self.radius)
  ```
- **GOTCHA**: Check `direction.length() > 0` before normalizing to avoid division by zero
- **VALIDATE**: `ruff check src/game/entities/zombie.py`

#### Task 12: CREATE `src/game/systems/spawner.py`

- **ACTION**: CREATE zombie spawner system with difficulty ramping
- **IMPLEMENT**:
  - `__init__()`: Set initial spawn interval
  - `update(dt, elapsed_time)`: Decrement spawn timer, return True when ready to spawn
  - `get_spawn_interval(elapsed_time)`: Calculate current spawn interval with linear ramp
  - `get_spawn_position()`: Return random position at screen edge
- **MIRROR**: System module pattern (functions or class)
- **IMPORTS**: `from __future__ import annotations`, `import random`, `import pygame`, `from src.game.core.constants import *`
- **PATTERN**:
  ```python
  class ZombieSpawner:
      def __init__(self) -> None:
          self.spawn_timer = SPAWN_INTERVAL_START

      def update(self, dt: float, elapsed_time: float) -> bool:
          """Update spawn timer. Returns True when ready to spawn."""
          self.spawn_timer -= dt
          if self.spawn_timer <= 0:
              self.spawn_timer = self.get_spawn_interval(elapsed_time)
              return True
          return False

      def get_spawn_interval(self, elapsed_time: float) -> float:
          """Calculate spawn interval with linear ramp."""
          progress = min(elapsed_time / SPAWN_RAMP_SECONDS, 1.0)
          return SPAWN_INTERVAL_START - (SPAWN_INTERVAL_START - SPAWN_INTERVAL_MIN) * progress

      def get_spawn_position(self) -> pygame.Vector2:
          """Get random position at screen edge."""
          side = random.choice(['top', 'bottom', 'left', 'right'])
          if side == 'top':
              return pygame.Vector2(random.uniform(0, WIDTH), 0)
          elif side == 'bottom':
              return pygame.Vector2(random.uniform(0, WIDTH), HEIGHT)
          elif side == 'left':
              return pygame.Vector2(0, random.uniform(0, HEIGHT))
          else:  # right
              return pygame.Vector2(WIDTH, random.uniform(0, HEIGHT))
  ```
- **GOTCHA**: Linear interpolation for spawn rate, reset timer to NEW interval (not fixed value)
- **VALIDATE**: `ruff check src/game/systems/spawner.py`

#### Task 13: UPDATE `src/game/scenes/play.py` (add zombie spawning)

- **ACTION**: Add zombie list and spawner to PlayScene
- **IMPLEMENT**:
  - Add `self.zombies: list[Zombie] = []`
  - Add `self.spawner = ZombieSpawner()`
  - In `update`: Call spawner, create zombies (cap at MAX_ZOMBIES), update all zombies
  - In `draw`: Draw all zombies
- **MIRROR**: Similar to bullet management in Task 10
- **IMPORTS**: Add `from src.game.entities.zombie import Zombie`, `from src.game.systems.spawner import ZombieSpawner`, `from src.game.core.constants import MAX_ZOMBIES`
- **PATTERN**:
  ```python
  def __init__(self, game) -> None:
      # ... existing code ...
      self.zombies: list[Zombie] = []
      self.spawner = ZombieSpawner()

  def update(self, dt: float) -> None:
      # ... existing code ...

      # Spawn zombies
      if self.spawner.update(dt, self.timer) and len(self.zombies) < MAX_ZOMBIES:
          spawn_pos = self.spawner.get_spawn_position()
          self.zombies.append(Zombie(spawn_pos))

      # Update zombies
      for zombie in self.zombies:
          zombie.update(dt, self.player.pos)

  def draw(self, screen: pygame.Surface) -> None:
      # ... existing code ...

      # Draw zombies
      for zombie in self.zombies:
          zombie.draw(screen)
  ```
- **GOTCHA**: Check MAX_ZOMBIES cap before spawning, pass player position to zombie update
- **VALIDATE**: `zombie-shooter/.venv/bin/python zombie-shooter/src/game/main.py` (zombies spawn and chase player)

---

### Milestone 6: Collisions, Damage, Kills

#### Task 14: CREATE `src/game/systems/collisions.py`

- **ACTION**: CREATE collision detection system using distance squared
- **IMPLEMENT**:
  - `check_collision_circle(pos1, r1, pos2, r2)`: Circle-circle collision
  - `check_bullet_zombie_collisions(bullets, zombies)`: Return list of (bullet_idx, zombie_idx) pairs
  - `check_player_zombie_collision(player_pos, player_radius, zombie_pos, zombie_radius)`: Single check
- **MIRROR**: Circle collision pattern from "CIRCLE_COLLISION_CHECK" section
- **IMPORTS**: `from __future__ import annotations`, `import pygame`
- **PATTERN**:
  ```python
  def check_collision_circle(
      pos1: pygame.Vector2, r1: float, pos2: pygame.Vector2, r2: float
  ) -> bool:
      """Check if two circles overlap using distance squared (no sqrt)."""
      dx = pos2.x - pos1.x
      dy = pos2.y - pos1.y
      distance_squared = dx * dx + dy * dy
      radius_sum = r1 + r2
      return distance_squared <= radius_sum * radius_sum


  def check_bullet_zombie_collisions(
      bullets: list, zombies: list
  ) -> list[tuple[int, int]]:
      """Check all bullet-zombie collisions. Returns [(bullet_idx, zombie_idx), ...]."""
      collisions = []
      for b_idx, bullet in enumerate(bullets):
          for z_idx, zombie in enumerate(zombies):
              if check_collision_circle(bullet.pos, bullet.radius, zombie.pos, zombie.radius):
                  collisions.append((b_idx, z_idx))
      return collisions


  def check_player_zombie_collisions(
      player_pos: pygame.Vector2, player_radius: float, zombies: list
  ) -> list[int]:
      """Check player-zombie collisions. Returns list of zombie indices."""
      colliding = []
      for z_idx, zombie in enumerate(zombies):
          if check_collision_circle(player_pos, player_radius, zombie.pos, zombie.radius):
              colliding.append(z_idx)
      return colliding
  ```
- **GOTCHA**: Return indices, not objects (so caller can remove from lists), don't use sqrt (distance squared is sufficient)
- **VALIDATE**: `ruff check src/game/systems/collisions.py`

#### Task 15: UPDATE `src/game/scenes/play.py` (add collision handling)

- **ACTION**: Add collision detection and damage/kill logic
- **IMPLEMENT**:
  - In `update`: Check bullet-zombie collisions, remove collided entities, increment kills
  - In `update`: Check player-zombie collisions, apply damage (CONTACT_DPS * dt per zombie)
  - In `update`: Check if player HP <= 0, switch to GameOverScene (will create next)
- **MIRROR**: Existing update structure
- **IMPORTS**: Add `from src.game.systems.collisions import check_bullet_zombie_collisions, check_player_zombie_collisions`, `from src.game.core.constants import CONTACT_DPS`
- **PATTERN**:
  ```python
  def update(self, dt: float) -> None:
      # ... existing code ...

      # Bullet-zombie collisions
      bullet_zombie_hits = check_bullet_zombie_collisions(self.bullets, self.zombies)

      # Remove hit bullets and zombies (reverse order to avoid index issues)
      bullets_to_remove = set()
      zombies_to_remove = set()
      for b_idx, z_idx in bullet_zombie_hits:
          bullets_to_remove.add(b_idx)
          zombies_to_remove.add(z_idx)
          self.kills += 1

      self.bullets = [b for i, b in enumerate(self.bullets) if i not in bullets_to_remove]
      self.zombies = [z for i, z in enumerate(self.zombies) if i not in zombies_to_remove]

      # Player-zombie collisions (damage over time)
      colliding_zombies = check_player_zombie_collisions(
          self.player.pos, self.player.radius, self.zombies
      )
      if colliding_zombies:
          damage = CONTACT_DPS * dt * len(colliding_zombies)
          self.player.hp -= damage

      # Check game over
      if self.player.hp <= 0:
          from src.game.scenes.game_over import GameOverScene
          self.game.change_scene(GameOverScene(self.game, self.kills, won=False))
  ```
- **GOTCHA**: Use sets to avoid removing same entity twice, multiply damage by number of colliding zombies AND dt, import GameOverScene in function to avoid circular import
- **VALIDATE**: `zombie-shooter/.venv/bin/python zombie-shooter/src/game/main.py` (can kill zombies, can take damage and die)

---

### Milestone 7: Win Condition + End Screens

#### Task 16: CREATE `src/game/scenes/game_over.py`

- **ACTION**: CREATE game over scene showing result, kills, and restart instructions
- **IMPLEMENT**:
  - `__init__(game, kills, won)`: Store result and kills
  - Display "You Win!" or "Game Over" based on won flag
  - Display kills count
  - Display "Press R to Restart" and "Press ESC for Menu"
  - R key → restart PlayScene
  - ESC key → return to MenuScene
- **MIRROR**: Menu scene pattern from Task 5
- **IMPORTS**: `from __future__ import annotations`, `import pygame`, `from src.game.core.scene import Scene`, `from src.game.core.constants import WIDTH, HEIGHT`
- **PATTERN**:
  ```python
  class GameOverScene(Scene):
      def __init__(self, game, kills: int, won: bool) -> None:
          self.game = game
          self.kills = kills
          self.won = won
          self.font_large = pygame.font.Font(None, 74)
          self.font_medium = pygame.font.Font(None, 48)
          self.font_small = pygame.font.Font(None, 36)

      def handle_event(self, event: pygame.event.Event) -> None:
          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_r:
                  from src.game.scenes.play import PlayScene
                  self.game.change_scene(PlayScene(self.game))
              elif event.key == pygame.K_ESCAPE:
                  from src.game.scenes.menu import MenuScene
                  self.game.change_scene(MenuScene(self.game))

      def update(self, dt: float) -> None:
          pass

      def draw(self, screen: pygame.Surface) -> None:
          screen.fill((0, 0, 0))

          # Result text
          result_text = "You Win!" if self.won else "Game Over"
          result_color = (0, 255, 0) if self.won else (255, 0, 0)
          result_surface = self.font_large.render(result_text, True, result_color)

          # Kills text
          kills_surface = self.font_medium.render(f"Kills: {self.kills}", True, (255, 255, 255))

          # Instructions
          restart_surface = self.font_small.render("Press R to Restart", True, (200, 200, 200))
          menu_surface = self.font_small.render("Press ESC for Menu", True, (200, 200, 200))

          # Center and blit
          screen.blit(result_surface, (WIDTH // 2 - result_surface.get_width() // 2, 150))
          screen.blit(kills_surface, (WIDTH // 2 - kills_surface.get_width() // 2, 280))
          screen.blit(restart_surface, (WIDTH // 2 - restart_surface.get_width() // 2, 400))
          screen.blit(menu_surface, (WIDTH // 2 - menu_surface.get_width() // 2, 450))
  ```
- **GOTCHA**: Different colors for win (green) vs lose (red), import scenes in event handler to avoid circular imports
- **VALIDATE**: `ruff check src/game/scenes/game_over.py`

#### Task 17: UPDATE `src/game/scenes/play.py` (add win condition)

- **ACTION**: Add timer check for win condition
- **IMPLEMENT**:
  - In `update`: After incrementing timer, check if `timer >= SURVIVE_SECONDS`
  - If so, switch to GameOverScene with `won=True`
- **MIRROR**: Existing game over check from Task 15
- **IMPORTS**: Add `from src.game.core.constants import SURVIVE_SECONDS`
- **PATTERN**:
  ```python
  def update(self, dt: float) -> None:
      self.timer += dt

      # Check win condition
      if self.timer >= SURVIVE_SECONDS:
          from src.game.scenes.game_over import GameOverScene
          self.game.change_scene(GameOverScene(self.game, self.kills, won=True))
          return  # Don't process rest of update

      # ... rest of update code ...
  ```
- **GOTCHA**: Return early after switching scene to avoid processing game logic on final frame
- **VALIDATE**: `zombie-shooter/.venv/bin/python zombie-shooter/src/game/main.py` (full game loop works, can win by surviving 60s)

---

### Milestone 8: Testing & Polish

#### Task 18: UPDATE `tests/test_collisions.py`

- **ACTION**: Create unit tests for collision system
- **IMPLEMENT**:
  - Test `check_collision_circle` with overlapping, touching, and separated circles
  - Test edge cases: same position, zero radius, large distance
  - Test `check_bullet_zombie_collisions` with multiple bullets and zombies
- **MIRROR**: pytest style with descriptive test names
- **IMPORTS**: `from __future__ import annotations`, `import pygame`, `from src.game.systems.collisions import check_collision_circle, check_bullet_zombie_collisions`, `from src.game.entities.bullet import Bullet`, `from src.game.entities.zombie import Zombie`
- **PATTERN**:
  ```python
  """Tests for collision detection system."""

  from __future__ import annotations

  import pygame

  from src.game.systems.collisions import (
      check_collision_circle,
      check_bullet_zombie_collisions,
  )
  from src.game.entities.bullet import Bullet
  from src.game.entities.zombie import Zombie


  def test_check_collision_circle_overlapping() -> None:
      """Test that overlapping circles are detected."""
      pos1 = pygame.Vector2(0, 0)
      pos2 = pygame.Vector2(5, 0)
      assert check_collision_circle(pos1, 10, pos2, 10) is True


  def test_check_collision_circle_touching() -> None:
      """Test that touching circles are detected."""
      pos1 = pygame.Vector2(0, 0)
      pos2 = pygame.Vector2(20, 0)
      assert check_collision_circle(pos1, 10, pos2, 10) is True


  def test_check_collision_circle_separated() -> None:
      """Test that separated circles are not detected."""
      pos1 = pygame.Vector2(0, 0)
      pos2 = pygame.Vector2(25, 0)
      assert check_collision_circle(pos1, 10, pos2, 10) is False


  def test_check_collision_circle_same_position() -> None:
      """Test collision at same position."""
      pos = pygame.Vector2(100, 100)
      assert check_collision_circle(pos, 5, pos, 5) is True


  def test_check_bullet_zombie_collisions_empty() -> None:
      """Test with no bullets or zombies."""
      assert check_bullet_zombie_collisions([], []) == []


  def test_check_bullet_zombie_collisions_no_hits() -> None:
      """Test when bullets and zombies don't collide."""
      bullet = Bullet(pygame.Vector2(0, 0), pygame.Vector2(1, 0))
      zombie = Zombie(pygame.Vector2(100, 100))
      collisions = check_bullet_zombie_collisions([bullet], [zombie])
      assert collisions == []


  def test_check_bullet_zombie_collisions_hit() -> None:
      """Test when bullet hits zombie."""
      bullet = Bullet(pygame.Vector2(50, 50), pygame.Vector2(1, 0))
      zombie = Zombie(pygame.Vector2(52, 50))
      collisions = check_bullet_zombie_collisions([bullet], [zombie])
      assert len(collisions) == 1
      assert collisions[0] == (0, 0)
  ```
- **GOTCHA**: Test edge cases (empty lists, same position, exact touching), use descriptive test names
- **VALIDATE**: `cd zombie-shooter && .venv/bin/python -m pytest tests/test_collisions.py -v`

---

## Testing Strategy

### Unit Tests to Write

| Test File                   | Test Cases                                                    | Validates                           |
| --------------------------- | ------------------------------------------------------------- | ----------------------------------- |
| `tests/test_collisions.py`  | Overlapping circles, touching, separated, same pos, edge cases | Circle collision detection accuracy |

### Edge Cases Checklist

From PRP-001 Section 7:

- [ ] Closing the window exits cleanly (no hang) - pygame.QUIT event handled
- [ ] ESC always works - handled in menu and implicit in game over
- [ ] Player stays in bounds - clamping logic in player.update
- [ ] Bullet list doesn't grow indefinitely - bullets filtered by is_alive()
- [ ] Zombie list doesn't grow indefinitely - zombies removed on collision, capped at MAX_ZOMBIES
- [ ] Damage is based on dt (no frame-rate dependence) - `damage = CONTACT_DPS * dt * num_zombies`
- [ ] Restart resets timer, HP, entities, kills - new PlayScene instance created on R press
- [ ] Win screen triggers exactly once at 60s - early return after scene switch

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```bash
cd zombie-shooter && ruff check . && ruff format --check .
```

**EXPECT**: Exit 0, no errors or warnings

### Level 2: UNIT_TESTS

```bash
cd zombie-shooter && .venv/bin/python -m pytest tests/ -v
```

**EXPECT**: All tests pass, coverage >= 80% for collisions.py

### Level 3: TYPE_CHECK

```bash
cd zombie-shooter && .venv/bin/python -m mypy src/game --strict --ignore-missing-imports
```

**EXPECT**: No type errors (if mypy installed, otherwise skip)

### Level 4: RUN_GAME

```bash
cd zombie-shooter && .venv/bin/python src/game/main.py
```

**EXPECT**: Game launches, menu appears, full game loop works

### Level 5: MANUAL_VALIDATION

Execute manual test plan from PRP-001 Section 5.1:

1. Launch game → Menu appears with title and instructions
2. Press ENTER → Play scene starts with player at center
3. Press WASD → Player moves smoothly, stays on screen
4. Move mouse and left click → Bullets fire toward mouse cursor
5. Wait for zombies → Zombies spawn at edges and chase player
6. Shoot zombies → Zombies disappear, kills counter increments
7. Let zombie touch player → HP decreases over time
8. Get HP to 0 → Game Over screen appears with kills count
9. Press R → Game restarts from Play scene (HP, timer, entities reset)
10. Survive 60 seconds → You Win screen appears
11. Press ESC from game over → Returns to Menu
12. Press ESC from menu → Game exits cleanly
13. Observe FPS → Should be stable at 60 FPS throughout

**EXPECT**: All interactions work as specified, no crashes, smooth performance

---

## Acceptance Criteria

- [ ] All 18 tasks completed in order
- [ ] Level 1-4 validation commands pass with exit 0
- [ ] Unit tests achieve >= 80% coverage for collision system
- [ ] Manual validation checklist completed successfully
- [ ] Code follows existing patterns (type hints, docstrings, naming conventions)
- [ ] No regressions (game still runs after each milestone)
- [ ] Performance: 60 FPS maintained with 50+ zombies and multiple bullets
- [ ] All 7 milestones deliver specified functionality
- [ ] Edge cases from PRP-001 Section 7 all handled

---

## Completion Checklist

- [ ] Milestone 1: Boot & Core Loop - Game class and scene switching works
- [ ] Milestone 2: Menu Scene - Menu displays and transitions to Play
- [ ] Milestone 3: Play Scene + Player - Player moves with WASD, stays on screen
- [ ] Milestone 4: Aim + Shoot - Bullets fire toward mouse with cooldown
- [ ] Milestone 5: Zombies - Zombies spawn and chase player
- [ ] Milestone 6: Collisions - Bullets kill zombies, zombies damage player
- [ ] Milestone 7: Win/Lose - Timer-based win condition, game over screen, restart works
- [ ] Milestone 8: Testing - Unit tests pass, manual validation complete
- [ ] Static analysis (ruff) passes
- [ ] Type checking passes (if mypy available)
- [ ] Game runs smoothly at 60 FPS
- [ ] All edge cases handled correctly

---

## Risks and Mitigations

| Risk                                | Likelihood | Impact | Mitigation                                                   |
| ----------------------------------- | ---------- | ------ | ------------------------------------------------------------ |
| Circular imports between scenes     | HIGH       | HIGH   | Import scenes inside event handlers, not at module level     |
| Frame rate drops with many entities | MEDIUM     | MEDIUM | Use distance squared (no sqrt), cap zombies at 50, filter bullets efficiently |
| Diagonal movement too fast          | HIGH       | LOW    | Normalize velocity vector before multiplying by speed        |
| Zombie spawning off-screen edges    | LOW        | LOW    | Use random.uniform for continuous spawn positions            |
| Player HP going negative            | LOW        | LOW    | Check `hp <= 0` immediately, switch scene before rendering   |
| Bullet list memory leak             | MEDIUM     | HIGH   | Filter bullets with is_alive() every frame                   |
| Delta-time inconsistency            | LOW        | MEDIUM | Use `clock.tick(60) / 1000.0` pattern consistently           |
| Division by zero in normalization   | MEDIUM     | HIGH   | Check `length() > 0` before calling normalize()              |

---

## Notes

### Design Decisions

1. **No ECS**: Simple object-based architecture per PRP-001 spec - prioritizes readability and learning over scalability
2. **Circle collisions only**: Distance squared optimization avoids expensive square root, adequate for MVP
3. **Scene import pattern**: Import scenes in event handlers to avoid circular dependencies while keeping clean separation
4. **Delta-time everywhere**: All movement/timers use dt multiplication for frame-rate independence
5. **Placeholder graphics**: Only pygame.draw primitives (circles) - no image assets needed, focuses on architecture

### Trade-offs

- **Performance vs Simplicity**: O(n*m) collision checking is simple but won't scale to thousands of entities (acceptable for MVP with 50 zombie cap)
- **Coupling**: Scenes know about each other for switching (could use enum-based registry, but adds complexity)
- **Global constants**: Single constants.py instead of per-module constants (easier to tune, but harder to encapsulate)

### Future Considerations (Post-MVP)

From PRP-001 Section 8 - explicitly deferred to future PRPs:
- Sprite art and animations
- Sound effects and music
- Multiple weapons and pickups
- Wave UI and difficulty curve tuning beyond spawn rate
- Obstacles and map boundaries
- Particle effects and screen shake
- Settings menu (volume, sensitivity)
- Save/load progression

---

**Generated**: 2026-01-22
**Status**: READY FOR IMPLEMENTATION
**Confidence Score**: 9/10 for one-pass implementation success

**Rationale for Score**:
- All patterns extracted from existing codebase (main.py, pyproject.toml)
- External research provides battle-tested pygame patterns
- Task dependencies clearly ordered (no parallel work needed)
- Validation commands at each step prevent compounding errors
- Edge cases explicitly handled with code examples
- Only minor risk: circular imports (mitigated with clear import pattern)

**Next Step**: To execute, run: `/prp-implement zombie-shooter/.claude/PRPs/plans/topdown-zombie-shooter-mvp.plan.md`

---

## External Research Sources

- [pygame.math Vector2 Documentation](https://www.pygame.org/docs/ref/math.html)
- [PyGame Scene Manager: Centralized Scene Logic](https://nerdparadise.com/programming/pygame/part7)
- [Delta Time in Python: Comprehensive Guide](https://coderivers.org/blog/delta-time-python/)
- [Circle Collision Detection with Distance Squared](https://github.com/Rabbid76/PyGameExamplesAndAnswers/blob/master/documentation/pygame/pygame_collision_and_intesection.md)
- [Building Game Screens with Pygame](https://medium.com/@fulton_shaun/main-menus-to-cutscenes-building-game-screens-with-pygame-7415065c9fb9)
- [pygame-scene-manager GitHub](https://github.com/DumbChester021/pygame-scene-manager)
- [Pygame Movement and Motion Patterns](https://github.com/Rabbid76/PyGameExamplesAndAnswers/blob/master/documentation/pygame/pygame_movement_and_motion.md)
