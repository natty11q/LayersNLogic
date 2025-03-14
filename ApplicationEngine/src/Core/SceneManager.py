from ApplicationEngine.src.Core.Scene import *

class SceneManager:
    def __init__(self):
        self.scenes : dict[str,Scene] = {}
        self.activeScene : Scene | None = None

    def add_scene(self, scene : Scene):
        self.scenes[scene.name] = scene
    
    def set_active_scene(self, name : str):
        self.activeScene = self.scenes.get(name)
    
    def update(self, dt : float):
        if self.activeScene:
            self.activeScene.Update(dt)

    def PhysicsUpdate(self, tickTime : float):
        if self.activeScene:
            self.activeScene.PhysicsUpdate(tickTime)

    def draw(self):
        if self.activeScene:
            self.activeScene.Draw()