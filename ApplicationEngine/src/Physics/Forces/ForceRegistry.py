from ApplicationEngine.src.Physics.Forces.ForceRegistration import *


class ForceRegistry:
    def __init__(self):

        self.registry : list[ForceRegistration] = []

    def add(self, rb : RigidBody2D, fg : ForceGenerator):
        fr : ForceRegistration = ForceRegistration(fg , rb)

        self.registry.append(fr)


    def remove(self, rb : RigidBody2D, fg : ForceGenerator):
        fr : ForceRegistration = ForceRegistration(fg , rb)
        self.registry.remove(fr)

    
    def clear(self):
        self.registry.clear()

    
    def updateForces(self, dt : float):
        for fr in self.registry:
            fr.fg.updateForce(fr.rb, dt)
        
    
    def zeroForces(self):
        for fr in self.registry:
            # TODO: impl
            # fr.rb.zeroForces()

            pass