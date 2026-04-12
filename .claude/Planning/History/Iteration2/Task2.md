# Task 2: HP System & Game Over

## Summary
HP drain system with game over. HPService (MonoBehaviour) tracks HP with BPM-scaled passive drain, restores on hit, penalizes on miss. Game over at HP=0 stops BeatClock and LineSpawner. Debug text shows HP and "GAME OVER".

## Subtasks

### Subtask 2.1: HP Config & HPService with Tests ✅
- Added HP parameters to SessionConfigSO: MaxHp (100), DrainPerBeat (2.5), HpPerfect (15), HpGood (8), HpBad (2), HpMissPenalty (10)
- Created HPService (MonoBehaviour) with CurrentHp, ProcessGrade, ApplyDrain, IsGameOver, OnGameOver event, ResetHp
- Drain rate scales with BPM: drainPerSecond = DrainPerBeat / SecondsPerBeat
- 13 edit mode tests: restore per grade, miss penalty, clamping, passive drain, game over flag/event, game over stops operations, reset

### Subtask 2.2: Game Over Integration & Debug Display ✅
- SliceEvaluator injects HPService + BeatClock, calls ProcessGrade after scoring
- HandleGameOver stops BeatClock, shows "GAME OVER" text
- LineSpawner guards HandleBeat with IsGameOver check
- HPService component added to GameplayRoot in scene
- Bound HPService in GameplayInstaller (FromComponentInHierarchy)
- Debug text shows HP alongside score/combo; "GAME OVER" with final score on death
- DrainPerBeat replaced DrainRate for BPM-consistent HP economy

## Files Created
- `Gameplay/Scripts/Services/HPService.cs`
- `Tests/Editor/HPServiceTests.cs`

## Files Modified
- `Gameplay/Scripts/Data/SessionConfigSO.cs` (HP params, DrainPerBeat)
- `Gameplay/Scripts/Installers/GameplayInstaller.cs` (HPService binding)
- `Gameplay/Scripts/Services/SliceEvaluator.cs` (HP integration, game over handling)
- `Gameplay/Scripts/Services/BeatClock.cs` (Stop method)
- `Gameplay/Scripts/Services/LineSpawner.cs` (game over guard)
- `Gameplay/Scenes/GameplayScene.unity` (HPService on GameplayRoot)

## Tests Added
13 edit mode tests in HPServiceTests
