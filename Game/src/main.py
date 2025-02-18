## ============================== setup ===================================
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from ApplicationEngine.include.Maths.Vector.Vector import Vec2, Vec4
import ApplicationEngine.AppEngine as LNLEngine
## ============================= App Code =================================



import math


class MovingSquare(LNLEngine.Quad):
    def __init__(self, topLeft: LNLEngine.Vector.Vec2, width: float, height: float, colour: LNLEngine.Vector.Vec4):
        super().__init__(topLeft, width, height, colour)
        self.RestPos : LNLEngine.Vector.Vec2 = topLeft
        
    def _OnUpdate(self):
        self._topLeft = LNLEngine.Vector.Vec2( self.RestPos.x + ( 300 * math.cos(LNLEngine.LLEngineTime.Time() * 2) ), self.RestPos.y + ( 300 * math.sin(LNLEngine.LLEngineTime.Time() * 2) ))

class TestLayer(LNLEngine.Layer):
    def __init__(self, name="TestLayer"):
        super().__init__(name)
        self.gameWindow = LNLEngine.Game.Get().GetWindow()
        
        # =================================
        testSquareWidth = 100
        testSquareHeight = 100
        
        self.TestSquare = MovingSquare(
            LNLEngine.Vector.Vec2(
                self.gameWindow.GetWidth() / 2 - (testSquareWidth/2),
                self.gameWindow.GetHeight() / 2 - (testSquareHeight/2)
            ),
            testSquareWidth, testSquareHeight,
            LNLEngine.Vector.Vec4(255,255,0,0)
        )
        
        LNLEngine.Renderer.SetClearColour(LNLEngine.Vector.Vec4(30,10,40))
    
    def OnUpdate(self):
        LNLEngine.Renderer.Clear()
        
        
        LNLEngine.Renderer.DrawTriangle([LNLEngine.Vector.Vec2(10,10),LNLEngine.Vector.Vec2(100,50) , LNLEngine.Vector.Vec2(200,400)], LNLEngine.Vector.Vec4(100, 200, 255, 255))
        LNLEngine.Renderer.DrawTriangle([LNLEngine.Vector.Vec2(200,10),LNLEngine.Vector.Vec2(100,800) , LNLEngine.Vector.Vec2(700,4)], LNLEngine.Vector.Vec4(100, 200, 80, 255))

        # print(LNLEngine.LLEngineTime.Time())
        self.TestSquare.Update()
        self.TestSquare.Draw()
        
        


class DoomExample(LNLEngine.Game):
    def __init__(self):
        super().__init__()
        
        props = LNLEngine.WindowProperties("DoomExample", 900, 600)
        self._window = LNLEngine.Window.CreateWindow(props)
        
        LNLEngine.Renderer.PushLayer(TestLayer())

    def _OnUpdate(self):
        return super()._OnUpdate()
    


if __name__ == "__main__":
    gameInst = LNLEngine.Game.CreateGame(DoomExample)
    gameInst.Run()