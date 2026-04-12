# State Update

Shared procedure for updating project state after changes. Used by sync, reconciliation, and freeform wrap-up.

---

## Detect Changes

Find what changed since the last context-updating commit:

1. Find the most recent commit with a `[Sync]`, `[Iter ...]`, `[Ad-hoc]`, or `[Pipeline]` prefix — these are commits where state was updated.
2. Diff against HEAD:
   ```
   git diff <last-synced-commit>..HEAD --name-status
   ```
3. This gives the list of added, modified, and deleted files.

---

## Update Context

Read `$CONSTANTS` to check CONTEXT_SYSTEM. If `none`, skip this section entirely.

If CONTEXT_SYSTEM = `inline`:

For each **added or modified** file, update its context. See the auto-loaded `unity-context-system` skill for formats and lookup procedure.

- **`.cs` scripts**: Read the file, write/update the `/* @context ... */` block at the top using `Edit`
- **Assets** (prefab, ScriptableObject, audio, texture, etc.): Write a `.context` companion YAML file next to the asset using `Write`
- **Folders** with added/removed/modified files: Write/update `_context.yaml` in the folder using `Write`
- **GameObjects**: Use MCP tools to read/update `ContextInfo.Summary` on the GameObject. Not every GameObject needs ContextInfo — only meaningful units (group roots, objects with specific roles). Skip purely structural children.

For **deleted** files:
- Remove the file's entry from its folder's `_context.yaml`
- Delete `.context` companion files if the asset was deleted

---

## Review Architecture and Specification

1. Read `$ARCHITECTURE`. Check whether the changes affect:
   - Subsystem responsibilities or dependencies
   - Feature folder structure
   - Scene setup or hierarchy
   - Zenject context configuration

2. Read `$PROJECT_SPECIFICATION`. Check whether the changes affect:
   - Game mechanics or behaviors
   - Edge cases or rules
   - System interactions

If updates are needed, propose them to the developer and get confirmation before editing.
