# Task 3: Session Config & Beat Pattern Data

ScriptableObject for session config (BPM, time signature, approach rates, timing windows, thresholds, grading weights). Beat pattern data model.

## Subtasks

### Subtask 3.1 — Create SessionConfigSO ScriptableObject ✅
- Created `_RhythmRatio/Gameplay/Scripts/Data/SessionConfigSO.cs` with all session parameters
- Fields: BPM, BeatsPerMeasure, preview/line timing, timing windows, ratio/angle thresholds, grading weights
- SecondsPerBeat computed property
- Created default asset instance at `_RhythmRatio/Gameplay/Data/SessionConfig.asset`
- Bound in GameplayInstaller via `[SerializeField]` + `FromInstance().AsSingle()`
- Wired to SceneContext's GameplayInstaller in scene
- No automated tests (pure data container)

### Subtask 3.2 — Create BeatPatternSO ScriptableObject ✅
- Created `BeatPatternSO.cs` with bool[] Beats field and HasSliceOnBeat helper
- Default: 4 beats, all active
- Created default asset instance at `_RhythmRatio/Gameplay/Data/BeatPattern.asset`
- Bound in GameplayInstaller via `[SerializeField]` + `FromInstance().AsSingle()`
- Wired to SceneContext's GameplayInstaller in scene
- No automated tests (pure data container)
