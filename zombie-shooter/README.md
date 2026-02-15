# 🧟 Zombie Shooter

A fast-paced top-down survival shooter built with Pygame. Play as a Rambo-style action hero fighting endless waves of zombies with increasing difficulty. How long can you survive?

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.6+-green.svg)
![Tests](https://img.shields.io/badge/Tests-132%20passing-brightgreen.svg)

## 🎮 Features

### Core Gameplay
- **Endless Survival Mode**: Fight increasingly difficult waves of zombies
- **Increasing Difficulty**: Spawn rate ramps up over time - survive as long as you can
- **Score Tracking**: Survival time displayed in real-time
- **Smooth Animations**: Animated player and zombie sprites with walk cycles

### Player Character
- **Rambo-style Hero**: Muscular action hero with red headband
- **Walk Animations**: 4-directional animated walk cycle (up, down, left, right)
- **Shooting Animations**: Gun extends when firing - visual feedback for every shot
- **Movement**: Smooth 8-directional movement with WASD controls

### Weapons System
- **Pistol**: Starting weapon, balanced fire rate
- **Shotgun**: Spreads 5 pellets, devastating at close range
- **SMG**: Rapid fire, perfect for hordes
- **Weapon Pickups**: Collect new weapons during gameplay

### Zombie Variants
- **Normal Zombie**: Standard threat, moderate speed
- **Runner**: 2x speed, low HP - fast and dangerous
- **Tank**: 3x HP, slow, larger hitbox - tough to kill
- **Exploder**: Explodes on death, damages nearby zombies and player
- **Spitter**: Ranged acid attacks - keeps its distance

### Gore System
- **Blood Particles**: Spawn on zombie death with physics
- **Blood Decals**: Persistent ground splatter (fades over time)
- **Dead Corpses**: Zombie bodies remain visible after death
- **Explosion Effects**: Enhanced particles for exploder variant

### Quality of Life
- **Health System**: 100 HP with contact damage from zombies
- **Weapon Switching**: Cycle through collected weapons (1, 2, 3 keys)
- **FPS Counter**: Performance monitoring
- **Pause**: ESC to pause game

## 🕹️ Controls

| Key/Input | Action |
|-----------|--------|
| **W** | Move up |
| **A** | Move left |
| **S** | Move down |
| **D** | Move right |
| **Mouse Move** | Aim direction |
| **Left Click** | Shoot (hold for continuous fire) |
| **1** | Switch to Pistol |
| **2** | Switch to Shotgun (if collected) |
| **3** | Switch to SMG (if collected) |
| **ESC** | Pause / Return to menu |

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- `uv` (recommended) or `pip`

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd top_down_zombie_shooter/zombie-shooter
```

2. **Create virtual environment and install dependencies**

Using `uv` (recommended):
```bash
uv venv
uv pip install -e .
```

Or using `pip`:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

### Running the Game

**With activated virtual environment:**
```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python src/game/main.py
```

**Or directly:**
```bash
.venv/bin/python src/game/main.py
```

**With PYTHONPATH (alternative):**
```bash
export PYTHONPATH="src"
.venv/bin/python src/game/main.py
```

## 📁 Project Structure

```
zombie-shooter/
├── pyproject.toml              # Project configuration and dependencies
├── README.md                   # This file
├── src/
│   ├── assets/                 # Game assets
│   │   ├── players/           # Player sprite sheets (walk + shoot)
│   │   └── zombies/           # Zombie sprite sheets (5 variants)
│   └── game/
│       ├── main.py            # Entry point
│       ├── core/              # Core game engine
│       │   ├── game.py        # Game loop and window management
│       │   ├── scene.py       # Base scene class
│       │   └── constants.py   # Game constants and balance
│       ├── scenes/            # Game scenes
│       │   ├── menu.py        # Main menu
│       │   ├── play.py        # Main gameplay scene
│       │   └── game_over.py   # Game over screen
│       ├── entities/          # Game entities
│       │   ├── player.py      # Player character with animations
│       │   ├── zombie.py      # Zombie with variants
│       │   ├── bullet.py      # Projectiles
│       │   ├── pickup.py      # Weapon pickups
│       │   ├── blood_particle.py      # Gore particles
│       │   ├── blood_decal.py         # Ground blood
│       │   ├── dead_zombie.py         # Corpses
│       │   └── acid_projectile.py     # Spitter attacks
│       ├── systems/           # Game systems
│       │   ├── animation.py   # Animation state management
│       │   ├── collisions.py  # Collision detection
│       │   └── spawner.py     # Zombie spawning with difficulty ramp
│       └── assets/
│           └── loader.py      # Asset loading and caching
└── tests/                     # Comprehensive test suite
    ├── test_player_integration.py
    ├── test_zombie_integration.py
    ├── test_weapon_behavior.py
    ├── test_gore_integration.py
    └── ... (132 tests total)
```

## 🎯 Gameplay Mechanics

### Survival Mode
- **No time limit** - survive as long as possible
- **Progressive difficulty** - zombie spawn rate increases continuously
- **Spawn ramping** - starts at 1.0s intervals, reaches 0.25s minimum over 45 seconds
- **Max zombies** - up to 50 zombies on screen simultaneously

### Combat System
- **Weapon stats**:
  - **Pistol**: 0.15s fire rate, single bullet
  - **Shotgun**: 0.5s fire rate, 5 pellets with 30° spread
  - **SMG**: 0.08s fire rate, single bullet (rapid fire)
- **Bullet damage**: One-shot kill for normal/runner/exploder, 3 hits for tank
- **Contact damage**: 10 DPS when touching zombies
- **Player HP**: 100 HP, game over at 0

### Zombie Variants (Weighted Spawn)
- **Normal (70%)**: 140 speed, 1 HP, 16 radius
- **Runner (15%)**: 280 speed, 1 HP, 16 radius
- **Tank (15%)**: 98 speed, 3 HP, 24 radius (larger)
- **Exploder (10%)**: 140 speed, 1 HP, 80 radius explosion on death
- **Spitter (10%)**: 100 speed, 1 HP, ranged acid attacks (400 range)

### Gore Effects
- **Blood particles**: 8 particles spawn on death with physics
- **Blood decals**: 28px pools persist for visual feedback
- **Corpse persistence**: Dead zombies visible for 10 seconds
- **Explosion particles**: Enhanced effects for exploder variant (16 particles)

## 🧪 Development

### Running Tests

Run the full test suite (132 tests):
```bash
export PYTHONPATH="src"
.venv/bin/pytest tests/ -v
```

Run specific test file:
```bash
export PYTHONPATH="src"
.venv/bin/pytest tests/test_player_integration.py -v
```

Run with coverage:
```bash
export PYTHONPATH="src"
.venv/bin/pytest tests/ --cov=game --cov-report=html
```

### Code Quality

**Linting:**
```bash
.venv/bin/ruff check src/ tests/
```

**Formatting:**
```bash
.venv/bin/ruff format src/ tests/
```

**Type checking (if mypy installed):**
```bash
mypy src/
```

### Project Standards
- ✅ **Type hints** on all functions and methods
- ✅ **Google-style docstrings** for documentation
- ✅ **Ruff** for linting and formatting (88 char line length)
- ✅ **Pytest** for comprehensive testing (132 tests passing)
- ✅ **Asset caching** for performance optimization
- ✅ **Module-level sprite caching** to minimize memory

## 🎨 Asset Generation

All sprites are **programmatically generated** using Pygame:

- **Player sprites**: 48×48 pixels, Rambo-style character
  - 4 walk animations (3 frames each): `walk_down.png`, `walk_up.png`, `walk_left.png`, `walk_right.png`
  - 4 shoot poses (1 frame each): `shoot_down.png`, `shoot_up.png`, `shoot_left.png`, `shoot_right.png`

- **Zombie sprites**: 48×48 pixels, 5 variants
  - Each variant has 4 directions × 3 frames = 12 sprites
  - Normal, runner, tank, exploder, spitter variants
  - Color-coded for visual distinction

Generated via scripts in development process - no external art assets required.

## 📊 Technical Details

### Performance
- **Target FPS**: 60 FPS
- **Resolution**: 1280×720 (configurable in constants.py)
- **Entity cap**: 50 zombies maximum for performance
- **Sprite caching**: All sprites loaded once and cached

### Architecture Patterns
- **Scene-based architecture**: Menu → Play → GameOver
- **Entity-component pattern**: Separate entities for player, zombies, bullets, etc.
- **System-based logic**: Animation, collision, spawning as separate systems
- **Module-level caching**: Sprites shared across all entity instances

### Animation System
- **Frame-based animations**: 10 FPS animation playback
- **Direction detection**: Velocity-based automatic direction switching
- **State management**: Separate walk and shoot animation states
- **Smooth transitions**: Frame interpolation with delta time

## 🐛 Known Issues / Future Improvements

### Planned Features
- [ ] Score system (points for kills)
- [ ] High score tracking
- [ ] Sound effects and music
- [ ] Health pickups
- [ ] Dash/dodge ability
- [ ] Wave system with breaks
- [ ] Upgrade system between waves

### Performance Notes
- Game may slow down with 50+ zombies on lower-end hardware
- Particle effects accumulate - may affect performance in long runs

## 🤝 Contributing

This is a personal project, but feedback and suggestions are welcome!

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `pytest tests/`
5. Run linter: `ruff check src/ tests/`
6. Commit your changes: `git commit -m 'Add amazing feature'`
7. Push to branch: `git push origin feature/amazing-feature`
8. Open a Pull Request

## 📝 License

This project is created for educational and demonstration purposes.

## 🙏 Credits

- **Game Engine**: [Pygame](https://www.pygame.org/)
- **Development**: Built with Python 3.13
- **Sprites**: Programmatically generated pixel art
- **Inspiration**: Classic top-down shooters and survival games

## 🎮 Have Fun!

Survive as long as you can, collect weapons, and rack up kills. The zombies never stop coming... how long will you last?

**Good luck, survivor!** 🧟‍♂️💀🔫
