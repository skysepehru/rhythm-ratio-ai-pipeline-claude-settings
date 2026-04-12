# Task 3: Ratio Pool, Difficulty Progression & Line Colors

## Summary
All 5 ratios (Common through Mythic) with tier-colored previews. DifficultyService unlocks tiers progressively based on successful slice count. Grade-based resolved colors (Perfect=white, Good=green, Bad=orange, Miss=red).

## Subtasks

### Subtask 3.1: RatioTier Data, DifficultyService & Tests ✅
- Created RatioTiers enum (Common, Rare, Epic, Legendary, Mythic)
- Created static RatioDefinitions class: GetRatio(tier) → float (a:b → a/(a+b)), GetColor(tier) → Color (Gray, Blue, Purple, Gold, Red)
- Added difficulty thresholds to SessionConfigSO (RareUnlockSlices=10, EpicUnlockSlices=25, LegendaryUnlockSlices=50, MythicUnlockSlices=80)
- Created DifficultyService (pure C#): RecordSlice(), GetUnlockedTiers(), PickRandomTier(), Reset()
- 21 edit mode tests (10 RatioDefinitions + 11 DifficultyService) — all passing

### Subtask 3.2: LineData ResolvedColor & Grade Colors in LineDrawer ✅
- Added ResolvedColor to LineData (default red in Reset())
- LineDrawer: preview uses line.LineColor (tier color), line phase = white, resolved uses line.ResolvedColor
- SliceEvaluator sets ResolvedColor via GradeToColor (Perfect=white, Good=green, Bad=orange, Miss=red)
- LineSpawner miss handler sets ResolvedColor to red
- Removed hardcoded _previewColor from LineDrawer

### Subtask 3.3: LineSpawner & DifficultyService Integration ✅
- LineSpawner uses DifficultyService.PickRandomTier() for ratio + LineColor from RatioDefinitions
- DifficultyService.RecordSlice() called from SliceEvaluator on non-miss
- DifficultyService bound AsSingle in GameplayInstaller
- Preview changed from dashed to solid, alpha increased from 0.5 to 0.7
- Manual test passed: tier colors on preview, white lines, grade colors on resolved, tiers unlock progressively

## Files Created
- `Assets/_RhythmRatio/Gameplay/Scripts/Data/RatioTiers.cs`
- `Assets/_RhythmRatio/Gameplay/Scripts/Data/RatioDefinitions.cs`
- `Assets/_RhythmRatio/Gameplay/Scripts/Services/DifficultyService.cs`
- `Assets/_RhythmRatio/Tests/Editor/RatioDefinitionsTests.cs`
- `Assets/_RhythmRatio/Tests/Editor/DifficultyServiceTests.cs`

## Files Modified
- `Assets/_RhythmRatio/Gameplay/Scripts/Data/SessionConfigSO.cs` (difficulty thresholds)
- `Assets/_RhythmRatio/Gameplay/Scripts/Data/LineData.cs` (ResolvedColor)
- `Assets/_RhythmRatio/Gameplay/Scripts/Services/LineDrawer.cs` (tier/grade colors, solid preview)
- `Assets/_RhythmRatio/Gameplay/Scripts/Services/SliceEvaluator.cs` (ResolvedColor, DifficultyService)
- `Assets/_RhythmRatio/Gameplay/Scripts/Services/LineSpawner.cs` (DifficultyService, tier ratio/color)
- `Assets/_RhythmRatio/Gameplay/Scripts/Installers/GameplayInstaller.cs` (DifficultyService binding)

## Tests
- 21 new edit mode tests (RatioDefinitionsTests + DifficultyServiceTests)
