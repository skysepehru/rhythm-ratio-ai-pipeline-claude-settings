# Revisions

When development goes wrong — subtask approach fails, task is scoped incorrectly, or assumptions prove false — the workflow needs a mechanism to revise and recover.

---

## Triggers

**AI self-check** — the agent checks assumptions at natural checkpoints:
- After planning a subtask, before implementing: "does what I see in the code match what I expected?"
- During implementation, if hitting unexpected state: stop and flag rather than hack around it
- After implementation, before committing: "did this achieve the goal or did I work around the actual problem?"

**Developer interrupt** — the developer sees something going wrong. The agent classifies the scope and proposes a revision path.

**Principle: flag early, don't power through.** If assumptions don't match reality, stop and raise it before committing.

---

## Revision Levels

### Subtask Revision

Current subtask approach isn't working. Discard uncommitted changes, mark the subtask as revised, create a replacement.

In CurrentIteration.md:
```markdown
### Subtask 2: Implement SwipeDetector REVISED
**Attempted:** Direct raycast approach
**Why revised:** Touch input doesn't work with UI layer — raycasts get blocked by Canvas
**Replaced by:** Subtask 2b

### Subtask 2b: Implement SwipeDetector (EventSystem approach)
...
```

When the task completes and moves to `History/Iteration[N]/Task[M].md`, the revision history goes with it.

### Task Revision

The task breakdown is wrong, or the entire task approach is flawed. Two paths:

- **Partial**: Re-scope remaining subtasks only. Completed subtasks stay.
- **Full revert**: Discard ALL completed subtasks in the task. Single revert commit covering all subtask commits.

The agent assesses the scope of the problem and proposes which path to the developer. Document what triggered the revision in CurrentIteration.md:

```markdown
## Task 3: Input System REVISED (full revert)
**Why revised:** EventSystem approach incompatible with world-space gameplay — need physics-based input
**Reverted commits:** abc123..def456
**Replaced by:** Task 3b: Input System (Physics-based)
```

When the iteration completes, IterationHistory.md gets a one-liner:
```markdown
- Task 3: Input System (revised — original approach incompatible with world-space gameplay, fully reverted)
```

### Iteration Revision

Multiple tasks are fundamentally wrong (e.g., architectural assumption was false). Completed tasks stay. Remaining tasks get re-planned. Architecture.md is updated first.

Noted directly in IterationHistory.md:
```markdown
## Iteration 2 — Revision Note
After Task 2, discovered that the assumed audio pipeline doesn't work on mobile.
Remaining tasks re-planned. Architecture.md updated.
```

---

## Git Strategy for Revisions

Failed work stays in git history. A single revert commit undoes the changes, with the commit message referencing revision details in CurrentIteration.md.

- **Subtask revert**: single commit reverting the failed subtask's changes
- **Task revert**: single commit reverting all subtask commits in that task

See `git-strategy.md` for commit message formats.
