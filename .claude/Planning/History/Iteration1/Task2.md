# Task 2: Swipe Input Service

Swipe detection using Enhanced Touch API. Raises events with position + direction.

## Subtasks

### Subtask 2.1 — Create SwipeDetector MonoBehaviour with Zenject binding ✅
- Created `_RhythmRatio/Input/Scripts/` folder with SwipeData struct and SwipeDetector MonoBehaviour
- SwipeDetector uses Enhanced Touch API (onFingerDown/onFingerUp), fires OnSwipeDetected with SwipeData
- Static CalculateSwipeData method for testable pure math (midpoint, direction, angle)
- Ignores taps below configurable _minSwipeDistance threshold (default 50px)
- Added Unity.InputSystem reference to RhythmRatio.asmdef
- Bound in GameplayInstaller via FromComponentInHierarchy().AsSingle()
- Added SwipeDetector GO to scene root with ContextInfo
- Edit mode tests: 5 tests for CalculateSwipeData (horizontal, vertical, diagonal, normalization)
- Play mode tests: 2 integration tests using InputTestFixture (swipe fires event, tap ignored)
- All tests pass
