---
name: unity-ai-onboard
description: Set up AI-driven development for a Unity project. Single entry point — replaces scaffold, plan, architecture, and dev init.
disable-model-invocation: true
---

# AI Onboarding

Set up everything needed for AI-driven development on a Unity project. This is the single entry point — run it once at the start.

Most deterministic steps (file creation, git init, Unity project, packages, scaffold) are handled by `scripts/onboard.py`. Claude handles conversation, AI-judgment steps, and MCP interaction.

---

## Step 0: Pre-checks

1. Does `.claude/State/Constants.md` exist with a fully populated Project Profile section?
   - **Yes** → Project is already onboarded. Tell the developer to read `.claude/AIFlow.md` for how to use AI on this project. **STOP.**
2. Does `Assets/` folder exist in the project root?
   - **Yes** → Existing project. Jump to **Step 1b: Existing Project Onboarding**.
   - **No** → Greenfield project. Continue to **Step 1: Query Developer**.

---

## Step 1b: Existing Project Onboarding

Existing projects use **limited mode** — convention skills only, no spec/architecture/planning/context.

Ask the developer:
- Project name (PascalCase — e.g., `RhythmRatio`)
- Company or username (used for namespaces — e.g., `UnityTechnologies`)
- Does the project use Zenject? (true/false)

Run the onboarding script:

```bash
python3 scripts/onboard.py \
  --project-dir <PROJECT_DIR> \
  --name <NAME> \
  --company <COMPANY> \
  --scope unknown \
  --state existing \
  --ownership solo \
  --workflow limited \
  --zenject <true/false> \
  --skip-git
```

Where `scripts/` is relative to the plugin installation directory (find it via the plugin path).

Tell the developer:

