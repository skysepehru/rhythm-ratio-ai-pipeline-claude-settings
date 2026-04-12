# Iteration 4, Task 3: Gameplay HUD & Cleanup

## Summary
Added GameplayHUD panel with live score, HP bar, and grade feedback. Removed DebugOverlay and debug text from SliceEvaluator.

## Subtasks

### 3.1: Gameplay HUD + remove DebugOverlay
- Created GameplayHUD panel on UICanvas with ScoreText, HPBarBackground/HPBarFill, and GradeText
- Score updates live from ScoreService in Update
- HP bar uses anchor-based fill (75% screen width, positioned below notch safe area)
- Grade feedback: color-coded text (Perfect!/Good/Meh/Missed) with fade in (0.08s) and fade out (0.25s) animation, configurable duration via SessionConfigSO.GradeFeedbackDuration (default 0.75s)
- Added OnGradeResolved event to SliceEvaluator for UI to subscribe to
- Removed DebugOverlay GameObject from scene
- Removed debug text (_debugText) field and HandleGameOver from SliceEvaluator
- Added GradeFeedbackDuration field to SessionConfigSO
- Files: UIManager.cs, SliceEvaluator.cs, SessionConfigSO.cs, GameplayScene.unity
