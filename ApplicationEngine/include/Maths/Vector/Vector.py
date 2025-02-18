from __future__ import annotations
import math

## TODO: Extend




# The Vector class
class Vector:

    # Initialiser
    def __init__(self, x : float = 0, y : float = 0):
        self.x : float = x
        self.y : float = y

    def _OnUpdate(self): ...

    # Returns a string representation of the vector
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    # Tests the equality of this vector and another
    def __eq__(self, other : Vector) -> bool:  # type: ignore
        return self.x == other.x and self.y == other.y

    # Tests the inequality of this vector and another
    def __ne__(self, other : Vector) -> bool:  # type: ignore
        return not self.__eq__(other)

    # Returns a tuple with the point corresponding to the vector
    def get_p(self) -> tuple [float, ...]:
        return (self.x, self.y)

    # Returns a copy of the vector
    def copy(self) -> Vector:
        return Vector(self.x, self.y)

    # Adds another vector to this vector
    def add(self, other : Vector) -> Vector:
        self.x += other.x
        self.y += other.y
        
        self._OnUpdate()
        return self

    def __add__(self, other : Vector) -> Vector:
        return self.copy().add(other)
    
        self._OnUpdate()

    # Negates the vector (makes it point in the opposite direction)
    def negate(self) -> Vector:
        
        self.multiply(-1)
        self._OnUpdate()
        return self

    def __neg__(self) -> Vector:
        return self.copy().negate()

    # Subtracts another vector from this vector
    def subtract(self, other : Vector):
        return self.add(-other)

    def __sub__(self, other : Vector) -> Vector:
        return self.copy().subtract(other)

    # Multiplies the vector by a scalar
    def multiply(self, k : float) -> Vector:
        self.x *= k
        self.y *= k
        self._OnUpdate()
        return self

    def __mul__(self, k : float) -> Vector:
        return self.copy().multiply(k)

    def __rmul__(self, k : float) -> Vector:
        return self.copy().multiply(k)

    # Divides the vector by a scalar
    def divide(self, k : float) -> Vector:
        return self.multiply(1/k)

    def __truediv__(self, k : float) -> Vector:
        return self.copy().divide(k)

    # Normalizes the vector
    def normalize(self) -> Vector:
        return self.divide(self.length())

    # Returns a normalized version of the vector
    def get_normalized(self) -> Vector:
        return self.copy().normalize()

    # Returns the dot product of this vector with another one
    def dot(self, other : Vector) -> float:
        return self.x * other.x + self.y * other.y

    # Returns the length of the vector
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    # Returns the squared length of the vector
    def length_squared(self):
        return self.x**2 + self.y**2

    # Reflect this vector on a normal
    def reflect(self, normal : Vector) -> Vector:
        n = normal.copy()
        n.multiply(2*self.dot(normal))
        self.subtract(n)
        return self

    # Returns the angle between this vector and another one
    def angle(self, other : Vector) -> float | None:
        return math.acos(self.dot(other) / (self.length() * other.length()))

    # Rotates the vector 90 degrees anticlockwise
    def rotate_anti(self) -> Vector | None:
        self.x, self.y = -self.y, self.x
        return self

    # Rotates the vector according to an angle theta given in radians
    def rotate_rad(self, theta : float) -> Vector | None:
        rx = self.x * math.cos(theta) - self.y * math.sin(theta)
        ry = self.x * math.sin(theta) + self.y * math.cos(theta)
        self.x, self.y = rx, ry
        return self

    # Rotates the vector according to an angle theta given in degrees
    def rotate(self, theta : float) -> Vector | None:
        theta_rad = theta / 180 * math.pi
        return self.rotate_rad(theta_rad)
    
    # project the vector onto a given vector
    def get_proj(self, vec : Vector)-> Vector | None:
        unit = vec.get_normalized()
        return unit.multiply(self.dot(unit))


