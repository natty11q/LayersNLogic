from __future__ import annotations

from ApplicationEngine.include.Common import *
# from ApplicationEngine.include.Maths.Maths import *
# from ApplicationEngine.include.Window.Window import *
from ApplicationEngine.src.Object.Object import *
from ApplicationEngine.src.Core.LevelManager import *
# from ApplicationEngine.src.Graphics.Renderer.Renderer import *
# import ApplicationEngine.src.Core.Utility.Temporal as Temporal

import os
import json


class SceneType(Enum):
    Undef = auto()
    Menu = auto()
    Game = auto()





class Scene:
    def __init__(self, name : str):
        self.name = name
        self.objects : list[GameObject] = []  # List of GameObject instances
        self.UIElements : list[GameObject] = []  # List of GameObject instances
        self.levelManager : LevelManager = LevelManager()

        self.sceneType : SceneType = SceneType.Undef

        AddEventListener( self.OnEvent )

    def AddObject(self, obj : GameObject):
        self.objects.append(obj)
    
    def GetLevelManager(self):
        return self.levelManager

    def _OnUpdate(self, dt : float):
        ...
    
    def OnEvent(self, e : Event):
        ...

    def Update(self, dt : float):
        if self.sceneType not in [SceneType.Menu]:
            self.levelManager.Update(dt)

        self._OnUpdate(dt)

        for obj in self.objects:
            obj.Update(dt)
    
    def PhysicsUpdate(self, tickTime : float):
        self.levelManager.PhysicsUpdate(tickTime)
        for obj in self.objects:
            obj.PhysicsUpdate(tickTime)

    def Draw(self):
        self.levelManager.Draw()
        for obj in self.objects:
            obj.Draw()