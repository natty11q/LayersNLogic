
from ApplicationEngine.include.Maths.Maths import *
import ApplicationEngine.AppEngine as LNLEngine
## ============================= App Code =================================

from Game.src.World.WorldGrid import *

class Tile(LNLEngine.GameObject2D):
    def __init__(self, 
                    texture : LNLEngine.Texture,
                    gridPosition : Vec2,
                    mass : float = 0.0,
                    size : Vec2 = Vec2(1,1)):
        
        super().__init__( ( gridPosition + (size / 2) ) * WorldGrid.GRID_SIZE, mass)


        self.size = size * WorldGrid.GRID_SIZE
        self.sprite = LNLEngine.Sprite(texture, gridPosition * WorldGrid.GRID_SIZE  - Vec2(WorldGrid.GRID_SIZE/2, WorldGrid.GRID_SIZE/2), self.size.x, self.size.y)


        self.colliders : list[LNLEngine.Collider2D] = []

        c1 = self._InitCollider(self.size)


        self.body.setCollider(c1)
        self.colliders.append(c1)
    
    def BeginPlay(self):
        LNLEngine.Game.Get().GetPhysicsSystem2D().addRigidbody(self.body, (not self.body.mass == 0.0))


    def Draw(self):
        self.sprite.SetPos(self.body.getCollider().getLocalMin()) #type: ignore
        self.sprite.Draw()
    

    def _InitCollider(self, size : Vec2) -> LNLEngine.Collider2D:
        """seperate colider init for modification in inherited classes

        Args:
            size (Vec2): width and height [use teh first index as radius if dealing with a sphere]

        Returns:
            LNLEngine.Collider2D: collision shape
        """
        # c1 = LNLEngine.Box2D()
        c1 = LNLEngine.AABB()
        c1.setRigidBody(self.body)
        c1.setSize(size)

        return c1

class TileChunk(LNLEngine.GameObject2D):
    # TODO: modify to sue the topleft grid as the position instead of the centre 
    def __init__(self, 
                    gridPosition : Vec2,
                    gridSize : Vec2 = Vec2(1,1),
                    topTexture : LNLEngine.Texture = LNLEngine.Texture("debug"),
                    bodyTexture : LNLEngine.Texture | None = None,
                    mass : float = 0.0):
        
        centrePos = (gridPosition + (gridSize / 2)) * WorldGrid.GRID_SIZE
        
        super().__init__(centrePos, mass)

        self.size = gridSize

        self.topSprite : LNLEngine.Sprite = LNLEngine.Sprite(topTexture,
                                          gridPosition * WorldGrid.GRID_SIZE,
                                          WorldGrid.GRID_SIZE, WorldGrid.GRID_SIZE
                                          )
        
        self.bodySprite : LNLEngine.Sprite = self.topSprite

        if bodyTexture:
            self.bodySprite : LNLEngine.Sprite = LNLEngine.Sprite(bodyTexture,
                                          gridPosition * WorldGrid.GRID_SIZE,
                                          WorldGrid.GRID_SIZE, WorldGrid.GRID_SIZE
                                          )
            
        c1 = self._InitCollider(gridSize * WorldGrid.GRID_SIZE)

        self.colliders : list[LNLEngine.Collider2D] = []
        
        self.body.setCollider(c1)
        self.colliders.append(c1)


    def BeginPlay(self):
        LNLEngine.Game.Get().GetPhysicsSystem2D().addRigidbody(self.body, False)


    def _InitCollider(self, size : Vec2) -> LNLEngine.Collider2D:
        """seperate colider init for modification in inherited classes

        Args:
            size (Vec2): width and height [use teh first index as radius if dealing with a sphere]

        Returns:
            LNLEngine.Collider2D: collision shape
        """


        c1 = LNLEngine.Box2D()
        # c1 = LNLEngine.AABB()
        c1.setRigidBody(self.body)
        c1.setSize(size)

        return c1
    

    def Draw(self):
        for x in range(int(self.size.x)):
            for y in range(int(self.size.y)):
                # TODO: cange the shader uniform setup to run in the update so that i can just change the pos 
                self.topSprite.SetPos(
                    self.body.getCollider().getLocalMin() + Vec2(x * WorldGrid.GRID_SIZE, y * WorldGrid.GRID_SIZE) ) #type: ignore
                self.bodySprite.SetPos(
                    self.body.getCollider().getLocalMin() + Vec2(x * WorldGrid.GRID_SIZE, y * WorldGrid.GRID_SIZE) ) #type: ignore
                if y == 0:
                    self.topSprite.Draw()
                else:
                    self.bodySprite.Draw()
         
        # self.topSprite.SetWidth(self.size.x * WorldGrid.GRID_SIZE)
        # self.topSprite.SetHeight(self.size.y * WorldGrid.GRID_SIZE)

        # self.topSprite.Draw()
