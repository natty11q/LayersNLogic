from __future__ import annotations

import ApplicationEngine.AppEngine as LNLEngine
import math

from ApplicationEngine.include.Maths.Vector.Vector import Vec2, Vec3, Vec4
from ApplicationEngine.include.Maths.Matrix.Matrix import Mat2, Mat3, Mat4

from Game.src.World.World import * 

class EnvironmentObject2D(LNLEngine.GameObject2D):
    def __init__(self):
        super().__init__()
        
