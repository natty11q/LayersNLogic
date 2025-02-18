from ApplicationEngine.include.Maths.Vector.Vector import *

class Quat:
    def __init__(self, x:float=0.0, y:float=0.0, z:float=0.0, w:float=0.0):
        self.x, self.y, self.z, self.w = x, y, z, w

    def __repr__(self):
        return f"Quat({self.x}, {self.y}, {self.z}, {self.w})"
    
    def __add__(self, other):
        if isinstance(other, Quat):
            return Quat(self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w)
        raise TypeError("Can only add Quat to Quat")
    
    def __mul__(self, other):
        if isinstance(other, Quat):  # Quaternion multiplication
            x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
            y = self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x
            z = self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w
            w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
            return Quat(x, y, z, w)
        raise TypeError("Can only multiply Quat by Quat")
    
    def norm(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2 + self.w**2)
    
    def normalize(self):
        n = self.norm()
        if n == 0:
            raise ValueError("Cannot normalize a zero quaternion")
        return Quat(self.x / n, self.y / n, self.z / n, self.w / n)
    
    def to_vec(self):
        """Convert quaternion to Vec3 (drop w) or Vec4"""
        if self.w == 0:
            return Vec3(self.x, self.y, self.z)
        return Vec4(self.x, self.y, self.z, self.w)
