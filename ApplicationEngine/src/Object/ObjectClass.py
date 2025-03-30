from __future__ import annotations

# from ApplicationEngine.include.Window.Window import *
from ApplicationEngine.include.Maths.Maths import *
from ApplicationEngine.src.Graphics.Renderer.Renderer import Renderer

from ApplicationEngine.src.Object.ObjectBase import *
from ApplicationEngine.src.Object.GameObjectAttributes import *
from ApplicationEngine.src.Event.EventHandler import *


# import inspect
from ApplicationEngine.src.Physics.LNL_Physics import *


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
    
    def __init__(self, *eat_args, **eat_kwargs):
        self._World_Position : Vec3 = Vec3()

        self._Attributes : list [ObjectAttribute.__class__] = []
        self.__Active : bool = True ## toggles wether an object is active in the editor and if physics is enabled for that object.
        
        self.id = LNL_IDGenerator.get_id()
        AddEventListener(self._OnEvent)

    # def __init_subclass__(cls,*args, **kwargs):
    #     """removes the need to super init every game object in the game code"""
        
    #     super().__init_subclass__(*args,**kwargs)
        
    #     # Store the original __init__ of the subclass
    #     original_init = cls.__init__

    #     def new_init(self, *args, **kwargs):
    #         # Call Base class __init__ first
    #         super(cls, self).__init__(*args, **kwargs)

    #         # Call the subclass's original __init__
    #         original_init(self, *args, **kwargs)

    #     cls.__init__ = new_init  # Override the subclass's __init__

 
    def SetAttribure(self, attrib : ObjectAttribute.__class__):
        self._Attributes.append(attrib)
        attrib.Attrib_OnAttach(self)

    def RemoveAttribure(self, attrib : ObjectAttribute.__class__):
        self._Attributes.remove(attrib)
        attrib.Attrib_OnDetach(self)
        
        
    def Activate(self): self.__Active = True
    def Deactivate(self): self.__Active = False
    def IsActive(self) -> bool: return self.__Active
    

    def BeginPlay(self): ...
    def EndPlay(self): ...

    def Draw(self): ... 


    def _OnPhysicsUpdate(self, tickTime: float): ...


    def _OnUpdate(self, deltatime : float): ...

    def _OnEvent(self, event : Event): ...
    
    
    def Update(self, deltatime : float):
        for attribute in self._Attributes:
            attribute.Attrib_OnUpdate(self)
        self._OnUpdate(deltatime)
    
    def PhysicsUpdate(self, tickTime : float):
        for attribute in self._Attributes:
            attribute.Attrib_OnPhysicsUpdate(self)
        self._OnPhysicsUpdate(tickTime)


class GameObject2D(GameObject):
    def __init__(self, position : Vec2 = Vec2(), mass : float = 1.0, rotation : float = 0.0):
        super().__init__()
        self.body : RigidBody2D = RigidBody2D()
        
        self.body.setTransform(position, rotation)
        self.body.setMass(mass)
        self.body.setOwner(self)

        self.body.addCollisionListener(self.OnCollision) # when colliding with another physics object
        self.body.addContactListener(self.OnContact) # when colliding with a non tangible object eg : portals which dont move in response to physics or impart a force on the player yet require a collision check
    
    def BeginPlay(self):
        super().BeginPlay()
        PhysicsSystem2D.Get().addRigidbody(self.body, True)


    def EndPlay(self):
        super().EndPlay()
        PhysicsSystem2D.Get().removeRigidbody(self.body)


    def _OnCollision(self, body : RigidBody2D, otherOwner : GameObject2D, otherBody : RigidBody2D, impulse : Vec2, manifold : CollisionManifold): ...
    
    def OnCollision(self, body : RigidBody2D, otherOwner : GameObject2D, otherBody : RigidBody2D, impulse : Vec2, manifold : CollisionManifold):
        for attribute in self._Attributes:
            attribute.Attrib_OnCollision(self, body, otherOwner, otherBody, impulse, manifold)
        self._OnCollision(body, otherOwner, otherBody, impulse, manifold)

    def _OnContact(self, body, otherOwner, otherBody): ...

    def OnContact(self, body, otherOwner, otherBody):
        for attribute in self._Attributes:
            attribute.Attrib_OnContact(self, body, otherOwner, otherBody)
        self._OnContact(body, otherOwner, otherBody)



class Triangle(GameObject):
    def __init__(self, v1 : Vec2 ,  v2 : Vec2 ,  v3 : Vec2 , colour : Vec4):
        super().__init__()
        self._positions = [v1,v2,v3]
        self._colour = colour
    
    
        
    def Draw(self):
        Renderer.DrawTriangle(self._positions, self._colour)


class Quad(GameObject):
    def __init__(self,topLeft : Vec2, width : float, height : float , colour : Vec4):
        super().__init__()
        self._topLeft = topLeft
        self._width  = width
        self._height = height
        self._colour = colour
    
    # def __init_subclass__(cls, *args, **kwargs):
    #     # super().__init_subclass__(*args, **kwargs)
        
    #     # # Store the original __init__ of the subclass
    #     # original_init = cls.__init__

    #     # # Get the parameters of the subclass’s __init__
    #     # subclass_signature = inspect.signature(original_init)
    #     # base_signature = inspect.signature(Quad.__init__)

    #     # def new_init(self, *args, **kwargs):
    #     #     # Extract arguments meant for Base and Subclass separately
    #     #     base_params = {k: kwargs.pop(k) for k in base_signature.parameters if k in kwargs}
    #     #     subclass_params = {k: kwargs[k] for k in subclass_signature.parameters if k in kwargs}

    #     #     # Call Base class __init__
    #     #     super(cls, self).__init__(*args, **base_params)

    #     #     # Call the subclass's original __init__
    #     #     original_init(self, * args, **subclass_params)

    #     # cls.__init__ = new_init  # Override the subclass's __init__

    
    def Draw(self):
        Renderer.DrawTriangle(
            [self._topLeft , Vec2(self._topLeft.x, self._topLeft.y + self._height), Vec2(self._topLeft.x + self._width, self._topLeft.y + self._height)]
                              ,self._colour)
        Renderer.DrawTriangle(
            [self._topLeft , Vec2(self._topLeft.x + self._width, self._topLeft.y + self._height), Vec2(self._topLeft.x + self._width, self._topLeft.y)]
                              ,self._colour)


class CircleObject(GameObject):
    def __init__(self, position : Vec3 = Vec3()):
        super().__init__()
        self._Position : Vec3 = position

    def Draw(self):
        pass
    
    def Update(self, deltatime: float):
        return super().Update(deltatime)
    