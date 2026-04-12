# Task 1: Line Feel Overhaul

Rework line rendering and timing to improve gameplay feel.

## Subtasks

### 1.1 ✅ Remove ratio gap from LineDrawer
Single continuous segment, no gap. Visual-only change, no test changes needed.

### 1.2 ✅ Make preview and line timing BPM-independent
PreviewLead stays in beats (scheduling), approach/fadeout durations now in seconds (visual). Converted timing fields (PreviewLead, PreviewApproachRate, PreviewFadeout, LineApproachRate, LineFadeout) from beats to seconds in SessionConfigSO. Updated LineSpawner, LineDrawer, and tests. Added test for BPM-independence.

### 1.3 ✅ Randomize line position
Added PositionOffsetRange to SessionConfigSO, Offset to LineData. Applied in LineDrawer, LineSpawner, SliceEvaluator, and AutoTester.

### 1.4 ✅ Vary line sizes with score-based progression
Added MinLineLength, MaxLineLength, FullVarietyScore to SessionConfigSO. Length per line in LineData. Removed hardcoded LINE_LENGTH from LineDrawer, SliceEvaluator, AutoTester.
