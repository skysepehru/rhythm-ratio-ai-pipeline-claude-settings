# Development Core

Shared reference for all development modes. Read this first.

---

## File References

| Variable | Path | Purpose |
|----------|------|---------|
| `$PROJECT_SPECIFICATION` | `.claude/State/ProjectSpecification.md` | Formalized game specification |
| `$ARCHITECTURE` | `.claude/State/Architecture.md` | System architecture and subsystem map |
| `$CONSTANTS` | `.claude/State/Constants.md` | Project state flags |
| `$PROJECT_PLAN` | `.claude/Planning/ProjectPlan.md` | Iteration roadmap |
| `$CURRENT_ITERATION` | `.claude/Planning/CurrentIteration.md` | Active iteration with tasks/subtasks |
| `$ITERATION_HISTORY` | `.claude/Planning/IterationHistory.md` | Completed iteration summaries |
| `$HISTORY_DIR` | `.claude/Planning/History/` | Per-task detail files |

---

## Implementation Guidelines

- **Use auto-loaded skills** as usual: coding conventions, Zenject conventions, folder conventions, MCP tools.
- **Use direct reads** (`Read`, `Grep`, `Glob`) for codebase navigation. Do NOT use the Explore agent.
- **Refresh the AssetDatabase via MCP** after creating or modifying scripts/assets via file writes, so Unity picks up changes.
- **Summaries first, full content later.** During planning, read context summaries only. Load full file content during implementation.

---

## Validation

Read `validation.md` in the `shared` skill folder. Follow the section matching TESTS in `$CONSTANTS`:
- TESTS = true → "Full Validation" section
- TESTS = false → "No-Test Validation" section

---

## Commit

Read `git-strategy.md` in this skill folder for commit message format.

**You are not done until you have committed.** Do not end your response without either committing or explicitly stating what is blocking the commit (e.g., awaiting developer manual testing confirmation).

---

## Key Principles

- **Flag early, don't power through.** If assumptions don't match reality, stop and raise it before committing. Read `revisions.md` if something goes wrong.
- **Tests with implementation.** If a subtask warrants tests, they're written in the same subtask — not as separate work.
- **Manual testing at task level.** Subtasks commit automatically after validation (compile + tests). Manual gameplay/visual testing happens at task completion.

