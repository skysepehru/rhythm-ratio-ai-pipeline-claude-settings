# Task 5: Line Spawning, Lifecycle & Rendering

## Summary
Line data model, object pool, beat-driven spawner with lifecycle state machine, and Shapes immediate mode renderer. Preview (dashed gray) fades in/out before the solid line (white) approaches and becomes sliceable.

## Subtasks

### 5.1 Line data model and data pool ✅
- Created LineStates enum (Inactive, PreviewFadeIn, PreviewHold, PreviewFadeOut, LineApproach, Sliceable, Resolved)
- Created LineData class (State, Ratio, Angle, BeatDspTime, LineColor, StateStartDspTime, Reset())
- Created LineDataPool (pre-allocates 16, Activate/Deactivate, ActiveLines, ActiveCount)
- Bound LineDataPool in GameplayInstaller AsSingle()
- Edit mode tests: 6 tests (activate, deactivate, full pool, reset, active lines)

### 5.2 Line spawner and lifecycle ✅
- Created LineSpawner MonoBehaviour with BeatClock/BeatPatternSO/SessionConfigSO/LineDataPool injection
- Spawns lines with look-ahead (PreviewLead beats) on BeatClock.OnBeat events
- Update() computes lifecycle state for all active lines via static ComputeLineState()
- Added StartDspTime property to BeatClock
- Bound LineSpawner in GameplayInstaller (FromComponentInHierarchy)
- Added LineSpawner GO under GameplayRoot in scene
- Edit mode tests: 11 tests for ComputeLineState

### 5.3 Shapes immediate mode renderer ✅
- Created LineDrawer extending ImmediateModeShapeDrawer
- Preview: dashed gray lines (PreviewFadeIn → PreviewFadeOut, no hold phase)
- Solid: white lines (LineApproach → Sliceable → Resolved fadeout)
- Added LineFadeout field to SessionConfigSO (beats, configurable in inspector)
- Added ShapesRuntime + Unity.RenderPipelines.Universal.Runtime to RhythmRatio.asmdef
- Bound LineDrawer in GameplayInstaller (FromComponentInHierarchy)
- Added LineDrawer GO under GameplayRoot in scene
- Simplified ComputeLineState: removed PreviewHold, added gap between preview and approach
- Fixed bug: Update() no longer reverts spawned-but-not-yet-approaching lines to Inactive
- Updated tests: 12 tests covering all states + gap + no-gap scenarios

## Files Created/Modified
- `Gameplay/Scripts/Data/LineStates.cs` — lifecycle enum
- `Gameplay/Scripts/Data/LineData.cs` — line data class
- `Gameplay/Scripts/Data/SessionConfigSO.cs` — added LineFadeout field
- `Gameplay/Scripts/Services/LineDataPool.cs` — object pool
- `Gameplay/Scripts/Services/LineSpawner.cs` — spawner + state machine
- `Gameplay/Scripts/Services/LineDrawer.cs` — Shapes renderer
- `Gameplay/Scripts/Services/BeatClock.cs` — added StartDspTime property
- `Gameplay/Scripts/Installers/GameplayInstaller.cs` — added LineSpawner + LineDrawer bindings
- `RhythmRatio.asmdef` — added ShapesRuntime + URP references
- `Tests/Editor/LineDataPoolTests.cs` — 6 pool tests
- `Tests/Editor/LineSpawnerTests.cs` — 12 state machine tests

## Test Count
30 edit mode tests total (all passing)
