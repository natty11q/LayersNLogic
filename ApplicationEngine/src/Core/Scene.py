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


class SceneManagerBase:
    def SetActiveScene(self, sceneName : str):
        ...


class Scene:
    def __init__(self, name : str):
        self.name = name
        self.objects : list[GameObject] = []  # List of GameObject instances
        self.UIElements : list[GameObject] = []  # List of GameObject instances
        self.levelManager : LevelManager = LevelManager()

        self.__mainCamera : Camera = OrthographicCamera()
        self.__hudCamera  : Camera = OrthographicCamera()

        self.sceneType : SceneType = SceneType.Undef
        self.__ownerSceneManager : SceneManagerBase | None = None


        AddEventListener( self.OnEvent )


    def SetMainCamera(self, camera : Camera):
        self.__mainCamera = camera
    def GetMainCamera(self, camera : Camera):
        return self.__mainCamera


    def SetHudCamera(self, camera : Camera):
        self.__hudCamera = camera    
    def GetHudCamera(self, camera : Camera):
        return self.__hudCamera

    def _OnBegin(self):
        ...

    def BeginPlay(self):
        self._OnBegin()
        # if self.levelManager.activeLevel:
        #     self.levelManager.activeLevel.BeginPlay()
        for obj in self.objects:
            obj.BeginPlay()

    def EndPlay(self):
        if self.levelManager.activeLevel:
           self.levelManager.activeLevel.EndPlay()
        for obj in self.objects:
            obj.EndPlay()

    def SetOwner(self, newOwner : SceneManagerBase):
        self.__ownerSceneManager = newOwner

    def GetOwner(self) -> SceneManagerBase | None:
        return self.__ownerSceneManager

    

    def AddObject(self, obj : GameObject):
        self.objects.append(obj)


    def AddUIElement(self, elm : GameObject):
        self.UIElements.append(elm)


    def GetLevelManager(self):
        return self.levelManager

    def _OnUpdate(self, dt : float):
        ...
    
    def OnEvent(self, e : Event):
        self.levelManager.OnEvent(e)

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
        Renderer.BeginScene(self.__mainCamera)
        
        self.levelManager.Draw()
        for obj in self.objects:
            obj.Draw()

        Renderer.EndScene()
    
    def DrawUI(self):
        Renderer.BeginScene(self.__hudCamera)
        
        # self.levelManager.Draw()
        for elm in self.UIElements:
            elm.Draw()

        Renderer.EndScene()