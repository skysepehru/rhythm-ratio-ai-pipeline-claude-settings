# Iteration History

## Iteration 1: Core Rhythm Engine & Slicing
**Completed:** 2026-03-22

Playable prototype with core gameplay loop:
- Scene & DI foundation (Zenject, orthographic camera, portrait mode)
- Swipe input via Enhanced Touch API (continuous drag detection)
- Session config & beat pattern (ScriptableObjects, inspector-editable)
- Beat clock & metronome (dspTime-driven, tick audio)
- Line spawning, lifecycle & rendering (preview → approach → sliceable → resolved, Shapes immediate mode)
- Accuracy evaluation (timing/ratio/angle, weighted grading, any-Miss-means-Miss)
- Swipe-to-line connector (proximity check, hit/miss audio, debug text)

**Tasks:** 6 (all complete, Task 6 subtask 6.3 revised once)
**Tests:** 54 edit mode tests

## Iteration 2: Scoring, HP & Difficulty
**Completed:** 2026-03-23

Complete gameplay loop with win/lose condition:
- Scoring with combo multiplier (ScoreService, debug display)
- HP system with BPM-scaled passive drain, restore/penalty on hit/miss (HPService)
- Game over at HP=0 stops BeatClock and LineSpawner
- All 5 ratio tiers (Common→Mythic) with tier-colored previews
- DifficultyService progressive tier unlock based on successful slice count
- Grade-based resolved colors (Perfect=white, Good=green, Bad=orange, Miss=red)

**Tasks:** 3 (all complete)
**Tests:** 45 new edit mode tests (99 total)

## Iteration 3: Gameplay Feel & Phase System
**Completed:** 2026-04-09

Overhauled gameplay feel and introduced phase-based progression:
- Line feel overhaul: single continuous segments (no ratio gap), BPM-independent timing, randomized positions, score-based size variety
- Phase system replacing DifficultyService: sequential phases with single ratio tiers, decreasing duration, intro pause with Shapes-rendered display, background color transitions
- Measure visualizer: Shapes-based scrolling timeline with beat ticks and line indicators, configurable zoom
- Ad-hoc additions: slice visual effect (physics-driven fragments), bidirectional ratio evaluation, swipe speed tracking, tier colors moved to SessionConfigSO, grade-based resolved colors removed

**Tasks:** 3 (all complete) + 1 ad-hoc commit
**Details:** History/Iteration3/

## Iteration 4: UI & Session Flow
**Completed:** 2026-04-12

Feature-complete MVC with full UI and session management:
- Session reset & game state management (GameSessionService, ResetState on all services)
- Start Screen with tap-to-start and high score display (PlayerPrefs)
- Game Over Screen with final score, high score persistence, tap-to-restart
- Gameplay HUD with live score, HP bar (anchor-based fill), grade feedback (fade in/out, color-coded)
- DebugOverlay removed, SliceEvaluator fires OnGradeResolved event for UI
- HPService starts with IsGameOver=true to prevent drain before game starts
- EventSystem added for UGUI input

**Tasks:** 3 (all complete)
**Details:** History/Iteration4/
