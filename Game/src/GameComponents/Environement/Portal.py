from __future__ import annotations

import ApplicationEngine.AppEngine as LNLEngine





class Portal(LNLEngine.GameObject):
    
    
    # TODO : Make this impl for 3 component vector and quats
    def __init__(self, position : LNLEngine.Vector.Vec2, rotation : float, Destination : Portal | None, radius : float = 50):
        self.position : LNLEngine.Vector.Vec2 = position
        self.rotation : float = rotation
        if Destination:
            self.__DestinationPortal : Portal = Destination
        else:
            self.__DestinationPortal : Portal = self
        self.rotation = radius
        
        
        self.Model : LNLEngine.Quad = LNLEngine.Quad(self.position, 100, 29, LNLEngine.Vector.Vec4(1,0,0,0))
        
        
    def LinkPortal(self, newPortal : Portal):
        self.DestinationPortal = newPortal
        newPortal.SetDestination(self)
        
    def SetDestination(self, destPortal : Portal):
        self.__DestinationPortal = destPortal


class CanTravelThroughPortals(LNLEngine.ObjectAttribute):
    
    @staticmethod
    def OnUpdate(object : LNLEngine.GameObject):
        # handle Portal here
        ...

class cube(LNLEngine.GameObject):
    def __init__(self):
        self.Attributes = [CanTravelThroughPortals]
    
    def _OnUpdate(self):
        super()._OnUpdate()