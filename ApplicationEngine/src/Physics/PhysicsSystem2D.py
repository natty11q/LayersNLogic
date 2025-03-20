from ApplicationEngine.src.Physics.Forces.ForceRegistry import *
from ApplicationEngine.include.Maths.Maths import *
from ApplicationEngine.src.Core.Utility.Temporal import *


from ApplicationEngine.src.Physics.Forces.Gravity2D import *


class PhysicsSystem2D:
    def __init__(self, gravity : Vec2):

        self.forceRegistry : ForceRegistry   = ForceRegistry()
        self.rigidBodies : list[RigidBody2D] = []
        self.gravity : Gravity2D = Gravity2D(gravity)


    def update(self, dt : float):
        self.fixedUpdate()

    def fixedUpdate(self):
        frame_tick_delta = 1/LLEngineTime.TickRate() # just incase the tick rate is set on the main thread casing inconsitiency
        self.forceRegistry.updateForces(frame_tick_delta)


        for i in range(len(self.rigidBodies)):
            self.rigidBodies[i].physicsUpdate(frame_tick_delta)

    

    def addRigidbody(self, body : RigidBody2D):
        self.rigidBodies.append(body)
        self.forceRegistry.add(body, self.gravity)
        # body.init()
