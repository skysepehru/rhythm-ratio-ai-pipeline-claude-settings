# Post-Script Verification

Run after the onboarding script completes. Uses MCP to verify everything is working.

The `unity-mcp-tools` skill (auto-loaded) guides tool usage — follow it for tool selection, lean defaults, and ScriptExecutor patterns.

---

## Step 1: Verify MCP Connection

Call `editor-application-get-state` to confirm Unity is running and MCP is connected.

If this fails, tell the developer to check that:
- Unity is open with the project loaded
- MCP server is running (Tools > MCP Unity > Server Window)

## Step 2: Refresh Assets

Call `assets-refresh` to ensure Unity picks up all files created by the onboarding script (directories, asmdefs, scripts).

## Step 3: Check for Compile Errors

Call `console-get-logs` and check for compilation errors. If there are errors, diagnose and fix them before continuing.

## Step 4: Verify Packages

Read Constants.md for project configuration, then verify:
- If ZENJECT = true, confirm Zenject is installed — check `package-list` for `com.svermeulen.extenject` (OpenUPM install), fall back to `Assets/Plugins/` (Asset Store installs)
- Confirm Unity-MCP is installed — check `package-list` for `com.ivanmurzak.unity.mcp`
