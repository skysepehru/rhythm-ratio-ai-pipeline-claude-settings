# Validation

Validation means ensuring that what was built actually works. It happens after every subtask (before commit), after every task, and after every iteration.

Mode files direct you to the right section based on TESTS in Constants.md:
- **TESTS = true** → follow "Full Validation" below
- **TESTS = false** → skip to "No-Test Validation" at the bottom

---

# Full Validation

## Two Categories

| Category | How | When |
|----------|-----|------|
| Code-testable | Unit tests + integration tests | Every subtask, run before commit |
| Gameplay/visual | Developer manually tests, reports back | Agent prompts after every subtask |

For gameplay/visual validation, the commit happens **after** the developer confirms — not before. The subtask stays uncommitted until the developer has tested and given feedback.

---

## Tests Are Part of the Subtask

Tests are written WITH the implementation, not as separate work. If a subtask adds ScoreManager, the unit/integration tests for ScoreManager are written in the same subtask.

**"No automated tests needed" is a valid answer.** Not every subtask warrants tests. Test the public interface of a class — how it will actually be used — not its internals. Don't add methods to a class just to have something testable.

---

## Subtask Plan Declares What's Tested How

During subtask planning, the agent states:
- Which unit/integration tests will be written (if any)
- What needs manual developer verification (gameplay/visual)

Both sides know what to expect before implementation starts.

---

## Failure Flow

1. Tests fail — agent analyzes Unity logs and test output
2. Agent retries the fix (has access to Unity logs and MCP tools)
3. If still stuck (agent uses judgment) — discusses with developer
4. May trigger a revision (see `revisions.md`)

---

## Breaking Earlier Tests

If the current subtask breaks a test written in an earlier subtask:
- If the fix is simple and obvious, the agent fixes it in place as part of the current subtask.
- If the breakage is unexpected or could have broader consequences, the agent consults the developer — this may trigger a revision to go back as far as needed.

---

## Future: Automated Visual/Gameplay Testing

Not for now. Future vision: AI-controlled play mode with screenshots, rendering optimized for AI image recognition, runtime MCP tools for game control. The goal is to automate the "developer manually tests" category.

---

# No-Test Validation

When TESTS = false. No tests are written, no tests are run. Developer tests manually in engine.

**All checks are mandatory. Do not skip any without an explicit reason stated to the developer.**

1. **Compile check**: Check Unity console for compile errors via MCP. Fix all errors before proceeding.
2. **Gameplay/visual**: If the change affects anything visible or interactive, ask the developer to verify in the editor before committing.

The commit happens **after** the developer confirms — not before.
