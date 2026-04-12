# Rhythm Ratio — Project Specification

## Overview
Rhythm Ratio is a hyper-casual mobile rhythm game for iOS and Android. Players swipe to slice lines at specific ratios and timings. The game runs infinitely with increasing difficulty, tracking score and HP.

## Screens & UI

Single scene, no scene reloading. UI is UGUI overlay on gameplay.

### Start Screen
- "Tap to start" prompt
- High score display (persisted via PlayerPrefs)
- Tap anywhere → gameplay begins

### Gameplay HUD
- **Score Display** — current score (top area)
- **HP Bar** — visual bar showing current HP (top area)
- **Gameplay Area** — center of screen where lines appear

### Game Over Screen
- Final score
- High score (updated if beaten)
- "Tap to restart" prompt
- Tap anywhere → resets all services in-place (no scene reload) and starts new session

## Gameplay

### Rhythm System
- Gameplay runs on a configurable **base BPM** (beats per minute) and **time signature** (e.g., 4/4, 3/4)
- BPM is dynamic: increases per phase and via perfect streaks (see Phase-Based Progression and Perfect Streak System)
- Beat pattern is configurable: not every beat requires a slice — some beats can be rests
- A beat pattern definition determines which beats within a measure have slices

### Preview System
- Previews and lines are conceptually separate phases (may share the same pooled object)
- A **preview** appears `preview_lead` beats before the slice is due (session-wide constant, default: 2 beats)
- The preview has its own approach rate (`preview_ar`): it fades in over `preview_ar` beats
- After the preview is fully visible, it remains for a duration then **fades out** over `preview_fadeout` beats
- The preview fully communicates the direction (angle) and ratio of the upcoming slice
- The preview is visually distinct from the actual slice line (e.g., ghost/outline style)

### Line Appearance (Approach Rate)
- After the preview fades out, the **actual line** appears at the **center** of the gameplay area
- The line becomes visible `line_ar` beats before the exact slice time (line_ar = line approach rate)
- The line fades/scales in to become fully visible at the exact slice time
- `line_ar` scales proportionally with BPM (defined in beats, converted to ms)

### Slicing Input
- Uses Unity Input System Enhanced Touch API (no Input Actions)
- A dedicated service detects swipe gestures and raises events with:
  - **Position**: midpoint of the swipe
  - **Direction**: angle/vector of the swipe
- Must handle tap-without-swipe gracefully (ignore or distinguish)
- Must minimize input latency

### Accuracy — Timing
Timing accuracy is based on the difference between user's slice time and the exact beat time:
- **Perfect**: within ±`perfect_window` ms of exact time
- **Good**: within ±`good_window` ms (but outside perfect)
- **Bad**: within ±`bad_window` ms (but outside good)
- **Miss**: outside `bad_window` OR no slice before next beat

All timing windows scale proportionally with BPM.

### Accuracy — Position (Ratio)
The line must be sliced at the correct ratio point. **Bidirectional evaluation**: slicing at either end of the line counts as the same ratio (e.g., 3/10 and 7/10 are equivalent). Accuracy grades:
- **Perfect**: within ±`perfect_ratio_threshold` of the target ratio (or its complement)
- **Good**: within ±`good_ratio_threshold`
- **Bad**: within ±`bad_ratio_threshold`
- **Miss**: outside `bad_ratio_threshold`

Thresholds are defined as fractions of the line length.

### Accuracy — Direction
The swipe angle must match the line's orientation. Accuracy grades:
- **Perfect**: within ±`perfect_angle_threshold` degrees
- **Good**: within ±`good_angle_threshold` degrees
- **Bad**: within ±`bad_angle_threshold` degrees
- **Miss**: outside `bad_angle_threshold`

### Combined Grade
The final grade uses a **worst-grade-wins** rule across three components:
- **Timing accuracy**
- **Position accuracy**
- **Direction accuracy**

The combined grade equals the worst individual grade. For example: Perfect + Perfect + Bad → Bad.

### Scoring
- Points per slice based on final grade: Perfect=300, Good=100, Bad=50, Miss=0
- **Combo multiplier**: consecutive non-miss slices increment a combo counter
  - Multiplier = 1 + floor(combo / 10) × 0.1 (or similar tunable formula)
  - Combo resets to 0 on miss
