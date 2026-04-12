# Mode: Agent-Driven Development (with Context System)

You are the development agent for an AI-driven Unity game project. You handle structured subtask work and freeform development.

**First action: Read `ref-development-core.md` in this skill folder.**

---

## Routing

- **`$ARGUMENTS` is `progress`** → Progress Mode (below)
- **Anything else** → Freeform Mode (below)
- **Empty** → Ask the developer what they want to do

---

## Freeform Mode

Do whatever the developer asks, with full project awareness. Works at any time: mid-iteration, between iterations, or alongside progress work.

### Step 1: Context Retrieval

1. Load `$PROJECT_SPECIFICATION`.
2. Spawn the `context-navigator` agent with the developer's request as input. It navigates Architecture.md → folder context → file context → GameObject context and returns a ranked list of relevant file paths with one-line reasons.
3. **Plan from the agent's output** — do not load full file content yet.

### Step 2: Implement

Load full content of files needed. Do the work.

### Step 3: Validate

Follow validation per `ref-development-core.md`.

### Step 4: Update State

**Read `ref-state-update.md`** — follow "Update Context" and "Review Architecture and Specification" sections for all created/modified files.

### Step 5: Commit

Commit with `[Ad-hoc]` prefix. Follow `ref-development-core.md` commit rules.

---

## Progress Mode

Implement the next subtask, or break down the iteration into tasks/subtasks if not yet done.

### Phase 1: Reconciliation

Before any work, check what happened since the last pipeline session.

#### 1a: Git State Check

1. Check for uncommitted/unstaged changes and any commits made since the last `[Iter ...]` commit.
2. For each non-pipeline commit, review its message and changed files. Judge whether it affects game code, assets, or architecture.
3. For out-of-band changes that need documenting:
   - Small changes (1 file, trivial fix): note in `$CURRENT_ITERATION` under "Unplanned Work" section.
   - Notable changes (multiple files, behavior change): add to `$HISTORY_DIR/Iteration[N]/Unplanned.md`.
   - New functionality / architectural impact: promote to a Task in `$CURRENT_ITERATION` (named "Task N: Hotfix - [Description]").
4. Walk through relevant changes with the developer.
5. **Read `ref-state-update.md`** — follow "Update Context" and "Review Architecture and Specification" sections for all affected files.
6. Make ONE commit with all context/history/state updates for documented unplanned work.

#### 1b: Task Relevance Check

For each `[Ad-hoc]` commit since the last `[Iter ...]` commit:
- Does this affect any current task's scope, approach, or completion?
- Task partially done by freeform work → reduce scope or mark subtasks done
- Task approach invalidated → revision per `revisions.md`

Agent proposes changes, developer confirms.

If nothing relevant across 1a-1b, proceed to Phase 2.

### Phase 2: Determine Current Work

Read `$CURRENT_ITERATION`.

**If empty (header only)** — break down the iteration:
1. Read: `$PROJECT_SPECIFICATION`, `$PROJECT_PLAN`, `$CURRENT_ITERATION`, `$ITERATION_HISTORY`, `$ARCHITECTURE`.
2. Spawn the `context-navigator` agent to find files relevant to the iteration's goals. Summaries only, no full content.
3. Break the iteration into Tasks (user-story level).
4. For each task, identify any **new technical approach decisions** — Unity features, third-party tools, or implementation patterns not yet used in the project. Flag these to the developer.
5. Break the first task into Subtasks (atomic units).
6. Discuss with the developer and iterate until approved. Developer confirms technical approach decisions.
7. Record approved technical decisions in `$ARCHITECTURE` under the relevant subsystem.
8. Save everything to `$CURRENT_ITERATION`, marking the first subtask as current.
9. Commit. Read `git-strategy.md` for format.
10. Continue to Phase 3.

**If not empty** — find the current subtask. Continue to Phase 3.

### Phase 3-6: Execute Subtasks (Subagent Loop)

For each subtask in the current task, spawn the `subtask-worker` agent with:
- The current subtask description from `$CURRENT_ITERATION`
- The parent task context (goals, prior subtask outcomes)
- Context mode: `inline`
- Any relevant notes (technical decisions from Phase 2, issues from prior subtasks)

The subagent autonomously handles: planning, implementation, validation (compile + tests), context updates, and commit. It does NOT stop for developer feedback or manual testing.

**After the subagent completes:**
1. Review its output for issues (assumption mismatches, validation failures, blockers).
2. If the subagent flagged a critical issue, consult the developer — may trigger a revision per `revisions.md`.
3. If there are more subtasks in the current task, spawn the subagent for the next one.
4. If all subtasks in the current task are done, continue to Phase 7.

### Phase 7: Task Completion

All subtasks in the current task are done.

1. Prompt the developer for **manual gameplay/visual testing** of the completed task. Wait for confirmation.
2. Task-level validation if needed (broader integration tests). Gets its own commit if performed.
3. Move full subtask details from `$CURRENT_ITERATION` to `$HISTORY_DIR/Iteration[N]/Task[M].md`.
4. Update `$CURRENT_ITERATION` to contain only a summary of the completed task.
5. Mark the task as complete with notes.
6. **Read `ref-state-update.md`** — follow "Review Architecture and Specification" section. Update with developer's confirmation if needed.
7. Break the next task into subtasks. Identify new technical approach decisions and discuss.
8. Record approved technical decisions in `$ARCHITECTURE`.
9. Commit. Read `git-strategy.md` for format.
10. **STOP. This invocation is complete.** Tell the developer to run `/unity-claude:unity-development progress` again.

**If all tasks in the iteration are done:**

1. Iteration-level validation if needed.
2. Review the iteration goal from `$PROJECT_PLAN` with the developer. Summarize what was built and ask for confirmation the goal has been met.
3. Update `$CURRENT_ITERATION` and commit.
4. **Read `ref-iteration-progress.md`** and follow the iteration advancement process.

