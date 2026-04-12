# Task 6: Accuracy Evaluation & Integration

## Summary
Ratio marker visualization, timing/position/direction accuracy evaluation, combined weighted grade. Connects swipe input to active line evaluation. Debug text overlay showing results. Hit/miss audio feedback.

## Subtasks

### 6.1 Ratio marker and angle constraints ✅
- Lines drawn as two segments with a gap (0.225 world units) at ratio position
- Gap appears during both preview and solid phases
- Line angle constrained to 60°–120° (±30° from vertical for portrait mode)
- Modified: LineDrawer.cs, LineSpawner.cs

### 6.2 Accuracy evaluator ✅
- AccuracyEvaluator static class with EvaluateTiming, EvaluateRatio, EvaluateAngle, CombineGrades
- Grade enum: Perfect, Good, Bad, Miss
- Uses Mathf.DeltaAngle for angle wrapping
- Weighted grade combination with configurable weights
- 24 edit mode tests covering all methods and edge cases

### 6.3 Swipe-to-line connector REVISED
- Original attempt tried to wire everything without a test harness
- Revised into 6.3b (debug test) and 6.3c (full connector)

### 6.3b Swipe debug test ✅
- SwipeDebugger (temporary) logged swipe ratio vs target on sliceable lines
- SwipeDetector revised: fires OnSwipeDetected every frame while dragging (prev→current, 5px min threshold)
- Validated input pipeline end-to-end

### 6.3c Swipe-to-line connector ✅
- SliceEvaluator MonoBehaviour (renamed from SwipeDebugger)
- Proximity check: only evaluates if swipe midpoint is within 0.5 world units of line
- Perpendicular angle comparison: swipe direction compared to line normal (±90°)
- Any-Miss-means-Miss rule: if any of timing/ratio/angle is Miss, combined grade is Miss
- IsSliced flag on LineData prevents double-slicing
- Hit audio: 1760Hz blip (50ms), Miss audio: 220Hz blip (120ms) — generated at runtime
- LineSpawner fires OnLineMissed for expired unsliced lines
- Fast fadeout: sliced (0.08s), missed (0.1s)
- Grade displayed on DebugText overlay

## Files Created/Modified
- `Gameplay/Scripts/Services/AccuracyEvaluator.cs` — static evaluator class
- `Gameplay/Scripts/Services/SliceEvaluator.cs` — swipe-to-line connector (was SwipeDebugger)
- `Gameplay/Scripts/Services/LineSpawner.cs` — added OnLineMissed event, angle constraint
- `Gameplay/Scripts/Services/LineDrawer.cs` — ratio gap rendering, fast fadeout for sliced/missed
- `Gameplay/Scripts/Data/LineData.cs` — added IsSliced flag
- `Gameplay/Scripts/Installers/GameplayInstaller.cs` — added SliceEvaluator binding
- `Input/Scripts/SwipeDetector.cs` — revised to fire continuously while dragging
- `Tests/Editor/AccuracyEvaluatorTests.cs` — 24 edit mode tests

## Test Count
54 edit mode tests total (all passing)
