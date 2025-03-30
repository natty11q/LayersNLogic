from __future__ import annotations 
from abc import ABC


from ApplicationEngine.src.Object.ObjectBase import *
# from ApplicationEngine.src.Object.ObjectClass import GameObject

from ApplicationEngine.src.Physics.LNL_Physics import *

class ObjectAttribute(ABC):

    
    
    @staticmethod
    def Attrib_OnUpdate(obj : GameObjectBase):
        ...

    @staticmethod
    def Attrib_OnPhysicsUpdate(obj : GameObjectBase):
        ...

    @staticmethod
    def Attrib_OnCollision(obj, body : RigidBody2D, otherOwner : GameObjectBase, otherBody : RigidBody2D, impulse : Vec2, manifold : CollisionManifold):
        ...

    @staticmethod
    def Attrib_OnContact(obj : GameObjectBase,body : RigidBody2D, otherOwner : GameObjectBase, otherBody : RigidBody2D):
        ...
    

    @staticmethod
    def Attrib_OnAttach(obj : GameObjectBase):
        ...
    
    @staticmethod
    def Attrib_OnDetach(obj : GameObjectBase):
        ...