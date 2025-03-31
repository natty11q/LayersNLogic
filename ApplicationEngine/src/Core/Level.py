
from ApplicationEngine.include.Common import *
from ApplicationEngine.src.Object.Object import *

class LevelManagerBase:
    def setActiveLevel(self, levelName : str):
        ...

class Level():
    def __init__(self, name):
        self.name = name
        self.LevelObjects : dict[str, list[GameObject]] = {}
        self.__ownerLevelManager : LevelManagerBase | None = None
    def setOwner(self, newOwner : LevelManagerBase):
        self.__ownerLevelManager = newOwner

    def getOwner(self) -> LevelManagerBase | None:
        return self.__ownerLevelManager
    

    def BeginPlay(self):
        for componentType in self.LevelObjects.keys():
            for gameObj in self.LevelObjects[componentType]:
                gameObj.BeginPlay()

    def EndPlay(self):
        for componentType in self.LevelObjects.keys():
            for gameObj in self.LevelObjects[componentType]:
                gameObj.EndPlay()


    def AddLevelComponent(self, component : GameObject, c_type: str = "default_componet_type"):
        if self.LevelObjects.get(c_type, None) is None:
            self.LevelObjects[c_type] = []

        self.LevelObjects[c_type].append(component)
    
    def RemoveLevelComponent(self, component, type):
        ...
    def OnEvent(self, e : Event): ...
    
    def OnUpdate(self, deltatime): ...

    def Update(self, deltatime : float):
        for componentType in self.LevelObjects.keys():
            for gameObj in self.LevelObjects[componentType]:
                if gameObj.IsActive():
                    gameObj.Update(deltatime)

        self.OnUpdate(deltatime)

    def OnPhysicsUpdate(self, tickTime): ...

    def PhysicsUpdate(self, tickTime : float):
        for componentType in self.LevelObjects.keys():
            for gameObj in self.LevelObjects[componentType]:
                if gameObj.IsActive():
                    gameObj.PhysicsUpdate(tickTime)

        self.OnPhysicsUpdate(tickTime)

    def Draw(self):
        for componentType in self.LevelObjects.keys():
            for gameObj in self.LevelObjects[componentType]:
                if gameObj.IsActive():
                    gameObj.Draw()
