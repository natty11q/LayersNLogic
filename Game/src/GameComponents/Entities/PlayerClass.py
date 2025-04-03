from __future__ import annotations

import ApplicationEngine.AppEngine as LNLEngine
from ApplicationEngine.include.Maths.Vector.Vector import Vec2, Vec3, Vec4
from ApplicationEngine.include.Maths.Matrix.Matrix import Mat2, Mat3, Mat4
from Game.src.GameComponents.Environement.Portal import *


from ApplicationEngine.src.Graphics.SpriteAnimationClass import *
from Game.src.GameComponents.Environement.Attributes.CanTravelThroughPortals import *
import math

from Game.src.GameComponents.Environement.Environment import *

from Game.src.GameComponents.Entities.EntityClass import *
from Game.src.GameComponents.Entities.EnemyClass import *


class PlayerData:
    def __init__(self):
        self.score : float = 1000
        self.lives : int = 3


class PlayerStates(EntityStates):
    RUNNING     = auto()
    WALKING     = auto()
    RUNNING     = auto()
    SHOOTING    = auto()
    MELE        = auto()

class PlayerState(Enum):

    standing    = auto()
    walking_l     = auto()
    walking_r     = auto()
    shooting    = auto()
    whiping     = auto()


    jumping     = auto()
    landing     = auto()



