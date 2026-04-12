## 2026-03-23 AutoTester for runtime swipe simulation

**Commit:** 59801bf
**Trigger:** Developer requested before Task 3 to ease manual testing
**Changes:**
- `Debug/Scripts/AutoTester.cs`: MonoBehaviour that auto-swipes lines with configurable timing/ratio/angle accuracy sliders (0-1). Miss chance + overshoot at low accuracy.
- `Input/Scripts/SwipeDetector.cs`: Added `SimulateSwipe()` public method to fire through existing event pipeline.
- `Gameplay/Scripts/Installers/GameplayInstaller.cs`: Added AutoTester binding (FromComponentInHierarchy).
- `Gameplay/Scenes/GameplayScene.unity`: AutoTester GameObject added to scene.
**Impact on iteration:** None — debug utility, no architectural changes.
