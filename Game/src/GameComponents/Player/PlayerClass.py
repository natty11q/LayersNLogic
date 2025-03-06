from __future__ import annotations

import ApplicationEngine.AppEngine as LNLEngine
from ApplicationEngine.include.Maths.Vector.Vector import Vec2, Vec3, Vec4
import math

class PlayerInputHandlerAttribute(LNLEngine.ObjectAttribute):
    
    @staticmethod
    def AttribMethod(obj : Player): # type: ignore
        obj._World_Position = Vec3(100 * math.sin(LNLEngine.LLEngineTime.Time()))
        # print("did sth")
        # PlayerInputHandlerAttribute.newMethod()
    

    @staticmethod
    def newMethod():...
        # print("newMeth")



class Player(LNLEngine.GameObject):
    def __init__(self):
        super().__init__()
        self.SetAttribure(PlayerInputHandlerAttribute)

    def _OnUpdate(self):
        # LNLEngine.LNL_LogEngineInfo(self._World_Position)
        ...

    
    def Draw(self):

        pos = Vec2(10 + self._World_Position[0] ,10 + self._World_Position[1])
        pos2 = Vec2(100 - (self._World_Position[0] / 3),50 + self._World_Position[1])
        LNLEngine.Renderer.DrawTriangle([pos,pos2 , Vec2(200,400)], Vec4(100, 200, 255, 255))
        # LNLEngine.Renderer.DrawTriangle([Vec2(200,10),Vec2(100,800) , Vec2(700,4)], Vec4(100, 200, 80, 255))
