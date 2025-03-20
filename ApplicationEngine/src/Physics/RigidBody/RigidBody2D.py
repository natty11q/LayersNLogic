from ApplicationEngine.include.Maths.Maths import *
# from ApplicationEngine.src.Object.Object import * 


from typing import overload


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
    
    @overload
    def setTransform(self, position : Vec2): ...
    
    @overload
    def setTransform(self, position : Vec2, rotation : float): ...

    def setTransform(self, position : Vec2, rotation : float | None = None):
        self.position = position
        if rotation:
            self.rotation = rotation


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

    