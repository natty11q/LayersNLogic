# from __future__ import annotations
# from ApplicationEngine.include.Maths.Vector.Vector import *
# from ApplicationEngine.include.Maths.Vector.Vector import Vec2, Vec3, Vec4

# class Matrix:
#     def __init__(self, rows: int, cols: int, values: list[list[float]] = [[]]):
#         self.rows: int = rows
#         self.cols: int = cols
#         if (values == [[]]):
#             self._m_data: list[list[float]] = [[0] * cols for _ in range(rows)]
#         else:
#             assert len(values) == rows and all(len(row) == cols for row in values), "Invalid matrix dimensions"
#             self._m_data = values
    
#     def __str__(self):
#         return "\n".join([str(row) for row in self._m_data])
    
#     def __getitem__(self, index: tuple[int, int]) -> float:
#         row, col = index
#         return self._m_data[row][col]
    
#     def __setitem__(self, index: tuple[int, int], value: float):
#         row, col = index
#         self._m_data[row][col] = float(value)
    
#     def __mul__(self, other: Matrix | Vec2 | Vec3 | Vec4 | float | int):
#         if isinstance(other, Matrix):
#             assert self.cols == other.rows, "Matrix multiplication dimension mismatch"
#             result = [
#                 [sum(self[i, k] * other[k, j] for k in range(self.cols)) for j in range(other.cols)]
#                 for i in range(self.rows)
#             ]
#             return Matrix(self.rows, other.cols, result)
#         elif isinstance(other, (Vec2, Vec3, Vec4)):
#             assert self.cols == other.size(), "Matrix-vector multiplication dimension mismatch"
#             values = [
#                 sum(self[i, j] * other[j] for j in range(self.cols))
#                 for i in range(self.rows)
#             ]
#             return type(other)(*values[:other.size()])
#         elif isinstance(other, (float, int)):
#             return Matrix(self.rows, self.cols, [[elem * other for elem in row] for row in self._m_data])
#         else:
#             raise TypeError("Unsupported multiplication")

#     def transpose(self):
#         transposed = [[self[j, i] for j in range(self.rows)] for i in range(self.cols)]
#         return Matrix(self.cols, self.rows, transposed)

#     def determinant(self) -> float:
#         assert self.rows == self.cols, "Determinant is only defined for square matrices"
        
#         if self.rows == 2:
#             return self[0, 0] * self[1, 1] - self[0, 1] * self[1, 0]
        
#         elif self.rows == 3:
#             return (self[0, 0] * (self[1, 1] * self[2, 2] - self[1, 2] * self[2, 1]) -
#                     self[0, 1] * (self[1, 0] * self[2, 2] - self[1, 2] * self[2, 0]) +
#                     self[0, 2] * (self[1, 0] * self[2, 1] - self[1, 1] * self[2, 0]))
        
#         elif self.rows == 4:
#             def minor(matrix, row, col):
#                 return [[matrix[r, c] for c in range(4) if c != col] for r in range(4) if r != row]
            
#             det = 0.0
#             for c in range(4):
#                 sub_matrix = Matrix(3, 3, minor(self, 0, c))
#                 det += ((-1) ** c) * self[0, c] * sub_matrix.determinant()
#             return det
        
#         else:
#             raise NotImplementedError("Determinant calculation is only implemented for 2x2, 3x3, and 4x4 matrices")

#     def copy(self):
#         return Matrix(self.rows, self.cols, [row[:] for row in self._m_data])

#     def getData(self):
#         return [row[:] for row in self._m_data]

#     def to(self, cls):
#         """Convert the matrix to a given subclass type."""
#         assert issubclass(cls, Mat2 | Mat3 | Mat4), "Can only convert to a subclass of Matrix"
#         return cls(self._m_data)

# class Mat2(Matrix):
#     def __init__(self, values: list[list[float]] = [[]]):
#         super().__init__(2, 2, values if (values != [[]]) else [[1, 0], [0, 1]])
    
