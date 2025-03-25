from abc import ABC
from ApplicationEngine.src.Physics.RigidBody.RigidBody2D import *

class ForceGenerator(ABC):

    def updateForce(self, body : RigidBody2D, dt : float):
        ...
