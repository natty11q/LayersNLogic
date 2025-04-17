# Application Engine Documentation


### LogicEngine - RHUL - Nathaniel Frimpong-Santeng

the application engine acts as an interface between the developers and the **_SimpleGUICS2Pygame_** python import.

It extends the functionality of the import and provides more powerful functions for the game such as
* 3D rendering via model files
* audio handling (playlits, looping, panning, channel volumes)
* 3D spacial audio
* batch handling
* event system (handling + deligates)
* resourse management
* hardware interfacing
* networking
* 2D Physics Engine
* \+ more features


This allows for faster more efficient development with more complex features
providing more creative freedom in the development process by extending the toolset of developers.




# Understanding the Basics


To begin using the engine you will need to include Logic engine into your application.

In future this will be turned into a module so that it can be used after a single pip install, However for now you will need to also add the path to the engine into sys.path to ensure that the internal references within the engine remain functional.


it can be done like this:

```python
# MyGame.py

## ============================== setup ===================================
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import ApplicationEngine.AppEngine as LNLEngine

```
This setup assumes that the engine exists within the application in a setup such as this:


```bash
.
├── ApplicationEngine
│   ├── AppEngine.py
│   ├── include
│   └── src
└── Game
    └── src
        └── MyGame.py <- content is within MyGame.py
```


in this scenario MyGame.py acts Main and is what is initially run. the Application engine is two folders above, hence the `'../../'` appended to the `sys.path`.
Assuming a different setup, EG:

``` Bash
.
├── ApplicationEngine
│   ├── AppEngine.py
│   ├── include
│   └── src
└── Game
    ├── run.py
    └── src
        └── MyGame.py

```

you will want your code to be similiar to as follows:

```python
# run.py

## ============================== setup ===================================
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
## ============================= App Code =================================
import src.Mygame as MyGame

def main():
    MyGameInst = LNLEngine.Game.CreateGame(MyGame.MyGameClass)
    MyGameInst.Run()
    MyGameInst.Save()
```

```python
# MyGame.py
## ============================== setup ===================================
import ApplicationEngine.AppEngine as LNLEngine
## ============================= App Code =================================

class MyGameClass(LNLEngine.Game):
    # define game content here
    ...
```

## Foundational Knowledge

Become familiar with the major components of Logic Engine, the various tools and you can use, and the most common engine terms.


[GameClass Documentation](../Docs/Engine/GameClass.md "GameClass Documentation")
[LayerSystem Documentation](../Docs/Engine/LayerSystem.md "LayerSystem Documentation")
[Scenes Documentation](../Docs/Engine/Scenes.md "Scenes Documentation")
[Levels Documentation](../Docs/Engine/Levels.md "Levels Documentation")



# Creating A Game

