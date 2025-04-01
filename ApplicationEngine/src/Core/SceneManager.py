from ApplicationEngine.src.Core.Scene import *

class SceneManager(SceneManagerBase):
    def __init__(self):
        self.scenes : dict[str,Scene] = {}
        self.activeScene : Scene | None = None

    def AddScene(self, scene : Scene):
        if scene.name in self.scenes.keys():
            LNL_LogEngineWarning(f"attempted to add scene [{scene.name}], scene of the same name has already been added")
        scene.SetOwner(self)
        self.scenes[scene.name] = scene
    
    def SetActiveScene(self, sceneName : str):
        if sceneName not in self.scenes.keys():
            LNL_LogEngineError(f"attempted to set scene [{sceneName}] as active, but the scene [{sceneName}] has not been added")
            return
         # end the play of the currently actice scene before changing it
        if self.activeScene:
            self.activeScene.EndPlay()

        self.activeScene = self.scenes.get(sceneName)
        self.activeScene.BeginPlay() # type: ignore
    
    def OnEvent(self, e : Event):
        if self.activeScene:
            self.activeScene.OnEvent(e)



    def Update(self, dt : float):
        if self.activeScene:
            self.activeScene.Update(dt)

    def PhysicsUpdate(self, tickTime : float):
        if self.activeScene:
            self.activeScene.PhysicsUpdate(tickTime)

    def Draw(self):
        if self.activeScene:
            self.activeScene.Draw()