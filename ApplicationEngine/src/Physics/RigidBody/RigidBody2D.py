from ApplicationEngine.include.Maths.Maths import *


from typing import overload

from ApplicationEngine.src.Physics.Primatives._2D.Collider2D import *
#Temporary F declare
class Transform:
    def __init__(self):
        self.position : Vec2


class RigidBody2D:

    def __init__(self):
        
        self.rawTransform : Transform | None = None

        self.position : Vec2  = Vec2()
        self.rotation : float = 0.0         # rotation in degrees

        self.linearVelocity  : Vec2 = Vec2()
        self.angularVelocity : float = 0.0
        self.linearDamping  : float = 0.0
        self.angularDamping  : float = 0.0

        self.forceAccum : Vec2 = Vec2()

        self.ixedRotation : bool = False

        self.mass = 0.0
        self.inverseMass = 0.0

        self.collider : Collider2D | None = None

        self.COR = 1.0 # coeff of restitution

    def physicsUpdate(self, dt : float):
        if self.mass == 0.0: return  ## using 0 mass objects as infinite mass objects as there is no impl for 0 mass 

        acceleration : Vec2 = self.forceAccum * self.inverseMass
        self.linearVelocity.add(acceleration.multiply(dt))

        self.position.add(self.linearVelocity * dt)


        self.synchCollisionTransforms()
        self.clearAccumulators()

    def clearAccumulators(self):
        self.forceAccum.zero()

    def synchCollisionTransforms(self):
        if self.rawTransform:
            self.rawTransform.position = self.position
    

    def hasInfiniteMass(self) -> bool:
        return self.mass == 0.0
    


    @overload
    def setTransform(self, position : Vec2): ...
    
    @overload
    def setTransform(self, position : Vec2, rotation : float): ...

    def setTransform(self, position : Vec2, rotation : float | None = None):
        self.position = position
        if rotation:
            self.rotation = rotation

    def setVelocity(self, velocity : Vec2):
        self.linearVelocity = velocity

    def getVelocity(self):
        return self.linearVelocity

    def getRotation(self) -> float:
        return self.rotation
    def setRotation(self, newRotation): 
        self.rotation = newRotation


    def getPosition(self) -> Vec2:
        return self.position
    def setPosition(self, newPosition): 
        self.position = newPosition
    

    def getMass(self) -> float:
        return self.mass
    
    def getinverseMass(self) -> float:
        return self.mass
    
    def setMass(self, newMass): 
        self.mass = newMass
        if self.mass != 0.0:
            self.inverseMass = 1.0 / newMass

    
    def addForce(self, force : Vec2):
        self.forceAccum += force

    def setCollider(self, collider : Collider2D):
        self.collider = collider
    
    def getCollider(self):
        return self.collider
    

    def getCoefficientOfRestitution(self):
        return self.COR
    def setCoefficientOfRestitution(self, cor : float):
        self.COR = cor