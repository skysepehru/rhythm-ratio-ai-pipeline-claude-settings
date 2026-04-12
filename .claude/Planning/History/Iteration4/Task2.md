# Iteration 4, Task 2: Start Screen & Game Over Screen (UGUI)

## Summary
UGUI Canvas with StartScreen and GameOverScreen panels. UIManager toggles panels based on GameSessionService state. Tap input triggers state transitions. High score persisted via PlayerPrefs.

## Subtasks

### 2.1: UGUI Canvas setup + StartScreen panel
- Created UICanvas (ScreenSpace-Overlay, 1080x1920 CanvasScaler) with StartScreen and GameOverScreen panels
- Added UIManager MonoBehaviour: listens to GameSessionService.OnStateChanged, toggles panels, handles tap-to-start/restart via Button.onClick
- Removed temporary auto-start from GameSessionService (starts in WaitingToStart state)
- Fixed HPService to start with IsGameOver=true to prevent HP drain before game starts
- Added EventSystem for UGUI input
- Added UIManager binding to GameplayInstaller
- Files: UIManager.cs (new), GameSessionService.cs, HPService.cs, GameplayInstaller.cs, GameplayScene.unity

### 2.2: GameOverScreen panel + high score persistence
- Added FinalScoreText and HighScoreText to GameOverScreen panel
- UIManager displays final score from ScoreService on game over
- High score persisted to PlayerPrefs, updated if beaten
- StartScreen shows persisted high score on launch/restart
- Files: UIManager.cs, GameplayScene.unity
