from __future__ import annotations

import ApplicationEngine.AppEngine as LNLEngine
from ApplicationEngine.include.Maths.Vector.Vector import Vec2, Vec3, Vec4
from ApplicationEngine.include.Maths.Matrix.Matrix import Mat2, Mat3, Mat4
from ApplicationEngine.src.Graphics.SpriteAnimationClass import *

# =========================================================================

import math

from Game.src.GameComponents.Environement.Portal import *
from Game.src.GameComponents.Environement.Attributes.CanTravelThroughPortals import *

from Game.src.GameComponents.Environement.Environment import *


class EntityStates:
    DEAD = auto()
    IDLE = auto()
    ATTACKING   = auto()
    FALLING  = auto()
    HURT     = auto()



class Entity(LNLEngine.GameObject2D):
    def __init__(self, dimensions : Vec2, position : Vec2 = Vec2(), mass : float= 10, name : str = ""):
        super().__init__(position, mass)

        self.attack     : float  = 2
        self.defence    : float  = 1
        
        self.MaxHealth  : float  = 10.0
        self.CurrentHealth  : float  = self.MaxHealth

        self.isGrounded : bool = False

        self.target     : Entity | None = None # is the entity taargeting anopther entity?

        self.alive : bool = True

        
        self.body.setCollider(
            self._InitCollider(*dimensions.get_p())
        )
        self.body.linearDamping = 0.8


    def _InitCollider(self, w, h) -> LNLEngine.Collider2D:
        c1 : LNLEngine.Collider2D = LNLEngine.Box2D()
        c1.setSize(Vec2(w,h))
        c1.setRigidBody(self.body)

        return c1
        

    def SetHealth(self, newHelath : float):
        if newHelath >= 0:
            self.CurrentHealth = newHelath
        else:
            self.CurrentHealth = 0

    def GetHealth(self) -> float:
        return self.CurrentHealth
    

    def Grounded(self):
        return self.isGrounded
    

    def SetAttack(self, newAttack : float):
        self.attack = newAttack

    def GetAttack(self) -> float:
        return self.attack
    
    def SetDefence(self, newDefence : float):
        self.defence = newDefence

    def GetDefence(self):
        return self.defence
