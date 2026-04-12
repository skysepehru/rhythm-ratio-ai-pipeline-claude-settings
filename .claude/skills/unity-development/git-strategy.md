# Git Strategy

## Branching (v1 - Simple)

All work happens linearly on `main`. Commits are checkpoints.

```
main ──●──●──●──●──●──●──●──●──●──
       │     │     │     │     └─ Iteration 2 start
       │     │     │     └─ Iteration 1 end
       │     │     └─ Task 2 complete
       └─────┴─ subtask commits
```

No feature branches for v1. Can revert to any subtask commit if needed. Iteration boundaries are marked by commits (CurrentIteration.md header changes).

---

## Commit Points

| Event | Commit | Contents |
|-------|--------|----------|
| Subtask validated complete | Yes | Code + context updates |
| Handling developer changes | Yes | Context/history updates only (md files) |
| Task validated complete | Yes | md files (task history move, Architecture.md if updated) |
| Subtask/task revision revert | Yes | Revert of failed work + CurrentIteration.md update |
| Iteration end | Yes | md files marking completion |
| Iteration start | Yes | md files (CurrentIteration.md header change) |
| Freeform work complete | Yes | Code + context updates + state file updates if any |

Preference: Separate commits when only md files change. Keeps code commits clean.

---

## Commit Message Format

### For planned work

```
[Iter X, Task Y, Subtask Z] Description

- Bullet points for changes
- Context files updated: yes/no
```

### For unplanned work handling

```
[Unplanned] Description

- What was addressed
- Size: small/medium/large
- Context updates: ...
```

### For md-only commits

```
[Iter X, Task Y] Task complete - history and context updates

- Moved subtask details to History/
- Updated Architecture.md (if applicable)
```

### For revisions

```
[Iter X, Task Y, Subtask Z] REVERT — Description of why

- Reverts commits abc123..def456
- Reason: [short explanation]
- Replaced by: Subtask Z2
```

```
[Iter X, Task Y] REVERT — Description of why

- Reverts commits abc123..def456
- Reason: [short explanation]
- Replaced by: Task Yb
```

### For freeform (ad-hoc) work

```
[Ad-hoc] Description

- Bullet points for changes
- Context files updated: yes/no
```

### For pipeline operations

```
[Pipeline] Description
```

Used for: onboarding, context initialization, iteration advancement, and other pipeline-level operations.

### For iteration boundaries

```
[Iter X] Iteration complete

- Summary of iteration outcomes
- Tasks completed: ...
```

```
[Iter X] Iteration start

- Iteration goal: ...
```
