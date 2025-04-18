# Game Class



The Game class is used to handle the Top level logic of the engine
This is where the commands for calculating frame times and update calls for layers are handled.

the above is all handled within the engine.

When using the game engine, you will need to create a definition for a game class which will be used to insert the additional logic that makes your game your own.

this is done though inhertence.

```python

class MyGameClass(LNLEngine.Game):
    def __init__(self):
        super().__init__()
        ...

```


from here, Typically you will want to create your main window.



```python

class MyGameClass(LNLEngine.Game):
    def __init__(self):
        super().__init__()

    LNLEngine.Game.CreateGameWindow("PortalsDemo", 900, 600)
```



this will create a window with the title "MyGame" and dimensions of `900` for the width and `600` for the height.

this will create one main window that is handled by the game class.

If you want to have direct access to the window you can do that by directly accessing the `CreateWindow` function within the Window class of the engine 
eg:



```python

class MyGameClass(LNLEngine.Game):
    def __init__(self):
        super().__init__()

        props = LNLEngine.WindowProperties("MyGame", 900, 600)
        window = LNLEngine.Window.CreateWindow(props)
```


this gives you direct access to the winodw however this may cause problems if they are not handled properly as you will need to manually setup the window and run it.

It is reccomended that you handle the window setup from using the Game class's `CreateWindow` funciton however you may want to create your own if you are making your own windowmanager that may need to handle multiple windows for example.


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


Make In order To add the game class instance to the engine you must use the `CreateGame` function, passing in the Class itself as the argument.

This will return a game instance that you will use to run the game. 

this will begin the main game loop.

```python

class MyGameClass(LNLEngine.Game):
    def __init__(self):
        super().__init__()
        LNLEngine.Game.CreateGameWindow("MyGame", 900, 600)


if __name__ == "__main__":
    LNLEngine.Game.CreateGame(MyGameClass)
    LNLEngine.Game.RunGame() # <- based on a static instance of the game class.
    # does not require any arguments
```


The Game class is also where laters are Pushed to the Layerstack
as the engine's main logic should be handled within the layers.

as the game Class has been run, the layers will automatically be updated, passing in deltatime based on the frame time and timescale.

more infomration on the layersystem can be found here:

[LayerSystem Documentation](./LayerSystem.md "LayerSystem Documentation")


In order to push a layer to the stack you can simply use the Push Layer function provided by the game class.

```python

class MyGameLayer(LNLEngine.Layer):
    def __init__(self, name="TestLayer"):
        super().__init__(name)
    
    def OnEvent(self, event: LNLEngine.Event):...
    def OnUpdate(self, deltatime : float): ...

class MyGameClass(LNLEngine.Game):
    def __init__(self):
        super().__init__()
        LNLEngine.Game.CreateGameWindow("MyGame", 900, 600)
        
        self.PushLayer( MyGameLayer() )
        # you will want to create a new instance unlike with CreateGame
        # as it is creating a new instance and pushing it directly.


if __name__ == "__main__":
    LNLEngine.Game.CreateGame(MyGameClass)
    LNLEngine.Game.RunGame() 
```

You should not use the Renderer's implementation of the PushLayer unless you know what you are doing as this version is defined for window
controlled apis like simplegui only whereas, using a raw Opengl implementation or a vulkan implementation will use the game class's layerstack instead as it is updated in an open main game loop.

the Game class's implementation will work for ANY api so it is highly reccomended you use this implemntation to keep your application api agnostic at no extra cost.

These are the main components of the Game class that you will need to consider when creating a game using Logic Engine.

