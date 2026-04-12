# Rhythm Ratio — Architecture

Scoped through **Iteration 3: Gameplay Feel & Phase System**.

---

## Subsystems

### Input
- **Responsibility:** Detect swipe gestures using Unity Input System Enhanced Touch API (no Input Actions). Raise events with swipe position (midpoint), direction (angle/vector), and speed (circular buffer tracking). Ignore taps without movement. Minimize latency.
- **Key folder:** `_RhythmRatio/Input/`
- **Dependencies:** None

### Gameplay
- **Responsibility:** Everything that drives the core loop — beat clock (BPM, time signature, measure/beat tracking), line data lifecycle (preview phase → line approach phase → sliceable → resolved), accuracy evaluation (timing, position, direction + combined grade), object data pooling, session configuration (shared properties object read by all line-related code), metronome audio, and session orchestration (what to spawn and when).
- **Key folder:** `_RhythmRatio/Gameplay/`
- **Dependencies:** Input

### Gameplay (Iteration 2–3 additions)
- **Responsibility:** Scoring (score + combo multiplier), HP (passive drain + restore/penalty), game over detection, phase-based progression (PhaseService replacing DifficultyService), phase intro display, background color transitions, slice visual effects, measure visualizer. All within Gameplay subsystem.
- **Key folder:** `_RhythmRatio/Gameplay/`
- **Dependencies:** Input, Gameplay (Iter 1)

### UI (Iteration 4)
- **Responsibility:** UGUI overlay screens (Start, Game Over, Gameplay HUD), game state management, session reset orchestration, high score persistence.
- **Key folder:** `_RhythmRatio/UI/`
- **Dependencies:** Gameplay

---

## Feature Folders

| Feature Folder | Subsystem | Contents |
|---|---|---|
| `_RhythmRatio/Input/` | Input | Swipe detection service |
| `_RhythmRatio/Gameplay/` | Gameplay | Beat clock, line data management, preview/line lifecycle, accuracy evaluation, grading, metronome, session config, session orchestrator, scoring, HP, phase system, phase intro display, background color, slice effects, measure visualizer |

Internal structure of each follows `unity-folder-conventions` (Scripts/Services/, Scripts/Behaviour/, Scripts/Data/, etc.).

---

## Scenes

### Single Scene: Gameplay
- **Purpose:** The only scene for Iteration 1. Runs the core gameplay loop directly on launch.
- **Entry point:** This scene is the default loaded scene.
- **No scene loading strategy needed** — single scene, no additive loading yet. Menu scene will be added in Iteration 3.

### Camera Setup
- **Projection:** Orthographic (2D gameplay — lines drawn at screen center via Shapes)
- **Size:** Configured to match a mobile portrait aspect ratio (e.g., 9:16). Exact size TBD during implementation based on line length and screen coverage.
- **Position:** (0, 0, -10) looking at origin
- **Clear flags:** Solid color (white or dark background — TBD)

---

## Key Prefabs

None for Iteration 1. Lines are rendered via Shapes component mode — LineDrawer creates pooled child GameObjects with Shapes.Line components at runtime. Line data is managed as a data pool (list of structs/classes), not a GameObject pool.

A debug UI overlay for displaying accuracy feedback (text) will be created as a simple scene object or prefab during implementation.

---

## Scene Hierarchy

```
GameplayScene
├── SceneContext                # with GameplayInstaller
├── Main Camera                # orthographic, portrait mobile
├── GameplayRoot
│   ├── LineDrawer              # MonoBehaviour: draws all active lines + previews via Shapes component mode
│   └── MetronomeSource        # AudioSource for beat tick SFX
├── GameSessionService          # MonoBehaviour: game state + session orchestration
├── DebugOverlay               # temporary: accuracy grade text display
└── [UI]                       # placeholder — Iteration 4
```

---

## Zenject Context Setup

**Small project approach:** Project Context + single loaded scene.

### Project Context
- Default Zenject ProjectContext in `_RhythmRatio/Shared/Zenject/Resources/`
- No project-level bindings needed for Iteration 1 (no cross-scene services yet)

### Scene Context: GameplayScene
- **GameplayInstaller** (MonoInstaller on SceneContext GameObject)
- Binds all Iteration 1 services:
  - Swipe detection service (Input subsystem)
  - Beat clock / rhythm service (Gameplay subsystem)
  - Gameplay session service — orchestrates what to spawn when (Gameplay subsystem)
  - Accuracy evaluator service (Gameplay subsystem)
- All bound `AsSingle()`
- Game logic lives in MonoBehaviours, not IInitializable/ITickable
- Field injection with `[Inject]`, initialization in `Start()`

---

## Technical Decisions

### Beat Clock Timing
Use `AudioSettings.dspTime` (audio DSP clock) for rhythm-accurate timing instead of `Time.time`.

