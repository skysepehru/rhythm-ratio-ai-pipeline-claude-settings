# ScriptExecutor First-Time Setup

This file is loaded when a project has no Constants.md (or Constants.md lacks `SCRIPT_EXECUTOR_PATH`). It guides the one-time setup of ScriptExecutor — a Roslyn-based C# executor that lets the AI run arbitrary Unity Editor code via MCP.

---

## 1. Explain to the Developer

Tell the developer:

> This skill needs **ScriptExecutor** — a small utility script that compiles and runs arbitrary C# inside the Unity Editor via Roslyn. It's used instead of the raw `script-execute` MCP tool because it separates code writing from execution, making permission prompts readable.
>
> The mechanism: I write C# to a temp file (`.claude/Temp/mcp-execute.cs`), then call `ScriptExecutor.Run(filePath)` via MCP reflection. The script reads the file, deletes it, compiles it, and runs it. This is a one-time setup.

---

## 2. Determine Path and Namespace

Examine the project's `Assets/` folder structure to find a logical location:

- Look for an existing Editor scripts folder (e.g., `Assets/*/Editor/Scripts/` or `Assets/Editor/`)
- Look for existing namespace patterns in `.cs` files to match the project's conventions
- Look for assembly definitions that cover Editor code

**Default recommendation** (if no clear pattern exists):
- **Path**: `Assets/_Core/Editor/Scripts/AutomationHelpers/ScriptExecutor.cs`
- **Namespace**: `Core.Editor`

**If patterns exist**, adapt:
- If there's a `Assets/MyGame/Editor/` folder, recommend putting it there
- If existing scripts use `CompanyName.ProjectName.Editor` namespace, use `CompanyName.ProjectName.Editor`
- The script needs to be under an Editor folder (or covered by an Editor-only asmdef) since it uses `UnityEditor` APIs

Present the recommended path and namespace to the developer and ask for confirmation. The developer may adjust.

---

## 3. Create ScriptExecutor.cs

Once confirmed, create the script at the agreed path using `script-update-or-create` (which auto-refreshes the AssetDatabase).

Use this template, replacing `[Namespace]` with the confirmed namespace:

```csharp
using System;
using System.IO;
using System.Linq;
using System.Reflection;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using UnityEngine;

namespace [Namespace]
{
    public static class ScriptExecutor
    {
        public static string Run(string filePath)
        {
            if (string.IsNullOrEmpty(filePath) || !File.Exists(filePath))
                return $"Error: File not found at '{filePath}'";

            string code;
            try
            {
                code = File.ReadAllText(filePath);
                File.Delete(filePath);
            }
            catch (Exception ex)
            {
                return $"Error reading/deleting file: {ex.Message}";
            }

            try
            {
                var compilation = CSharpCompilation.Create(
                    assemblyName: "ScriptExecutor_Dynamic",
                    syntaxTrees: new[] { CSharpSyntaxTree.ParseText(code) },
                    references: AppDomain.CurrentDomain.GetAssemblies()
                        .Where(a => !a.IsDynamic && !string.IsNullOrEmpty(a.Location))
                        .Select(a => MetadataReference.CreateFromFile(a.Location))
                        .ToArray(),
                    options: new CSharpCompilationOptions(OutputKind.DynamicallyLinkedLibrary)
                );

                using (var ms = new MemoryStream())
                {
                    var result = compilation.Emit(ms);
                    if (!result.Success)
                    {
                        var errors = string.Join("\n", result.Diagnostics
                            .Where(d => d.Severity == DiagnosticSeverity.Error)
                            .Select(d => d.ToString()));
                        return $"Compilation failed:\n{errors}";
                    }

                    ms.Seek(0, SeekOrigin.Begin);
                    var assembly = Assembly.Load(ms.ToArray());
                    var type = assembly.GetType("Script");
                    if (type == null)
                        return "Error: Class 'Script' not found in compiled code";

                    var method = type.GetMethod("Main");
                    if (method == null)
                        return "Error: Method 'Main' not found in class 'Script'";

                    var returnValue = method.Invoke(null, null);
                    return returnValue?.ToString() ?? "(null)";
                }
            }
            catch (TargetInvocationException ex)
            {
                return $"Execution failed: {ex.InnerException?.Message ?? ex.Message}";
            }
            catch (Exception ex)
            {
                return $"Error: {ex.Message}";
            }
        }
    }
}
```

---

## 4. Create/Update Constants.md

Create `.claude/State/Constants.md` if it doesn't exist. Add or update these variables:

```markdown
# Constants

Project state flags and configuration values used by skills.

## MCP
SCRIPT_EXECUTOR_PATH = [confirmed path from project root]
SCRIPT_EXECUTOR_NAMESPACE = [confirmed namespace]
MCP_TOOL = https://github.com/IvanMurzak/Unity-MCP
```

If Constants.md already exists but lacks these variables, append them under a `## MCP` section.

---

## 5. Ensure Temp Folder

Create `.claude/Temp/` if it doesn't exist. This is where temp scripts are written before execution.

If the project uses git, ensure `.claude/Temp/` is in `.gitignore`. Check for an existing `.gitignore` entry like `.claude/Temp/` — if not present, append:
```
# Claude Code temp files
.claude/Temp/
```

---

## 6. Disable Redundant MCP Tools

Use `tool-set-enabled-state` to disable these tools (they are replaced by Claude Code capabilities or the ScriptExecutor flow):

| Tool | Reason |
|------|--------|
| `script-execute` | Replaced by ScriptExecutor flow (readable permission prompts) |
| `script-update-or-create` | Replaced by `Write` tool + `assets-refresh` |
| `script-read` | Replaced by `Read` tool |
| `assets-create-folder` | Replaced by `mkdir -p` + `assets-refresh` |
| `screenshot-scene-view` | Not needed |
| `screenshot-game-view` | Not needed |

Ensure `reflection-method-call` is **enabled** — it's critical for the ScriptExecutor flow.

**IMPORTANT:** After changing tool enabled/disabled states, Claude must be restarted for the changes to take effect. Tell the developer to restart Claude after this step completes.

---

## 7. Commit

If the project is a git repository, commit the changes:

```
ScriptExecutor setup for MCP automation
```

---

## Done

Setup is complete. Return to the main skill and continue with the original request.
