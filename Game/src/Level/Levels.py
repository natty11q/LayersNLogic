
import ApplicationEngine.AppEngine as LNLEngine

from ApplicationEngine.include.Maths.Maths import *
from Game.src.World.World import *

from Game.src.Level.LevelExitObject import *
from Game.src.GameComponents.Player.PlayerClass import *
import math



from Game.src.Level.TutorialLevel import *

class LNLLevel(LNLEngine.Level):
    def __init__(self,name , player : Player | None = None):
        super().__init__(name)

        self.player = player
        self.playerSpawnPos = Vec2(0,0)

        tex0 = Texture("Game/Assets/Sprites/environ/grassfull.png")
        tex1 = Texture("Game/Assets/Sprites/environ/rocksfull.png")
        
        chunk0 = TileChunk(Vec2(-10,8),  Vec2(40, 2),    tex0, tex1)


        self.endComponent = LevelExitObject(Vec2(17 * WorldGrid.GRID_SIZE,6 * WorldGrid.GRID_SIZE), self.getOwner(), "Level-0")        
        # self.AddLevelComponent(portal1)
        # self.AddLevelComponent(portal2)
        self.AddLevelComponent(self.endComponent, "ending")
        self.AddLevelComponent(chunk0)

    def BeginPlay(self):
        super().BeginPlay()
        if self.player:
            self.player.SetPosition(self.playerSpawnPos)
            LNL_LogFatal("ResetPos 1")

class Level_0(LNLLevel):
    def __init__(self,name, player : Player | None = None):
        super().__init__(name, player)


class Level_1(LNLLevel):
    def __init__(self,name, player : Player | None = None):
        super().__init__(name, player)





class Level_2(LNLLevel):
    def __init__(self,name, player : Player | None = None):
        super().__init__(name, player)



class Level_3(LNLLevel):
    def __init__(self,name, player : Player | None = None):
        super().__init__(name, player)



class Level_4(LNLLevel):
    def __init__(self,name, player : Player | None = None):
        super().__init__(name, player)
