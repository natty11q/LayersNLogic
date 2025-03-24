import ApplicationEngine.AppEngine as LNLEngine

from ApplicationEngine.include.Maths.Maths import *
import Game.src.Level.LevelClass as Level
from Game.src.MainMenu.UI.ButtonClass import *



class MainMenuScene(LNLEngine.Scene):
    def __init__(self):
        super().__init__("MainMenu")

        self.gameWindow = LNLEngine.Game.Get().GetWindow()

        LNLEngine.Renderer.SetClearColour(LNLEngine.Vec4(0.15,0.1,0.2,1.0))


        self.ScreenShader = LNLEngine.ScreenShader()
        # self.ScreenShader2 = LNLEngine.ScreenShader()
        self.ParticleShader = LNLEngine.ScreenShader(FragmentShader="ApplicationEngine/src/Object/Shaders/ParticleShader.frag", FragmentShaderIsPath=True)

        # ========== sprite load : )==============
        # tex = LNLEngine.Texture("Game/Assets/Menu/theguyfull.png", True)
        # self.TestSprite = LNLEngine.Sprite(tex, Vec2(0, 0) , self.gameWindow.GetWidth(),  self.gameWindow.GetHeight())
        # ==============

        self.camera : LNLEngine.PesrpectiveCamera = LNLEngine.PesrpectiveCamera(self.gameWindow.GetWidth(),self.gameWindow.GetHeight())


        tex = LNLEngine.Texture("Game/Assets/Menu/quitbutton.png")
        self.QuitButton : Menu_Button = Menu_Button(
                                            tex.tex_width / 4,
                                            tex.tex_height / 5,

                                            Vec2(600,450),

                                            "Game/Assets/Menu/quitbutton.png",
                                            "Game/Assets/Menu/quitbuttonhover.png",
                                            "quit"
                                        )
        tex = LNLEngine.Texture("Game/Assets/Menu/startbutton.png")
        self.StartButton : Menu_Button = Menu_Button(
                                            tex.tex_width  / 4,
                                            tex.tex_height / 5,

                                            Vec2(550,335),

                                            "Game/Assets/Menu/startbutton.png",
                                            "Game/Assets/Menu/startbuttonhover.png"
                                        )


        self.StartButton.AddOnClickkHandler(LNLEngine.Game.Get().GetSceneManager().set_active_scene, ["mainScene"])


        self.ParalaxDistance : float = 10



        tex = LNLEngine.Texture("Game/Assets/Menu/clearMenuLayer.png", True)
        self.MenuClearLayer = LNLEngine.Sprite(tex, Vec2(0, 0) , self.gameWindow.GetWidth(),  self.gameWindow.GetHeight())
        tex = LNLEngine.Texture("Game/Assets/Menu/theGuyHD.png", True)
        self.basePos = Vec2(0, -self.ParalaxDistance)
        self.MenuTheGuyLayer = LNLEngine.Sprite(tex, self.basePos , self.gameWindow.GetWidth() + 2*self.ParalaxDistance ,  self.gameWindow.GetHeight() + 2*self.ParalaxDistance)

        LNLEngine.pygame.mixer.music.load("Game/Assets/Audio/MenuAudio.mp3")
        LNLEngine.pygame.mixer.music.play()






        self.AddObject(self.ScreenShader)
        self.AddObject(self.MenuTheGuyLayer)

        self.AddObject(self.QuitButton)
        self.AddObject(self.StartButton)

        self.AddObject(self.MenuClearLayer)




    def OnEvent(self , e : LNLEngine.Event): ...


    def _OnUpdate(self, dt):
        LNLEngine.Renderer.Clear()

        self.ParalaxVector = self.ParalaxDistance * Vec2( ((-self.gameWindow.GetWidth() / 2) + LNLEngine.Mouse.GetPos()[0]) / (self.gameWindow.GetWidth() / 2) ,
                                                          ((-self.gameWindow.GetHeight() / 2) + LNLEngine.Mouse.GetPos()[1] ) / (self.gameWindow.GetHeight() / 2) )
        self.MenuTheGuyLayer.SetPos(self.basePos - self.ParalaxVector)
