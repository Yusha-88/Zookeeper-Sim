Change log

12/07/26 - Text displays near animals to alert the player of their hunger.

7/07/26 - Fixed issue where zebra NPC wasn't being animated properly and added final background of the zoo.

28/06/26 - Added spritesheet for zebra NPC.

23/06/26 - Added in spritesheet for elephant and tiger NPC.

16/06/26 - Added in spritesheet for penguin NPC, replacing in placeholder. 

13/06/26 - Moved the Animal NPCs boundary check from move() to a separate function check_boundary().

13/05/26 - Stopped Animal NPCs from moving off-screen. 

10/05/26 - Fixed an issue where the player can feed animals after they die. Added a death sprite for animals when they die.

9/05/26 - Animal NPCs now have placeholder sprites with idle animations.

5/05/26 - Zookeeper now has a placeholder sprite with idle and walking animations.

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