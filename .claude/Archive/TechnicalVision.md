Major Systems

## Slicing Input

There exists a service which its only job is to handle slicing and raise an event on itself for others to listen to.
It should use the new input system without input actions, using the enhanced touch API : https://docs.unity3d.com/Packages/com.unity.inputsystem@1.19/manual/Touch.html

It should handle scenarios where the user just touches a spot on the screen, but it shouldn't introduce latency as well.

It is always checking for slices and whenever there is a movement categorized as a slice, it will raise an event which will give the position(middle point of the slice) and direction of the slice.

## Line Spawning

As explained in the Project Description, The line spawning and gameplay works like this:
- The gameplay will have to guide the user to slice lines in a rhythm
- The gameplay runs on a BPM, and we also know how many beats there is in a measure (the top part of 3/4, 4/4, etc.)
  - For example, 120bpm is 500ms per beat. if it is 3/4, we have a measure every 1.5 seconds.
- The game needs to tell the player in advance that they need to slice in a way
  - This happens with Previews. For gameplay, it is specified how many beats in advance the preview should be shown.
  - The preview has its own visual characteristics, and is visually different from the corresponding line the player should slice 
  - For a session, the number of beats the preview should appear ahead of time is the same for all lines.
  - This number of beats can be a fraction, not necessarily whole numbers.
  - The preview fully shows the direction and ratio of the line
  
There should be a Gameplay service which contains an object including all the properties which derives how lines and previews are visually working. 
If bpm changes, everything should react acccordingly.
The lines do not hold their own state, they read it from a shared object passed onto them.

The Gameplay service keeps track of the time of the session. 
It also keeps track of which measure and beat we are on. The game continues infinitely but that's ok

The Gameplay service should have a method which recieves a time since game start and direction, and handles spawning and integrating with the slicing input service.
It calculated the accuracy stuff too, maybe using other services if necessary, not sure.
The spawning is with object pooling.

Then there is another service which handles giving it the directions. It will handle start and stuff, Th gameplay service itself might have a start itself too, not sure.

# Line visuals
We should use the Shape asset immediate mode drawing. It is in Plugins folder. The documentation is at https://acegikmo.com/shapes/docs/