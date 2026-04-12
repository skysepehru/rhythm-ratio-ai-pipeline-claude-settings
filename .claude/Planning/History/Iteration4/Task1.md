# Iteration 4, Task 1: Session Reset & Game State Management

## Goal
Add a GameSessionService that manages game states (WaitingToStart, Playing, GameOver) and orchestrates in-place reset of all services without scene reload.

## Subtasks

### 1.1 — Add ResetState() methods to all gameplay services ✅
- Added ResetState() to: BeatClock, HPService, ScoreService, PhaseService, LineDrawer, MeasureVisualizer, PhaseBackgroundColor, SliceEffect
- LineDataPool.ResetAll() deactivates all pooled lines
- Extracted BeatClock.StartClock() from Start() for reuse
- Removed HPService auto-restart coroutine
- Renamed from Reset() to ResetState() to avoid Unity's MonoBehaviour.Reset() lifecycle callback

### 1.2 — Create GameSessionService ✅
- Created GameSessionService as MonoBehaviour (FromComponentInHierarchy AsSingle)
- GameStates enum: WaitingToStart, Playing, GameOver
- Fires OnStateChanged event on transitions
- StartGame(): resets all 9 services, starts BeatClock + PhaseService initial phase, transitions to Playing
- Subscribes to HPService.OnGameOver → stops BeatClock, transitions to GameOver
- RestartGame() delegates to StartGame()
- Removed BeatClock auto-start from Start()
- Removed PhaseService.StartInitialPhase() from LineSpawner.Start()
- Removed BeatClock.Stop() from SliceEvaluator.HandleGameOver()
- Added MeasureVisualizer and PhaseBackgroundColor bindings to GameplayInstaller

## Files Changed
- `Assets/_RhythmRatio/Gameplay/Scripts/Services/GameSessionService.cs` (new)
- `Assets/_RhythmRatio/Gameplay/Scripts/Services/BeatClock.cs`
- `Assets/_RhythmRatio/Gameplay/Scripts/Services/HPService.cs`
- `Assets/_RhythmRatio/Gameplay/Scripts/Services/ScoreService.cs`
- `Assets/_RhythmRatio/Gameplay/Scripts/Services/PhaseService.cs`
- `Assets/_RhythmRatio/Gameplay/Scripts/Services/LineDrawer.cs`
- `Assets/_RhythmRatio/Gameplay/Scripts/Services/LineSpawner.cs`
- `Assets/_RhythmRatio/Gameplay/Scripts/Services/SliceEvaluator.cs`
- `Assets/_RhythmRatio/Gameplay/Scripts/Behaviour/MeasureVisualizer.cs`
- `Assets/_RhythmRatio/Gameplay/Scripts/Behaviour/PhaseBackgroundColor.cs`
- `Assets/_RhythmRatio/Gameplay/Scripts/Behaviour/SliceEffect.cs`
- `Assets/_RhythmRatio/Gameplay/Scripts/Installers/GameplayInstaller.cs`
- `Assets/_RhythmRatio/Gameplay/Scenes/GameplayScene.unity`

## Architectural Notes
- GameSessionService is MonoBehaviour (not pure C# as originally planned) — simpler lifecycle management, subscribes to events in Start()
- Architecture.md updated to reflect MonoBehaviour approach and scene hierarchy