class Player(Entity):
    def __init__(self, position: Vec2 = Vec2(), mass : float = 70.0 , name : str = "" , playerHud : PlayerHud | None = None):
        self.name = name
        self.width = 100
        self.height = 150
        super().__init__(Vec2(self.width, self.height), position, mass, name)

        self.SetAttribure(CanTravelThroughPortals)

        self.speed  = Vec2(900, 0)
        self.jump   = Vec2(0, 1500)

        self.direction : float = 1

        self.inGrounded : bool = True

        self.HitStunTimer = 0.0
        self.MaxHiststun_s = 0.5
        self.flashtimerMax = 0.5 / 10
        self.flashtimer = self.flashtimerMax

        self.shouldDrawOnHiststun = True


        self.lives      : int = 0


        tex = LNLEngine.Texture("Game/Assets/Sprites/Larx_Stand.png", True)
        r = 1
        c = 1
        s = 0.2
        guyStand = LNLEngine.SpriteAnimation.LoadFromSpritesheet(tex,
                                                                     r, c,
                                                                     self.width,self.height, 
                                                                     framerate=24,
                                                                     repeat= True)
        

        tex = LNLEngine.Texture("Game/Assets/Sprites/Larx_whip.jpeg", True)
        r = 12
        c = 1
        s = 0.32
        guyWhip = LNLEngine.SpriteAnimation.LoadFromSpritesheet(tex,
                                                                     r, c,
                                                                     self.width,self.height, 
                                                                     framerate=24,
                                                                     repeat= True)

        # tex = LNLEngine.Texture("Game/Assets/Sprites/Larx_Walk.jpeg", True)
        tex = LNLEngine.Texture("Game/Assets/Sprites/Larx_Run.png", True)
        r = 4
        c = 1
        s = 0.32
        guyWalk = LNLEngine.SpriteAnimation.LoadFromSpritesheet(tex,
                                                                     r, c,
                                                                     self.width,self.height, 
                                                                     framerate=24,
                                                                     repeat= True)

        tex = LNLEngine.Texture("Game/Assets/Sprites/Larx_Shoot.jpeg", True)
        r = 12
        c = 1
        s = 0.9
        guyShoot = LNLEngine.SpriteAnimation.LoadFromSpritesheet(tex,
                                                                     r, c,
                                                                     self.width,self.height, 
                                                                     framerate=24,
                                                                     repeat= True)
        tex = LNLEngine.Texture("Game/Assets/Sprites/guyjump.png", True)
        r = 5
        c = 1
        s = 0.9
        guyJump = LNLEngine.SpriteAnimation.LoadFromSpritesheet(tex,
                                                                     r, c,
                                                                     self.width,self.height, 
                                                                     framerate=24,
                                                                     repeat= True)



        # set manually for now
        self.animations : dict [str , SpriteAnimation] = {
            "standing"  : guyStand,
            "walking"   : guyWalk,
            "shooting"  : guyShoot,
            "whiping"   : guyWhip,
            "jumping"   : guyJump,
        }
        self.currentBody : SpriteAnimation = self.animations["standing"]


        self.playerState : PlayerState = PlayerState.standing
        self.isDead = False

        self.keys = {}
        for kcode in LNLEngine.KEY_MAP:
            self.keys[kcode] = 0

        self.playerHud = playerHud

    def BeginPlay(self):
        super().BeginPlay()
    



    def GetHud(self) -> PlayerHud | None:
        return self.playerHud

    def _OnUpdate(self, deltatime : float):
        self.isGrounded = False

        if self.HitStunTimer > 0:
            self.HitStunTimer -= deltatime
            self.flashtimer -= deltatime

        self.playerState : PlayerState = PlayerState.standing
        force : Vec2 = Vec2()
        inputVector : Vec2 = Vec2()

        if self.keys.get(LNLEngine.KEY_MAP['right']):

            inputVector += Vec2(1, 0)

            self.direction = 1
        if self.keys.get(LNLEngine.KEY_MAP['left']):
            inputVector += Vec2(-1, 0)
            self.direction = -1

        # if self.keys.get(LNLEngine.KEY_MAP['up']):
        #     inputVector += Vec2(0, -1)

        # if self.keys.get(LNLEngine.KEY_MAP['down']):
        #     inputVector += Vec2(0, 1)


        inputVector = inputVector.normalize()
        force += Vec2(inputVector[0] * self.speed[0] * self.body.getMass(), inputVector[1] * self.jump[1] * self.body.getMass())
        self.body.addForce(force)


        if inputVector.dot(Vec2(1,0)) > 0:
            self.playerState = PlayerState.walking_r
        elif inputVector.dot(Vec2(1,0)) < 0:
            self.playerState = PlayerState.walking_l
        
        


        if self.playerState == PlayerState.standing:
            self.currentBody : SpriteAnimation = self.animations["standing"]
        
        if self.playerState == PlayerState.walking_r:
            self.currentBody : SpriteAnimation = self.animations["walking"]

        if self.playerState == PlayerState.walking_l:
            self.animations["walking"].Flip_lr()
            self.currentBody : SpriteAnimation = self.animations["walking"]
        
        if self.playerState == PlayerState.whiping:
            self.currentBody : SpriteAnimation = self.animations["shooting"]
        
        if self.playerState == PlayerState.shooting:
            self.currentBody : SpriteAnimation = self.animations["whiping"]

        if self.playerState == PlayerState.jumping:
            self.currentBody : SpriteAnimation = self.animations["jumping"]


        self.currentBody.setPos(self.body.getCollider().getLocalMin())# type: ignore
        self.currentBody.setRot(self.body.getRotation()) # type: ignore
        
        self.currentBody.Update(deltatime)
        self.currentBody.Play()


        if self.CurrentHealth <= 0:
            self.isDead = True




        # self.currentBody.setPos(self.body.getPosition() - Vec2(math.sqrt(self.body.getCollider()._radius), math.sqrt(self.body.getCollider()._radius)))# type: ignore

    def SetPosition(self, pos : Vec2):
        self.body.setPosition(pos)

    def SetVelocity(self, vel : Vec2):
        self.body.setVelocity(vel)

    def _OnEvent(self, event : LNLEngine.Event):
        if event.GetName() == "KeyDown":
            self.keys[event.keycode] = 1

            if event.keycode == LNLEngine.KEY_MAP["left"]:
                    if self.body.getVelocity().x > 0:
                        self.body.setVelocity(Vec2(0,self.body.getVelocity().y))
            if event.keycode == LNLEngine.KEY_MAP["right"]:
                    if self.body.getVelocity().x < 0:
                        self.body.setVelocity(Vec2(0,self.body.getVelocity().y))
                    
        
            if event.keycode == LNLEngine.KEY_MAP["space"]:
                # self.body.addForce( -1 * self.jump * self.body.getMass())
                if self.isGrounded:
                    self.body.addImpulse( -1 * self.jump * self.body.getMass())
        if event.GetName() == "KeyUp":
            self.keys[event.keycode] = 0 
    
            if event.keycode == LNLEngine.KEY_MAP["left"]:
                    self.body.setVelocity(Vec2(0,self.body.getVelocity().y))
            if event.keycode == LNLEngine.KEY_MAP["right"]:                
                    self.body.setVelocity(Vec2(0,self.body.getVelocity().y))
                    


    def _OnCollision(self, body : LNLEngine.RigidBody2D, otherOwner : LNLEngine.GameObject2D, otherBody: LNLEngine.RigidBody2D, impulse: Vec2, manifold: LNLEngine.CollisionManifold):
        if isinstance(otherOwner , (TileChunk, EnvironmentObject2D) ):
            self.isGrounded = True
            if isinstance(otherOwner , EnvironmentObject2D):
                if isinstance(body.getCollider(), LNLEngine.Box2D):
                    if body.position.y + 100 < otherBody.position.y: 
                        # body.linearVelocity = otherBody.linearVelocity
                        body.addForce(Vec2(otherBody.forceAccum.x,0))

        if isinstance(otherOwner , Enemy):
            if self.HitStunTimer <= 0:
                self.CurrentHealth -= otherOwner.attack / self.defence
                self.HitStunTimer = self.MaxHiststun_s

    def Draw(self):
        if self.HitStunTimer > 0:
            if self.shouldDrawOnHiststun:
                self.currentBody.Draw()
                self.flashtimer 

            if self.flashtimer <= 0:
                self.shouldDrawOnHiststun = not self.shouldDrawOnHiststun
                self.flashtimer = self.flashtimerMax
        else:
            self.currentBody.Draw()

