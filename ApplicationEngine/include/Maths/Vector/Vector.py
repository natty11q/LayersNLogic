import math

## TODO: Extend





# The Vector class
class Vector:

    # Initialiser
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    # Returns a string representation of the vector
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    # Tests the equality of this vector and another
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # Tests the inequality of this vector and another
    def __ne__(self, other):
        return not self.__eq__(other)

    # Returns a tuple with the point corresponding to the vector
    def get_p(self):
        return (self.x, self.y)

    # Returns a copy of the vector
    def copy(self):
        return Vector(self.x, self.y)

    # Adds another vector to this vector
    def add(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __add__(self, other):
        return self.copy().add(other)

    # Negates the vector (makes it point in the opposite direction)
    def negate(self):
        return self.multiply(-1)

    def __neg__(self):
        return self.copy().negate()

    # Subtracts another vector from this vector
    def subtract(self, other):
        return self.add(-other)

    def __sub__(self, other):
        return self.copy().subtract(other)

    # Multiplies the vector by a scalar
    def multiply(self, k):
        self.x *= k
        self.y *= k
        return self

    def __mul__(self, k):
        return self.copy().multiply(k)

    def __rmul__(self, k):
        return self.copy().multiply(k)

    # Divides the vector by a scalar
    def divide(self, k):
        return self.multiply(1/k)

    def __truediv__(self, k):
        return self.copy().divide(k)

    # Normalizes the vector
    def normalize(self):
        return self.divide(self.length())

    # Returns a normalized version of the vector
    def get_normalized(self):
        return self.copy().normalize()

    # Returns the dot product of this vector with another one
    def dot(self, other):
        return self.x * other.x + self.y * other.y

    # Returns the length of the vector
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    # Returns the squared length of the vector
    def length_squared(self):
        return self.x**2 + self.y**2

    # Reflect this vector on a normal
    def reflect(self, normal):
        n = normal.copy()
        n.multiply(2*self.dot(normal))
        self.subtract(n)
        return self

    # Returns the angle between this vector and another one
    def angle(self, other):
        return math.acos(self.dot(other) / (self.length() * other.length()))

    # Rotates the vector 90 degrees anticlockwise
    def rotate_anti(self):
        self.x, self.y = -self.y, self.x
        return self

    # Rotates the vector according to an angle theta given in radians
    def rotate_rad(self, theta):
        rx = self.x * math.cos(theta) - self.y * math.sin(theta)
        ry = self.x * math.sin(theta) + self.y * math.cos(theta)
        self.x, self.y = rx, ry
        return self

    # Rotates the vector according to an angle theta given in degrees
    def rotate(self, theta):
        theta_rad = theta / 180 * math.pi
        return self.rotate_rad(theta_rad)
    
    # project the vector onto a given vector
    def get_proj(self, vec):
        unit = vec.get_normalized()
        return unit.multiply(self.dot(unit))


# Modified Vector class
class __Vector(Vector):

    # Initialiser
    def __init__(self, *args : list [float]):
        self.__m_vec = []
        self.__m_size = len(self.__m_vec)
        for arg in args:
            self.__m_vec.append(arg)

    # Returns a string representation of the vector
    def __str__(self):
        out = "("
        for value in self.__m_vec:
            out += value
            out += ", "
        out += ")"
        
        return out

    # Tests the equality of this vector and another
    def __eq__(self, other):
        if self.__m_size != other.size(): return False
        
        equal = True
        for i in range(self.__m_size):
            equal *= (self.__m_vec[i] == other[i])
        return equal

    # Tests the inequality of this vector and another
    def __ne__(self, other):
        return not self.__eq__(other)

    # Returns a tuple with the point corresponding to the vector
    def get_p(self):
        return tuple(self.__m_vec)

    # Returns a copy of the vector
    def copy(self):
        return __Vector(*self.__m_vec)

    # Adds another vector to this vector
    def add(self, other):
        assert (self.__m_size != other.size()), f"Attempted to add two incompatable vector types sizes: {self.__m_size} {other.size()}"
        
        for i in range(self.__m_size):
            self.__m_vec[i] += other[i]
        
        return self
    
    def size(self):
        return self.__m_size

    # Multiplies the vector by a scalar
    def multiply(self, other):
        assert (self.__m_size != other.size()), f"Attempted to multiply two incompatable vector types sizes: {self.__m_size} {other.size()}"
        
        for i in range(self.__m_size):
            self.__m_vec[i] *= other[i]
        return self


    def __getitem__(self, index):
        assert ( index > 0 and index < self.__m_size ), f"list index out of range for vector of size {self.__m_size}"
        return self.__m_vec[index]  

    def __setitem__(self, index, value):
        self.data[index] = value

    # Returns the dot product of this vector with another one
    def dot(self, other):
        assert (self.__m_size != other.size()), f"Attempted to multiply two incompatable vector types sizes: {self.__m_size} {other.size()}"
        dotP = 0
        for i in range(self.__m_size):
            dotP += self.__m_vec[i] * other[i]
        return dotP
        

    # Returns the length of the vector
    def length(self):
        
        return math.sqrt(self.length_squared())

    # Returns the squared length of the vector
    def length_squared(self):
        SquareSum = 0
        for value in self.__m_vec:
            SquareSum += value**2
        return SquareSum

    

    # Returns the angle between this vector and another one
    def angle(self, other):
        print("not applicabe to this vector impl")

    # Rotates the vector 90 degrees anticlockwise
    def rotate_anti(self):
        print("not applicabe to this vector impl")

    # Rotates the vector according to an angle theta given in radians
    def rotate_rad(self, theta):
        print("not applicabe to this vector impl")

    # Rotates the vector according to an angle theta given in degrees
    def rotate(self, theta):
        print("not applicabe to this vector impl")
    
    # project the vector onto a given vector
    def get_proj(self, vec):
        print("not applicabe to this vector impl")
        

