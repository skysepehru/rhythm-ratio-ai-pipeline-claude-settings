# Task 2: Phase System

Replace random ratio selection with sequential phases of same-ratio lines, with intro displays and background color changes.

## Subtasks

### 2.1 ✅ Create PhaseService
Pure C# service replacing DifficultyService. Sequential phases (Common→Rare→Epic→Legendary→Mythic, cycling). Phase duration (measures) decreases with score via SessionConfigSO config (InitialPhaseDuration, MinPhaseDuration, PhaseFullProgressionScore). LineSpawner uses PhaseService.CurrentTier instead of DifficultyService.PickRandomTier. Fires OnPhaseChanged event. DifficultyService and its tests deleted. PhaseServiceTests created with 12 tests.

### 2.2 ✅ Phase intro display
PhaseService gains IsIntroPaused flag and StartInitialPhase() for the first phase. LineSpawner skips spawning during intro pause. Created PhaseIntroDisplay MonoBehaviour — renders ratio text (TMP) + indicator line with slice point marker (Shapes Line + Disc) in tier color. Fast fade in (0.15s) / fade out (0.2s) with 0.5s margin before lines resume. IntroPauseMeasures config in SessionConfigSO. Added TMP to RhythmRatio.asmdef. Added 4 intro pause tests. Added PhaseIntroDisplay to GameplayRoot.

### 2.3 ✅ Background color transitions
Created PhaseBackgroundColor MonoBehaviour — lerps camera background per phase using configurable colors from SessionConfigSO (one Color field per tier, inspector-editable). Smooth 0.5s smoothstep transition. Added to GameplayRoot.

## Files Created
- `Gameplay/Scripts/Services/PhaseService.cs`
- `Gameplay/Scripts/Behaviour/PhaseIntroDisplay.cs`
- `Gameplay/Scripts/Behaviour/PhaseBackgroundColor.cs`
- `Tests/Editor/PhaseServiceTests.cs`

## Files Modified
- `Gameplay/Scripts/Services/LineSpawner.cs` — PhaseService integration, intro pause check
- `Gameplay/Scripts/Services/SliceEvaluator.cs` — removed DifficultyService dependency
- `Gameplay/Scripts/Data/SessionConfigSO.cs` — phase config fields + background colors
- `Gameplay/Scripts/Installers/GameplayInstaller.cs` — PhaseService binding
- `RhythmRatio.asmdef` — added TMP reference

## Files Deleted
- `Gameplay/Scripts/Services/DifficultyService.cs`
- `Tests/Editor/DifficultyServiceTests.cs`
