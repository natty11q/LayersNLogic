from ApplicationEngine.include.Maths.Maths import *




class Line2D:
    def __init__(self, start: Vec2, end : Vec2):
        self.start = start
        self.end = end

    
    def getStart(self):
        return self.start
    
    def getEnd(self):
        return self.end
    
    def length(self):
        return (self.end - self.start).length()

    # snake case for parity with vector class :(
    def length_squared(self):
        return (self.end - self.start).length_squared()