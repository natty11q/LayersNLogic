
from ApplicationEngine.src.Core.Level import *



class LevelManager:
    def __init__(self):
        self.levels : dict[str, Level] = {}
        self.activeLevel : Level | None = None
    
    def addLevel(self, level : Level):
        if level.name in self.levels.keys():
            LNL_LogEngineWarning(f"attempted to add level [{level.name}], level of the same name has already been added")
        self.levels[level.name] = level
    
    def setActiveLevel(self, levelName : str):
        if levelName not in self.levels.keys():
            LNL_LogEngineError(f"attempted to set level [{levelName}] as active, but the scene [{levelName}] has not been added")
            return
        self.activeLevel = self.levels[levelName]



    def Update(self, deltatime : float):
        if self.activeLevel:
            self.activeLevel.Update(deltatime)

    def PhysicsUpdate(self, tickTime : float):
        if self.activeLevel:
            self.activeLevel.PhysicsUpdate(tickTime)

    def Draw(self):
        if self.activeLevel:
            self.activeLevel.Draw()