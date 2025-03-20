from ApplicationEngine.src.Physics.Forces.ForceGenerator import *



class ForceRegistration:
    def __init__(self, fg : ForceGenerator, rb : RigidBody2D):
        self.fg = fg
        self.rb = rb

    
    def __eq__(self, other: object) -> bool:
        if not other: return False
        if not isinstance(other , ForceRegistration): return False

        return other.rb == self.rb and other.fg == self.fg