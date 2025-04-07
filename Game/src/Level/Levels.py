
import ApplicationEngine.AppEngine as LNLEngine

from ApplicationEngine.include.Maths.Maths import *
from Game.src.World.World import *

from Game.src.Level.LevelExitObject import *
from Game.src.GameComponents.Entities.PlayerClass import *
from Game.src.GameComponents.Entities.EnemyClass import *
import math



from Game.src.Level.TutorialLevel import *
from Game.src.GameComponents.Environement.Environment import *

class LNLLevel(LNLEngine.Level):
    def __init__(self,name , player : Player | None = None):
        super().__init__(name)

        self.player = player
        self.playerSpawnPos = Vec2(0,0)


    def BeginPlay(self):
        super().BeginPlay()
        if self.player:
            self.player.SetPosition(self.playerSpawnPos)
            LNL_LogFatal("ResetPos 1")

class Level_0(LNLLevel):
    def __init__(self,name, player : Player | None = None):
        super().__init__(name, player)


    def BeginPlay(self):
        Background = LNLEngine.ScreenShader(FragmentShader= "ApplicationEngine/src/Object/Shaders/cloudShader.frag", FragmentShaderIsPath=True)
        
        portal1 = Portal(Vec2(500, 400),math.pi/2)
        portal2 = Portal(Vec2(256, 400),math.pi/2)

        portal1.LinkPortal(portal2)
    

        tiles : list [GameObject] = []

        tex0 = Texture("Game/Assets/Sprites/environ/grassfull.png")
        tex1 = Texture("Game/Assets/Sprites/environ/rocksfull.png")
        
        chunk0 = TileChunk(Vec2(-10,8),  Vec2(40, 2),    tex0, tex1)
        chunk1 = TileChunk(Vec2(-1,3),  Vec2(2, 6),     tex0, tex1)
        chunk2 = TileChunk(Vec2(5,3),   Vec2(2, 6),     tex0, tex1)
        chunk3 = TileChunk(Vec2(10,5),  Vec2(2, 5),     tex0, tex1)

        tiles.append(chunk0)
        tiles.append(chunk1)
        tiles.append(chunk2)
        tiles.append(chunk3)

        endComponent = LevelExitObject(Vec2(17 * WorldGrid.GRID_SIZE,5.5 * WorldGrid.GRID_SIZE), self.getOwner(), "Level-1")

        self.AddLevelComponent(Background,"background")
        

        for tile in tiles:
            self.AddLevelComponent(tile, "terrain")

        self.AddLevelComponent(portal1)
        self.AddLevelComponent(portal2)
        
        if self.player:
            endComponent.SetHud(self.player.GetHud())
        self.AddLevelComponent(endComponent, "ending")




        super().BeginPlay()
        endComponent.SetLevelManager(self.getOwner())
        if self.player:
            endComponent.SetHud(self.player.GetHud())



class Level_1(LNLLevel):
    def __init__(self,name, player : Player | None = None):
        super().__init__(name, player)

    def BeginPlay(self):
        Background = LNLEngine.ScreenShader(FragmentShader= "ApplicationEngine/src/Object/Shaders/OceanScene.frag", FragmentShaderIsPath=True)
        
        # portal1 = Portal(Vec2(500, 400),math.pi/2)
        # portal2 = Portal(Vec2(256, 400),math.pi/2)

        # portal1.LinkPortal(portal2)
    

        tiles : list [GameObject] = []

        tex0 = Texture("Game/Assets/Sprites/environ/grassfull.png")
        tex1 = Texture("Game/Assets/Sprites/environ/rocksfull.png")
        
        chunk0 = TileChunk(Vec2(-10,8),  Vec2(40, 2),    tex0, tex1)
        # chunk1 = TileChunk(Vec2(-1,3),  Vec2(2, 6),     tex0, tex1)
        chunk2 = TileChunk(Vec2(5,3),   Vec2(5, 6),     tex0, tex1)
        # chunk3 = TileChunk(Vec2(10,5),  Vec2(2, 5),     tex0, tex1)

        tiles.append(chunk0)
        # tiles.append(chunk1)
        tiles.append(chunk2)
        # tiles.append(chunk3)

        endComponent = LevelExitObject(Vec2(17 * WorldGrid.GRID_SIZE,5.5 * WorldGrid.GRID_SIZE), self.getOwner(), "Level-2")


        box = LNLBox(100, Vec2(2,2))
        box.SetAttribure(CanTravelThroughPortals)

        box.body.setCoefficientOfRestitution(0.2)
        self.AddLevelComponent(Background,"background")
        

        for tile in tiles:
            self.AddLevelComponent(tile, "terrain")

        # self.AddLevelComponent(portal1)
        # self.AddLevelComponent(portal2)
        if self.player:
            endComponent.SetHud(self.player.GetHud())
        self.AddLevelComponent(endComponent, "ending")
        self.AddLevelComponent(box)




        super().BeginPlay()
        endComponent.SetLevelManager(self.getOwner())




class Level_2(LNLLevel):
    def __init__(self,name, player : Player | None = None):
        super().__init__(name, player)

    def BeginPlay(self):
        Background = LNLEngine.ScreenShader(FragmentShader= "ApplicationEngine/src/Object/Shaders/cloudShader.frag", FragmentShaderIsPath=True)
        
        portal1 = Portal(Vec2(500, 400))
        portal2 = Portal(Vec2(256, 400))

        portal1.LinkPortal(portal2)
    

        tiles : list [GameObject] = []

        tex0 = Texture("Game/Assets/Sprites/environ/grassfull.png")
        tex1 = Texture("Game/Assets/Sprites/environ/rocksfull.png")
        
        chunk0 = TileChunk(Vec2(-10,8),  Vec2(40, 2),    tex0, tex1)
        # chunk1 = TileChunk(Vec2(-1,3),  Vec2(2, 6),     tex0, tex1)
        # chunk2 = TileChunk(Vec2(5,3),   Vec2(5, 6),     tex0, tex1)
        # chunk3 = TileChunk(Vec2(10,5),  Vec2(2, 5),     tex0, tex1)

        tiles.append(chunk0)
        # tiles.append(chunk1)
        # tiles.append(chunk2)
        # tiles.append(chunk3)

        endComponent = LevelExitObject(Vec2(17 * WorldGrid.GRID_SIZE,5.5 * WorldGrid.GRID_SIZE), self.getOwner(), "Level-1")


        box = LNLBox(100, Vec2(2,2))
        box.SetAttribure(CanTravelThroughPortals)
        
        box.body.setCoefficientOfRestitution(0.2)



        enemy = Tier1Enemy(Vec2(WorldGrid.GRID_SIZE, WorldGrid.GRID_SIZE), Vec2(300, 0))


        self.AddLevelComponent(Background,"background")

        

        for tile in tiles:
            self.AddLevelComponent(tile, "terrain")

        self.AddLevelComponent(portal1)
        self.AddLevelComponent(portal2)

        if self.player:
            endComponent.SetHud(self.player.GetHud())
        self.AddLevelComponent(endComponent, "ending")
        self.AddLevelComponent(box)

        self.AddLevelComponent(enemy)



        super().BeginPlay()
        endComponent.SetLevelManager(self.getOwner())


class Level_3(LNLLevel):
    def __init__(self,name, player : Player | None = None):
        super().__init__(name, player)



class Level_4(LNLLevel):
    def __init__(self,name, player : Player | None = None):
        super().__init__(name, player)
