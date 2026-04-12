# Rhythm Ratio - Project Plan

## Game Summary
Hyper-casual mobile rhythm game where players swipe to slice lines at specific ratios and timings. Infinite gameplay with score, combo, and HP systems. See `ProjectSpecification.md` for full specification.

## Current Iteration
Complete. All planned iterations finished. Future work is freeform.

## Iterations

### Iteration 1: Core Rhythm Engine & Slicing
**Goal:** A playable prototype where lines appear at the center on beat, the player can swipe to slice them, and timing/position/direction accuracy is evaluated and displayed. Metronome ticks on each beat. No HP, no scoring UI, no menus — just the core gameplay loop running infinitely with a fixed BPM and 1/1 ratio.

### Iteration 2: Scoring, HP & Difficulty
**Goal:** Add scoring with combo multiplier, HP drain system (passive drain + restore/penalty on hit/miss), game over on HP=0, and difficulty progression that unlocks harder ratios over time. All ratios (1/1 through 5/7) with their color coding are playable. The game now has a complete gameplay loop with a win/lose condition, but no UI panels yet — debug display only.

### Iteration 3: Gameplay Feel & Phase System
**Goal:** Overhaul line behavior (remove ratio gaps, randomize position, vary sizes, decouple timing from BPM), replace random ratio selection with a phase-based progression system with intro screens and background color changes, and add a Shapes-based measure visualizer. The game feels significantly better to play.

### Iteration 4: UI & Session Flow
**Goal:** Minimal UI (Start Screen, Gameplay HUD, Game Over Screen) with tap-to-start/restart flow, in-place session reset (no scene reload), high score persistence (PlayerPrefs), and removal of debug overlay. The game is feature-complete for the MVC.
