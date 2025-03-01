from __future__ import annotations
from ApplicationEngine.include.Maths.Vector.Vector import *

class Matrix:
    def __init__(self, rows: int, cols: int, values: list[float] = []):
        self.rows : int = rows
        self.cols : int = cols
        self._m_data : list[float] = values if (values != []) else [0] * (rows * cols)
    
    def __str__(self):
        return "\n".join([str(self._m_data[i * self.cols:(i + 1) * self.cols]) for i in range(self.rows)])
    
    def __getitem__(self, index: tuple[int, int]) -> float:
        row, col = index
        return self._m_data[row * self.cols + col]
    
    def __setitem__(self, index: tuple[int, int], value: float):
        row, col = index
        self._m_data[row * self.cols + col] = float(value)
    
    def __mul__(self, other: Matrix | Vec2 | Vec3 | Vec4 | float | int):
        if isinstance(other, Matrix):
            assert self.cols == other.rows, "Matrix multiplication dimension mismatch"
            result = [
                sum(self[i, k] * other[k, j] for k in range(self.cols))
                for i in range(self.rows) for j in range(other.cols)
            ]
            return Matrix(self.rows, other.cols, result)
        elif isinstance(other, (Vec2, Vec3, Vec4)):
            assert self.cols == other.size(), "Matrix-vector multiplication dimension mismatch"
            values = [
                sum(self[i, j] * other[j] for j in range(self.cols))
                for i in range(self.rows)
            ]
            return type(other)(*values[:other.size()])
        elif isinstance(other, (float, int)):
            return Matrix(self.rows, self.cols, [i * other for i in self._m_data])
        else:
            raise TypeError("Unsupported multiplication")

    def transpose(self):
        transposed = [self[j, i] for i in range(self.cols) for j in range(self.rows)]
        return Matrix(self.cols, self.rows, transposed)

    def determinant(self) -> float:
        assert self.rows == self.cols, "Determinant is only defined for square matrices"
        
        if self.rows == 2:
            return self[0, 0] * self[1, 1] - self[0, 1] * self[1, 0]
        
        elif self.rows == 3:
            return (self[0, 0] * (self[1, 1] * self[2, 2] - self[1, 2] * self[2, 1]) -
                    self[0, 1] * (self[1, 0] * self[2, 2] - self[1, 2] * self[2, 0]) +
                    self[0, 2] * (self[1, 0] * self[2, 1] - self[1, 1] * self[2, 0]))
        
        elif self.rows == 4:
            def minor(matrix, row, col):
                return [matrix[r, c] for r in range(4) for c in range(4) if r != row and c != col]
            
            det = 0.0
            for c in range(4):
                sub_matrix = Matrix(3, 3, minor(self, 0, c))
                det += ((-1) ** c) * self[0, c] * sub_matrix.determinant()
            return det
        
        else:
            raise NotImplementedError("Determinant calculation is only implemented for 2x2, 3x3, and 4x4 matrices")

    def copy(self):
        return Matrix(self.cols, self.rows, self._m_data)

class Mat2(Matrix):
    def __init__(self, values: list[float] = []):
        super().__init__(2, 2, values if  (values != []) else [1, 0, 0, 1])
    
    def __mul__(self, other: Matrix | Vec2 | Vec3 | Vec4 | float | int):
        if isinstance(other, Mat2):
            assert self.cols == other.rows, "Matrix multiplication dimension mismatch"
            result = [
                sum(self[i, k] * other[k, j] for k in range(self.cols))
                for i in range(self.rows) for j in range(other.cols)
            ]
            return Mat2(result)
        elif isinstance(other, (float, int)):
            return Mat2([i * other for i in self._m_data])
        else:
            return Matrix(self.rows,self.cols,self._m_data) * other
        
    def determinant(self) -> float:
        return self[0, 0] * self[1, 1] - self[0, 1] * self[1, 0]
    def copy(self):
        return Mat2(self._m_data)


class Mat3(Matrix):
    def __init__(self, values: list[float] = []):
        super().__init__(3, 3, values if (values != []) else [1 if i == j else 0 for i in range(3) for j in range(3)])

    def __mul__(self, other: Matrix | Vec2 | Vec3 | Vec4 | float | int):
        if isinstance(other, Mat2):
            assert self.cols == other.rows, "Matrix multiplication dimension mismatch"
            result = [
                sum(self[i, k] * other[k, j] for k in range(self.cols))
                for i in range(self.rows) for j in range(other.cols)
            ]
            return Mat3(result)
        elif isinstance(other, (float, int)):
            return Mat3([i * other for i in self._m_data])
        else:
            return Matrix(self.rows,self.cols,self._m_data) * other

    def determinant(self) -> float:
        return (self[0, 0] * (self[1, 1] * self[2, 2] - self[1, 2] * self[2, 1]) -
                    self[0, 1] * (self[1, 0] * self[2, 2] - self[1, 2] * self[2, 0]) +
                    self[0, 2] * (self[1, 0] * self[2, 1] - self[1, 1] * self[2, 0]))
    def copy(self):
        return Mat3(self._m_data)
    
    
class Mat4(Matrix):
    def __init__(self, values: list[float] = []):
        super().__init__(4, 4, values if (values != []) else [1 if i == j else 0 for i in range(4) for j in range(4)])
    
    def __mul__(self, other: Matrix | Vec2 | Vec3 | Vec4 | float | int):
        if isinstance(other, Mat2):
            assert self.cols == other.rows, "Matrix multiplication dimension mismatch"
            result = [
                sum(self[i, k] * other[k, j] for k in range(self.cols))
                for i in range(self.rows) for j in range(other.cols)
            ]
            return Mat4(result)
        elif isinstance(other, (float, int)):
            return Mat4([i * other for i in self._m_data])
        else:
            return Matrix(self.rows,self.cols,self._m_data) * other

    def determinant(self) -> float:
        def minor(matrix, row, col):
                return [matrix[r, c] for r in range(4) for c in range(4) if r != row and c != col]
            
        det = 0.0
        for c in range(4):
            sub_matrix = Matrix(3, 3, minor(self, 0, c))
            det += ((-1) ** c) * self[0, c] * sub_matrix.determinant()
        return det

    def copy(self):
        return Mat4(self._m_data)

    # @staticmethod
    # def FromMat2( mat : Mat2) -> Mat4:
    #     return Mat()


# class Mat2:
#     def __init__(self, x : float = 0, y : float = 0):
#         pass
    

# class Mat3:
#     def __init__(self, x : float = 0, y : float = 0, z : float = 0):
#         pass
    
#     @staticmethod
#     def FromMat2( mat : Mat2) -> "Mat3":
#         return Mat3()


# class Mat4:
#     def __init__(self, x : float = 0, y : float = 0, z : float = 0, w : float = 0):
#         pass

#     @staticmethod
#     def FromMat2( mat : Mat2) -> "Mat3":
#         return Mat3()
    
#     @staticmethod
#     def FromMat3( mat : Mat3) -> "Mat4":
#         return Mat4()
    







# def translate(mat : Mat4 , vec : Vec3) -> Mat4:
#     return Mat4()
