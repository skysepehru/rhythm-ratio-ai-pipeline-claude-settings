# AI Development Flow

This project uses **agent-driven** development with inline context system.

## How It Works

Development is organized into **Iterations** (milestones) → **Tasks** (user-story level) → **Subtasks** (atomic units the agent handles one at a time).

The agent picks up the next subtask, plans it, implements it, validates it, updates project state, and commits. After each subtask, it stops and waits for you to invoke it again. You stay in control of pacing and direction.

### Commands

| Command | What it does |
|---------|-------------|
| `/unity-claude:unity-development progress` | Work on the next subtask in the current iteration. This is the main development loop. |
| `/unity-claude:unity-development <request>` | Freeform — ask for anything (ad-hoc work, exploration, refactoring). |
| `/unity-claude:unity-development sync` | Update context and state after you make manual changes outside the AI workflow. |
| `/unity-claude:backlog <description>` | Capture an issue or idea for later without interrupting current work. |

### What a Progress Session Looks Like

1. **Reconciliation** — Agent checks for changes since the last session (manual commits, freeform work, backlog items). Updates context and state if needed.
2. **Determine work** — Agent reads the current iteration. If tasks aren't broken down yet, it proposes a breakdown and discusses with you.
3. **Plan subtask** — Agent gathers context from architecture and file summaries, plans implementation and validation, discusses with you.
4. **Implement** — Agent writes code and tests.
5. **Validate** — Compile check, run tests, then prompt you for manual gameplay/visual testing.
6. **Wrap up** — Agent updates context for all modified files, reviews spec and architecture, commits.
7. **Stop** — Agent stops after each subtask. Run `progress` again to continue.

When all subtasks in a task are done, the agent does task-level wrap-up (history, architecture review, next task breakdown) and stops. When all tasks in an iteration are done, the agent advances to the next iteration.

### What the Agent Does Automatically

Every commit, the agent:
- Updates inline context summaries for all created/modified files
- Reviews Architecture.md and ProjectSpecification.md for needed updates
- Writes tests alongside implementation
- Follows project coding conventions (C#, Zenject, folder structure, UGUI)

## Key Files

| File | Purpose |
|------|---------|
| `.claude/State/Constants.md` | Project configuration and feature flags |
| `.claude/State/Architecture.md` | System architecture — subsystems, folder mappings, technical decisions |
| `.claude/State/ProjectSpecification.md` | Formalized game specification |
| `.claude/Planning/ProjectPlan.md` | Iteration roadmap |
| `.claude/Planning/CurrentIteration.md` | Active iteration with tasks and subtasks |
| `.claude/Planning/IterationHistory.md` | Summaries of completed iterations |
| `.claude/Planning/Backlog.md` | Issues and ideas captured for later |

## Active Conventions

Convention skills auto-load when relevant — you don't need to invoke them:
- **Coding conventions** — C# naming, style, organization, asmdef structure
- **Zenject conventions** — Dependency injection patterns
- **Folder conventions** — Where files go in the Unity project
- **UGUI development** — UI conventions
- **MCP tools** — Unity Editor interaction via MCP
- **Testing** — Edit mode vs play mode, Zenject test fixtures
- **Context system** — How context summaries are created and maintained
