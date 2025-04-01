
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


        Background = LNLEngine.ScreenShader(FragmentShader= "ApplicationEngine/src/Object/Shaders/cloudShader.frag", FragmentShaderIsPath=True)
        
        portal1 = Portal(Vec2(500, 400),math.pi/2)
        portal2 = Portal(Vec2(150, 400),math.pi/2)

        portal1.LinkPortal(portal2)
    

        self.tiles : list [GameObject] = []

        tex0 = Texture("Game/Assets/Sprites/environ/grassfull.png")
        tex1 = Texture("Game/Assets/Sprites/environ/rocksfull.png")
        
        chunk0 = TileChunk(Vec2(-1,8),  Vec2(25, 2),    tex0, tex1)
        chunk1 = TileChunk(Vec2(-1,3),  Vec2(2, 6),     tex0, tex1)
        chunk2 = TileChunk(Vec2(5,3),   Vec2(2, 6),     tex0, tex1)
        chunk3 = TileChunk(Vec2(10,5),  Vec2(2, 5),     tex0, tex1)

        self.tiles.append(chunk0)
        self.tiles.append(chunk1)
        self.tiles.append(chunk2)
        self.tiles.append(chunk3)

        self.endComponent = LevelExitObject(Vec2(13 * WorldGrid.GRID_SIZE,6 * WorldGrid.GRID_SIZE), self.getOwner(), "Level-0")

        self.AddLevelComponent(Background,"background")
        
        self.AddLevelComponent(portal1)
        self.AddLevelComponent(portal2)
        self.AddLevelComponent(self.endComponent, "ending")

        for tile in self.tiles:
            self.AddLevelComponent(tile, "terrain")

    def BeginPlay(self):
        super().BeginPlay()
        self.endComponent.SetLevelManager(self.getOwner())
        if self.player:
            self.player.SetPosition(Vec2(0,0))
            LNL_LogFatal("ResetPos")
    
    def OnUpdate(self, deltatime):
        ...