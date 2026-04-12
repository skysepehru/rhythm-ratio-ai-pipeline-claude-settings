# Planning & Architecture Initialization

Creates the project's knowledge base: Specification, Architecture, and (for driven mode) the planning infrastructure.

---

## File References

| Variable | Path | Purpose |
|----------|------|---------|
| `$PROJECT_DESCRIPTION` | `.claude/Planning/ProjectDescription.md` | Developer's freeform game design doc (input) |
| `$TECHNICAL_VISION` | `.claude/Planning/TechnicalVision.md` | Developer's architectural and technical approach (input) |
| `$PROJECT_SPECIFICATION` | `.claude/State/ProjectSpecification.md` | Formalized game spec (output) |
| `$PROJECT_PLAN` | `.claude/Planning/ProjectPlan.md` | Iteration roadmap (output, driven only) |
| `$CURRENT_ITERATION` | `.claude/Planning/CurrentIteration.md` | Active iteration progress (output, driven only) |
| `$ITERATION_HISTORY` | `.claude/Planning/IterationHistory.md` | Completed iteration summaries (output, driven only) |
| `$ARCHITECTURE` | `.claude/State/Architecture.md` | System architecture (output) |
| `$FOLDER_CONVENTIONS` | `.claude/skills/unity-folder-conventions/SKILL.md` | Folder structure conventions (reference) |

## CRITICAL: File Access Restriction

**ONLY read the files defined above. Do NOT explore the codebase or read any other files.** All decisions must be based solely on these files and developer input. Never read source code, scripts, or other project files.

---

## Part 1: Generate Specification

1. **Check prerequisites:**
   - Read `$PROJECT_DESCRIPTION` — if missing, tell developer to create it first
   - Read `$TECHNICAL_VISION` — if missing, tell developer to create it first

2. **Identify gaps in the description:**
   - Analyze `$PROJECT_DESCRIPTION` for ambiguities, missing edge cases, undefined behaviors, or implicit assumptions
   - Ask the developer clarifying questions
   - Continue until you have enough clarity to formalize the spec

3. **Generate `$PROJECT_SPECIFICATION`:**
   - Formalize `$PROJECT_DESCRIPTION` into a precise, unambiguous specification
   - Incorporate all clarifications from step 2
   - Make everything explicit — game states, edge cases, exact behaviors — so the development agent has unambiguous requirements
   - Write to `$PROJECT_SPECIFICATION`
   - Review with the developer and iterate until approved

---

## Part 2: Create Planning Files (Driven Mode Only)

**Skip this part entirely if WORKFLOW = assisted.** Assisted mode has no iterations, tasks, or subtasks.

### Philosophy

Right-size the plan to the project:
- **Small, well-specified** (clear mechanics, known patterns, limited scope): 1-2 iterations
- **Medium** (some uncertainty, multiple systems to integrate): 2-4 iterations
- **Large or exploratory** (significant unknowns, novel mechanics, broad scope): 4-6 iterations with learning milestones

Each iteration has a **Goal** (required) and an optional **Learn** (what questions it answers). Iterations do NOT define specific files, scripts, or implementation details.

### Steps

4. **Draft iterations** based on `$PROJECT_SPECIFICATION` and `$TECHNICAL_VISION`. The developer's technical vision informs sizing and sequencing — their chosen tools, approaches, and system structure affect what groups naturally together.

5. **Review iterations in batches of 2-3 with the developer:**
   - Include the FULL text of each iteration (Goal + optional Learn)
   - For each iteration, offer options: "Good", "Too big", "Too small", "Other (explain)"
   - Wait for feedback before drafting the next batch
   - If any iteration was marked "Too big", "Too small", or "Other", revise and re-ask that batch
   - Only proceed to the next batch when the current batch is all "Good"

6. **After all iterations approved, create files:**

   **`$PROJECT_PLAN`:**
   ```markdown
   # [Game Name] - Project Plan

   ## Game Summary
   Brief description. See `$PROJECT_SPECIFICATION` for full specification.

   ## Current Iteration
   Iteration 1: [Name]

   ## Iterations

   ### Iteration 1: [Name]
   **Goal:** [What will exist after this iteration]
   **Learn:** [What questions this answers — omit if pure execution]

   ### Iteration 2: [Name]
   ...
   ```

   **`$CURRENT_ITERATION`:**
   ```markdown
   # Current Iteration

   ## Iteration 1: [Name]
   Started: [date]

   ## Progress Log

   [Entries will be added here as development progresses]

   ## Summary

   Not started.
   ```

   **`$ITERATION_HISTORY`:**
   ```markdown
   # Iteration History

   [Records will be added here as iterations complete]
   ```

   **Create `$HISTORY_DIR`:** `.claude/Planning/History/` directory.

---

## Part 3: Generate Architecture

1. **Read all inputs:**
   - `$PROJECT_SPECIFICATION`, `$TECHNICAL_VISION`, `$FOLDER_CONVENTIONS`, Constants.md
   - If driven mode: `$PROJECT_PLAN`, `$CURRENT_ITERATION`

2. **Formalize the developer's technical vision.** `$TECHNICAL_VISION` contains the developer's decisions about how the project should be structured. Your job is to restate this vision precisely within the project's domain, mapped to folder conventions and Zenject patterns. Do not invent your own architecture — translate the developer's intent into the project's conventions.

3. **Map subsystems to feature folders** following `$FOLDER_CONVENTIONS`. List which features exist and what each contains — do not redefine the structural pattern from the conventions.

4. **Apply Zenject architectural principles** (if ZENJECT = true in Constants.md):
   - MonoBehaviours over Zenject abstractions — all game logic in MonoBehaviours, not IInitializable/ITickable
   - Field injection — prefer `[Inject]` fields, initialization in `Start()`
   - Custom factories over Zenject factories — inject `IInstantiator`, not `DiContainer`
   - Prefabs over scene objects — minimize scene-bound references
   - Composition over inheritance — flat hierarchies, compose behavior
   - AsSingle() over singletons — Zenject manages lifecycle
   - Visible startup — application root initiates significant startup actions

5. **Scope the architecture:**
   - **Driven mode**: Scope to the current iteration. Future iterations inform design direction but don't get concrete definitions.
   - **Assisted mode**: Scope to the whole project. The developer will work on whatever they want, so the full picture is needed.

6. **Write `$ARCHITECTURE`** containing:
   - **Subsystems**: Logical groupings with responsibility, key folders, dependencies. Do NOT list specific files/scripts.
   - **Feature Folders**: Which folders are needed, mapped to subsystems.
   - **Scenes**: Which scenes, loading strategy, entry point, camera setup.
   - **Key Prefabs**: Prefabs and their roles.
   - **Scene Hierarchy**: Expected runtime GameObject hierarchy. Mark placeholder groups for future systems.
   - **Zenject Context Setup**: Context hierarchy (if ZENJECT = true). Small projects: Project Context + single scene. Larger: scene parenting. Self-contained entities: GameObject Contexts.

7. **Discuss with developer** and iterate until approved.

---

## Part 4: Finalize

9. **Archive consumed inputs:** Move `$PROJECT_DESCRIPTION` and `$TECHNICAL_VISION` to `.claude/Archive/`. These are consumed inputs — moving them signals they shouldn't be referenced again.
