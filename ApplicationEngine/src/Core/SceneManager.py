from ApplicationEngine.src.Core.Scene import *

class SceneManager:
    def __init__(self):
        self.scenes : dict[str,Scene] = {}
        self.activeScene : Scene | None = None

    def add_scene(self, scene : Scene):
        self.scenes[scene.name] = scene
    
    def set_active_scene(self, name : str):
        if name not in self.scenes.keys():
            LNL_LogEngineError(f"attempted to set scene [{name}] as active, but the scene [{name}] has not been added")
            return
         # end the play of the currently actice scene before changing it
        if self.activeScene:
            self.activeScene.EndPlay()

        self.activeScene = self.scenes.get(name)
        self.activeScene.BeginPlay() # type: ignore
    
    def OnEvent(self, e : Event):
        if self.activeScene:
            self.activeScene.OnEvent(e)



    def update(self, dt : float):
        if self.activeScene:
            self.activeScene.Update(dt)

    def PhysicsUpdate(self, tickTime : float):
        if self.activeScene:
            self.activeScene.PhysicsUpdate(tickTime)

    def Draw(self):
        if self.activeScene:
            self.activeScene.Draw()