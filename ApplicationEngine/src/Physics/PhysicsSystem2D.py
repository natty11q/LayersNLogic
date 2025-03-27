from ApplicationEngine.src.Physics.Forces.ForceRegistry import *
from ApplicationEngine.include.Maths.Maths import *
from ApplicationEngine.src.Core.Utility.Temporal import *


from ApplicationEngine.src.Physics.Forces.Gravity2D import *

from ApplicationEngine.src.Physics.RigidBody.CollisionManifold import CollisionManifold
from ApplicationEngine.src.Physics.RigidBody.Collisions import *
from ApplicationEngine.src.Physics.RigidBody.IntersectionDetector2D import *

from ApplicationEngine.src.Physics.Primatives._2D.Collider2D import *

class PhysicsSystem2D:
    def __init__(self, gravity : Vec2):

        self.forceRegistry : ForceRegistry   = ForceRegistry()
        self.gravity : Gravity2D = Gravity2D(gravity)

        self.rigidBodies : list[RigidBody2D] = []
        self.bodies1 : list[RigidBody2D] = []
        self.bodies2 : list[RigidBody2D] = []
        self.collisions : list[CollisionManifold] = []

        self.inpulseIterations = 6


    def update(self, dt : float):
        self.fixedUpdate()

    def fixedUpdate(self):
        frame_tick_delta = 1/LLEngineTime.TickRate() # just incase the tick rate is set on the main thread casing inconsitiency
        
        self.bodies1.clear()
        self.bodies2.clear()
        self.collisions.clear()


        size = len(self.rigidBodies)

        for i in range(size):
            for j in range(i+1, size):
                # if i == j: continue

                result : CollisionManifold = CollisionManifold()

                r1 : RigidBody2D = self.rigidBodies[i]
                r2 : RigidBody2D = self.rigidBodies[j]

                c1 : Collider2D | None = r1.getCollider()
                c2 : Collider2D | None = r2.getCollider()

                if c1 and c2 and not (r1.hasInfiniteMass() and r2.hasInfiniteMass() ):
                    result = Collisions.findCollisionFeatures(c1 , c2)
                
                if result and result.isColliding():
                    self.bodies1.append(r1)
                    self.bodies2.append(r2)

                    percent = 0.18   # usually between 0.2 and 0.8, fraction of penetration to correct per frame.
                    slop = 0.01     # small penetration allowance (to avoid jittering).

                    total_inverse_mass = r1.getinverseMass() + r2.getinverseMass()
                    if total_inverse_mass == 0:
                        return

                    # Compute the amount of penetration to correct.
                    correction_magnitude = max(result.depth - slop, 0.0) / total_inverse_mass * percent
                    correction = result.normal * correction_magnitude

                    
                    if r1.hasInfiniteMass():
                        r2.setPosition( r2.getPosition() + correction * total_inverse_mass )
                    elif not r2.hasInfiniteMass():
                        r1.setPosition( r1.getPosition() - correction * total_inverse_mass )
                    else:
                        r1.setPosition( r1.getPosition() - correction * r1.inverseMass )
                        r2.setPosition( r2.getPosition() + correction * r2.inverseMass )

                    self.collisions.append(result)

        # find any collisions    
        self.forceRegistry.updateForces(frame_tick_delta)

        for k in range(self.inpulseIterations):
            for i in range(len(self.collisions)):
                jSize = len(self.collisions[i].getContactPoints())
                for j in range(jSize):
                    r1 : RigidBody2D = self.bodies1[i]
                    r2 : RigidBody2D = self.bodies2[i]

                    self.applyInpulse(r1, r2, self.collisions[i])

        # resolve collisions


        for i in range(len(self.rigidBodies)):
            self.rigidBodies[i].physicsUpdate(frame_tick_delta)

    def applyInpulse(self, a : RigidBody2D, b : RigidBody2D, m : CollisionManifold):
        invMass1 : float = a.getinverseMass()
        invMass2 : float = b.getinverseMass()

        invMassSum : float  = invMass1 + invMass2

        if (invMassSum == 0.0): return
        

        relativeVel : Vec2 = b.getVelocity() - a.getVelocity()
        relativeNormal : Vec2 = m.getNormal().get_normalized()

        if relativeVel.dot(relativeNormal) > 0.0:
            return
        
        e : float = min(a.getCoefficientOfRestitution(), b.getCoefficientOfRestitution())

        numerator : float = (-(1.0 + e) * relativeVel.dot(relativeNormal))

        j : float = numerator / invMassSum

        # if len(m.getContactPoints()) > 0 and j != 0.0:
        #     j /= len(m.getContactPoints())
        
        impulse : Vec2 = relativeNormal * j
        a.setVelocity( a.getVelocity() + (impulse * invMass1) *  -1)
        b.setVelocity( b.getVelocity() + (impulse * invMass2) *  1)



    def addRigidbody(self, body : RigidBody2D, addGravity : bool = False):
        self.rigidBodies.append(body)

        if addGravity:
            self.forceRegistry.add(body, self.gravity)
        # body.init()