# Modified Vector class
class __Vector(Vector):

    def __init__(self, *args : float):
        self._m_vec : list [float] = []
        self._m_size = len(self._m_vec)
        for arg in args:
            self._m_vec.append(arg)

    # Returns a string representation of the vector
    def __str__(self):
        out = "("
        for value in self._m_vec:
            out += str(value)
            out += ", "
        out += ")"
        
        return out

    # Tests the equality of this vector and another
    def __eq__(self, other : __Vector) -> bool: # type: ignore
        if self._m_size != other.size(): return False
        
        equal : bool = True
        for i in range(self._m_size):
            equal = equal & (self._m_vec[i] == other[i])
        return equal

    # Tests the inequality of this vector and another
    def __ne__(self, other : __Vector): # type: ignore
        return not self.__eq__(other)

    # Returns a tuple with the point corresponding to the vector
    def get_p(self) -> tuple [float , ...]:
        return tuple(self._m_vec)

    # Returns a copy of the vector
    def copy(self) -> Vector:
        return __Vector(*self._m_vec)

    # Adds another vector to this vector
    def add(self, other : __Vector): # type: ignore
        assert (self._m_size != other.size()), f"Attempted to add two incompatable vector types sizes: {self._m_size} {other.size()}"
        
        for i in range(self._m_size):
            self._m_vec[i] += other[i]
        
        self._OnUpdate()
        return self
    
    def size(self):
        return self._m_size

    # Multiplies the vector by a scalar
    def multiply(self, k : float) -> Vector:
        for i in range(self._m_size):
            self._m_vec[i] *= k
        self._OnUpdate()
        return self


    def __getitem__(self, index : int):
        assert ( index > 0 and index < self._m_size ), f"list index out of range for vector of size {self._m_size}"
        return self._m_vec[index]  

    def __setitem__(self, index : int, value : float):
        self._m_vec[index] = value
        self._OnUpdate()

    # Returns the dot product of this vector with another one
    def dot(self, other : __Vector): # type: ignore
        assert (self._m_size != other.size()), f"Attempted to multiply two incompatable vector types sizes: {self._m_size} {other.size()}"
        dotP = 0
        for i in range(self._m_size):
            dotP += self._m_vec[i] * other[i]
        
        self._OnUpdate()
        return dotP
        

    # Returns the length of the vector
    def length(self):
        
        return math.sqrt(self.length_squared())

    # Returns the squared length of the vector
    def length_squared(self):
        SquareSum = 0
        for value in self._m_vec:
            SquareSum += value**2
        return SquareSum

    

    # Returns the angle between this vector and another one
    def angle(self, other : Vector) -> None:
        print("not applicabe to this vector impl")

    # Rotates the vector 90 degrees anticlockwise
    def rotate_anti(self):
        print("not applicabe to this vector impl")

    # Rotates the vector according to an angle theta given in radians
    def rotate_rad(self, theta : float):
        print("not applicabe to this vector impl")

    # Rotates the vector according to an angle theta given in degrees
    def rotate(self, theta : float):
        print("not applicabe to this vector impl")
    
    # project the vector onto a given vector
    def get_proj(self, vec : Vector):
        print("not applicabe to this vector impl")
        


class Vec2(__Vector):
    def __init__(self, x:float=0, y:float=0):
        super().__init__(x, y)
        self._OnUpdate()
    
    
        
    def _OnUpdate(self) -> None:
        self.x : float = self._m_vec[0]
        self.y : float = self._m_vec[1]
        
        self.re : float = self._m_vec[0]
        self.im : float = self._m_vec[1]
        
    def __sizeof__(self) -> int:
        return super().__sizeof__()
    
    
    def __getattr__(self, name):
        """Allows swizzling (e.g., vec.xy, vec.yzx, etc.)"""
        mapping = {'x': 0, 'y': 1, 'r': 0, 'i': 1}
        if all(c in mapping for c in name):
            indices = [mapping[c] for c in name]
            values  = [self._m_vec[i] for i in indices if i < len(self._m_vec)]
            return Vector(*values) if len(values) > 1 else values[0]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")



class Vec3(__Vector):
    def __init__(self, x:float=0 , y:float=0, z:float=0):
        super().__init__(x , y , z)
        self._OnUpdate()
    
    def _OnUpdate(self) -> None:
        self.x : float = self._m_vec[0]
        self.y : float = self._m_vec[1]
        self.z : float = self._m_vec[2]
        
        
        self.r : float = self._m_vec[0]
        self.g : float = self._m_vec[1]
        self.b : float = self._m_vec[2]

    def toVec2(self):
        return Vec3(self.x, self.y)
    
    def __getattr__(self, name):
        """Allows swizzling (e.g., vec.xy, vec.yzx, etc.)"""
        mapping = {'x': 0, 'y': 1, 'z': 2, 'r': 0, 'g': 1, 'b': 2}
        if all(c in mapping for c in name):
            indices = [mapping[c] for c in name]
            values  = [self._m_vec[i] for i in indices if i < len(self._m_vec)]
            return Vector(*values) if len(values) > 1 else values[0]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")


class Vec4(__Vector):
    def __init__(self, x:float = 0, y:float = 0, z:float = 0, w:float = 0):
        super().__init__(x, y, z, w)
        self._OnUpdate()
    
    def _OnUpdate(self) -> None:
        self.x : float = self._m_vec[0]
        self.y : float = self._m_vec[1]
        self.z : float = self._m_vec[2]
        self.w : float = self._m_vec[3]


        self.r : float = self._m_vec[0]
        self.g : float = self._m_vec[1]
        self.b : float = self._m_vec[2]
        self.a : float = self._m_vec[3]

    def __getattr__(self, name):
        """Allows swizzling (e.g., vec.xy, vec.yzx, etc.)"""
        mapping = {'x': 0, 'y': 1, 'z': 2, 'w': 3, 'r': 0, 'g': 1, 'b': 2, 'a': 3}
        if all(c in mapping for c in name):
            indices = [mapping[c] for c in name]
            values  = [self._m_vec[i] for i in indices if i < len(self._m_vec)]
            return Vector(*values) if len(values) > 1 else values[0]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
    
    def toVec3(self):
        return Vec3(self.x, self.y, self.z)

class Color(Vec4):
    def __init__(self, x:float = 255, y:float = 255, z:float = 255, w:float = 255):
        super().__init__(x, y, z, w)
        self._OnUpdate()