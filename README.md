Change log

22/04/26 - Moved logic that stops Zookeeper from leaving the screen after colliding with Animal to a function.

21/04/26 - Zookeeper no longer has to be colliding into Animal to feed it. Animals can only eat when their health falls below 70%.

19/04/26 - Zookeeper player can now feed Animal NPCs, restoring their health.

18/04/26 - Added collision between the player zookeeper and the animal NPCs.

2/04/26 - Added sounds for the animal AI, where they can make a sound in reaction to how hungry they are.

1/04/26 - Created Alive and Dead state, death condition, and death animation.

31/03/26 - Animal NPCs now move slower according to their hunger levels. Created initial hunger and movement speed attributes.

29/03/26 - Swapped height and width attributes for the max height and max width screen boundary check.

28/03/26 - Added validation for hunger attribute and TODO comments for future development.

27/03/26 - Animal NPCs have a hunger state and a drain hunger method.

25/03/26 - Fixed Animal NPC movement so they don't go offscreen. 

24/03/26 - Added timed random movements for the Animal NPCs.

17/03/26 - Added basic NPC movement.

16/03/26 - Added animal class.

15/03/26 - Initial creation of project and added player input movement for the zookeeper.