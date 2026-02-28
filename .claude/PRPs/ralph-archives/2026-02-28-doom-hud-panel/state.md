---
iteration: 1
max_iterations: 20
plan_path: ".claude/PRPs/plans/doom-hud-panel.plan.md"
input_type: "plan"
started_at: "2026-02-28T00:00:00Z"
---

# PRP Ralph Loop State

## Codebase Patterns
- All constants are plain Python int/tuple — NO pygame imports in constants.py
- Module-level helper functions in play.py pre-build surfaces (build once, blit every frame)
- Player fields follow `self.xxx = 0.0` float init pattern; timers decremented in update()
- Tests: `pygame.init()` at module top, plain `def test_xxx()` pytest functions
- Import inside method body used for late/circular imports (e.g., GameOverScene at play.py:401)
- E501 lint (88 char limit): split long draw calls using intermediate variables for Rect coords
- `BLEND_RGB_MULT` flag on SRCALPHA surface: affects only RGB of non-transparent pixels

## Current Task
Execute doom-hud-panel.plan.md — 6 tasks.

## Plan Reference
.claude/PRPs/plans/doom-hud-panel.plan.md

## Instructions
1. Read the plan file
2. Implement all incomplete tasks
3. Run ALL validation commands from the plan
4. If any validation fails: fix and re-validate
5. Update plan file: mark completed tasks, add notes
6. When ALL validations pass: output <promise>COMPLETE</promise>

## Progress Log
(Append learnings after each iteration)

---
