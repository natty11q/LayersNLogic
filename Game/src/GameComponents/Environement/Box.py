from Game.src.GameComponents.Environement.EnvironmentObject import * 


class Box(EnvironmentObject2D):
    boxTexture = LNLEngine.Texture("",False)
    def __init__(self,mass : float ,dimensions : Vec2 = Vec2(1,1)):
        super().__init__(mass = mass) 
        self.dimensions = dimensions * WorldGrid.GRID_SIZE  
        self.sprite = LNLEngine.Sprite(Box.boxTexture, self.body.position - self.dimensions/2, self.dimensions.x, self.dimensions.y)
        
        self.colliders : list[LNLEngine.Collider2D] = [] 
        col1 = self._InitCollider(self.dimensions) 

        self.body.setCollider(col1) 
        self.colliders.append(col1)


 


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
