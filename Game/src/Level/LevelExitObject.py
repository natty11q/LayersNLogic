
import ApplicationEngine.AppEngine as LNLEngine

from ApplicationEngine.include.Maths.Maths import *
from Game.src.World.World import *

from Game.src.GameComponents.Player.PlayerClass import *
import math



class LevelExitObject(LNLEngine.GameObject2D):
    def __init__(self, position : Vec2, levelManager : LNLEngine.LevelManager, nextLevelName : str = ""):
        super().__init__(position, 0.0, 0.0)

        self.levelManager : LNLEngine.LevelManager
        self.nextLevelName : str = nextLevelName

        self.overlap = False


        tex = Texture("")
        self.drawOffset = -(1/2) * Vec2(tex.tex_width, tex.tex_height)
        self.sprite = Sprite(tex , position + self.drawOffset, tex.tex_width, tex.tex_height )


        c = self.InitCollider(tex.tex_width, tex.tex_height)
        self.body.setCollider(c)


    def InitCollider(self, w, h):
        c1 = LNLEngine.Box2D()
        c1.setSize(Vec2(20,WorldGrid.GRID_SIZE * 2))
    
        c1.setRigidBody(self.body)
        return c1


    def BeginPlay(self):
        return super().BeginPlay()


    def SetNextLevelName(self, nextLevel : str):
        self.nextLevelName = nextLevel


    def changeLevel(self):
        self.levelManager.setActiveLevel(self.nextLevelName)


    def _OnEvent(self, event: LNLEngine.Event):
        if self.overlap:
            if event.GetName() == "KeyDown":
                if event.keycode == LNLEngine.KEY_MAP["space"]:
                    self.changeLevel()
                    event._m_handled = True # no need to pass event further down to other handlers


    def OnCollision(self, body: LNLEngine.RigidBody2D, otherOwner: LNLEngine.GameObject2D, otherBody: LNLEngine.RigidBody2D, impulse: LNLEngine.Vec2, manifold: LNLEngine.CollisionManifold):
        self.overlap = False
        if isinstance(otherOwner, Player):
            self.overlap = True

        
    def _OnUpdate(self, deltatime: float):
        self.sprite.SetPos(self.body.getPosition() + self.drawOffset)

    def Draw(self):
        self.sprite.Draw()