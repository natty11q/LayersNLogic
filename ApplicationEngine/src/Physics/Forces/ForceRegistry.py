from ApplicationEngine.src.Physics.Forces.ForceRegistration import *

class ForceRegistry:
    def __init__(self):
        self.registry: list[ForceRegistration] = []
        # Use the id() values as keys since objects may not be hashable.
        self.cache: dict[tuple[int, int], ForceRegistration] = {}

    def add(self, rb: RigidBody2D, fg: ForceGenerator):
        key = (id(rb), id(fg))
        # Only add if not already registered.
        if key not in self.cache:
            fr = ForceRegistration(fg, rb)
            self.cache[key] = fr
            self.registry.append(fr)

    def remove(self, rb: RigidBody2D, fg: ForceGenerator):
        key = (id(rb), id(fg))
        if key in self.cache:
            fr = self.cache.pop(key)
            if fr in self.registry:
                self.registry.remove(fr)

    def clear(self):
        self.registry.clear()
        self.cache.clear()

    def updateForces(self, dt: float):
        for fr in self.registry:
            fr.fg.updateForce(fr.rb, dt)

    def zeroForces(self):
        for fr in self.registry:
            # TODO: impl
            # fr.rb.zeroForces()

            pass