from ApplicationEngine.include.Maths.Maths import *
from enum import Enum, auto

from typing import overload

from ApplicationEngine.src.Physics.Primatives._2D.Collider2D import *
#Temporary F declare
class Transform:
    def __init__(self):
        self.position : Vec2


class ShapeType(Enum):
    Circle  = auto()
    AABB    = auto()
    Box2D   = auto()
    Polygon = auto()


class RigidBody2D:

    def __init__(self):
        self._contactListeners = []
        self._collisionResponseListeners = []
        
        self.rawTransform : Transform | None = None

        self.position : Vec2  = Vec2()
        self.rotation : float = 0.0         # rotation in degrees

        self.linearVelocity  : Vec2 = Vec2()
        self.angularVelocity : float = 0.0
        self.linearDamping  : float = 0.0
        self.angularDamping  : float = 0.0


        # self.frictionCoefficient : float = 0.0
        self.staticFriction : float = 0.0
        self.dynamicFriction : float = 0.0

        self.forceAccum : Vec2 = Vec2()

        self.fixedRotation : bool = False

        self.mass = 0.0
        self.inverseMass = 0.0

        self.density = 0.0
        self.area = 0.0


        self.isStatic : bool = False
        self.isActor  : bool = True

        self.collider : Collider2D | None = None

        self.COR = 1.0 # coeff of restitution

        self.owner : object = None

        self.StoredImpulse : Vec2 = Vec2()
    
    def setOwner(self, newOwner : object):
        self.owner = newOwner
    def getOwner(self) -> object | None:
        return self.owner


    def addCollisionListener(self, listener):
        self._collisionResponseListeners.append(listener)

    def removeCollisionListener(self, listener):
        self._collisionResponseListeners.remove(listener)

    def _notifyCollision(self, otherOwner : object , other_body, impulse : Vec2, manifold):
        for listener in self._collisionResponseListeners:
            listener(self, otherOwner, other_body, impulse, manifold)


    def addContactListener(self, listener):
        self._contactListeners.append(listener)

    def removeContactListener(self, listener):
        self._contactListeners.remove(listener)

    def _notifyContact(self, otherOwner : object , other_body):
        for listener in self._contactListeners:
            listener(self, otherOwner, other_body)


    def physicsUpdate(self, dt : float):
        if self.mass == 0.0: return  ## using 0 mass objects as infinite mass objects as there is no impl for 0 mass 

        acceleration : Vec2 = self.forceAccum * self.inverseMass
        self.linearVelocity.add(acceleration.multiply(dt))
        self.linearVelocity *= (1 - self.linearDamping * dt)

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
        """returns the rotation in radians"""
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
        # return self.mass
        return self.inverseMass
    
    def setMass(self, newMass): 
        self.mass = newMass
        if self.mass != 0.0:
            self.inverseMass = 1.0 / newMass
        else:
            self.inverseMass = 0

    
    def addForce(self, force : Vec2):
        self.forceAccum += force

    def addImpulse(self, impulse : Vec2):
        self.StoredImpulse += impulse

    def setCollider(self, collider : Collider2D):
        self.collider = collider
    
    def getCollider(self):
        return self.collider
    

    def getCoefficientOfRestitution(self):
        return self.COR
    def setCoefficientOfRestitution(self, cor : float):
        self.COR = cor


    def getFrictionCoefficient(self):
        return self.frictionCoefficient
    def setFrictionCoefficient(self, mu : float):
        self.frictionCoefficient = mu


    def GetStoredImpulse(self) -> Vec2:
        return self.StoredImpulse