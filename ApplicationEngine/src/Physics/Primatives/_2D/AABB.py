from ApplicationEngine.src.Physics.RigidBody.RigidBody2D import *

from ApplicationEngine.src.Physics.Primatives._2D.Collider2D import *

class AABB(Collider2D):
    def __init__(self, _min: Vec2 = Vec2(0,0), _max: Vec2 = Vec2(1,1)):
        """ Axis Aligned Bounding Box

        Args:
            _min (Vec2): bottom left Position
            _max (Vec2): top right
        """


        self._size      : Vec2 = Vec2(*_max.get_p()) - _min
        self._halfSize  : Vec2 = self._size * 0.5
        # self._center    : Vec2 = Vec2(*_min.get_p()) + (Vec2(*_max.get_p()) * 0.5)

        self._rigidBody : RigidBody2D = RigidBody2D()


    def getLocalMin(self) -> Vec2:
        """get the bottom left corner of the AABB collider"""
        return self._rigidBody.getPosition() - self._halfSize  # position will be the centre of the collider

    def getHalfSize(self) -> Vec2:
        return self._halfSize
    def getSize(self) -> Vec2:
        return self._size
    
    def setSize(self, size : Vec2):
        self._size = Vec2(*size.get_p())
        self._halfSize = self._size / 2

    def getLocalMax(self) -> Vec2:
        """get the top right corner of the AABB collider"""
        return self._rigidBody.getPosition() + self._halfSize
    

    def getRigidBody(self) -> RigidBody2D:
        return self._rigidBody
    
    def setRigidBody(self, rb : RigidBody2D):
        self._rigidBody = rb