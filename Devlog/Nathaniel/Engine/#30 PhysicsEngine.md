For the physics engine, I have decided to use a seperate coord system to the screen space coords, starting from the bottom left as 0, 0 instead of the top left.

this is as It reduces likely hood of mistakes when creating the physics engine maths as the y values may be flipped


the position can be fixed on render using a function to convert it in the renderer