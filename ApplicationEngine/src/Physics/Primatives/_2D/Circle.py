from ApplicationEngine.src.Physics.RigidBody.RigidBody2D import *
from ApplicationEngine.src.Physics.Primatives._2D.Collider2D import *


class Circle(Collider2D):

    def __init__(self):
        self._radius : float = 1.0
        self._rigidBody : RigidBody2D = RigidBody2D()

    def getRadius(self) -> float:
        return self._radius
    
    def getCentre(self) -> Vec2:
        return self._rigidBody.getPosition()
    
    def getRigidBody(self) -> RigidBody2D:
        return self._rigidBody
    
    def setRigidBody(self, rb : RigidBody2D):
        self._rigidBody = rb

    def setRadius(self, radius : float):
        self._radius = radius