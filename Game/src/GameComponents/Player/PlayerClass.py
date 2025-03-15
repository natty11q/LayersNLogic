from __future__ import annotations

import ApplicationEngine.AppEngine as LNLEngine
from ApplicationEngine.include.Maths.Vector.Vector import Vec2, Vec3, Vec4
from ApplicationEngine.include.Maths.Matrix.Matrix import Mat2, Mat3, Mat4
from Game.src.GameComponents.Environement.Portal import *

import math

class PlayerInputHandlerAttribute(LNLEngine.ObjectAttribute):
    
    @staticmethod
    def Attrib_OnUpdate(obj : Player): # type: ignore
        obj._World_Position = Vec3(100 * math.sin(LNLEngine.LLEngineTime.Time()))
        # print("did sth")
        # PlayerInputHandlerAttribute.newMethod()
    

    @staticmethod
    def newMethod():...
        # print("newMeth")

class AffectedByGravityAttribute(LNLEngine.ObjectAttribute):
    GravitationalConstant = 9.81
    Gravity = Vec3(0, GravitationalConstant, 0)

    @staticmethod
    def Attrib_OnUpdate(obj : Player): # type: ignore
        # obj._World_Position = Vec3(100 * math.sin(LNLEngine.LLEngineTime.Time()))

        obj.Velocity += AffectedByGravityAttribute.Gravity * LNLEngine.LLEngineTime.DeltaTime()
        # print("did sth")
        # PlayerInputHandlerAttribute.newMethod()


class CanTravelThroughPortals(LNLEngine.ObjectAttribute):
    # InPortalColision = False

    @staticmethod
    def Attrib_OnUpdate(obj : Player): # type: ignore
        # handle Portal here 
        # LNLEngine.LNL_LogInfo("checking Portal collision 1")
        for portal in Portal.portals:
            ## getting the halfway point between the vertices {simple impl for now to keep it simple}

            # LNLEngine.LNL_LogInfo("checking Portal collision ")
            # collided = False
            # if portal.intersectsPoint(obj._World_Position):
            #     collided = True
            # if portal.intersectsPoint(obj._World_Position + Vec3(obj.width)):
            #     collided = True
            # if portal.intersectsPoint(obj._World_Position + Vec3(0, obj.height)):
            #     collided = True
            # if portal.intersectsPoint(obj._World_Position + Vec3(obj.width, obj.height)):
            #     collided = True
            
            if portal.intersectsQuad([obj._World_Position.toVec2().get_p(), 
                                      (obj._World_Position.toVec2() + Vec2(obj.width)).get_p(),
                                    (obj._World_Position.toVec2() + Vec2(0, obj.height)).get_p()
                                    ,(obj._World_Position.toVec2() + Vec2(obj.width, obj.height)).get_p()]):

                
                # input()
                LNLEngine.LNL_LogInfo("Portal collision ")
                LNLEngine.LNL_LogInfo("lkinked? : ", portal.checkLink())

                if portal.checkLink() and not obj.InPortalColision and not obj.InPortalColisionOnFrame:                    
                    LNLEngine.LNL_LogInfo("Portal teleportation ")

                    offset : Vec2 = obj._World_Position.toVec2() - portal.vertices[0]

                    dest : Portal = portal.GetDestination()

                    normalisedDistRationOut_y : float = (offset.dot(portal.tangent.get_normalized()) * portal.tangent).length() / portal.alongVec.length()
                    normalisedDistRationOut_x : float = (offset.dot(portal.normal.get_normalized()) * portal.normal).length()  / portal.normal.length()

                    destOffsetOut = (dest.alongVec * normalisedDistRationOut_y) + (dest.normal * normalisedDistRationOut_x)
                    # destCenter = dest.vertices[0] + (dest.vertices[1] - dest.vertices[0]).multiply(0.5)
                    obj._World_Position = LNLEngine.Vec3(destOffsetOut[0] - (obj.width/2), destOffsetOut[1] - (obj.height/2))
                    

                   # normal should be normalised but i am dividing jsut in case 
                   # angle is in radians
                    angleRot = math.acos(portal.normal.dot(dest.normal) / (portal.normal.length() * dest.normal.length()))
                    oV = Vec2(obj.Velocity[0], obj.Velocity[1]) * Mat2([
                                                                        [math.cos(-angleRot) , -math.sin(-angleRot)],
                                                                        [math.sin(-angleRot) , math.cos(-angleRot)]
                                                                            ])
                    
                    obj.Velocity = Vec3(*oV.get_p())

                obj.InPortalColisionOnFrame = True
                





class Player(LNLEngine.GameObject):
    def __init__(self, name : str):
        super().__init__()
        # self.SetAttribure(PlayerInputHandlerAttribute)

        # self.SetAttribure(AffectedByGravityAttribute)
        # self.SetAttribure(CanTravelThroughPortals)
        self.name = name


        self.Velocity = Vec3()
        self.Colour = Vec4(0,0,255,255)
        self._World_Position = Vec3(700, 50)

        self.width = 100
        self.height = 100

        self.speed  = 1000


        self.InPortalColision = False
        self.InPortalColisionOnFrame = False

        self.keys = {}
        for kcode in LNLEngine.KEY_MAP:
            self.keys[kcode] = 0

    def _OnUpdate(self, deltatime : float):
        # LNLEngine.LNL_LogEngineInfo(self._World_Position)
        self.InPortalColision = self.InPortalColisionOnFrame
        self.InPortalColisionOnFrame = False
        self._World_Position += self.Velocity
        
        if self.keys.get(LNLEngine.KEY_MAP['right']):
            self._World_Position += Vec3(self.speed,0,0) * deltatime
        if self.keys.get(LNLEngine.KEY_MAP['left']):
            self._World_Position -= Vec3(self.speed,0,0) * deltatime
        if self.keys.get(LNLEngine.KEY_MAP['up']):
            self._World_Position -= Vec3(0,self.speed,0) * deltatime
        if self.keys.get(LNLEngine.KEY_MAP['down']):
            self._World_Position += Vec3(0,self.speed,0) * deltatime

    def _OnEvent(self, event : LNLEngine.Event):
        if event.GetName() == "KeyDown":
            self.keys[event.keycode] = 1
        if event.GetName() == "KeyUp":
            self.keys[event.keycode] = 0
    
    def Draw(self):

        LNLEngine.Quad(Vec2(self._World_Position[0],self._World_Position[1]), 100, 100, self.Colour).Draw()
        # LNLEngine.Renderer.DrawTriangle([pos,pos2 , Vec2(200,400)], Vec4(100, 200, 255, 255))
        # LNLEngine.Renderer.DrawTriangle([Vec2(200,10),Vec2(100,800) , Vec2(700,4)], Vec4(100, 200, 80, 255))
