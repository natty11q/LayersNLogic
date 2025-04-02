
import ApplicationEngine.AppEngine as LNLEngine

from ApplicationEngine.include.Maths.Maths import *
from Game.src.World.World import *

from Game.src.Level.LevelExitObject import *
from Game.src.GameComponents.Player.PlayerClass import *
import math


class TutorialLevel(LNLEngine.Level):
    def __init__(self,name , player : Player | None = None):
        super().__init__(name)

        self.player = player

    def BeginPlay(self):
        Background = LNLEngine.ScreenShader(FragmentShader= "ApplicationEngine/src/Object/Shaders/cloudShader.frag", FragmentShaderIsPath=True)
        
        portal1 = Portal(Vec2(500, 400),math.pi/2)
        portal2 = Portal(Vec2(150, 400),math.pi/2)

        portal1.LinkPortal(portal2)
    

        tiles : list [GameObject] = []

        tex0 = Texture("Game/Assets/Sprites/environ/grassfull.png")
        tex1 = Texture("Game/Assets/Sprites/environ/rocksfull.png")
        
        chunk0 = TileChunk(Vec2(-10,8),  Vec2(40, 2),    tex0, tex1)
        chunk1 = TileChunk(Vec2(-1,3),  Vec2(2, 6),     tex0, tex1)
        chunk2 = TileChunk(Vec2(5,3),   Vec2(2, 6),     tex0, tex1)
        chunk3 = TileChunk(Vec2(10,5),  Vec2(2, 5),     tex0, tex1)

        tiles.append(chunk0)
        # tiles.append(chunk1)
        # tiles.append(chunk2)
        # tiles.append(chunk3)

        endComponent = LevelExitObject(Vec2(17 * WorldGrid.GRID_SIZE,6 * WorldGrid.GRID_SIZE), self.getOwner(), "Level-0")

        self.AddLevelComponent(Background,"background")
        
        # self.AddLevelComponent(portal1)
        # self.AddLevelComponent(portal2)
        self.AddLevelComponent(endComponent, "ending")

        for tile in tiles:
            self.AddLevelComponent(tile, "terrain")
        
        
        
        
        super().BeginPlay()
        
        endComponent.SetLevelManager(self.getOwner())
        if self.player:
            self.player.SetPosition(Vec2(0,-1000))
            LNL_LogFatal("ResetPos")
    
    def OnUpdate(self, deltatime):
        ...