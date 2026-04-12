---
name: unity-context-system
description: Context system for navigating project code. ALWAYS Auto-loaded when reading or navigating project code in Unity projects.
---

# Context System

Every file, asset, folder, and GameObject has a short summary. Read summaries first — load full content only when implementing.

---

## Lookup Procedure

**Preferred: Spawn the `context-navigator` agent** with a description of what you need to find. It follows the procedure below automatically and returns a ranked list of relevant file paths with reasons.

**Manual procedure** (when not using the agent):
1. **Start in `.claude/State/Architecture.md`** — find the subsystem relevant to your task. It lists key folders and files.
2. **Read the folder's `_context.yaml`** — one-line summaries of each file. Narrow down what matters.
3. **Read individual context** — `@context` block at top of .cs files, `.context` companion file for assets, or ContextInfo component on GameObjects.
4. **STOP.** Plan from summaries. Do NOT read full file content yet — that happens during implementation only.

### ContextInfo on GameObjects (MCP)

GameObjects store context in a `ContextInfo` MonoBehaviour. To read it, traverse the scene hierarchy from root objects with a bounded depth using ScriptExecutor. Do not retrieve all ContextInfo in a scene — start shallow (depth 2) and drill into relevant branches.

---

## Storage Formats

| Type | Storage | Location |
|------|---------|----------|
| Scripts (.cs) | `@context` comment block | Top of file |
| GameObjects | `ContextInfo` MonoBehaviour | Component on the GameObject |
| Assets (audio, textures, etc.) | `.context` companion YAML | Next to asset (e.g., `SliceSound.wav.context`) |
| Folders | `_context.yaml` | In the folder |

### Script @context

```csharp
/* @context
summary: Detects swipe gestures from touch/mouse input. Fires OnSwipeDetected.
tags: input, swipe, gameplay
*/
```

### Installer @context

Installers list their bindings — natural dependency maps.

```csharp
/* @context
summary: Binds all gameplay systems
tags: gameplay, scoring, slicing
bindings:
  - IScoreManager → ScoreManager
  - IComboTracker → ComboTracker
  - SliceEvaluator (self)
*/
```

### Folder _context.yaml

```yaml
summary: All input handling code. Touch detection, swipe recognition.
contains:
  - SwipeDetector: Core swipe detection
  - TouchHandler: Low-level touch processing
```

### ContextInfo Component (GameObjects)

Attached to GameObjects in scenes and prefabs. Created by scaffold at `Assets/_[ProjectName]/Shared/Scripts/ContextInfo.cs`.

```csharp
public class ContextInfo : MonoBehaviour
{
    [TextArea(3, 10)]
    public string Summary;
}
```

**Not every GameObject needs ContextInfo.** Add it to GameObjects that represent meaningful units — group roots, objects with specific gameplay roles, or anything an agent would need to understand. Skip purely structural children (mesh renderers, colliders, layout elements). If a parent groups related children, the parent gets ContextInfo describing the group; children only get it if they are individually notable.

### Asset .context

```yaml
summary: Satisfying slice feedback sound. Short, punchy.
tags: audio, sfx, gameplay
```

---

## Cross-References

Don't include references to other files in context unless very closely related (e.g., a View referencing its Presenter). Architecture.md subsystem mappings and installer binding lists handle broader relationships.