#     def __mul__(self, other: Matrix | Vec2 | Vec3 | Vec4 | float | int) -> Matrix | Vec2 | Vec3 | Vec4:
#         if isinstance(other, Mat2):
#             assert self.cols == other.rows, "Matrix multiplication dimension mismatch"
#             result = [
#                 [sum(self[i, k] * other[k, j] for k in range(self.cols)) for j in range(other.cols)]
#                 for i in range(self.rows)
#             ]
#             return Mat2(result)
#         else:
#             return super().__mul__(other)

#     def copy(self):
#         return Mat2([row[:] for row in self._m_data])

# class Mat3(Matrix):
#     def __init__(self, values: list[list[float]] = [[]]):
#         super().__init__(3, 3, values if (values != [[]]) else [[1 if i == j else 0 for j in range(3)] for i in range(3)])
    
#     def __mul__(self, other: Matrix | Vec2 | Vec3 | Vec4 | float | int) -> Matrix | Vec2 | Vec3 | Vec4:
#         if isinstance(other, Mat2):
#             assert self.cols == other.rows, "Matrix multiplication dimension mismatch"
#             result = [
#                 [sum(self[i, k] * other[k, j] for k in range(self.cols)) for j in range(other.cols)]
#                 for i in range(self.rows)
#             ]
#             return Mat3(result)
#         else:
#             return super().__mul__(other)
        
#     def copy(self):
#         return Mat3([row[:] for row in self._m_data])

# class Mat4(Matrix):
#     def __init__(self, values: list[list[float]] = [[]]):
#         super().__init__(4, 4, values if (values != [[]]) else [[1 if i == j else 0 for j in range(4)] for i in range(4)])

#     def __mul__(self, other: Matrix | Vec2 | Vec3 | Vec4 | float | int) -> Matrix | Vec2 | Vec3 | Vec4:
#         if isinstance(other, Mat2):
#             assert self.cols == other.rows, "Matrix multiplication dimension mismatch"
#             result = [
#                 [sum(self[i, k] * other[k, j] for k in range(self.cols)) for j in range(other.cols)]
#                 for i in range(self.rows)
#             ]
#             return Mat4(result)
#         else:
#             return super().__mul__(other)
    
#     def copy(self):
#         return Mat4([row[:] for row in self._m_data])








from __future__ import annotations
from typing import overload
from typing import TypeVar, Union, Self
from ApplicationEngine.include.Maths.Vector.Vector import Vec2, Vec3, Vec4, Vector


# Define a generic matrix type
M = TypeVar("M", bound="Matrix")

class Matrix:
    def __init__(self, rows: int, cols: int, values: list[list[float]] = [[]]):
        self.rows: int = rows
        self.cols: int = cols
        if values == [[]]:
            self._m_data: list[list[float]] = [[0] * cols for _ in range(rows)]
        else:
            assert len(values) == rows and all(len(row) == cols for row in values), "Invalid matrix dimensions"
            self._m_data = values

    def __str__(self):
        return "\n".join([str(row) for row in self._m_data])

    def __getitem__(self, index: tuple[int, int]) -> float:
        row, col = index
        return self._m_data[row][col]
    
    def __setitem__(self, index: tuple[int, int], value: float):
        row, col = index
        self._m_data[row][col] = float(value)
    


    @overload
    def __mul__(self, other: Vec2) -> Vec2: ...

    @overload
    def __mul__(self, other: Vec3) -> Vec3: ...

    @overload
    def __mul__(self, other: Vec4) -> Vec4: ...


    @overload
    def __mul__(self, other: Mat2) -> Mat2: ...

    @overload
    def __mul__(self, other: Mat3) -> Mat3: ...
    
    @overload
    def __mul__(self, other: Mat4) -> Mat4: ...

    @overload
    def __mul__(self, other: Matrix) -> Matrix: ...


    def __mul__(self, other: object) -> Matrix | Mat2 | Mat3 | Mat4 | Vec2 | Vec3 | Vec4:
        if isinstance(other, Matrix):
            assert self.cols == other.rows, "Matrix multiplication dimension mismatch"
            result = [
                [sum(self[i, k] * other[k, j] for k in range(self.cols)) for j in range(other.cols)]
                for i in range(self.rows)
            ]
            if isinstance(self, (Mat2,Mat3,Mat4)):
                return type(self)(result)
            else:
                return Matrix(self.rows, self.cols, result)
