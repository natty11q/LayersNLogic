import ApplicationEngine.AppEngine as LNLEngine

from ApplicationEngine.include.Maths.Maths import *
import Game.src.Level.LevelClass as Level
from Game.src.MainMenu.UI.ButtonClass import *




# class Button(LNLEngine.GameObject):
#     def __init__(self, width : float, height : float, position : Vec2, name = ""):
#         super().__init__()

#         self.selected = False

#         self.BasePosition   : Vec2 = position
#         self.Position   : Vec2 = position
#         self.width  : float = width 
#         self.height : float = height
#         self.name : str = name



#         tex = LNLEngine.Texture("Game/Assets/Menu/quitbuttonhover.png")
#         self.ButtonSprite = LNLEngine.Sprite(tex, self.Position , self.width ,  self.height)


#     def OnButtonPressed(self): ...
        
    
    
#     # def ApplyHover(self):
#     #     LNL_LogEngineInfo("Button Hovered")
#     #     ...

#     # # def _OnEvent(self, event: LNLEngine.Event):
#     # #     if event.GetName() == "MaouseClick":
#     # #         ...
#     def Overlaps(self, mPos : Vec2) -> bool:
#         """check if position given overlaps with the button """


#         LNL_LogEngineInfo(f"button {self.name}, id: {self.id}, pressed")

#         return True


#     def _OnUpdate(self, deltatime: float):
        
#         # mpos = LNLEngine.Mouse.GetPos()
#         # if self.Overlaps(mpos):


#         # if self.selected:
#         #     self.ApplyHover()\

#         self.Position = Vec2(
#             self.BasePosition.x,
#             self.BasePosition.y + (50 * math.sin( LNLEngine.LLEngineTime.Time() ))
#         )
#         self.ButtonSprite.SetPos(self.Position)

#     def Draw(self):

#         self.ButtonSprite.Draw()
        

class MenuLayer(LNLEngine.Layer):
    def __init__(self, name="TestLayer"):
        super().__init__(name)

        self.gameWindow = LNLEngine.Game.Get().GetWindow()

        LNLEngine.Renderer.SetClearColour(LNLEngine.Vec4(0.15,0.1,0.2,1.0))


        self.ScreenShader = LNLEngine.ScreenShader()
        # self.ScreenShader2 = LNLEngine.ScreenShader()
        self.ParticleShader = LNLEngine.ScreenShader(FragmentShader="ApplicationEngine/src/Object/Shaders/ParticleShader.frag", FragmentShaderIsPath=True)

        # ========== sprite load : )==============
        tex = LNLEngine.Texture("Game/Assets/Menu/theguyfull.png")
        self.TestSprite = LNLEngine.Sprite(tex, Vec2(0, 0) , self.gameWindow.GetWidth(),  self.gameWindow.GetHeight())
        # ==============

        self.camera : LNLEngine.PesrpectiveCamera = LNLEngine.PesrpectiveCamera(self.gameWindow.GetWidth(),self.gameWindow.GetHeight())


        self.QuitButton : Menu_Button = Menu_Button(
                                            tex.tex_width  / 20,
                                            tex.tex_height / 25,

                                            Vec2(600,450),

                                            "Game/Assets/Menu/quitbutton.png",
                                            "Game/Assets/Menu/quitbuttonhover.png",
                                            "quit"
                                        )
        self.StartButton : Menu_Button = Menu_Button(
                                            tex.tex_width  / 20,
                                            tex.tex_height / 25,

                                            Vec2(550,335),

                                            "Game/Assets/Menu/startbutton.png",
                                            "Game/Assets/Menu/startbuttonhover.png"
                                        )


        self.StartButton.AddOnClickkHandler(print, ["start Button Pressed"])


        self.ParalaxDistance : float = 10



        tex = LNLEngine.Texture("Game/Assets/Menu/clearMenuLayer.png")
        self.MenuClearLayer = LNLEngine.Sprite(tex, Vec2(0, 0) , self.gameWindow.GetWidth(),  self.gameWindow.GetHeight())
        tex = LNLEngine.Texture("Game/Assets/Menu/theGuyHD.png")
        self.basePos = Vec2(0, -self.ParalaxDistance)
        self.MenuTheGuyLayer = LNLEngine.Sprite(tex, self.basePos , self.gameWindow.GetWidth() + 2*self.ParalaxDistance ,  self.gameWindow.GetHeight() + 2*self.ParalaxDistance)

        LNLEngine.pygame.mixer.music.load("Game/Assets/Audio/MenuAudio.mp3")
        LNLEngine.pygame.mixer.music.play()

    def OnUpdate(self, deltatime: float):
        LNLEngine.Renderer.Clear()

        LNLEngine.Renderer.BeginScene(self.camera)

        self.QuitButton.Update(deltatime)
        self.StartButton.Update(deltatime)

        self.ScreenShader.Draw()

        LNLEngine.RenderCommand.Enable(LNLEngine.GL_BLEND)
        LNLEngine.Renderer.CustomRendererCommand(LNLEngine.glBlendFunc, [LNLEngine.GL_SRC_ALPHA, LNLEngine.GL_ONE_MINUS_SRC_ALPHA])
        LNLEngine.Renderer.CustomRendererCommand(LNLEngine.glDepthMask, [LNLEngine.GL_FALSE])

        self.MenuTheGuyLayer.Draw()

        LNLEngine.Renderer.CustomRendererCommand(LNLEngine.glDepthMask, [LNLEngine.GL_TRUE])
        LNLEngine.RenderCommand.Disable(LNLEngine.GL_BLEND)



        self.ParalaxVector = self.ParalaxDistance * Vec2( ((-self.gameWindow.GetWidth() / 2) + LNLEngine.Mouse.GetPos()[0]) / (self.gameWindow.GetWidth() / 2) ,
                                                          ((-self.gameWindow.GetHeight() / 2) + LNLEngine.Mouse.GetPos()[1] ) / (self.gameWindow.GetHeight() / 2) )


        self.MenuTheGuyLayer.SetPos(self.basePos - self.ParalaxVector)





        # self.TestSprite.Draw()
        self.QuitButton.Draw()
        self.StartButton.Draw()
        # for button in self.Buttons.values():
        #     button.Draw()


        LNLEngine.RenderCommand.Enable(LNLEngine.GL_BLEND)
        LNLEngine.Renderer.CustomRendererCommand(LNLEngine.glBlendFunc, [LNLEngine.GL_SRC_ALPHA, LNLEngine.GL_ONE_MINUS_SRC_ALPHA])
        LNLEngine.Renderer.CustomRendererCommand(LNLEngine.glDepthMask, [LNLEngine.GL_FALSE])

        self.MenuClearLayer.Draw()

        LNLEngine.Renderer.CustomRendererCommand(LNLEngine.glDepthMask, [LNLEngine.GL_TRUE])
        LNLEngine.RenderCommand.Disable(LNLEngine.GL_BLEND)
        

        # self.ScreenShader2.Draw()
        # self.ParticleShader.Draw()
        
        LNLEngine.Renderer.EndScene()
