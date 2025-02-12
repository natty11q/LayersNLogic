

class MatrixBase:
    def __init__(self):
        pass

class Mat2:
    def __init__(self, x : float = 0, y : float = 0):
        pass
    

class Mat3:
    def __init__(self, x : float = 0, y : float = 0, z : float = 0):
        pass
    
    @staticmethod
    def FromMat2( mat : Mat2) -> "Mat3":
        return Mat3()


class Mat4:
    def __init__(self, x : float = 0, y : float = 0, z : float = 0, w : float = 0):
        pass

    @staticmethod
    def FromMat2( mat : Mat2) -> "Mat3":
        return Mat3()
    
    @staticmethod
    def FromMat3( mat : Mat3) -> "Mat4":
        return Mat4()