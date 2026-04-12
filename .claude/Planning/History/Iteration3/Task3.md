# Task 3: Measure Visualizer

## Summary
Shapes-based scrolling measure visualizer at screen bottom showing beat ticks and upcoming line indicators.

## Subtasks

### 3.1: Create MeasureVisualizer ✅
**Files created:**
- `Assets/_RhythmRatio/Gameplay/Scripts/Behaviour/MeasureVisualizer.cs` — Scrolling timeline MonoBehaviour
- `Assets/_RhythmRatio/Tests/Editor/MeasureVisualizerTests.cs` — 6 edit mode tests

**Files modified:**
- `Assets/_RhythmRatio/Gameplay/Scripts/Data/SessionConfigSO.cs` — Added `VisualizerBeats` field
- `Assets/_RhythmRatio/Gameplay/Scenes/GameplayScene.unity` — Added MeasureVisualizer GO under GameplayRoot

**Implementation details:**
- Horizontal bar at screen bottom, 50% screen width centered
- Beat ticks and line indicators scroll right-to-left (left = now, right = future)
- Indicators predicted from BeatPatternSO (not LineDataPool) so all future slice beats visible
- Tier colors brightened via Lerp toward white for visibility on dark backgrounds
- Indicators rendered as thick Line segments (not Disc — better opacity)
- Edge fading: fade in from right, fade out past left
- Smooth fade during phase intro pause via m_indicatorVisibility
- Configurable zoom via `VisualizerBeats` in SessionConfigSO (default 4 beats)
- Static `ComputeNormalizedTimeOffset` for testability
- Now marker (Disc) at left edge marks current time

**Tests:** 6 edit mode tests for ComputeNormalizedTimeOffset
