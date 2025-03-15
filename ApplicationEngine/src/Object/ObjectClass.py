# from ApplicationEngine.include.Window.Window import *
from ApplicationEngine.include.Maths.Maths import *
from ApplicationEngine.src.Graphics.Renderer.Renderer import Renderer

from ApplicationEngine.src.Object.ObjectBase import *
from ApplicationEngine.src.Object.GameObjectAttributes import *
from ApplicationEngine.src.Event.EventHandler import *

SQUARE_VERTICES : list [float] = [
    ## position
    -1.0, -1.0,  0.0,  
     1.0, -1.0,  0.0,  
     1.0,  1.0,  0.0,  
    -1.0,  1.0,  0.0,  
]


SQUARE_INDICES : list [int] = [
    0, 1 ,2,
    0, 2, 3,
]




class GameObject(GameObjectBase):
    
    def __init__(self):
        self._World_Position : Vector.Vec3 = Vector.Vec3()
        self.__Attributes : list [ObjectAttribute.__class__] = []
        self.__Active : bool = True ## toggles wether an object is active in the editor and if physics is enabled for that object.
        AddEventListener(self._OnEvent)
 
    def SetAttribure(self, attrib : ObjectAttribute.__class__):
        self.__Attributes.append(attrib)
        attrib.Attrib_OnAttach(self)

    def RemoveAttribure(self, attrib : ObjectAttribute.__class__):
        self.__Attributes.remove(attrib)
        attrib.Attrib_OnDetach(self)
        
        
    def Activate(self): self.__Active = True
    def Deactivate(self): self.__Active = False
    def IsActive(self) -> bool: return self.__Active
    
    def Draw(self): ... 


    def _OnPhysicsUpdate(self, tickTime: float): ...


    def _OnUpdate(self, deltatime : float): ...

    def _OnEvent(self, event : Event): ...
    
    
    def Update(self, deltatime : float):
        for attribute in self.__Attributes:
            attribute.Attrib_OnUpdate(self)
        self._OnUpdate(deltatime)
    
    def PhysicsUpdate(self, tickTime : float):
        for attribute in self.__Attributes:
            attribute.Attrib_OnPhysicsUpdate(self)
        self._OnPhysicsUpdate(tickTime)



class Triangle(GameObject):
    def __init__(self, v1 : Vector.Vec2 ,  v2 : Vector.Vec2 ,  v3 : Vector.Vec2 , colour : Vector.Vec4):
        super().__init__()
        self._positions = [v1,v2,v3]
        self._colour = colour
        
    def Draw(self):
        Renderer.DrawTriangle(self._positions, self._colour)


class Quad(GameObject):
    def __init__(self,topLeft : Vector.Vec2, width : float, height : float , colour : Vector.Vec4):
        super().__init__()
        self._topLeft = topLeft
        self._width  = width
        self._height = height
        self._colour = colour
    
    def Draw(self):
        Renderer.DrawTriangle(
            [self._topLeft , Vector.Vec2(self._topLeft.x, self._topLeft.y + self._height), Vector.Vec2(self._topLeft.x + self._width, self._topLeft.y + self._height)]
                              ,self._colour)
        Renderer.DrawTriangle(
            [self._topLeft , Vector.Vec2(self._topLeft.x + self._width, self._topLeft.y + self._height), Vector.Vec2(self._topLeft.x + self._width, self._topLeft.y)]
                              ,self._colour)


class CircleObject(GameObject):
    def __init__(self, position : Vector.Vec3 = Vector.Vec3()):
        self._Position : Vector.Vec3 = position

    def Draw(self):
        pass
    
    def Update(self, deltatime: float):
        return super().Update(deltatime)
    