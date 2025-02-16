import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import ApplicationEngine.AppEngine as LNLEngine



class TestLayer(LNLEngine.Layer):
    def __init__(self, name="TestLayer"):
        super().__init__(name)
    
    def OnUpdate(self):
        LNLEngine.Renderer.DrawTriangle([LNLEngine.Vector.Vec2(10,10),LNLEngine.Vector.Vec2(100,50) , LNLEngine.Vector.Vec2(200,400)], LNLEngine.Vector.Vec4(100, 200, 255, 0))

class DoomExample(LNLEngine.Game):
    def __init__(self):
        super().__init__()
        props = LNLEngine.WindowProperties("DoomExample", 900, 600)
        self._window = LNLEngine.Window.CreateWindow(props)
        
        LNLEngine.Renderer.PushLayer(TestLayer())

    def _OnUpdate(self):
        return super()._OnUpdate()


if __name__ == "__main__":
    gameInst = DoomExample()
    gameInst.Run()