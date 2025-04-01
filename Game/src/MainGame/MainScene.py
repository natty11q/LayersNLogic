import ApplicationEngine.AppEngine as LNLEngine
from ApplicationEngine.include.Maths.Maths import *

## ============================= App Code =================================
from Game.src.MainMenu.UI.ButtonClass import *
from Game.src.GameComponents.Player.PlayerClass import *



from Game.src.Level.Levels import *


class MainScene(LNLEngine.Scene):
    def __init__(self):
        super().__init__("MainScene")

        Camera    = LNLEngine.OrthographicCamera(-5.0, 5.0, -5.0, 5.0)
        HudCamera = LNLEngine.OrthographicCamera(-5.0, 5.0, -5.0, 5.0)

        self.SetMainCamera(Camera)
        self.SetHudCamera(HudCamera)

        self.player  = Player(Vec2(0,0), 70,  "player1")
        self.player.body.setCoefficientOfRestitution(0.15)

        self.AddObject(self.player)
        self.AddUIElement(PlayerHud(self.player))
        

        lm : LNLEngine.LevelManager = self.GetLevelManager()

        lm.addLevel(TutorialLevel("Tutorial-0"))        
        lm.addLevel(Level_0("Level-0"))
        lm.addLevel(Level_1("Level-1"))
        lm.addLevel(Level_2("Level-2"))
        lm.addLevel(Level_3("Level-3"))

    def _OnBegin(self):
        self.GetLevelManager().SetActiveLevel("Tutorial-0")

    def _OnUpdate(self, dt: float):

        LNLEngine.Renderer.Clear()

        self.Draw()
        self.DrawUI()