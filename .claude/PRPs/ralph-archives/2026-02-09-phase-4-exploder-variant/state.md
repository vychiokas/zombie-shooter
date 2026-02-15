---
iteration: 1
max_iterations: 20
plan_path: ".claude/PRPs/plans/phase-4-exploder-variant.plan.md"
input_type: "prd"
started_at: "2026-02-09T22:30:00Z"
---

# PRP Ralph Loop State

## Codebase Patterns

**Death Detection** (play.py:197): `if zombie.hp <= 0:` triggers gore spawn and removal
**Circle Collision** (collisions.py:8-26): `check_collision_circle()` uses distance squared (no sqrt)
**Particle Spawn** (play.py:82-99): Random angles + velocities, append to list
**Damage Application**: Direct HP modification `entity.hp -= damage`, check if HP <= 0
**Variant System**: ZOMBIE_VARIANTS dict with speed/hp/radius/weight, variant param to Zombie()
**Sprite Loading**: Automatic variant directory handling (zombies/{variant}/)
**Test Pattern**: test_{variant}_variant.py with stats, behavior, sprite, integration tests

## Current Task

Execute Phase 4 (Exploder variant) plan - implement explosion on death with AOE damage to player and zombies.

## Plan Reference

.claude/PRPs/plans/phase-4-exploder-variant.plan.md

## Instructions

1. Read the plan file
2. Implement all incomplete tasks (5 core tasks)
3. Run ALL validation commands from the plan
4. If any validation fails: fix and re-validate
5. Update plan file: mark completed tasks, add notes
6. When ALL validations pass: output <promise>COMPLETE</promise>

## Progress Log

---
