from __future__ import annotations

import ApplicationEngine.AppEngine as LNLEngine
from ApplicationEngine.include.Maths.Vector.Vector import Vec2, Vec3, Vec4
from ApplicationEngine.include.Maths.Matrix.Matrix import Mat2, Mat3, Mat4
from Game.src.GameComponents.Environement.Portal import *


from ApplicationEngine.src.Graphics.SpriteAnimationClass import *

import math



class CanTravelThroughPortals(LNLEngine.ObjectAttribute):
    # InPortalColision = False
    CollisionRegistry : dict[ LNLEngine.GameObjectBase, dict [str, bool] ]= {}
    @staticmethod
    def Attrib_OnAttach(obj: LNLEngine.GameObjectBase):
        CanTravelThroughPortals.CollisionRegistry[obj] = {"onframe" : False, "current" : False}

    @staticmethod
    def Attrib_OnUpdate(obj : Player): # type: ignore
        ...
    
    @staticmethod
    def Attrib_OnPhysicsUpdate(obj: LNLEngine.GameObjectBase):
        if not CanTravelThroughPortals.CollisionRegistry[obj]["onframe"]:
            CanTravelThroughPortals.CollisionRegistry[obj]["current"] = False


        CanTravelThroughPortals.CollisionRegistry[obj]["onframe"] = False


    @staticmethod
    def Attrib_OnContact(obj: LNLEngine.GameObjectBase, body: LNLEngine.RigidBody2D, otherOwner: LNLEngine.GameObjectBase, otherBody: LNLEngine.RigidBody2D):
        if not isinstance(otherOwner, Portal):
            return
        
        portal = otherOwner
        if not portal.IsActive():
            return
        

        CanTravelThroughPortals.CollisionRegistry[obj]["onframe"] = True
        if not LNLEngine.IntersectionDetector2D.pointInBox2D(body.getPosition(), otherBody.getCollider()): #type: ignore
            return
        

        if CanTravelThroughPortals.CollisionRegistry[obj]["current"]: # check if currently in a portal collision
            return
        
        positionOffset : Vec2 = body.getPosition() - otherBody.getPosition()

        totalRotation = portal.GetDestination().body.getRotation() -  portal.body.getRotation()

        currentPos = body.getPosition()
        currentVel = body.getVelocity()

        currentRot = body.getRotation()

        updatedPositionOffset = LNLEngine.LNLMAths.rotate_vec2(positionOffset, Vec2(0,0), math.degrees(totalRotation))

        # newPos : Vec2 = currentPos - portal.body.getPosition() + portal.GetDestination().body.getPosition() + updatedPositionOffset
        newPos : Vec2 = currentPos - portal.body.getPosition() + portal.GetDestination().body.getPosition() 
        newVel = LNLEngine.LNLMAths.reflectVec2(currentVel , LNLEngine.LNLMAths.rotate_vec2(Vec2(1,0),Vec2(0,0),math.degrees(portal.rotation)).normalize())
        newVel = LNLEngine.LNLMAths.rotate_vec2(newVel, Vec2(0,0), math.degrees(totalRotation))

        body.setTransform(newPos)
        body.setVelocity(newVel)

        CanTravelThroughPortals.CollisionRegistry[obj]["current"] = True


