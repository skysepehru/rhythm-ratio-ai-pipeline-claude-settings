# Mode: Agent-Assisted Development (with Context System)

You are assisting the developer with AI-powered development on a Unity game project. The developer leads — you implement what they ask, with full project awareness.

**First action: Read `ref-development-core.md` in this skill folder.**

---

## Workflow

Every invocation follows this flow. `$ARGUMENTS` is treated as the developer's request.

If `$ARGUMENTS` is empty, ask the developer what they want to work on.

### Step 1: Context Retrieval

1. Load `$PROJECT_SPECIFICATION`.
2. Spawn the `context-navigator` agent with the developer's request as input. It navigates Architecture.md → folder context → file context → GameObject context and returns a ranked list of relevant file paths with one-line reasons.
3. **Plan from the agent's output** — do not load full file content yet.

### Step 2: Implement

Load full content of files needed. Do the work.

### Step 3: Validate

Follow validation per `ref-development-core.md`.

### Step 4: Update State

**Read `ref-state-update.md`** — follow "Update Context" and "Review Architecture and Specification" sections for all created/modified files. This is mandatory every commit — every commit should leave these files accurate.

### Step 5: Commit

Commit with `[Ad-hoc]` prefix. Follow `ref-development-core.md` commit rules.
