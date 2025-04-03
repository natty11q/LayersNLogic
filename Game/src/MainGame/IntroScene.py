import ApplicationEngine.AppEngine as LNLEngine
from ApplicationEngine.include.Maths.Maths import *

## ============================= App Code =================================
from Game.src.MainMenu.UI.ButtonClass import *
from Game.src.GameComponents.Entities.PlayerClass import *



from Game.src.Level.Levels import *


class IntroScene(LNLEngine.Scene):
    def __init__(self):
        super().__init__("IntroScene")
        self.Camera    = LNLEngine.OrthographicCamera(-1.0, 1.0, -1.0, 1.0)
        self.ScreenShader = LNLEngine.ScreenShader(FragmentShader="ApplicationEngine/src/Object/Shaders/templeScene.frag", FragmentShaderIsPath= True)

        self.AddObject(self.ScreenShader)

    def _OnBegin(self):
        self.SetMainCamera(self.Camera)


    def OnEvent(self, e: LNLEngine.Event):
        sm = self.GetOwner()
        if sm:
            if sm.activeScene:
                if sm.activeScene.name != self.name:
                    return
        
        if e.GetType() == LNLEngine.LNL_EventType.KeyDown:
            if e.keycode == LNLEngine.KEY_MAP["space"]:
                sm = self.GetOwner()
                if sm:
                    sm.SetActiveScene("MainScene")


    def _OnUpdate(self, dt: float):

        LNLEngine.Renderer.Clear()

        self.Draw()
        self.DrawUI()

        LNLEngine.Renderer.DrawText("a demo of what the possibilities are for", Vec2(100, 450), 45, Vec3())
        LNLEngine.Renderer.DrawText("layers and logic.", Vec2(300, 500), 45, Vec3())
        LNLEngine.Renderer.DrawText("Press Space to continue", Vec2(200, 550), 45, Vec3())