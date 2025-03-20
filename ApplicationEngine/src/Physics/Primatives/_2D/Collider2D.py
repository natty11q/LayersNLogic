from ApplicationEngine.include.Maths.Maths import *
from ApplicationEngine.src.Object.Object import *


class Collider2D:
    def __init__(self):
        self._offset : Vec2 = Vec2()

    
    def getIntertiaTensor(self, mass : float) -> float:
        ...