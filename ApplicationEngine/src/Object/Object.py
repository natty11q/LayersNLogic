from ApplicationEngine.include.Window.Window import *
from ApplicationEngine.include.Maths.Maths import *



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




class GameObject:
    def __init__(self):
        pass
    
    
    def Draw(self, window : Window): ... 
    
    
    def _OnUpdate(self): ...
    
    
    def Update(self):
        pass



class CircleObject(GameObject):
    def __init__(self, position : Vector.Vec3 = Vector.Vec3()):
        self.__Position : Vector.Vec3 = position

    def Draw(self, window : Window):
        pass
    
    def Update(self):
        return super().Update()
    