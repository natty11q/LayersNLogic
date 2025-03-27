from __future__ import annotations 
from abc import ABC


from ApplicationEngine.src.Object.ObjectBase import *
# from ApplicationEngine.src.Object.ObjectClass import GameObject

class ObjectAttribute(ABC):

    
    
    @staticmethod
    def Attrib_OnUpdate(obj : GameObjectBase):
        ...

    @staticmethod
    def Attrib_OnPhysicsUpdate(obj : GameObjectBase):
        ...
    

    @staticmethod
    def Attrib_OnAttach(obj : GameObjectBase):
        ...
    
    @staticmethod
    def Attrib_OnDetach(obj : GameObjectBase):
        ...