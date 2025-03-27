from __future__ import annotations

from ApplicationEngine.include.Maths.Maths import *
from ApplicationEngine.src.Event.EventHandler import *

class Mouse:
    _KEYS : dict[int, bool]  = {0 : False, 1 : False, 2 : False, 3 : False}
    _POS  : Vec2        = Vec2()


    
    @staticmethod
    def GetPos() -> Vec2:
        return Mouse._POS

    @staticmethod
    def SetPos(pos : Vec2 | tuple [float] | list [float]):
        ...

    @staticmethod
    def GetPressed():
        """returns _KEYS list (list[bool]) saying wether the button of that index is pressed or not"""
        return Mouse._KEYS

    @staticmethod
    def __OnEvent(event : Event):
        if event.GetName() == "MouseButtonDown":
            Mouse._KEYS[event.button] = True

        if event.GetName() == "MouseButtonUp":
            Mouse._KEYS[event.button] = False

        if event.GetName() == "MouseMoved":
            Mouse._POS[0] = event.x 
            Mouse._POS[1] = event.y

    

    @classmethod
    def Init(cls):
        AddEventListener(cls.__OnEvent)

        