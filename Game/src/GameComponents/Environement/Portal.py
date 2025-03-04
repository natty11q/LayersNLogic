from __future__ import annotations

import ApplicationEngine.AppEngine as LNLEngine
import math




class Portal(LNLEngine.GameObject):
    portals : list[Portal] = []
    
    # TODO : Make this impl for 3 component vector and quats
    def __init__(self, position : LNLEngine.Vector.Vec2, rotation : float, Destination : Portal | None = None, radius : float = 50):
        self.position : LNLEngine.Vector.Vec2 = position
        self.rotation : float = rotation
        if Destination:
            self.__DestinationPortal : Portal | None = Destination
        else:
            self.__DestinationPortal : Portal | None = self
        self.radius = radius
        
        
        self.Model : LNLEngine.Quad = LNLEngine.Quad(self.position, 100, 29, LNLEngine.Vector.Vec4(1,0,0,0))


    def checkLink(self):
        if self.__DestinationPortal is not None:
            return True
        return False
    
    def LinkPortal(self, newPortal : Portal):
        if isinstance(self.__DestinationPortal, Portal):
            self.DestinationPortal = newPortal
            newPortal.SetDestination(self)
        self.__DestinationPortal = None
        
    def SetDestination(self, destPortal : Portal):
        self.__DestinationPortal = destPortal

    def GetDestination(self) -> Portal | None:
        return self.__DestinationPortal


class CanTravelThroughPortals(LNLEngine.ObjectAttribute):
    
    @staticmethod
    def OnUpdate(object : LNLEngine.GameObject):
        # handle Portal here 
        for portal in Portal.portals:
            dX = object._World_Position[0] - portal.position[0] 
            dY = object._World_Position[1] - portal.position[1] 
            if dX*dX + dY*dY <= portal.radius**2:
                dest : Portal|None = portal.GetDestination()
                if dest is not None:                    
                    object._World_Position = LNLEngine.Vector.Vec3(dest.position[0], dest.position[1])


class cube(LNLEngine.GameObject):
    def __init__(self):
        self.Attributes = [CanTravelThroughPortals]
    
    def _OnUpdate(self):
        super()._OnUpdate() 





