from ApplicationEngine.src.Physics.RigidBody.CollisionManifold import *
from ApplicationEngine.src.Physics.Primatives._2D.Collider2D import *


class Collisions:


    @staticmethod
    def findCollisionFeatures_CircleAndCircle(a : Circle, b : Circle) -> CollisionManifold:
        result : CollisionManifold = CollisionManifold()

        sumRadii : float = a.getRadius() + b.getRadius()
        distance : Vec2 = b.getCentre() - a.getCentre()

        if (distance.length_squared() - (sumRadii ** 2) > 0):
            return result
        

        depth : float = abs(distance.length() - sumRadii) * 0.5
        normal : Vec2 = Vec2(*distance.get_p()).normalize()

        distanceToPoint = a.getRadius() - depth

        contactPoint : Vec2 = a.getCentre() + (normal * distanceToPoint)

        result = CollisionManifold(normal , depth)
        result.addContactPoint(contactPoint)

        return result



    @staticmethod
    def findCollisionFeatures(a : Collider2D, b : Collider2D) -> CollisionManifold:
        
        if isinstance(a ,Circle) and isinstance(b, Circle):
            return Collisions.findCollisionFeatures_CircleAndCircle(a , b)
        
        else :
            assert False and "not implemented"