class PlayerHud(LNLEngine.GameObject):
    def __init__(self, playerRef : Player, playerData : PlayerData, scale : int = 1):
        super().__init__()
        healthTexture = Texture("Game/Assets/Sprites/LNL_Health_positive.png", True)
        self.healthSprite = Sprite(healthTexture, Vec2(0,0), WorldGrid.GRID_SIZE / 2, WorldGrid.GRID_SIZE / 2)
        
        damageTexture = Texture("Game/Assets/Sprites/LNL_Health_negative.png", True)
        self.damageSprite = Sprite(damageTexture, Vec2(0,0), WorldGrid.GRID_SIZE / 2, WorldGrid.GRID_SIZE / 2)
        
        UIBar = Texture("Game/Assets/Sprites/uibar.png", False)
        self.UIBarSprite = Sprite(UIBar, Vec2(0,0), 900, WorldGrid.GRID_SIZE * 1.2 )

        self.playerRef = playerRef
        self.playerDataRef = playerData

        # self.timer = LNLEngine.Temporal.LLEngineTime.StartTimerMs()
        self.startTime = LNLEngine.Temporal.LLEngineTime.Time()

    def _OnUpdate(self, deltatime: float):
        self.playerDataRef.score -= deltatime * 2.3125467  # arbritrary multiplier to desync from time
        if self.playerDataRef.score < 0:
            self.playerDataRef.score = 0

    def Draw(self):
        # TODO : modify huds to use a seperate camera so that the position moves with everything

        self.UIBarSprite.Draw()

        for i in range( int(self.playerRef.MaxHealth) ):
            if i < self.playerRef.CurrentHealth:
                self.healthSprite.SetPos(Vec2(i * (WorldGrid.GRID_SIZE / 2) , WorldGrid.GRID_SIZE * 1.2))
                self.healthSprite.Draw()
            else:
                self.damageSprite.SetPos(Vec2(i * (WorldGrid.GRID_SIZE / 2) , WorldGrid.GRID_SIZE * 1.2))
                self.damageSprite.Draw()


        Renderer.DrawText(str(self.playerDataRef.lives), Vec2(170, 45), 24, Vec3(255,255,255))
        # Renderer.DrawText(str(int(LNLEngine.Temporal.LLEngineTime.GetTimerValue(self.timer))), Vec2(470, 45), 24, Vec3(255,255,255))
        Renderer.DrawText(str(int(LNLEngine.Temporal.LLEngineTime.Time() - self.startTime)), Vec2(470, 45), 24, Vec3(255,255,255))
        Renderer.DrawText(str(int(self.playerDataRef.score)), Vec2(730, 45), 24, Vec3(255,255,255))
        return super().Draw()