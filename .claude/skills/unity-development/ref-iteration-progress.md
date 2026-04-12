# Iteration Progress

Evaluate the current iteration and advance to the next. Triggered when all tasks in an iteration are complete. **Driven workflow only.**

**CRITICAL: File access restriction.** Only read the files listed in `ref-development-core.md`. Do NOT explore the codebase or read source code. All decisions are based on planning files and developer input.

**Planning philosophy:** Iterations are a rolling horizon, not a fixed plan. Only a few iterations are planned ahead at any time. Every iteration boundary is a replanning checkpoint — remaining iterations are expected to change based on what was learned. New iterations get added as needed.

---

## Process

### 1. Read Context

Read: `$PROJECT_SPECIFICATION`, `$PROJECT_PLAN`, `$ITERATION_HISTORY`, `$CURRENT_ITERATION`, `$ARCHITECTURE`.

### 2. Evaluate Readiness

Based ONLY on these files (not codebase exploration):
- Is the iteration goal achieved?
- Did we learn what we needed to learn? (if the iteration had a Learn goal)
- Are there unresolved blockers or issues?

### 3. Present Findings

Show the developer:
- Summary of current iteration status
- Recommendation: "Ready to progress" OR "Not ready" (with reasons)

If the developer disagrees, discuss. Be open to being convinced — the developer may have context not in the files.

### 4. Collect Developer Feedback

Before replanning, ask the developer:
- How did this iteration go? Anything that felt wrong, slow, or missing?
- Any features, improvements, or ideas they want to add to upcoming work?
- Any code quality issues or technical debt they want addressed?

This is the moment to surface everything the developer has been thinking during development. Don't rush past it.

### 5. Review Learnings

Build a picture of how the project has evolved to inform replanning:

**Iteration History:** Review `$ITERATION_HISTORY` for patterns — recurring issues, scope creep, things that took longer than expected, learnings that shift priorities.

**Spec & Architecture drift:** Diff `$PROJECT_SPECIFICATION` and `$ARCHITECTURE` against the commit where the current iteration started (the `[Pipeline] Advance to Iteration [N]` commit, or the onboarding commit for iteration 1). Summarize what changed — new systems added, scope expanded, architectural decisions made during development. These changes may make planned iterations obsolete, too small, or missing new work.

Present a summary of all learnings to the developer before drafting changes.

### 6. Replan Remaining Iterations

With the developer's agreement, replan:

1. **Evaluate existing iterations** in `$PROJECT_PLAN` — for each remaining iteration, assess whether it's still relevant, correctly scoped, and correctly ordered given what was learned. Propose changes: keep as-is, modify, reorder, split, merge, or drop.
2. **Draft new iterations** if needed — based on developer feedback, spec/architecture drift, and learnings.
3. **Review with the developer** in batches of 2-3 iterations:
   - Include FULL text of each iteration (Goal + optional Learn)
   - Options per iteration: "Good", "Too big", "Too small", "Other (explain)"
   - Revise and re-ask until all marked "Good"

### 7. Update Files

**Update `$PROJECT_PLAN`:**
- Update "Current Iteration" field to the next iteration
- Add/modify/remove iterations as discussed

**Append to `$ITERATION_HISTORY`** (add new record at END, never replace whole file):
```markdown
## Iteration [N]: [Name]
**Goal:** [Original goal from $PROJECT_PLAN]
**Outcome:** [What actually happened]
**Learned:** [Key insights from $CURRENT_ITERATION]
**Impact:** [How this affects future iterations]
**Tasks:**
- Task 1: [Name]
- Task 2: [Name]
- ...
**Details:** History/Iteration[N]/
```

**Flush `$CURRENT_ITERATION`** (replace entire content):
```markdown
# Current Iteration

## Iteration [N+1]: [Name]
Started: [date]

## Progress Log

[Entries will be added here as development progresses]

## Summary

Not started.
```

### 8. Commit

Commit with message: `[Pipeline] Advance to Iteration [N+1]`
