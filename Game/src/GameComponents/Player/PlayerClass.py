from __future__ import annotations

import ApplicationEngine.AppEngine as LNLEngine
from ApplicationEngine.include.Maths.Vector.Vector import Vec2, Vec3, Vec4
from ApplicationEngine.include.Maths.Matrix.Matrix import Mat2, Mat3, Mat4
from Game.src.GameComponents.Environement.Portal import *


from ApplicationEngine.src.Graphics.SpriteAnimationClass import *

import math



class CanTravelThroughPortals(LNLEngine.ObjectAttribute):
    # InPortalColision = False
    CollisionRegistry : dict[ LNLEngine.GameObjectBase, dict [str, bool] ]= {}
    @staticmethod
    def Attrib_OnAttach(obj: LNLEngine.GameObjectBase):
        CanTravelThroughPortals.CollisionRegistry[obj] = {"onframe" : False, "current" : False}

    @staticmethod
    def Attrib_OnUpdate(obj : Player): # type: ignore
        ...
    
    @staticmethod
    def Attrib_OnPhysicsUpdate(obj: LNLEngine.GameObjectBase):
        if not CanTravelThroughPortals.CollisionRegistry[obj]["onframe"]:
            CanTravelThroughPortals.CollisionRegistry[obj]["current"] = False


        CanTravelThroughPortals.CollisionRegistry[obj]["onframe"] = False


    @staticmethod
    def Attrib_OnContact(obj: LNLEngine.GameObjectBase, body: LNLEngine.RigidBody2D, otherOwner: LNLEngine.GameObjectBase, otherBody: LNLEngine.RigidBody2D):
        if not isinstance(otherOwner, Portal):
            return
        
        portal = otherOwner
        if not portal.IsActive():
            return
        

        CanTravelThroughPortals.CollisionRegistry[obj]["onframe"] = True
        if not LNLEngine.IntersectionDetector2D.pointInBox2D(body.getPosition(), otherBody.getCollider()): #type: ignore
            return
        

        if CanTravelThroughPortals.CollisionRegistry[obj]["current"]: # check if currently in a portal collision
            return
        
        positionOffset : Vec2 = body.getPosition() - otherBody.getPosition()

        totalRotation = portal.GetDestination().body.getRotation() -  portal.body.getRotation()

        currentPos = body.getPosition()
        currentVel = body.getVelocity()

        currentRot = body.getRotation()

        updatedPositionOffset = LNLEngine.LNLMAths.rotate_vec2(positionOffset, Vec2(0,0), math.degrees(totalRotation))

        # newPos : Vec2 = currentPos - portal.body.getPosition() + portal.GetDestination().body.getPosition() + updatedPositionOffset
        newPos : Vec2 = currentPos - portal.body.getPosition() + portal.GetDestination().body.getPosition() 
        newVel = LNLEngine.LNLMAths.reflectVec2(currentVel , LNLEngine.LNLMAths.rotate_vec2(Vec2(1,0),Vec2(0,0),math.degrees(portal.rotation)).normalize())
        newVel = LNLEngine.LNLMAths.rotate_vec2(newVel, Vec2(0,0), math.degrees(totalRotation))

        body.setTransform(newPos)
        body.setVelocity(newVel)

        CanTravelThroughPortals.CollisionRegistry[obj]["current"] = True






class PlayerState(Enum):

    standing    = auto()
    walking_l     = auto()
    walking_r     = auto()
    shooting    = auto()
    whiping     = auto()


    jumping     = auto()
    landing     = auto()

class Enemy:
    def __init__(self, position: Vec2, mass : float = 20 , name : str = ""):
        ...
    
    def Draw(self):
        ...

class Player(LNLEngine.GameObject2D):
    def __init__(self, position: Vec2 = Vec2(), mass : float = 70 , name : str = ""):
        super().__init__(position, mass = mass)
        self.SetAttribure(CanTravelThroughPortals)
        self.name = name

        self.width = 100
        self.height = 150

        self.speed  = Vec2(900, 0)
        self.jump   = Vec2(0, 50000)

        self.direction : float = 1

        self.inAir : bool = False


        self.lives      : int = 0
        self.health     : float = 2
        self.maxHealth  : float = 100


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
        

        self.keys = {}
        for kcode in LNLEngine.KEY_MAP:
            self.keys[kcode] = 0

        c1 : LNLEngine.Collider2D = LNLEngine.Box2D()
        # c1 : LNLEngine.Collider2D = LNLEngine.AABB()
        # c1 : LNLEngine.Collider2D = LNLEngine.Circle()
        c1.setSize( Vec2(self.width, self.height) )
        # c1.setRadius( self.height / 2 )
        c1.setRigidBody(self.body)
        self.body.setCollider(c1)
        self.body.linearDamping = 0.8


    def BeginPlay(self):
        super().BeginPlay()
            

    def _OnUpdate(self, deltatime : float):

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




        # self.currentBody.setPos(self.body.getPosition() - Vec2(math.sqrt(self.body.getCollider()._radius), math.sqrt(self.body.getCollider()._radius)))# type: ignore

    def SetPosition(self, pos : Vec2):
        self.body.setPosition(pos)

    def SetVelocity(self, vel : Vec2):
        self.body.setVelocity(vel)

    def _OnEvent(self, event : LNLEngine.Event):
        if event.GetName() == "KeyDown":
            self.keys[event.keycode] = 1

            if event.keycode == LNLEngine.KEY_MAP["space"]:
                self.body.addForce( -1 * self.jump * self.body.getMass())
        if event.GetName() == "KeyUp":
            self.keys[event.keycode] = 0
    

    def _OnCollision(self, body : LNLEngine.RigidBody2D, otherOwner : LNLEngine.GameObject2D, otherBody: LNLEngine.RigidBody2D, impulse: Vec2, manifold: LNLEngine.CollisionManifold):
        if isinstance(otherOwner , Enemy): ...
            # self.health -= Enemy.attack / Player.defence

    def Draw(self):
        self.currentBody.Draw()

class PlayerHud(LNLEngine.GameObject):
    def __init__(self, playerRef : Player, scale : int = 1):
        super().__init__()
        healthTexture = Texture("Game/Assets/Sprites/LNL_Health_positive.png", True)
        self.healthSprite = Sprite(healthTexture, Vec2(0,0), WorldGrid.GRID_SIZE / 2, WorldGrid.GRID_SIZE / 2)
        
        damageTexture = Texture("Game/Assets/Sprites/LNL_Health_negative.png", True)
        self.damageSprite = Sprite(damageTexture, Vec2(0,0), WorldGrid.GRID_SIZE / 2, WorldGrid.GRID_SIZE / 2)

        self.playerRef = playerRef

    def Draw(self):
        # TODO : modify huds to use a seperate camera so that the position moves with everything
        for i in range( int(self.playerRef.maxHealth) ):
            if i < self.playerRef.health:
                self.healthSprite.SetPos(Vec2(i * (WorldGrid.GRID_SIZE / 2) ,0))
                self.healthSprite.Draw()
            else:
                self.damageSprite.SetPos(Vec2(i * (WorldGrid.GRID_SIZE / 2) ,0))
                self.damageSprite.Draw()
        return super().Draw()