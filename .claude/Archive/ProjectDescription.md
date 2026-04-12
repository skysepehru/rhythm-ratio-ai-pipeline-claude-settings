This is the description of the first version of the rhythm ratio game.
This document is intended to guide AI in developing the game, and in the process, also help me refine my AI workflow when working with Unity Projects.
We will be initially developing an MVC but the code quality and performance should be production level.

# Project Outline
Rhythm Ratio is a hyper-casual mobile game for iOS and Android.
You will have to swipe on your screen to slice lines appearing on your screen. The lines appear on the screen according to a specific rhythm.
The game goes on infinitely, with the prospect of having it be level-based in the future. It is initially infinite for simplicity as an mvc

# Game MVC Flow
- Main Menu Panel
    - Simple white background
    - High Score
    - Play button
    - SFX volume slider
- Play Panel
    - Pause Button
        - Opens Pause Panel
            - Resume Button
            - SFX volume slider
            - Back to main menu
    - Score
    - HP Bar
    - The gameplay section, which is in the middle of the screen. Exact description in the next section.
    - The Incoming Ratio Text(Icon)
    - Game Lost Panel
        - Score
        - High Score
        - Retry Button
        - Back To Main Menu
# Gameplay
The slicing happens on a line which appears on screen in select intervals:
- Say the beat is 4/4. If the user has to slice on the 4th beat, they will get a preview of this beat a certain amount in advance, for example 2 beats earlier, or 1/8th earlier. This amount stays the same throughout the entire game. the bmp might increase, the this distance of the preview to the user has to beat stays the same in measurement of beat spacing.
- According to this, the timing of the slicing is determined. With that in mind:
    - The line for slicing is shown to the player ahead of time "ar" miliseconds ahead of time.(This is different from the preview, preview just tells the user that They have to press some beats from now)(ar stands for approach rate)
    - The time in which the user actually does the slice relative to the exact time determines the accuracy.
        - User slice time is outside exact slice time minus-plus "good-time" : Perfect Accuracy
        - User slice time is outside exact Slice time minus-plus "bad time" : Good Accuracy
        - User slice time is outside exact Slice time minus-plus "fail time" : bad Accuracy
        - User slice time is between exact Slice time minus "fail time" and exact Slice time minus approach time: player missed
        - User slice time is after exact Slice time plus "fail time" : player missed
    - All of the properties stay the same throughout the game. However they all scale according to bpm (song speed)
- The lines should be sliced according to a certain ratio.
    - Some ratios are easier than others. 1/1 is definitely easier than 3/7.
    - The look of the lines in case of different ratios might look different, but the looks do not indicate where the line is supposed to be cut. However, another element in the gameplay scene shows the ratio of the upcoming slice as soon as the previous slice is over.
        - The most important characteristic of the lines that indicate their ratio is their color. their difficulty correspond to the color according to common rarity of items in video games:
            - Gray 1/1
            - Blue 1/2
            - Purple 2/3
            - Gold 3/7
            - Red 5/7
    - the lines show up with an orientation (rotation around the z axis). This determines what angle the user should slice the line
    - The user also gets a fail/bad/good/perfect score based on the position it was sliced and the direction is was sliced.
        - There should be a system using certain threshold to calculate the final slicing grade based on the position and the direction of the slice.
- The game starts with a certain speed from easy 1/1 slices and then gets slowly harder
# HP System
Uses an osu!-style HP drain system:
- HP drains passively over time
- Successful slices restore HP (more for Perfect, less for Good/Bad)
- Misses drain additional HP
- Game ends when HP reaches 0