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
    def __mul__(self, other: Vec2) -> Vec2: ...
    @overload
    def __mul__(self, other: Vec3) -> Vec3: ...
    @overload
    def __mul__(self, other: Vec4) -> Vec4: ...
    
    @overload
    def __mul__(self : Mat2, other: Mat2) -> Mat2: ...
    @overload
    def __mul__(self : Mat3, other: Mat3) -> Mat3: ...
    @overload
    def __mul__(self : Mat4, other: Mat4) -> Mat4: ...
    
    @overload
    def __mul__(self : Mat2, other: float | int) -> Mat2: ...
    @overload
    def __mul__(self : Mat3, other: float | int) -> Mat3: ...
    @overload
    def __mul__(self : Mat4, other: float | int) -> Mat4: ...
    
    @overload
    def __mul__(self, other: Matrix) -> Matrix: ...
    @overload
    def __mul__(self, other: float | int) -> Matrix: ...


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
    def __rmul__(self : Mat4, other : Mat4) -> Mat4: ...
    @overload
    def __rmul__(self : Mat3, other : Mat3) -> Mat3: ...
    @overload
    def __rmul__(self : Mat2, other : Mat2) -> Mat2: ...
    @overload
    def __rmul__(self : Mat4, other: float | int) -> Mat4: ...
    @overload
    def __rmul__(self : Mat3, other: float | int) -> Mat3: ...
    @overload
    def __rmul__(self : Mat2, other: float | int) -> Mat2: ...
    @overload
    def __rmul__(self, other: Vec2) -> Vec2: ...
    @overload
    def __rmul__(self, other: Vec3) -> Vec3: ...
    @overload
    def __rmul__(self, other: Vec4) -> Vec4: ...
    @overload
    def __rmul__(self, other: float | int) -> Matrix: ...

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
        

    @overload
    def inverse(self : Mat2) -> Mat2: ...
    @overload
    def inverse(self : Mat3) -> Mat3: ...
    @overload
    def inverse(self : Mat4) -> Mat4: ...

    def inverse(self) -> Matrix | Mat2 | Mat3 | Mat4:
        assert self.rows == self.cols, "Inverse is only defined for square matrices"
        # Compute the inverse using NumPy
        inv_data = np.linalg.inv(self._m_data)
        # Return an instance of the same type as self using the inverse data
        if isinstance(self, (Mat2, Mat3, Mat4)):
            return type(self)(values=inv_data.tolist())
        else:
            return Matrix(self.rows, self.cols, inv_data.tolist())

    @overload
    def transpose(self : Mat2) -> Mat2: ...
    @overload
    def transpose(self : Mat3) -> Mat3: ...
    @overload
    def transpose(self : Mat4) -> Mat4: ...

    def transpose(self) -> Matrix | Mat2 | Mat3 | Mat4:
        transposed_data = self._m_data.T
        return Matrix(self.cols, self.rows, transposed_data.tolist())

    def determinant(self) -> float:
        assert self.rows == self.cols, "Determinant is only defined for square matrices"
        if self.rows in (2, 3, 4):
            return float(np.linalg.det(self._m_data))
        else:
            raise NotImplementedError("Determinant calculation is only implemented for 2x2, 3x3 and 4x4 matrices")

    @overload
    def copy(self : Mat2) -> Mat2: ...
    @overload
    def copy(self : Mat3) -> Mat3: ...
    @overload
    def copy(self : Mat4) -> Mat3: ...

    def copy(self: Matrix) -> Matrix | Mat2 | Mat3 | Mat4:
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

    Parameters:
    - left: The coordinate for the left vertical clipping plane.
    - right: The coordinate for the right vertical clipping plane.
    - bottom: The coordinate for the bottom horizontal clipping plane.
    - top: The coordinate for the top horizontal clipping plane.
    - z_near: The coordinate for the near depth clipping plane.
    - z_far: The coordinate for the far depth clipping plane.

    Returns:
    - A 4x4 orthographic projection matrix.
    """
    # Calculate the ranges for each axis
    rl = right - left
    tb = top - bottom
    fn = z_far - z_near

    # Ensure no division by zero
    assert rl != 0 and tb != 0 and fn != 0, "Invalid orthographic projection parameters."

    # Create the orthographic projection matrix
    ortho_matrix = Mat4([
        [2.0 / rl, 0.0, 0.0, -(right + left) / rl],
        [0.0, 2.0 / tb, 0.0, -(top + bottom) / tb],
        [0.0, 0.0, -2.0 / fn, -(z_far + z_near) / fn],
        [0.0, 0.0, 0.0, 1.0]
    ])

    return ortho_matrix


def perspective(fovy: float, aspect: float, near: float, far: float) -> Mat4:
    """
    Creates a perspective projection matrix similar to glm::perspective.
    
    Parameters:
      fovy   : vertical field of view in radians.
      aspect : aspect ratio (width/height).
      near   : near clipping plane.
      far    : far clipping plane.
    
    Returns:
      A Mat4 representing the perspective projection matrix.
    """
    f = 1.0 / np.tan(fovy / 2.0)
    m22 = (far + near) / (near - far)
    m23 = (2 * far * near) / (near - far)
    return Mat4([
        [f / aspect, 0.0,  0.0,  0.0],
        [0.0,        f,    0.0,  0.0],
        [0.0,        0.0,  m22,  m23],
        [0.0,        0.0, -1.0,  0.0]
    ])


# TODO: make mat3 version
def translate(mat: Mat4, translation: Vec3) -> Mat4:
    """
    Applies a translation to the given 4x4 matrix.
    
    This function mimics glm::translate, where the translation matrix is
    multiplied with the input matrix. It assumes a column vector convention,
    so the multiplication is mat * T.
    
    Parameters:
      mat: A Mat4 representing the initial transformation.
      translation: A Vec3 representing the translation along x, y, and z.
    
    Returns:
      A new Mat4 with the translation applied.
    """
    tx = translation.x
    ty = translation.y
    tz = translation.z
    
    # Build the translation matrix (row-major order for column vectors)
    translation_matrix = Mat4([
        [1.0, 0.0, 0.0, tx],
        [0.0, 1.0, 0.0, ty],
        [0.0, 0.0, 1.0, tz],
        [0.0, 0.0, 0.0, 1.0]
    ])
    
    # Multiply the input matrix by the translation matrix.
    # This is equivalent to m * T in glm.
    return mat * translation_matrix




# TODO: make mat3 and mat2 versions
def rotate(mat: Mat4, angle: float, axis: Vec3) -> Mat4:
    """
    Applies a rotation to the given 4x4 matrix using an axis-angle representation,
    similar to glm::rotate.
    
    Parameters:
      mat: A Mat4 representing the initial transformation.
      angle: The rotation angle in radians.
      axis: A Vec3 representing the axis of rotation.
      
    Returns:
      A new Mat4 with the rotation applied (i.e. mat * rotation_matrix).
      
    Note:
      This function assumes the use of column vectors (v' = M * v), so the
      rotation matrix is multiplied on the right of the input matrix.
    """
    # Ensure the axis is normalized.
    axis_norm = axis.normalize()  # Assuming this returns a normalized Vec3
    cos_a = np.cos(angle)
    sin_a = np.sin(angle)
    one_minus_cos = 1.0 - cos_a

    x = axis_norm.x
    y = axis_norm.y
    z = axis_norm.z

    # Construct the rotation matrix using the Rodrigues' rotation formula.
    rotation_matrix = Mat4([
        [cos_a + x * x * one_minus_cos,      x * y * one_minus_cos - z * sin_a,  x * z * one_minus_cos + y * sin_a, 0.0],
        [y * x * one_minus_cos + z * sin_a,    cos_a + y * y * one_minus_cos,      y * z * one_minus_cos - x * sin_a, 0.0],
        [z * x * one_minus_cos - y * sin_a,    z * y * one_minus_cos + x * sin_a,  cos_a + z * z * one_minus_cos,     0.0],
        [0.0,                                0.0,                                0.0,                               1.0]
    ])

    # Multiply the input matrix by the rotation matrix.
    return mat * rotation_matrix