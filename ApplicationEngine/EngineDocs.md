# Application Engine Documentation

### LogicEngine - RHUL - Nathaniel Frimpong-Santeng

The Application Engine acts as an interface between developers and the **_SimpleGUICS2Pygame_** Python import.  
It extends the capabilities of the library and adds powerful features such as:

- 3D rendering via model files  
- Audio handling (playlist, looping, panning, channel volumes)  
- 3D spatial audio  
- Batch rendering  
- Event system (handling + delegates)  
- Resource management  
- Hardware interfacing  
- Networking  
- 2D Physics Engine  
- ...and more

By extending their toolset with more complex features, developers are able to work faster and more efficiently with a broader toolset and greater creative freedom.

---

# Understanding the Basics

To begin using the engine, you'll need to include the LogicEngine in your application.

> [!NOTE]
> In the future, this will be available as a pip-installable module.  
> For now, you must manually append the engine's path to `sys.path` to maintain internal reference integrity.

Example setup:

```python
# MyGame.py

## ============================== setup ===================================
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import ApplicationEngine.AppEngine as LNLEngine
```

This setup assumes your file structure looks like this:

```bash
.
├── ApplicationEngine
│   ├── AppEngine.py
│   ├── include
│   └── src
└── Game
    └── src
        └── MyGame.py  # <- Your main script
```

In this case, `MyGame.py` is the entry point, and the application engine resides two folders above, hence `'../../'`.

If your structure is different, for example:

```bash
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

You would set it up like this:

```python
# run.py

## ============================== setup ===================================
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
## ============================= App Code =================================
import src.MyGame as MyGame

def main():
    MyGameInst = LNLEngine.Game.CreateGame(MyGame.MyGameClass)
    MyGameInst.Run()
    MyGameInst.Save()
```

And in `MyGame.py`:

```python
# MyGame.py

## ============================== setup ===================================
import ApplicationEngine.AppEngine as LNLEngine
## ============================= App Code =================================

class MyGameClass(LNLEngine.Game):
    # Define game content here
    ...
```

---

## Foundational Knowledge

Before building, it’s helpful to understand the core parts of LogicEngine, the tools available, and common engine concepts:

- [GameClass Documentation](../Docs/Engine/GameClass.md "GameClass Documentation")
- [LayerSystem Documentation](../Docs/Engine/LayerSystem.md "LayerSystem Documentation")
- [Scenes Documentation](../Docs/Engine/Scenes.md "Scenes Documentation")
- [Levels Documentation](../Docs/Engine/Levels.md "Levels Documentation")
- [Debugging Documentation](../Docs/Engine/Debugging.md "Debugging Documentation")

---

# Creating a Game

Once you've set up the engine, you can create your own game by defining a custom game class.

The `Game` class handles top-level logic such as window creation and layer management. Your custom class must inherit from the engine's `Game` class.

Example:

```python
# MyGame.py

## ============================== setup ===================================
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import ApplicationEngine.AppEngine as LNLEngine
## ============================= App Code =================================

class MyGameLayer(LNLEngine.Layer):
    def __init__(self, name="TestLayer"):
        super().__init__(name)
    
    def OnEvent(self, event: LNLEngine.Event): ...
    def OnUpdate(self, deltatime : float): ...

class MyGameClass(LNLEngine.Game):
    def __init__(self):
        super().__init__()
        LNLEngine.Game.CreateGameWindow("MyGame", 900, 600)
        
        self.PushLayer(MyGameLayer())
        # Note: PushLayer expects a new instance, unlike CreateGame,
        # which receives a class reference.

if __name__ == "__main__":
    LNLEngine.Game.CreateGame(MyGameClass)
    LNLEngine.Game.RunGame()
```

---

## Understanding Layers in Practice

(Additional section content will go here.)

