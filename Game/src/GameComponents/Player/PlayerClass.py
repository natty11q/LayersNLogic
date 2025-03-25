from __future__ import annotations

import ApplicationEngine.AppEngine as LNLEngine
from ApplicationEngine.include.Maths.Vector.Vector import Vec2, Vec3, Vec4
from ApplicationEngine.include.Maths.Matrix.Matrix import Mat2, Mat3, Mat4
from Game.src.GameComponents.Environement.Portal import *


from ApplicationEngine.src.Graphics.SpriteAnimationClass import *

import math

class PlayerInputHandlerAttribute(LNLEngine.ObjectAttribute):
    
    @staticmethod
    def Attrib_OnUpdate(obj : Player): # type: ignore
        obj._World_Position = Vec3(100 * math.sin(LNLEngine.LLEngineTime.Time()))
        # print("did sth")
        # PlayerInputHandlerAttribute.newMethod()
    

    @staticmethod
    def newMethod():...
        # print("newMeth")

class AffectedByGravityAttribute(LNLEngine.ObjectAttribute):
    GravitationalConstant = 9.81
    Gravity = Vec3(0, GravitationalConstant, 0)

    @staticmethod
    def Attrib_OnUpdate(obj : Player): # type: ignore
        ...
        # obj._World_Position = Vec3(100 * math.sin(LNLEngine.LLEngineTime.Time()))

        # obj.Velocity += AffectedByGravityAttribute.Gravity * LNLEngine.LLEngineTime.DeltaTime()
        # print("did sth")
        # PlayerInputHandlerAttribute.newMethod()


class CanTravelThroughPortals(LNLEngine.ObjectAttribute):
    # InPortalColision = False

    @staticmethod
    def Attrib_OnUpdate(obj : Player): # type: ignore
        # handle Portal here 
        # LNLEngine.LNL_LogInfo("checking Portal collision 1")
        for portal in Portal.portals:
            ## getting the halfway point between the vertices {simple impl for now to keep it simple}

            # LNLEngine.LNL_LogInfo("checking Portal collision ")
            # collided = False
            # if portal.intersectsPoint(obj._World_Position):
            #     collided = True
            # if portal.intersectsPoint(obj._World_Position + Vec3(obj.width)):
            #     collided = True
            # if portal.intersectsPoint(obj._World_Position + Vec3(0, obj.height)):
            #     collided = True
            # if portal.intersectsPoint(obj._World_Position + Vec3(obj.width, obj.height)):
            #     collided = True
            
            if portal.intersectsQuad([obj._World_Position.toVec2().get_p(), 
                                      (obj._World_Position.toVec2() + Vec2(obj.width)).get_p(),
                                    (obj._World_Position.toVec2() + Vec2(0, obj.height)).get_p()
                                    ,(obj._World_Position.toVec2() + Vec2(obj.width, obj.height)).get_p()]):

                
                # input()
                LNLEngine.LNL_LogInfo("Portal collision ")
                LNLEngine.LNL_LogInfo("lkinked? : ", portal.checkLink())

                if portal.checkLink() and not obj.InPortalColision and not obj.InPortalColisionOnFrame:                    
                    LNLEngine.LNL_LogInfo("Portal teleportation ")

                    offset : Vec2 = obj._World_Position.toVec2() - portal.vertices[0]

                    dest : Portal = portal.GetDestination()

                    normalisedDistRationOut_y : float = (offset.dot(portal.tangent.get_normalized()) * portal.tangent).length() / portal.alongVec.length()
                    normalisedDistRationOut_x : float = (offset.dot(portal.normal.get_normalized()) * portal.normal).length()  / portal.normal.length()

                    destOffsetOut = (dest.alongVec * normalisedDistRationOut_y) + (dest.normal * normalisedDistRationOut_x)
                    # destCenter = dest.vertices[0] + (dest.vertices[1] - dest.vertices[0]).multiply(0.5)
                    obj._World_Position = LNLEngine.Vec3(destOffsetOut[0] - (obj.width/2), destOffsetOut[1] - (obj.height/2))
                    

                   # normal should be normalised but i am dividing jsut in case 
                   # angle is in radians
                    angleRot = math.acos(portal.normal.dot(dest.normal) / (portal.normal.length() * dest.normal.length()))
                    oV = Vec2(obj.body.getVelocity()[0], obj.body.getVelocity()[1]) * Mat2([
                                                                        [math.cos(-angleRot) , -math.sin(-angleRot)],
                                                                        [math.sin(-angleRot) , math.cos(-angleRot)]
                                                                            ])
                    
                    obj.body.setVelocity( Vec3(*oV.get_p()).toVec2() )

                obj.InPortalColisionOnFrame = True
                





