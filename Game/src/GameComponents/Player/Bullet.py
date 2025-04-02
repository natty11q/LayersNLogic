from __future__ import annotations

import ApplicationEngine.AppEngine as LNLEngine
from ApplicationEngine.include.Maths.Vector.Vector import Vec2, Vec3, Vec4
from ApplicationEngine.include.Maths.Matrix.Matrix import Mat2, Mat3, Mat4
from Game.src.GameComponents.Environement.Portal import *


from ApplicationEngine.src.Graphics.SpriteAnimationClass import *

import math

class Bullet(LNLEngine.GameObject2D):
    def _init_(self,hitBox : Vec2|None):
        super().__init__() 

        self.hitBox = Vec2(1,1) #Will add setter in case wanting to add other ammo types  

        

    def setHitBox(self, hBox : Vec2):
        self.hitBox = hBox
         
    def getHitBox(self):
        return self.hitBox 
    




    