
[Portals Example 1]: ../Docs/img/portalExample_1.png "Portals Example pre block"
[Portals Example 2]: ../Docs/img/portalExample_2.png "Portals Example post block"
[External input 1]: ../Docs/img/ExternalInput_1.png "External input pre made"

<head>
<style>
    * {
        /* color: orange; */
  text-align:center;
}

h3, h2 {
  text-decoration: underline;
}

</style>

</head>

<div>

<h1 style="text-align:center;"> Layers ∧ Logic </h1>
<p  style="text-align:center;"><em> layers and logic</em></p>

</div>

## Overview

### Concept
Layers and logic is a game designed to test the users intuition by combining elements of many games and expanding upon that, 
taking in new input methods and iterating on previous techniques though story and gameplay.


<br>


### How is this done?
One of the ideas we had druing development was to involve the user in the game's contexts; having the character acknowledge the user's presence.
this allows for a sort of personal interaction with the game as the character breakswhat seesm to be the 4th wall.

An idea for how this would be implemented is by having the user interacti with an external input that may have to be inputted or created by the player

For example, a scene where the player comes across an obstacle that is difficult to overcome, the player may have to search for a solution. this may cause the player to discover some schematics for a button device. this would be in the form of instructions to put a button on a breadboard and add some arduino uno code that will then be plugged into the computer. now this button can be used to activate objects in the game's environment and used to solve certain puzzles ingame.

> An example where the player comes across a locked door that cannot be opened with anything in the game world.

![player comes across locked door][External input 1]

> Player reads instructions and creates the required equiptment.

![player reads instructions][External input 2]

> Player implements feature and uses it to open the door.

![player reads instructions][External input 3]


<br>

There will aslo be other elements used to do this. this can be done via elements such as portals. these can be used in tandem with a physics engine to solve ingame puzzles.



> Here is an exaplme where the player is presented with a cliff that is too high for the player's jump to overcome. from here the player must use their environemnt to overcome this.

![player presented with cliff to get over to reach objective][Portals Example 1]

> The player in this instance would have to be ready to stand above the portal and cause the block to fall though. the momentum gained whilst the block was falling will be transfered to the player giving them the height required to get over the obstacle.

![player overcome cliff to get over to reach objective using portals][Portals Example 2]