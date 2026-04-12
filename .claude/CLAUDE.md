# Rhythm Ratio Unity

Hyper casual rhythm game for mobile. Swipe to slice lines at specific ratios and timings. Infinite gameplay with score and HP systems.
Full specification in `.claude/State/ProjectSpecification.md`.
Development is driven by an AI workflow that generates tasks and subtasks based on the project specification and architecture, guiding the developer through each step of the process.

## AI-Driven Development Workflow

This project uses AI-driven development via the `unity-claude` plugin. The workflow is configured during onboarding and described in `.claude/AIFlow.md`.

### Flow Overview

1. Developer runs `/unity-claude:unity-development progress` repeatedly to develop subtask by subtask (driven workflow)
2. Developer can run `/unity-claude:unity-development <request>` anytime for freeform development
3. Developer can run `/unity-claude:backlog <description>` anytime to capture issues for later
4. Developer can run `/unity-claude:unity-development sync` after manual changes to keep context and state current
5. Iteration advancement is handled automatically within the development skill when all tasks are complete

### Key Files

| File | Purpose |
|------|---------|
| `.claude/State/Constants.md` | Project configuration and feature flags |
| `.claude/State/Architecture.md` | System architecture (formalized from developer's technical vision) |
| `.claude/State/ProjectSpecification.md` | Formalized game spec (generated from description, living reference) |
| `.claude/AIFlow.md` | Generated guide: how AI development works on this project |
| `.claude/Planning/ProjectPlan.md` | Iteration roadmap (driven workflow) |
| `.claude/Planning/CurrentIteration.md` | Active iteration progress with tasks/subtasks (driven workflow) |
| `.claude/Planning/IterationHistory.md` | Summaries of completed iterations (driven workflow) |
| `.claude/Planning/History/` | Per-task detail files for completed work (driven workflow) |
| `.claude/Planning/Backlog.md` | Issues and ideas captured for later |

### Work Hierarchy (Driven Workflow)

**Iterations** (milestones — may be as few as 1-2 for small projects) → **Tasks** (user-story level) → **Subtasks** (atomic units an agent tackles one at a time)

### Skills

**Auto-loaded** (available automatically when relevant):

| Skill | Trigger |
|-------|---------|
| `unity-coding-conventions` | Writing C# code |
| `zenject-conventions` | Writing Zenject code |
| `unity-folder-conventions` | Creating files or folders |
| `unity-context-system` | Reading or navigating project code |
| `unity-mcp-tools` | Interacting with Unity Editor via MCP |
| `unity-ugui-development` | Writing UGUI code |

**Pipeline skills** (developer-invoked):

- `/unity-claude:unity-development` - Main development driver (`progress` / freeform)
- `/unity-claude:backlog` - Add items to the project backlog
- `/unity-claude:unity-development sync` - Update context and state after manual changes

**Reference skills** (consult when needed):

- `unity-testing` - Test writing guidance (edit vs play mode, Zenject fixtures)
- `unity-ugui-list` - UI list generation pattern
