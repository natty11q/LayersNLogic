
from ApplicationEngine.include.Common import *
from ApplicationEngine.src.Object.Object import *


class Level():
    def __init__(self, name):
        self.name = name
        self.LevelObjects : dict[str, list[GameObject]] = {}
    
    def AddLevelComponent(self, c_type: str, component : GameObject):
        if self.LevelObjects.get(c_type, None) is None:
            self.LevelObjects[c_type] = []

        self.LevelObjects[c_type].append(component)

    def Update(self, deltatime : float):
        for componentType in self.LevelObjects.keys():
            for gameObj in self.LevelObjects[componentType]:
                if gameObj.IsActive():
                    gameObj.Update(deltatime)

    def PhysicsUpdate(self, tickTime : float):
        for componentType in self.LevelObjects.keys():
            for gameObj in self.LevelObjects[componentType]:
                if gameObj.IsActive():
                    gameObj.PhysicsUpdate(tickTime)

    def Draw(self):
        for componentType in self.LevelObjects.keys():
            for gameObj in self.LevelObjects[componentType]:
                if gameObj.IsActive():
                    gameObj.Draw()
