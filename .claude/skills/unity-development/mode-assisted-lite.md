# Mode: Agent-Assisted Development (no Context System)

You are assisting the developer with AI-powered development on a Unity game project. The developer leads — you implement what they ask, with full project awareness. This mode does NOT use the context system — use direct code exploration instead.

**First action: Read `ref-development-core.md` in this skill folder.**

---

## Workflow

Every invocation follows this flow. `$ARGUMENTS` is treated as the developer's request.

If `$ARGUMENTS` is empty, ask the developer what they want to work on.

### Step 1: Gather Context

1. Load `$ARCHITECTURE` + `$PROJECT_SPECIFICATION`.
2. Identify relevant subsystems from `$ARCHITECTURE`.
3. Use direct code exploration (`Glob`, `Grep`, `Read`) to understand the relevant code.

### Step 2: Implement

Load full content of files needed. Do the work.

### Step 3: Validate

Follow validation per `ref-development-core.md`.

### Step 4: Update State

**Read `ref-state-update.md`** — follow "Review Architecture and Specification" section for all created/modified files. This is mandatory every commit — every commit should leave these files accurate.

### Step 5: Commit

Commit with `[Ad-hoc]` prefix. Follow `ref-development-core.md` commit rules.
