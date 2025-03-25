from ApplicationEngine.src.Physics.RigidBody.RigidBody2D import *
from ApplicationEngine.src.Physics.Primatives._2D.Line2D import Line2D
from ApplicationEngine.src.Physics.Primatives._2D.Circle import Circle
from ApplicationEngine.src.Physics.Primatives._2D.AABB import AABB
from ApplicationEngine.src.Physics.Primatives._2D.Box2D import Box2D
from ApplicationEngine.src.Physics.Primatives._2D.Ray2D import Ray2D
from ApplicationEngine.src.Physics.Primatives._2D.RaycastResult2D import RaycastResult2D



class CollisionManifold:
    @overload
    def __init__(self): ...
    
    @overload
    def __init__(self, normal : Vec2 = Vec2(), depth : float = 0.0): ...


    def __init__(self, normal : Vec2 | None = None, depth : float = 0.0) -> None:
        if normal:
            self.normal : Vec2 = normal
            self._isColliding = True
        else:
            self.normal : Vec2 = Vec2()
            self._isColliding = False
        
        self.contactPoints : list[Vec2] = []
        self.depth : float = depth

    
    def addContactPoint(self, contact : Vec2):
        self.contactPoints.append(contact)

    def getNormal(self) -> Vec2:
        return self.normal
    
    def getContactPoints(self) -> list[Vec2]:
        return self.contactPoints

    def getDepth(self) -> float:
        return self.depth
    

    def isColliding(self) -> bool:
        return self._isColliding