#   Preserve matrix type
        elif isinstance(other, (Vec2, Vec3, Vec4)):
            assert self.cols == other.size(), "Matrix-vector multiplication dimension mismatch"
            values = [
                sum(self[i, j] * other[j] for j in range(self.cols))
                for i in range(self.rows)
            ]
            return type(other)(*values[:other.size()])  # Preserve vector type
        elif isinstance(other, (float, int)):
            if isinstance(self, (Mat2,Mat3,Mat4)):
                return type(self)([[elem * other for elem in row] for row in self._m_data])
            else:
                return Matrix(self.rows, self.cols, [[elem * other for elem in row] for row in self._m_data])
        else:
            raise TypeError("Unsupported multiplication")


    


    def transpose(self):
        transposed = [[self[j, i] for j in range(self.rows)] for i in range(self.cols)]
        return Matrix(self.cols, self.rows, transposed)

    def determinant(self) -> float:
        assert self.rows == self.cols, "Determinant is only defined for square matrices"
        
        if self.rows == 2:
            return self[0, 0] * self[1, 1] - self[0, 1] * self[1, 0]
        
        elif self.rows == 3:
            return (self[0, 0] * (self[1, 1] * self[2, 2] - self[1, 2] * self[2, 1]) -
                    self[0, 1] * (self[1, 0] * self[2, 2] - self[1, 2] * self[2, 0]) +
                    self[0, 2] * (self[1, 0] * self[2, 1] - self[1, 1] * self[2, 0]))
        
        else:
            raise NotImplementedError("Determinant calculation is only implemented for 2x2 and 3x3 matrices")

    def copy(self: Matrix) -> Union[Matrix, Mat2, Mat3, Mat4]:
        if isinstance(self, (Mat2,Mat3,Mat4)):
            return type(self)([row[:] for row in self._m_data])
        else:
            return Matrix(self.rows, self.cols, [row[:] for row in self._m_data])

    def getData(self):
        return [row[:] for row in self._m_data]

    def to(self, cls: type[M]) -> M:
        """Convert the matrix to a given subclass type."""
        assert issubclass(cls, Matrix), "Can only convert to a subclass of Matrix"
        return cls(values = self._m_data, rows=self.rows, cols=self.cols)


class Mat2(Matrix):
    def __init__(self, values: list[list[float]] = [[]]):
        super().__init__(2, 2, values if values is not None else [[1, 0], [0, 1]])


class Mat3(Matrix):
    def __init__(self, values: list[list[float]] = [[]]):
        super().__init__(3, 3, values if values is not None else [[1 if i == j else 0 for j in range(3)] for i in range(3)])


class Mat4(Matrix):
    def __init__(self, values: list[list[float]] = [[]]):
        super().__init__(4, 4, values if values is not None else [[1 if i == j else 0 for j in range(4)] for i in range(4)])

# # Example usage in the camera class

# def _RecalculateViewMatrix(self):
#     transform: Mat4 = toMat4(self._m_Rotation) * translate(Mat4(), self._m_Position)
#     self._m_ViewMatrix = inverse(transform)
#     self._m_ViewProjectionMatrix = self._m_ViewMatrix * self._m_ProjectionMatrix


# Let me know if you want me to add helper functions like 'translate' and 'inverse'! 🚀


def ortho(left: float, right: float, bottom: float, top: float, z_near: float = -1.0, z_far: float = 1.0) -> Mat4:
    """
    Creates an orthographic projection matrix.

    :param left: Left vertical clipping plane.
    :param right: Right vertical clipping plane.
    :param bottom: Bottom horizontal clipping plane.
    :param top: Top horizontal clipping plane.
    :param z_near: Near depth clipping plane.
    :param z_far: Far depth clipping plane.
    :return: A 4x4 orthographic projection matrix.
    """
    
    ortho_matrix = Mat4([
        [2 / (right - left), 0, 0, -(right + left) / (right - left)],
        [0, 2 / (top - bottom), 0, -(top + bottom) / (top - bottom)],
        [0, 0, -2 / (z_far - z_near), -(z_far + z_near) / (z_far - z_near)],
        [0, 0, 0, 1]
    ])

    return ortho_matrix