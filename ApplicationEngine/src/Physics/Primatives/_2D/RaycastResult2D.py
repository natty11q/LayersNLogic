from __future__ import annotations

from ApplicationEngine.src.Physics.Primatives._2D.Ray2D import * 

from typing import overload, Union

class RaycastResult2D:
    @ overload
    def __init__(self):
        ...

    @ overload
    def __init__(self, point : Vec2, normal : Vec2, t : float, hit : bool):
        ...

    def __init__(self , point : Vec2 = Vec2(), normal : Vec2 = Vec2(), t : float = -1, hit : bool = False):

        self.point : Vec2   = point
        self.normal : Vec2  = normal
        self.t : float   = t
        self.hit : bool  = hit

    
    ## confusing naming, done so that raycast results can be recalculated without having to construct a new object
    def init(self, point : Vec2, normal : Vec2, t : float, hit : bool):
        self.point : Vec2   = point
        self.normal : Vec2  = normal
        self.t : float   = t
        self.hit : bool  = hit


    @staticmethod
    def reset( result : RaycastResult2D | None):
        if result:
            result.point = Vec2()
            result.normal = Vec2()
            result.t = -1
            result.hit = False