class PlayerState(Enum):

    standing    = auto()
    walking_l     = auto()
    walking_r     = auto()
    shooting    = auto()
    whiping     = auto()


    jumping     = auto()
    landing     = auto()



class Player(LNLEngine.GameObject2D):
    def __init__(self, name : str):
        super().__init__(mass= 70)
        # self.SetAttribure(PlayerInputHandlerAttribute)

        # self.SetAttribure(AffectedByGravityAttribute)
        # self.SetAttribure(CanTravelThroughPortals)
        self.name = name


        # self.Velocity = Vec3()
        self.Colour = Vec4(0,0,255,255)
        # self._World_Position = Vec3(7

        self.width = 100
        self.height = 100

        self.speed  = 100


        self.InPortalColision = False
        self.InPortalColisionOnFrame = False



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

        tex = LNLEngine.Texture("Game/Assets/Sprites/Larx_Walk.jpeg", True)
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



        # set manually for now
        self.animations : dict [str , SpriteAnimation] = {
            "standing"  : guyStand,
            "walking"   : guyWalk,
            "shooting"  : guyShoot,
            "whiping"   : guyWhip,
        }
        self.currentBody : SpriteAnimation = self.animations["standing"]


        self.playerState : PlayerState = PlayerState.standing
        

        self.keys = {}
        for kcode in LNLEngine.KEY_MAP:
            self.keys[kcode] = 0


        self.body.linearDamping = 0.8
        LNLEngine.Game.Get().GetPhysicsSystem2D().addRigidbody(self.body, False)

    def _OnUpdate(self, deltatime : float):
        # LNLEngine.LNL_LogEngineInfo(self._World_Position)
        self.InPortalColision = self.InPortalColisionOnFrame
        self.InPortalColisionOnFrame = False
        
        self.playerState : PlayerState = PlayerState.standing

        force : Vec2 = Vec2()

        inputVector : Vec2 = Vec2()

        if self.keys.get(LNLEngine.KEY_MAP['right']):
            inputVector += Vec2(1, 0)

        if self.keys.get(LNLEngine.KEY_MAP['left']):
            inputVector += Vec2(-1, 0)

        if self.keys.get(LNLEngine.KEY_MAP['up']):
            inputVector += Vec2(0, 1)

        if self.keys.get(LNLEngine.KEY_MAP['down']):
            inputVector += Vec2(0, -1)


        inputVector = inputVector.normalize()
        force += inputVector * self.speed * self.body.getMass()
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


        self.currentBody.Update(deltatime)
        self.currentBody.Play()


    def _OnEvent(self, event : LNLEngine.Event):
        if event.GetName() == "KeyDown":
            self.keys[event.keycode] = 1
        if event.GetName() == "KeyUp":
            self.keys[event.keycode] = 0
    
    def Draw(self):

        # LNLEngine.Quad(Vec2(self._World_Position[0],self._World_Position[1]), self.width, self.height, self.Colour).Draw()
        # LNLEngine.Renderer.DrawTriangle([pos,pos2 , Vec2(200,400)], Vec4(100, 200, 255, 255))
        # LNLEngine.Renderer.DrawTriangle([Vec2(200,10),Vec2(100,800) , Vec2(700,4)], Vec4(100, 200, 80, 255))

        self.currentBody.setPos(self.body.getPosition() )
        self.currentBody.Draw()