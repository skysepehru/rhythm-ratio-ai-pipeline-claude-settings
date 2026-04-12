# Task 1: Scoring & Combo System

## Summary
Added scoring with combo multiplier. ScoreService (pure C#) tracks score, combo count, and multiplier. SessionConfigSO extended with scoring parameters. SliceEvaluator integrates ScoreService. Debug text shows score + combo.

## Subtasks

### Subtask 1.1: Scoring Config & ScoreService with Tests ✅
- Added scoring parameters to SessionConfigSO: PerfectPoints (300), GoodPoints (100), BadPoints (50), ComboMultiplierStep (0.1), ComboMultiplierInterval (10)
- Created ScoreService (pure C# class) with ProcessGrade(Grade), Score, Combo, Multiplier properties
- Multiplier formula: 1 + floor(combo / interval) * step
- 12 edit mode tests: point awards per grade, combo increment/reset, multiplier calculation, cumulative scoring with multiplier, reset

### Subtask 1.2: SliceEvaluator Integration & Debug Display ✅
- Bound ScoreService in GameplayInstaller (AsSingle)
- SliceEvaluator injects ScoreService, calls ProcessGrade after evaluation
- HandleMiss calls ProcessGrade(Miss) to reset combo
- Debug text updated to show score and combo alongside grade
- Manual test confirmed: score increments, combo resets on miss

## Files Created
- `Gameplay/Scripts/Services/ScoreService.cs`
- `Tests/Editor/ScoreServiceTests.cs`

## Files Modified
- `Gameplay/Scripts/Data/SessionConfigSO.cs` (scoring params)
- `Gameplay/Scripts/Installers/GameplayInstaller.cs` (ScoreService binding)
- `Gameplay/Scripts/Services/SliceEvaluator.cs` (scoring integration + debug display)

## Tests Added
12 edit mode tests in ScoreServiceTests
