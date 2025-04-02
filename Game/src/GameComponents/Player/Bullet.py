from __future__ import annotations

import ApplicationEngine.AppEngine as LNLEngine
from ApplicationEngine.include.Maths.Vector.Vector import Vec2, Vec3, Vec4
from ApplicationEngine.include.Maths.Matrix.Matrix import Mat2, Mat3, Mat4
from Game.src.GameComponents.Environement.Portal import *


from ApplicationEngine.src.Graphics.SpriteAnimationClass import *

import math

class Bullet(LNLEngine.GameObject2D):
    def _init_(self,hitBox : Vec2 = Vec2(1,1)):
        super().__init__() 

        bulletTexture = LNLEngine.Texture("Game/Assets/Sprites/Bullet_Shot.jpeg",False) 
        self.hitBox = hitBox * WorldGrid.GRID_SIZE 
        self.sprite = LNLEngine.Sprite(bulletTexture, self.body.position - self.hitBox/2, self.hitBox.x, self.hitBox.y)
        c = self._InitCollider( Vec2(WorldGrid.GRID_SIZE / 2, 20) )
        self.body.setCollider(c)


        self.ttl : float = 0 # how long the bullet has left before it despawns

    def _InitCollider(self, size : Vec2) -> LNLEngine.Collider2D:
        c1 = LNLEngine.AABB()
        c1.setRigidBody(self.body)
        c1.setSize(size)

        return c1
    
    def BeginPlay(self):
        # bullets arent affected by gravity 
        LNLEngine.Game.Get().GetPhysicsSystem2D().addRigidbody(self.body, False)


    def setHitBox(self, hBox : Vec2):
        self.hitBox = hBox
         
    def getHitBox(self):
        return self.hitBox 
    
    def _OnUpdate(self, deltatime: float):
        self.sprite.SetPos(self.body.getCollider().getLocalMin())# type: ignore
        self.sprite.SetRot(self.body.getRotation()) # type: ignore
        
    def Draw(self):
        self.sprite.Draw()