# Manual Unity Setup

The developer completes these steps after the Unity project is created and packages are installed. The agent guides them through each step and verifies completion before proceeding to automated setup.

---

## 1. MCP Setup

The Unity-MCP package is already installed. The developer needs to set it up and connect it to Claude Code.

Tell the developer to follow the setup instructions at [github.com/IvanMurzak/Unity-MCP](https://github.com/IvanMurzak/Unity-MCP).

Once they say it's ready, verify the connection by calling `editor-application-get-state`.

### Configure MCP Tools

Ask the developer to **enable the `tool-set-enabled-state` tool** in the MCP settings — it may be disabled by default. Once enabled, use it to disable the following tools:

| Tool to Disable | Reason |
|-----------------|--------|
| `script-execute` | Replaced by ScriptExecutor flow (Write temp file → `reflection-method-call`) |
| `script-update-or-create` | Replaced by `Write` tool + `assets-refresh` |
| `script-read` | Replaced by `Read` tool |
| `assets-create-folder` | Replaced by `mkdir -p` + `assets-refresh` |
| `screenshot-scene-view` | Not needed |
| `screenshot-game-view` | Not needed |

Verify that `reflection-method-call` is **enabled** — this is critical for the ScriptExecutor flow.

See the `unity-mcp-tools` skill for the full expected tool state.

## 2. IDE Setup

1. Verify the JetBrains Rider Editor package is installed (check `package-list` for `com.unity.ide.rider`). If missing, install it.
2. Tell the developer to verify Rider is set as the External Script Editor in **Edit > Preferences > External Tools**.
3. Open the project in Rider to generate the `.idea` folder, or ask the developer to do so.

## 3. Automate Project Settings

Use ScriptExecutor to configure project settings from Constants.md values:

- `PlayerSettings.productName` → PROJECT_NAME
- `PlayerSettings.companyName` → COMPANY_NAME
- `PlayerSettings.SetApplicationIdentifier(BuildTargetGroup.Android, "com.[company].[project]")` (and iOS if applicable)
- Activate Input System: set `PlayerSettings.activeInputHandler` to `PlayerSettings.ActiveInputHandler.Both`
- Configure URP: ensure a `UniversalRenderPipelineAsset` exists in `Assets/Settings/` and is assigned in `GraphicsSettings.defaultRenderPipeline` and `QualitySettings`

Refresh the asset database after applying all settings.
