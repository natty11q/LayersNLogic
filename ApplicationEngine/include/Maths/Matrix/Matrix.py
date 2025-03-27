from __future__ import annotations
from typing import overload, TypeVar, Union
import numpy as np
from ApplicationEngine.include.Common import *
from ApplicationEngine.include.Maths.Vector.Vector import Vec2, Vec3, Vec4, Vector

M = TypeVar("M", bound="Matrix")

class Matrix:
    def __init__(self, rows: int, cols: int, values: list[list[float]]| np.ndarray| None = None):
        self.rows: int = rows
        self.cols: int = cols
        if values is None:
            self._m_data = np.zeros((rows, cols), dtype=float)
        else:
            # Convert input to a NumPy array and ensure shape matches.
            arr = np.array(values, dtype=float)
            assert arr.shape == (rows, cols), "Invalid matrix dimensions"
            self._m_data = arr

    def __str__(self) -> str:
        return str(self._m_data)

    def __getitem__(self, index: tuple[int, int]) -> float:
        row, col = index
        return self._m_data[row, col]
    
    def __setitem__(self, index: tuple[int, int], value: float):
        row, col = index
        self._m_data[row, col] = float(value)

    @overload
    def __mul__(self, other: float | int) -> Matrix: ...
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
            result_data = np.dot(self._m_data, other._m_data)
            # If self is an instance of a specific subclass, return that type.
            if isinstance(self, (Mat2, Mat3, Mat4)):
                return type(self)(result_data.tolist())
            else:
                return Matrix(self.rows, other.cols, result_data.tolist())
        elif isinstance(other, (float, int)):
            result_data = self._m_data * other
            if isinstance(self, (Mat2, Mat3, Mat4)):
                return type(self)(result_data.tolist())
            else:
                return Matrix(self.rows, self.cols, result_data.tolist())
        elif isinstance(other, (Vec2, Vec3, Vec4)):
            vec = np.array(other.get_p(), dtype=float)
            assert self.cols == vec.size, "Matrix-vector multiplication dimension mismatch"
            result_vec = np.dot(self._m_data, vec)
            return type(other)(*result_vec.tolist())
        else:
            raise TypeError("Unsupported multiplication")

    @overload
    def __rmul__(self, other: float | int) -> Matrix: ...
    @overload
    def __rmul__(self, other: Vec2) -> Vec2: ...
    @overload
    def __rmul__(self, other: Vec3) -> Vec3: ...
    @overload
    def __rmul__(self, other: Vec4) -> Vec4: ...

    def __rmul__(self, other: object) -> Matrix | Mat2 | Mat3 | Mat4 | Vector | Vec2 | Vec3 | Vec4:
        if isinstance(other, (float, int)):
            return self * other
        elif isinstance(other, (Vector, Vec2, Vec3, Vec4)):
            vec = np.array(other.get_p(), dtype=float)
            assert self.rows == vec.size, "Vector-matrix multiplication dimension mismatch"
            result = np.dot(self._m_data, vec)

            if isinstance(other, (Vec2, Vec3, Vec4)):
                return type(other)(*result)
            else:
                return Vector(result[0], result[1])
        else:
            LNL_LogEngineFatal(type(other))
            raise TypeError("Unsupported reverse multiplication")

    def transpose(self) -> Matrix:
        transposed_data = self._m_data.T
        return Matrix(self.cols, self.rows, transposed_data.tolist())

    def determinant(self) -> float:
        assert self.rows == self.cols, "Determinant is only defined for square matrices"
        if self.rows in (2, 3):
            return float(np.linalg.det(self._m_data))
        else:
            raise NotImplementedError("Determinant calculation is only implemented for 2x2 and 3x3 matrices")

    def copy(self: Matrix) -> Matrix:
        if isinstance(self, (Mat2,Mat3,Mat4)):
            return type(self)([row[:] for row in self._m_data])
        else:
            return Matrix(self.rows, self.cols, [row[:] for row in self._m_data])

    def getData(self):
        return self._m_data.copy()
    
    def nparr(self) -> np.ndarray:
        """
            Returns a 1D NumPy array containing the matrix data in row-major order.

            Useful for shader unifroms
        """
        return self._m_data.flatten()

    def to(self, cls: type[M]) -> M:
        """Convert the matrix to a given subclass type."""
        assert issubclass(cls, Matrix), "Can only convert to a subclass of Matrix"
       
        return cls(values = self._m_data, rows=self.rows, cols=self.cols)


class Mat2(Matrix):
    def __init__(self, values: list[list[float]] | np.ndarray | None = None, cols: int = 2, rows: int = 2):
        if values is None:
            default = np.array([[1, 0], [0, 1]], dtype=float)
            super().__init__(2, 2, default)
        else:
            super().__init__(2, 2, values)

class Mat3(Matrix):
    def __init__(self, values: list[list[float]] | np.ndarray | None = None, cols: int = 3, rows: int = 3):
        if values is None:
            default = np.eye(3, dtype=float)
            super().__init__(3, 3, default)
        else:
            super().__init__(3, 3, values)

class Mat4(Matrix):
    def __init__(self, values: list[list[float]] | np.ndarray | None = None, cols: int = 4, rows: int = 4):
        if values is None:
            default = np.eye(4, dtype=float)
            super().__init__(4, 4, default)
        else:
            super().__init__(4, 4, values)

def ortho(left: float, right: float, bottom: float, top: float, z_near: float = -1.0, z_far: float = 1.0) -> Mat4:
    """
    Creates an orthographic projection matrix.
    """
    ortho_data = np.array([
        [2 / (right - left), 0, 0, -(right + left) / (right - left)],
        [0, 2 / (top - bottom), 0, -(top + bottom) / (top - bottom)],
        [0, 0, -2 / (z_far - z_near), -(z_far + z_near) / (z_far - z_near)],
        [0, 0, 0, 1]
    ], dtype=float)
    return Mat4(ortho_data)
