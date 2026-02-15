# Top-Down Zombie Shooter

A complete game development project built using AI-assisted **Plan-Research-Plan (PRP)** methodology, demonstrating structured feature planning, autonomous implementation, and comprehensive testing.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.6+-green.svg)
![Tests](https://img.shields.io/badge/Tests-132%20passing-brightgreen.svg)
![PRP](https://img.shields.io/badge/PRP-Methodology-orange.svg)

## 🎯 Project Overview

This repository showcases:
- **Complete Game**: A polished top-down zombie survival shooter with animated sprites, multiple weapons, and 5 zombie variants
- **PRP Methodology**: Structured AI-assisted development workflow with PRDs, implementation plans, and execution reports
- **Comprehensive Testing**: 132 tests with full validation coverage
- **Production-Ready Code**: Type hints, docstrings, linting, and proper architecture

## 📂 Repository Structure

```
top_down_zombie_shooter/
├── README.md                           # This file - project overview
├── zombie-shooter/                     # The game itself
│   ├── README.md                       # Game documentation
│   ├── src/game/                       # Game source code
│   ├── tests/                          # 132 comprehensive tests
│   └── pyproject.toml                  # Project configuration
└── .claude/                            # PRP methodology artifacts
    ├── PRPs/
    │   ├── README.md                   # PRP methodology documentation
    │   ├── prds/                       # Product Requirements Documents (5)
    │   ├── plans/                      # Implementation plans (21)
    │   ├── reports/                    # Implementation reports (23)
    │   └── ralph-archives/             # Autonomous execution logs (7)
    └── commands/                       # PRP command implementations
```

## 🎮 The Game: Zombie Shooter

A fast-paced top-down survival shooter featuring:
- **Endless Survival Mode**: Fight increasingly difficult waves of zombies
- **5 Zombie Variants**: Normal, Runner, Tank, Exploder, Spitter
- **3 Weapons**: Pistol, Shotgun, SMG with different stats
- **Animated Sprites**: Rambo-style player with walk and shoot animations
- **Gore System**: Blood particles, decals, and corpses
- **132 Tests**: Comprehensive test coverage

**[📖 Read the game README](zombie-shooter/README.md)** for controls, setup, and gameplay details.

### Quick Start (Play the Game)

```bash
cd zombie-shooter
uv venv && uv pip install -e .
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python src/game/main.py
```

## 🔄 PRP Methodology

This project was developed using the **Plan-Research-Plan (PRP)** methodology, an AI-assisted development workflow that emphasizes:

1. **PRD Creation**: Document problem, solution, and implementation phases
2. **Plan Generation**: Explore codebase, extract patterns, create detailed plans
3. **Autonomous Execution**: Ralph agent implements plans with automatic validation
4. **Reporting**: Document what was built, learnings, and patterns discovered

**[📖 Read the PRP README](.claude/PRPs/README.md)** for complete methodology documentation.

### PRP Workflow Example

```bash
# 1. Create a PRD for a new feature
/prp-prd "implement health pickups that spawn randomly"

# 2. Generate implementation plan from PRD phase
/prp-plan .claude/PRPs/prds/health-pickups.prd.md

# 3. Execute plan autonomously
/prp-ralph .claude/PRPs/plans/health-pickups.plan.md

# 4. Review implementation report
cat .claude/PRPs/reports/health-pickups-report.md
```

## 📊 Project Metrics

| Metric | Count |
|--------|-------|
| **PRDs** | 5 complete product requirements documents |
| **Implementation Plans** | 21 detailed feature plans |
| **Implementation Reports** | 23 completion reports |
| **Ralph Executions** | 7 autonomous implementation runs |
| **Tests** | 132 tests passing |
| **Lines of Code** | ~6,500 (game + tests) |
| **Implementation Success Rate** | ~100% (one-pass for most phases) |

## 🎯 Key Features Delivered

### Player Character (PRD 005)
- ✅ Rambo-style animated sprite (48×48 pixels)
- ✅ 4-directional walk animations (3 frames each)
- ✅ 4-directional shooting animations (gun extends on fire)
- ✅ Integration with existing animation system

### Zombie System (PRD 002, 004)
- ✅ 5 variants: Normal, Runner, Tank, Exploder, Spitter
- ✅ Animated walk cycles (4 directions, 3 frames)
- ✅ Weighted spawn system with difficulty ramping
- ✅ Unique behaviors (speed, HP, explosions, ranged attacks)

### Gore System (PRD 003)
- ✅ Blood particle physics (8 particles per death)
- ✅ Persistent blood decals (fade over time)
- ✅ Corpse entities (visible for 10 seconds)
- ✅ Explosion effects for Exploder variant

### Weapon System (PRD 001)
- ✅ 3 weapons: Pistol, Shotgun, SMG
- ✅ Weapon pickups with spawning system
- ✅ Different fire rates and behaviors
- ✅ Shotgun spread pattern (5 pellets)

## 🧪 Testing & Quality

```bash
# Run all tests
cd zombie-shooter
export PYTHONPATH="src"
.venv/bin/pytest tests/ -v

# Run linter
.venv/bin/ruff check src/ tests/

# Run formatter
.venv/bin/ruff format src/ tests/
```

**Test Coverage:**
- Player integration tests
- Zombie variant tests
- Weapon behavior tests
- Gore system tests
- Animation system tests
- Collision detection tests
- Spawning system tests

## 🏗️ Architecture Highlights

**Game Architecture:**
- Scene-based system (Menu → Play → GameOver)
- Entity-component pattern for game objects
- Separate systems for animation, collision, spawning
- Module-level sprite caching for performance

**PRP Architecture:**
- PRDs define product requirements and phases
- Plans include codebase patterns to mirror
- Ralph agent executes with iterative validation
- Reports capture learnings and patterns

## 📝 Development Standards

- ✅ **Type hints** on all functions
- ✅ **Google-style docstrings**
- ✅ **Ruff** for linting and formatting
- ✅ **Pytest** for testing
- ✅ **Asset caching** for performance
- ✅ **Comprehensive validation** (lint, tests, integration)

## 🚀 Use Cases

### For Game Developers
- Study the game architecture and entity system
- Learn sprite animation implementation
- See collision detection patterns
- Understand spawning and difficulty ramping

### For AI/LLM Practitioners
- Study the PRP methodology for structured AI-assisted development
- Review how codebase patterns are extracted and mirrored
- See autonomous implementation with validation loops
- Learn how to structure prompts for code generation

### For Project Managers
- Review PRDs for product requirement documentation
- Study phase breakdown and parallelism planning
- See metrics and success criteria definition
- Understand implementation reporting

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Game README](zombie-shooter/README.md) | Game features, controls, setup instructions |
| [PRP README](.claude/PRPs/README.md) | PRP methodology, workflow, document types |
| [PRDs](.claude/PRPs/prds/) | 5 product requirements documents |
| [Plans](.claude/PRPs/plans/) | 21 implementation plans with patterns |
| [Reports](.claude/PRPs/reports/) | 23 implementation reports with learnings |
| [Ralph Archives](.claude/PRPs/ralph-archives/) | Autonomous execution logs |

## 🎓 Learning Resources

### Study the PRP Methodology
1. Read [.claude/PRPs/README.md](.claude/PRPs/README.md) for workflow overview
2. Pick a PRD (e.g., `005_rambo-player-sprite-animations.prd.md`)
3. Follow its implementation phases through plans and reports
4. Review Ralph archives to see autonomous execution

### Study the Game Architecture
1. Read [zombie-shooter/README.md](zombie-shooter/README.md) for overview
2. Start with `src/game/main.py` - the entry point
3. Review `src/game/core/game.py` - game loop
4. Explore `src/game/entities/` - player, zombies, bullets
5. Check `tests/` - see how features are tested

## 🤝 Contributing

This is a demonstration project, but you can:
- Fork and experiment with the game
- Study the PRP methodology for your own projects
- Suggest improvements to the documentation
- Share your own PRP implementations

## 🎮 Try It Now

**Play the game:**
```bash
cd zombie-shooter
uv venv && uv pip install -e .
source .venv/bin/activate
python src/game/main.py
```

**Controls:**
- WASD: Move
- Mouse: Aim
- Left Click: Shoot
- 1/2/3: Switch weapons
- ESC: Pause

Survive as long as you can! 🧟‍♂️💀🔫

## 📄 License

Created for educational and demonstration purposes.

## 🙏 Credits

- **Game Engine**: [Pygame](https://www.pygame.org/)
- **Development**: Python 3.11+ with AI-assisted PRP methodology
- **Sprites**: Programmatically generated pixel art
- **Methodology**: Plan-Research-Plan (PRP) workflow

---

**Good luck, survivor!** 🎮

*Built with Claude Code using PRP methodology*
