# Game Class

The `Game` class is responsible for managing the top-level logic of the engine. This includes tasks such as calculating frame times and calling update functions on layers. All of this is handled internally by the engine.

When using the engine to build your own game, you’ll need to create a custom game class that inherits from `Game`. This allows you to insert game-specific logic.

---

### Inheriting from the Game Class

You can define your own game class like this:

```python
class MyGameClass(LNLEngine.Game):
    def __init__(self):
        super().__init__()
        ...
```

---

### Creating a Main Window

Typically, you'll want to create a window as part of your game setup:

```python
class MyGameClass(LNLEngine.Game):
    def __init__(self):
        super().__init__()

    LNLEngine.Game.CreateGameWindow("PortalsDemo", 900, 600)
```

This will create a window titled `"MyGame"` with a width of `900` and height of `600`. This window is managed by the `Game` class internally.

---

### Accessing the Window Directly

If you need direct access to the window, you can use the `CreateWindow` method from the `Window` class:

```python
class MyGameClass(LNLEngine.Game):
    def __init__(self):
        super().__init__()

        props = LNLEngine.WindowProperties("MyGame", 900, 600)
        window = LNLEngine.Window.CreateWindow(props)
```

This gives you direct control over the window, but keep in mind that you’ll be responsible for its setup and lifecycle. If not handled properly, this can lead to issues. It's generally recommended to use the `Game` class's `CreateWindow` method unless you have a specific need, such as building a custom window manager.

---

### Example: Custom Window Manager

```python
class MyWindowManager:
    def __init__(self):
        self.Windows : list[LNLEngine.Window] = []
        self.WindowStates : list[bool] = []

    def AddWindow(self, props : LNLEngine.WindowProperties, initState = True) -> int:
        self.Windows.append(LNLEngine.Window.CreateWindow(props))
        self.WindowStates.append(initState)

        return len(self.Windows) - 1
    
    def RemoveWindowById(id : int):
        w = self.Windows.pop(id)
        del w
        self.WindowStates.pop(id)
    
    def Update(self, dt : float):
        for i in range(len(self.windows)):
            window = self.Windows[i]
            if self.WindowStates[i]:
                window.Update(dt)

class MyGameClass(LNLEngine.Game):
    def __init__(self):
        super().__init__()

        props = LNLEngine.WindowProperties("MyGame", 900, 600)
        window = LNLEngine.Window.CreateWindow(props)
```

---

### Starting the Game

To create and run the game instance, use the `CreateGame` and `RunGame` methods:

```python
class MyGameClass(LNLEngine.Game):
    def __init__(self):
        super().__init__()
        LNLEngine.Game.CreateGameWindow("MyGame", 900, 600)


if __name__ == "__main__":
    LNLEngine.Game.CreateGame(MyGameClass)
    LNLEngine.Game.RunGame()  # Uses the static game instance. No arguments required.
```

---

### Working with Layers

The `Game` class manages the engine’s `LayerStack`. Layers are automatically updated as the engine runs, with delta time passed in based on the current frame time and timescale.

More information can be found in the [LayerSystem Documentation](./LayerSystem.md "LayerSystem Documentation").

To push a layer to the stack, use the `PushLayer` method:

```python
class MyGameLayer(LNLEngine.Layer):
    def __init__(self, name="TestLayer"):
        super().__init__(name)
    
    def OnEvent(self, event: LNLEngine.Event): ...
    def OnUpdate(self, deltatime : float): ...

class MyGameClass(LNLEngine.Game):
    def __init__(self):
        super().__init__()
        LNLEngine.Game.CreateGameWindow("MyGame", 900, 600)
        
        self.PushLayer(MyGameLayer())  # Always create a new instance before pushing.
```

---

### API Considerations

> [!WARNING]
> Avoid using the renderer's `PushLayer` method unless you know exactly what you're doing. That implementation is intended for window-managed APIs like SimpleGUI. If you’re using a lower-level API like OpenGL or Vulkan, the `Game` class's `LayerStack` should be used instead.

Using the `Game` class for layer management ensures that your application remains **API-agnostic**, with no additional complexity.

---

### Summary

These are the core features of the `Game` class that you'll need when building a game using Logic Engine. By inheriting from `Game`, using its built-in window creation and layer stack methods, and leveraging the engine’s main loop, you can create a scalable, maintainable game structure with ease.