### Line Rendering
Shapes component mode. LineDrawer (MonoBehaviour) creates a pool of child GameObjects with two `Shapes.Line` components each (left/right segments around ratio gap). Updated in LateUpdate. No immediate mode — incompatible with iOS/Android.

### Session Configuration
ScriptableObject holding all session parameters: BPM, time signature, approach rates, timing windows, accuracy thresholds. Inspector-editable.

### Beat Pattern
Serialized data defining which beats in a measure have slices (supports rests). Editable in inspector.

### Ratio Data Model (Iteration 2, updated Iter 3)
`RatioTier` enum + static `RatioDefinitions` helper class mapping each tier to its float ratio value. Tier colors moved from hardcoded RatioDefinitions to configurable SessionConfigSO fields. Bidirectional ratio evaluation: slicing at either end counts as the same ratio.

### Line Color Phases (Iteration 3 update)
All phases (preview, line, sliceable) use ratio tier color configured in SessionConfigSO. Grade-based resolved colors removed. On successful slice, SliceEffect spawns two physics-driven fragments in swipe direction with speed-proportional force.

### Game State & Session Reset (Iteration 4)
GameSessionService (MonoBehaviour via Zenject `FromComponentInHierarchy().AsSingle()`) owns game state (WaitingToStart, Playing, GameOver) and orchestrates in-place reset of all services without scene reload. Each resettable service implements a ResetState() method. Subscribes to HPService.OnGameOver in Start() and transitions state. Controls BeatClock startup/stop and PhaseService initial phase.

### UI Approach (Iteration 4)
UGUI overlay Canvas with panel toggling (Start Screen, Game Over Screen, Gameplay HUD). Single scene, no scene loading. Tap input on screens triggers GameSessionService state transitions. High score persisted via PlayerPrefs.

### ScoreService (Iteration 2)
Pure C# class (no MonoBehaviour). Bound via Zenject `AsSingle()`. HPService is a MonoBehaviour for passive drain in `Update()`.

### Phase System (Iteration 3)
Replaces DifficultyService's random tier selection. PhaseService controls sequential phases, each with a single ratio tier. Phase duration (measures) decreases as score increases. On phase start, line spawning pauses for 1-2 measures while an intro display (Shapes-rendered text + indicator line) shows the ratio. Background color transitions per phase.

### BPM-Independent Timing (Iteration 3)
Preview and line timing fields (PreviewLead, PreviewApproachRate, PreviewFadeout, LineApproachRate, LineFadeout) are defined in seconds, not beats. Timing windows remain BPM-scaled per spec.

### Line Rendering Changes (Iteration 3)
Lines render as single continuous segments (no ratio gap). Position randomized with configurable X/Y offset range. Length varies per line based on score progression.

### Measure Visualizer (Iteration 3)
Shapes-based (not UGUI) scrolling timeline at screen bottom (50% screen width centered). Beat ticks and upcoming line indicators scroll right-to-left (left edge = now). Indicators predicted from BeatPatternSO with brightened tier colors. Configurable zoom via `VisualizerBeats` in SessionConfigSO. Smoothly hides during phase intro. Rendered by MeasureVisualizer MonoBehaviour.

### HP Drain Scaling (Iteration 2, updated Ad-hoc)
Drain rate defined as `DrainPerBeat` (HP lost per beat interval), not per second. Actual drain/sec = `EffectiveDrainPerBeat / CurrentSecondsPerBeat`. Drain increases per phase (`DrainIncreasePerPhase`), capped at `MaxDrainPerBeat`. PhaseService computes EffectiveDrainPerBeat.

### Dynamic BPM (Ad-hoc)
BPM is no longer constant. BeatClock tracks a current BPM with smooth lerp support (re-anchors beat counting on each change). BPM increases by `BpmPerPhase` each phase (smooth lerp during intro). Perfect streak adds `BpmPerPerfect` per consecutive perfect (capped at `MaxPerfectStreakBonuses`). On streak break, BPM fast-resets to phase base BPM (`StreakBpmResetSpeed`). All timing-dependent code uses `BeatClock.CurrentSecondsPerBeat` instead of `SessionConfigSO.SecondsPerBeat`.

### Music System (Ad-hoc)
MusicService plays a looping AudioClip at game start. Pitch is synced to BPM: `pitch = CurrentBpm / BaseBpm`. Music and beats stay synced since both derive from the same dynamic BPM.

### Phase Progression (Ad-hoc update)
After initial sequential cycle (Common→Mythic), phases are selected by weighted random. Easier tiers lose weight over time (`EasyWeightDecayPerPhase`). Configurable base weights per tier (`PostCycleBaseWeights`).

### Perfect Streak System (Ad-hoc)
SliceEvaluator tracks consecutive perfect slices. Each perfect adds BPM bonus. On 5th+ consecutive perfect, HP is fully restored. Streak break (miss or non-perfect) fast-resets BPM. Configurable streak audio clips per streak count.
