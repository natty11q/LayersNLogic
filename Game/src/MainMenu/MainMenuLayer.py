import ApplicationEngine.AppEngine as LNLEngine

from ApplicationEngine.include.Maths.Maths import *
import Game.src.Level.LevelClass as Level




class Button(LNLEngine.GameObject):
    def __init__(self, width : float, height : float, position : Vec2, name = ""):
        super().__init__()

        self.selected = False

        self.Position   : Vec2 = position
        self.width  : float = width 
        self.height : float = height 

        tex = LNLEngine.Texture("Game/Assets/Menu/quitbuttonhover.png")
        self.ButtonSprite = LNLEngine.Sprite(tex, self.Position , self.width ,  self.height)

    # def ApplyHover(self):
    #     LNL_LogEngineInfo("Button Hovered")
    #     ...

    # # def _OnEvent(self, event: LNLEngine.Event):
    # #     if event.GetName() == "MaouseClick":
    # #         ...
    # def Overlaps(mPos : Vec2):
    #     # ...... 
    #     return True


    def _OnUpdate(self, deltatime: float):
        
        # mpos = LNLEngine.Mouse.GetPos()
        # if self.Overlaps(mpos):


        # if self.selected:
        #     self.ApplyHover()\

        self.Position = Vec2(
            self.Position.x,
            self.Position.y + (5 * math.sin( LNLEngine.LLEngineTime.Time() ))
        )

    def Draw(self):

        self.ButtonSprite.SetPos(self.Position)
        self.ButtonSprite.Draw()
        

class MenuLayer(LNLEngine.Layer):
    def __init__(self, name="TestLayer"):
        super().__init__(name)

        self.gameWindow = LNLEngine.Game.Get().GetWindow()

        LNLEngine.Renderer.SetClearColour(LNLEngine.Vec4(0.15,0.1,0.2,1.0))


        self.ScreenShader = LNLEngine.ScreenShader()

        # ========== sprite load : )==============
        tex = LNLEngine.Texture("Game/Assets/Menu/theguyfull.png")
        self.TestSprite = LNLEngine.Sprite(tex, Vec2(0, 0) , self.gameWindow.GetWidth(),  self.gameWindow.GetHeight())
        # ==============

        self.camera : LNLEngine.PesrpectiveCamera = LNLEngine.PesrpectiveCamera(self.gameWindow.GetWidth(),self.gameWindow.GetHeight())


        self.Quit : Button = Button(tex.tex_width / 20, tex.tex_height / 25, Vec2(400, 300))

        # self.Buttons = {
        #     "Start" : Button(),
        #     "Quit"  : Button()
        # }

    def OnUpdate(self, deltatime: float):
        LNLEngine.Renderer.Clear()

        LNLEngine.Renderer.BeginScene(self.camera)

        self.Quit.Update(deltatime)


        # self.TestSprite.Draw()
        self.Quit.Draw()
        # for button in self.Buttons.values():
        #     button.Draw()


        LNLEngine.Renderer.EndScene()
