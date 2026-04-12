# Task 4: Beat Clock & Metronome

Beat clock service driven by AudioSettings.dspTime. Tracks current measure/beat. Fires beat events. Metronome tick audio on each beat.

## Subtasks

### Subtask 4.1 — Create BeatClock MonoBehaviour ✅
- Created `_RhythmRatio/Gameplay/Scripts/Services/BeatClock.cs`
- Tracks beat/measure via AudioSettings.dspTime, fires OnBeat and OnMeasure events
- Static ComputeBeatFromDspTime helper for testable pure math
- Bound in GameplayInstaller via FromComponentInHierarchy().AsSingle()
- Added BeatClock GO under GameplayRoot with ContextInfo
- Edit mode tests: 7 tests (compute beat at various times, measure wrapping)
- All tests pass

### Subtask 4.2 — Wire metronome tick audio ✅
- Generated procedural MetronomeTick.wav (880Hz sine, 50ms, linear decay) at `Gameplay/Audio/`
- Added _metronomeSource and _tickClip serialized fields to BeatClock
- Plays tick via PlayOneShot on each beat
- Wired MetronomeSource AudioSource and MetronomeTick clip in scene
- Manual verification: ticks audible at 120 BPM