> This pipeline uses **Unity-MCP** ([github.com/IvanMurzak/Unity-MCP](https://github.com/IvanMurzak/Unity-MCP)) for Unity Editor interaction. Please install it in your project if you haven't already. The `unity-mcp-tools` convention skill will handle ScriptExecutor setup on first use.

Commit: `[Pipeline] Onboard existing project (limited mode)`

**STOP.**

---

## Step 1: Query Developer

Gather project information. Ask all questions at once using AskUserQuestion:

**Identity:**
- Project name (PascalCase, used for folders, namespaces — e.g., `RhythmRatio`)
- Company or username (used for namespaces — e.g., `UnityTechnologies`)

**Project Profile** — explain each option to the developer:

- **Scope** — how big is the project in terms of technical implementation complexity?
  - `prototype`: 1-2 day game jams, quick feature tests
  - `small`: Polished hyper-casual mobile game, weeks of work
  - `medium`: Small polished video game, many systems, months of work
  - `large`: Small-medium indie game, many complex interconnected systems, 6-18 months
  - `very-large`: Proper indie game, 2+ years

- **Ownership** — what is your role on the team?
  - `solo`: Only developer, full ownership over technical decisions
  - `team-owner`: In a team, responsible for codebase, defines conventions including AI conventions
  - `team-ai-driven`: In a team, not the lead, but AI workflow is team-enabled
  - `team`: In a team, alone in how you use AI tools, no guarantee teammates follow your conventions

- **Workflow** — how will development be driven?
  - `driven`: Development mainly done by agents following iteration/task breakdown
  - `assisted`: Development mainly done by developer, with AI assistance

Show these recommendations based on scope:

| Scope | Recommended Workflow | TESTS | CONTEXT_SYSTEM |
|-------|---------------------|-------|----------------|
| Prototype | Driven | false | none |
| Small | Driven | true | inline |
| Medium | Assisted | true | inline |

**Features** (developer can override recommendations):
- TESTS: true / false (default per scope above)
- CONTEXT_SYSTEM: inline / none (default per scope above)
- ZENJECT: true / false

### Determine Mode

Evaluate the variables to determine the development mode. First match wins:

1. **SCOPE = large or very-large** → **Limited mode**.
2. **OWNERSHIP = team** (without owner role) → **Limited mode**.
3. **WORKFLOW = driven** → **Driven mode**.
4. **WORKFLOW = assisted** → **Assisted mode**.

### Check Directory Convention

Check the current directory name against the convention: repository directories should be **kebab-case ending with `-unity`** (e.g., `rhythm-ratio-unity` for project `RhythmRatio`).

- **Matches convention** → Continue.
- **Doesn't match** → Recommend the developer rename the directory to follow the convention. Offer two options:
  1. **Rename (recommended)**: Exit Claude, rename the directory, `cd` into it, and launch Claude again. **STOP.**
  2. **Continue anyway**: Proceed with the current directory name.

### Run the Onboarding Script

After gathering all info, run the script with all args:

```bash
python3 scripts/onboard.py \
  --project-dir <PROJECT_DIR> \
  --name <NAME> \
  --company <COMPANY> \
  --scope <SCOPE> \
  --state greenfield \
  --ownership <OWNERSHIP> \
  --workflow <WORKFLOW> \
  --tests <true/false> \
  --context-system <inline/none> \
  --zenject <true/false> \
  [--description "<one-line description>"] \
  [--editor-version "<version>"]
```

Where `scripts/` is relative to the plugin installation directory (find it via the plugin path).

Tell the developer:

> This pipeline uses **Unity-MCP** ([github.com/IvanMurzak/Unity-MCP](https://github.com/IvanMurzak/Unity-MCP)) for Unity Editor interaction. It will be installed automatically in a later step. All MCP tool guidance in this pipeline is specific to this implementation. If you use a different MCP package, you'll need to update the `unity-mcp-tools` convention skill to match your implementation's tool names and parameters.

The script handles: git init, .gitignore, GitHub repo, Unity project creation, Unity editor open, OpenUPM packages, directory scaffold, asmdefs, core scripts, AIFlow.md, CLAUDE.md, planning stubs (driven), and commits at logical boundaries.

---

## Step 2: Manual Setup

**Read `ref-scaffold-manual.md`** in this skill folder. Guide the developer through:
1. MCP setup (Unity-MCP configuration, tool enable/disable)
2. IDE setup (Rider package, external editor setting)

---

## Step 3: Post-Script Verification

**Read `ref-scaffold-automated.md`** for MCP verification steps:
1. Verify MCP connection via `editor-application-get-state`
2. Run `assets-refresh` to pick up all created files
3. Check `console-get-logs` for compile errors

**Read `ref-package-install.md`** for Unity registry packages (installed via MCP, not CLI):
- Install Input System (`com.unity.inputsystem`) via MCP `package-add`
- Install URP (`com.unity.render-pipelines.universal`) via MCP `package-add`

Automate project settings via ScriptExecutor (from `ref-scaffold-manual.md`):
- `PlayerSettings.productName`, `PlayerSettings.companyName`
- `PlayerSettings.SetApplicationIdentifier()` for Android/iOS
- Activate Input System: `PlayerSettings.activeInputHandler = Both`

---

## Step 4: Limited Mode Path

If the mode is **Limited**:

1. Inform the developer which convention skills are active and available (coding conventions, folder conventions, MCP tools, testing, UGUI — and Zenject conventions if ZENJECT = true).
2. The script already generated AIFlow.md and CLAUDE.md.
3. Commit and push with message: `[Pipeline] Onboard project (limited mode)`
4. **STOP.** Tell the developer they can use convention skills for assisted development. No further pipeline setup needed.

---

## Step 5: Planning & Architecture

**Read `ref-planning-init.md`** and execute:

1. **Generate Specification** — read ProjectDescription.md, ask clarifying questions, create ProjectSpecification.md. Review with developer.
2. **Create Planning Files** — (driven mode only) draft iterations, review with developer, create ProjectPlan.md + CurrentIteration.md + IterationHistory.md.
3. **Generate Architecture** — read spec + technical vision, create Architecture.md. Review with developer.
4. **Archive inputs** — move ProjectDescription.md and TechnicalVision.md to `.claude/Archive/`.

---

## Step 6: Context Bootstrap

If CONTEXT_SYSTEM != none:

**Read `ref-context-bootstrap.md`** and create context for all existing project assets:
- @context blocks on scripts
- _context.yaml for folders
- ContextInfo on GameObjects
- .context companions for assets

---

## Step 7: Final Commit

Commit and push all changes with message: `[Pipeline] Onboard project`

---

## Step 8: Next Steps

Tell the developer what to do next:

- **Driven mode**: Run `/unity-claude:unity-development progress` to start working on the first subtask.
- **Assisted mode**: Run `/unity-claude:unity-development <request>` with whatever you want to work on.
