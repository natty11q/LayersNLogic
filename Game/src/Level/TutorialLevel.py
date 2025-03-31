
import ApplicationEngine.AppEngine as LNLEngine

from ApplicationEngine.include.Maths.Maths import *
from Game.src.World.World import *

from Game.src.GameComponents.Player.PlayerClass import *
import math


class TutorialLevel(LNLEngine.Level):
    def __init__(self,name):
        super().__init__(name)

        screenShader = LNLEngine.ScreenShader(FragmentShader= "ApplicationEngine/src/Object/Shaders/cloudShader.frag", FragmentShaderIsPath=True)

        portal1 = Portal(Vec2(800, 400),math.pi/2)
        portal2 = Portal(Vec2(100, 400),math.pi/2)

        portal1.LinkPortal(portal2)
    

        self.tiles : list [GameObject] = []

        tex0 = Texture("Game/Assets/Sprites/environ/grassfull.png", True)
        tex1 = Texture("Game/Assets/Sprites/environ/rocksfull.png", True)
        
        chunk0 = TileChunk(Vec2(-1,8),Vec2(50, 2), tex0, tex1)
        self.tiles.append(chunk0)

        self.AddLevelComponent(screenShader,"background")
        
        self.AddLevelComponent(portal1)
        self.AddLevelComponent(portal2)

        for tile in self.tiles:
            self.AddLevelComponent(tile, "terrain")

    
    def OnUpdate(self, deltatime):
        ...