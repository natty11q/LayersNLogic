import ApplicationEngine.AppEngine as LNLEngine
from ApplicationEngine.include.Maths.Maths import *

## ============================= App Code =================================
from Game.src.MainMenu.UI.ButtonClass import *
from Game.src.GameComponents.Entities.PlayerClass import *



from Game.src.Level.Levels import *


class MainScene(LNLEngine.Scene):
    def __init__(self):
        super().__init__("MainScene")
        self.player : Player | None = None
        self.Camera    = LNLEngine.OrthographicCamera(-1.0, 1.0, -1.0, 1.0)


    def _OnBegin(self):
        self.playerData = PlayerData()


        self.Camera    = LNLEngine.OrthographicCamera(-1.0, 1.0, -1.0, 1.0)
        HudCamera = LNLEngine.OrthographicCamera(-1.0, 1.0, -1.0, 1.0)

        self.SetMainCamera(self.Camera)
        self.SetHudCamera(HudCamera)

        self.player  = Player(Vec2(0,0), 70,  "player1")
        self.player.body.setCoefficientOfRestitution(0.15)

        self.AddObject(self.player)
        h = PlayerHud(self.player, self.playerData)
        self.AddUIElement(h)

        self.player.playerHud = h
        

        lm : LNLEngine.LevelManager = self.GetLevelManager()

        lm.addLevel(TutorialLevel("Tutorial-0" , self.player))        
        lm.addLevel(Level_0("Level-0", self.player))
        lm.addLevel(Level_1("Level-1", self.player))
        lm.addLevel(Level_2("Level-2", self.player))
        lm.addLevel(Level_3("Level-3", self.player))

        self.GetLevelManager().SetActiveLevel("Tutorial-0")

    def OnEvent(self, e: LNLEngine.Event):
        if e.GetType() == LNLEngine.LNL_EventType.KeyDown:

            if e.keycode == LNLEngine.KEY_MAP["R"]:
                lm = self.GetLevelManager()
                if lm:
                    if lm.activeLevel:
                        # reset the current level if the player still has lives 
                        lm.SetActiveLevel(lm.activeLevel.name)
                        self.playerData.lives -= 1


    def _OnUpdate(self, dt: float):

        LNLEngine.Renderer.Clear()

        # ignore the poor code, setup due to time constraints.
        if self.player:
            if self.player.isDead:
                if self.playerData.lives <= 0: 
                    sm = self.GetOwner()
                    if sm:
                        sm.SetActiveScene("MainMenu")
                        # reset to the main menu if there are no player lives left
                else:
                    lm = self.GetLevelManager()
                    if lm:
                        if lm.activeLevel:
                            # reset the current level if the player still has lives 
                            lm.SetActiveLevel(lm.activeLevel.name)
                            self.playerData.lives -= 1
                            self.player.isDead = False
                            self.player.CurrentHealth = self.player.MaxHealth
                


        
            # self.Camera.SetPosition(self.Camera.GetPosition())
            self.Camera.SetPosition(Vec3( (self.player.body.getPosition().x / 640) -0.5, (-self.player.body.getPosition().y / 640) + 0.8, 0))

        self.Draw()
        self.DrawUI()