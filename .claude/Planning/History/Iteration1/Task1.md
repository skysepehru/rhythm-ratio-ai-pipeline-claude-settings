# Task 1: Scene & DI Foundation

Set up Gameplay scene with orthographic camera, Zenject ProjectContext + SceneContext, skeleton GameplayInstaller.

## Subtasks

### Subtask 1.1 — Create Gameplay scene ✅
- Created GameplayScene at `_RhythmRatio/Gameplay/Scenes/GameplayScene.unity`
- Orthographic camera at (0, 0, -10), size 5, dark solid background
- Removed default Directional Light
- Set as build scene index 0
- Context files created for scene, folders, and Main Camera GameObject

### Subtask 1.2 — Set up Zenject contexts & installer ✅
- Added Zenject reference to `RhythmRatio.asmdef`
- Created ProjectContext prefab at `_RhythmRatio/Shared/Zenject/Resources/ProjectContext.prefab`
- Created skeleton `GameplayInstaller.cs` at `_RhythmRatio/Gameplay/Scripts/Installers/`
- Added SceneContext GameObject to GameplayScene with SceneContext + GameplayInstaller components
- GameplayInstaller wired to SceneContext's `_monoInstallers`
- Play mode enters cleanly with no Zenject errors
- Context files created for new folders, assets, and SceneContext GameObject

### Subtask 1.3 — Create scene hierarchy GameObjects ✅
- Created GameplayRoot (empty parent) at scene root
- Created MetronomeSource as child of GameplayRoot with AudioSource (PlayOnAwake=false)
- Created DebugOverlay canvas (Screen Space - Overlay) at scene root
- Created DebugText child of DebugOverlay with UI Text (white, size 24, upper half anchor)
- ContextInfo added to all 4 new GameObjects
- Hierarchy matches Architecture.md (LineRenderer deferred to Task 5)
