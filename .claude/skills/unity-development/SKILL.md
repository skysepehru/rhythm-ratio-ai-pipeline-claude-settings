---
name: unity-development
description: Main development driver for AI-driven Unity game development. Progress through subtasks, sync after manual changes, or do freeform development.
argument-hint: "progress|sync|<request>"
disable-model-invocation: true
---

# Unity Development

Development entry point. Routes to the correct mode file based on project configuration.

---

## Routing

### Step 1: Read Configuration

Read `.claude/State/Constants.md` for WORKFLOW and CONTEXT_SYSTEM values.

### Step 2: Handle Special Arguments

//Remove init mention
If `$ARGUMENTS` is `init`:
- This is no longer handled here. Tell the developer to use `/unity-claude:unity-ai-onboard` instead.
- **STOP.**

If `$ARGUMENTS` is `sync`:
- **Read `ref-state-update.md`** in this skill folder. Follow all three sections in order:
  1. **Detect Changes** — find what changed since last synced commit
  2. **Update Context** — update context for all changed files (if context system enabled)
  3. **Review Architecture and Specification** — propose updates if needed
- Commit with prefix `[Sync]`:
  ```
  [Sync] Update context for recent changes

  - Context updated: [list of files/folders]
  - Architecture.md: [updated/no changes]
  - ProjectSpecification.md: [updated/no changes]
  ```
- **STOP.**

### Step 3: Load Mode File

Based on Constants.md values, **read the matching mode file** in this skill folder and follow it:

| WORKFLOW | CONTEXT_SYSTEM | Mode File |
|----------|---------------|-----------|
| driven | inline | `mode-driven.md` |
| driven | none | `mode-driven-lite.md` |
| assisted | inline | `mode-assisted.md` |
| assisted | none | `mode-assisted-lite.md` |

The mode file contains the complete workflow. Follow it from the top.

---

## Reference Files

These files are loaded on demand by mode files — not upfront:

| File | Location | When to Load |
|------|----------|-------------|
| `ref-development-core.md` | This folder | First action in any mode — shared file refs, guidelines, principles |
| `ref-state-update.md` | This folder | When updating context, arch, or spec |
| `ref-iteration-progress.md` | This folder | When all tasks in an iteration are done (driven workflows) |
| `git-strategy.md` | This folder | At commit time |
| `revisions.md` | This folder | When something goes wrong or assumptions don't match |
| `validation.md` | `shared` folder | During planning and after implementation |

MCP tool usage is covered by the auto-loaded `unity-mcp-tools` skill.
