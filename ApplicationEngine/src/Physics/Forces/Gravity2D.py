from ApplicationEngine.src.Physics.Forces.ForceGenerator import *
from ApplicationEngine.src.Physics.RigidBody.RigidBody2D import RigidBody2D




class Gravity2D(ForceGenerator):
    def __init__(self , force : Vec2):
        self.gravity = force
    


    def updateForce(self, body: RigidBody2D, dt: float):
        body.addForce(self.gravity * body.getMass())