- Score per slice = base points × combo multiplier
- High score persisted via PlayerPrefs

### Line Visuals
- Lines are rendered using **Shapes** asset (component mode)
- Lines appear at randomized positions within configurable X/Y offset ranges
- Each line has:
  - **Orientation**: rotation around Z axis (determines required swipe angle)
  - **Length**: varies per line based on score progression (min/max configurable)
- Lines render as single continuous segments (no ratio gap)
- **All phases** (preview, line, sliceable) use **ratio tier colors** configured in SessionConfigSO:
    - Gray: 1/1 (Common)
    - Blue: 1/2 (Rare)
    - Purple: 2/3 (Epic)
    - Gold: 3/7 (Legendary)
    - Red: 5/7 (Mythic)
- On successful slice, a **slice effect** splits the line into two physics-driven fragments that fly apart in the swipe direction, with force proportional to swipe speed
- Lines do not hold their own state; they read from a shared data object

### Ratio Difficulty
Available ratios and their difficulty tiers (color applies to preview only):
| Ratio | Preview Color | Tier |
|-------|---------------|------|
| 1/1 | Gray | Common |
| 1/2 | Blue | Rare |
| 2/3 | Purple | Epic |
| 3/7 | Gold | Legendary |
| 5/7 | Red | Mythic |

### Phase-Based Progression
- Difficulty is managed by a **phase system**:
  - Each phase focuses on a single ratio tier
  - Phase duration (in measures) decreases as score increases
  - On phase start, line spawning pauses for an intro period while a display shows the upcoming ratio
  - Background color transitions to match the phase's tier color
  - **Initial cycle**: Common → Rare → Epic → Legendary → Mythic (sequential)
  - **After initial cycle**: Random weighted selection. Easier tiers lose weight over time (configurable decay). Base weights per tier are configurable.
- **BPM increases** by `BpmPerPhase` (default 5) each phase transition, smoothly during intro
- **HP drain increases** by `DrainIncreasePerPhase` each phase, capped at `MaxDrainPerBeat`

### Perfect Streak System
- Consecutive perfect slices form a streak
- Each perfect increases BPM by `BpmPerPerfect` (default 2), capped at `MaxPerfectStreakBonuses` (default 5) bonuses (so max +10 BPM from streak)
- On 5th and every subsequent consecutive perfect, HP is fully restored
- On streak break (miss or non-perfect slice), BPM smoothly but very quickly resets to phase base BPM
- Configurable audio clip per streak count

### Music
- A looping music clip plays from game start at the base BPM
- Music pitch adjusts with dynamic BPM changes (pitch = currentBpm / baseBpm), keeping music and beats synced

### HP System (osu!-style drain)
- HP range: 0 to `max_hp` (e.g., 100)
- HP starts at `max_hp`
- **Passive drain**: HP decreases by `drain_rate` per second continuously
- **Restore on hit**:
  - Perfect: +`hp_perfect` (e.g., +15)
  - Good: +`hp_good` (e.g., +8)
  - Bad: +`hp_bad` (e.g., +2)
- **Drain on miss**: -`hp_miss_penalty` (e.g., -10) in addition to passive drain
- HP clamped to [0, max_hp]
- **Game over** when HP reaches 0

### Object Pooling
- Lines are pooled and recycled (not instantiated/destroyed per beat)
- Pool managed by a dedicated service

### Audio
- Metronome tick sound on each beat for timing feedback
- Looping background music synced with dynamic BPM (see Music section)

## Session Flow
1. App opens → Start Screen shown ("Tap to start" + high score)
2. Player taps → gameplay begins, BPM and time signature start, metronome ticks
3. Preview for first slice fades in `preview_lead` beats ahead, then fades out
4. Actual line fades in `line_ar` beats before exact slice time at center
5. Player swipes to slice → timing + position + direction evaluated → grade shown
6. Score updates, HP adjusts, combo updates
7. Next slice queued per beat pattern
8. Phases progress through ratio tiers
9. HP drains passively; game ends when HP = 0
10. Game Over Screen shown (score, high score, "Tap to restart")
11. Player taps → all services reset in-place, new session begins (no scene reload)
