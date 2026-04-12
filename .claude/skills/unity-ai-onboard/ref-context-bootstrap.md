# Context System Bootstrap

Initialize context for all existing project assets after scaffolding. Only runs when CONTEXT_SYSTEM != none.

Uses **inline** backend — context stored directly in project files.

---

## Process

1. Read `Architecture.md` for the subsystem map — this tells you what folders and scripts exist.
2. Create context for every existing asset produced by scaffolding.
3. Call `assets-refresh` after creating any new files.

## What Needs Context

| Item | Context Type | How |
|------|-------------|-----|
| `.cs` scripts | `@context` block at top of file | `Edit` tool — add `/* @context ... */` block |
| Assets (prefabs, ScriptableObjects, audio, textures) | `.context` companion YAML | `Write` tool — create `AssetName.ext.context` next to asset |
| Folders with code/assets | `_context.yaml` | `Write` tool — create in the folder |
| GameObjects in scenes/prefabs | `ContextInfo` component | `gameobject-component-set` MCP tool — set `Summary` field |

## Context Format Reference

For exact formats, see the auto-loaded `unity-context-system` skill. Quick reference:

**Script @context:**
```csharp
/* @context
summary: One-line description of what this script does.
tags: relevant, tags
*/
```

**Installer @context (includes bindings):**
```csharp
/* @context
summary: Binds all gameplay systems
tags: gameplay, installer
bindings:
  - IScoreManager -> ScoreManager
  - SliceEvaluator (self)
*/
```

**Folder _context.yaml:**
```yaml
summary: What this folder contains and its role.
contains:
  - ScriptName: One-line description
  - OtherScript: One-line description
```

**Asset .context:**
```yaml
summary: What this asset is and its role.
tags: relevant, tags
```

**GameObject ContextInfo:**
Set the `Summary` field to a one-line description of the GameObject's role. Not every GameObject needs ContextInfo — only meaningful units (group roots, objects with specific gameplay roles). Skip purely structural children (mesh renderers, colliders, layout elements). If a parent groups related children, the parent gets ContextInfo; children only if individually notable.

## At Scaffold Time

After scaffolding, the project typically has:
- `_Core/Shared/Scripts/ContextInfo.cs` — already has @context
- `_Core/Editor/Scripts/AutomationHelpers/ScriptExecutor.cs` — already has @context
- `_Core/` folder — needs _context.yaml
- `_Core/Shared/Scripts/` folder — needs _context.yaml
- `_Core/Editor/Scripts/` folder — needs _context.yaml
- `_Core/Editor/Scripts/AutomationHelpers/` folder — needs _context.yaml
- `_[ProjectName]/` folder — needs _context.yaml (mostly empty at this point)
- `_[ProjectName]/Shared/Scripts/` — needs _context.yaml
- `_[ProjectName]/Tests/` — needs _context.yaml

Create _context.yaml for each folder. The script templates already include @context blocks.
