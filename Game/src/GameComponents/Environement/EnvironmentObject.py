from __future__ import annotations

import ApplicationEngine.AppEngine as LNLEngine
import math

from ApplicationEngine.include.Maths.Vector.Vector import Vec2, Vec3, Vec4
from ApplicationEngine.include.Maths.Matrix.Matrix import Mat2, Mat3, Mat4

from Game.src.World.World import * 

class EnvironmentObject2D(LNLEngine.GameObject2D):
    def __init__(self, position : Vec2 = Vec2(), mass : float = 1.0, rotation : float = 0.0):
        super().__init__(position,mass,rotation)
        
