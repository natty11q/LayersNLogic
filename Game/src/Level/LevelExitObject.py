
import ApplicationEngine.AppEngine as LNLEngine

from ApplicationEngine.include.Maths.Maths import *
from Game.src.World.World import *

from Game.src.GameComponents.Player.PlayerClass import *
import math



class LevelExitObject(LNLEngine.GameObject2D):
    def __init__(self, position : Vec2, levelManager : LNLEngine.LevelManagerBase | None, nextLevelName : str = ""):
        super().__init__(position, 0.0, 0.0)

        self.levelManager : LNLEngine.LevelManagerBase  | None = levelManager
        self.nextLevelName : str = nextLevelName

        self.overlap = False


        tex = Texture("Game/Assets/Sprites/LevelEndPortal.png", True)
        self.drawOffset = -(1/2) * Vec2(tex.tex_width, tex.tex_height)
        self.sprite = Sprite(tex , position + self.drawOffset, tex.tex_width, tex.tex_height  * 3)


        c = self.InitCollider(tex.tex_width, tex.tex_height)
        self.body.setCollider(c)


    def InitCollider(self, w, h):
        c1 = LNLEngine.Box2D()
        c1.setSize(Vec2(w, h))
    
        c1.setRigidBody(self.body)
        return c1


    def BeginPlay(self):
        self.body.isActor = False
        LNLEngine.PhysicsSystem2D.Get().addRigidbody(self.body, False)


    def SetNextLevelName(self, nextLevel : str):
        self.nextLevelName = nextLevel


    def SetLevelManager(self, levelManager : LNLEngine.LevelManagerBase | None):
        self.levelManager = levelManager

    def changeLevel(self):
        if self.levelManager:
            self.levelManager.SetActiveLevel(self.nextLevelName)


    def _OnEvent(self, event: LNLEngine.Event):
        if self.overlap:
            if event.GetName() == "KeyDown":
                if event.keycode == LNLEngine.KEY_MAP["up"]:
                    self.changeLevel()
                    # event._m_handled = True # no need to pass event further down to other handlers


    def OnContact(self, body, otherOwner, otherBody):
        self.overlap = False
        if isinstance(otherOwner, Player):
            self.overlap = True

        
    def _OnUpdate(self, deltatime: float):
        self.sprite.SetPos(self.body.getPosition() + self.drawOffset)

    def Draw(self):
        self.sprite.Draw()