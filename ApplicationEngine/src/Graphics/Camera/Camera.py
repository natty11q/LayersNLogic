
from ApplicationEngine.include.Maths.Maths import *
from ApplicationEngine.include.Maths.Vector.Vector import Vec3

# from ApplicationEngine.src.Window.Window import *



class Camera:
    def __init__(self,
                 width,
                 height,
                 
                 position : Vec3 = Vec3(),
                 rotation : Quat.Quat = Quat.Quat(),
                 
                 FOVdeg     : float = 45,
                 nearPlane  : float = 0.1,
                 farPlane   : float = 100
                ):
        
        self._m_FovDeg : float  = FOVdeg
        self._m_Position : Vec3   = position
        self._m_Rotation : Quat.Quat     = rotation
        
        self._m_Orientation : Vec3   = Vec3(0.0, 1.0, 0.0) # const
        self._m_Up : Vec3            = Vec3(0.0, 1.0, 0.0)
        
        
        self._m_ProjectionMatrix : Matrix.Mat4 = Matrix.Mat4()
        self._m_ViewMatrix : Matrix.Mat4 = Matrix.Mat4()
        self._m_ViewProjectionMatrix : Matrix.Mat4 = Matrix.Mat4()
        
        self._m_CameraMatrix : Matrix.Mat4 = Matrix.Mat4()
        
        self._m_NearPlane : float = nearPlane
        self._m_FarPlane : float = farPlane
        
        self.width : int = width
        self.height : int = height
        self.m_AspectRatio : float = (width / height)
        
        self._RecalculateViewMatrix()
        
    def Update(self, deltatime : float):
        self._OnUpdate(deltatime)
    
    def _OnUpdate(self, deltatime : float):
        ...
        
    # def HandleInputs(self, deltatime : float, window : Window):
    #     ...
        
    def SetPosition(self, position : Vec3):
        self._m_Position = position
        self._RecalculateViewMatrix()
    
    def SetRotation(self, rotation : Quat.Quat):
        self._m_Rotation = rotation
        self._RecalculateViewMatrix()
    
    def SetFOV(self, fovDeg : float):
        self._m_FovDeg = fovDeg
        self._RecalculateProjectionMatrix()

    def _RecalculateViewMatrix(self):
        # print(toMat4(self._m_Rotation).getData())
        # print("===================")
        # print(Matrix.Mat4().getData())
        # print("===================")
        # print(translate(Matrix.Mat4(), self._m_Position).getData())
        
        # transform : Matrix.Mat4 = toMat4(self._m_Rotation) * translate(Matrix.Mat4(), self._m_Position)
        # self._m_ViewMatrix = inverse(transform.to(Matrix.Mat4)).to(Matrix.Mat4)
        # self._m_ViewProjectionMatrix = self._m_ViewMatrix * self._m_ProjectionMatrix
    
        ...
    
    def _RecalculateProjectionMatrix(self):
        pass
    
    def GetProjectionMatrix(self): return self._m_ProjectionMatrix
    def GetViewMatrix(self): return self._m_ViewMatrix
    def GetViewProjectionMatrix(self): return self._m_ViewProjectionMatrix
    def GetRotation(self): return self._m_Rotation
    def GetPosition(self): return self._m_Position




class PesrpectiveCamera(Camera):
    def __init__(self, width, height, position: Vec3 = Vec3(), rotation: Quat.Quat = Quat.Quat(), FOVdeg: float = 45, nearPlane: float = 0.1, farPlane: float = 100):
        super().__init__(width, height, position, rotation, FOVdeg, nearPlane, farPlane)


class OrthographicCamera(Camera):
    def __init__(self, left : float = -1.0, right : float = 1.0, bottom : float = -1.0, top : float = 1.0):
        self._m_ProjectionMatrix : Mat4 = Matrix.ortho(left,right,bottom,top,-1.0,1.0)
        # self._m_ViewMatrix : Mat4 = Mat4()

        # self._m_ViewProjectionMatrix : Mat4 = Mat4()

        self._m_Position : Vec3  = Vec3()
        self._m_OrthoRotation : float = 0.0
        self._RecalculateViewMatrix()

    
    def SetPosition(self, position: Vec3):
        return super().SetPosition(position)
   
    def SetOrthoRotation(self, rotation : float):
        self._m_OrthoRotation = rotation
        self._RecalculateViewMatrix()


    def _RecalculateViewMatrix(self):

        ## 
        transform : Mat4 = Matrix.rotate(Mat4(), self._m_OrthoRotation, Vec3(0, 0, 1)).transpose() * Matrix.translate(Mat4() , self._m_Position).transpose()

        self._m_ViewMatrix = transform.inverse()
        self._m_ViewProjectionMatrix = self._m_ProjectionMatrix.transpose() * self._m_ViewMatrix



    def GetPosition(self):
        return super().GetPosition()

    def GetOrthoRotation(self):
        return self._m_OrthoRotation