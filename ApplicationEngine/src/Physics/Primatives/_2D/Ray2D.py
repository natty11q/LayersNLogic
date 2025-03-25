from ApplicationEngine.include.Maths.Maths import *


class Ray2D:
    def __init__(self, origin : Vec2, direction : Vec2, maxlen = sys.float_info.max):
        self.origin = Vec2(*origin.get_p())
        self.direction = direction.get_normalized()
        self.maxlen = maxlen

    def getOrigin(self):
        return self.origin
    
    def getDirection(self):
        return self.direction
    
    def getMaxLen(self):
        return self.maxlen