
from ApplicationEngine.include.Maths.Maths import *
from ApplicationEngine.src.Window.Window import *



class Camera:
    def __init__(self,
                 width,
                 height,
                 
                 position : Vector.Vec3 = Vector.Vec3(),
                 rotation : Quat.Quat = Quat.Quat(),
                 
                 FOVdeg     : float = 45,
                 nearPlane  : float = 0.1,
                 farPlane   : float = 100
                ):
        
        self._m_FovDeg : float  = FOVdeg
        self._m_Position : Vector.Vec3   = position
        self._m_Rotation : Quat.Quat     = rotation
        
        self._m_Orientation : Vector.Vec3   = Vector.Vec3(0.0, 1.0, 0.0) # const
        self._m_Up : Vector.Vec3            = Vector.Vec3(0.0, 1.0, 0.0)
        
        
        self._m_ProjectionMatrix : Matrix.Mat4
        self._m_ViewMatrix : Matrix.Mat4
        self._m_ViewProjectionMatrix : Matrix.Matrix
        
        self._m_CameraMatrix : Matrix.Mat4
        
        self._m_NearPlane : float = nearPlane
        self._m_FarPlane : float = farPlane
        
        self.width : int = width
        self.height : int = height
        self.m_AspectRatio : float = (width / height)
        
        
        
    def Update(self, deltatime : float):
        self._OnUpdate(deltatime)
    
    def _OnUpdate(self, deltatime : float):
        ...
        
    def HandleInputs(self, deltatime : float, window : Window):
        ...
        
    def SetPosition(self, position : Vector.Vec3):
        self._m_Position = position
        self._RecalculateViewMatrix()
    
    def SetRotation(self, rotation : Quat.Quat):
        self._m_Rotation = rotation
        self._RecalculateViewMatrix()
    
    def SetFOV(self, fovDeg : float):
        self._m_FovDeg = fovDeg
        self._RecalculateProjectionMatrix()
        
    def _RecalculateViewMatrix(self):
        transform  : Matrix.Mat4 = toMat4(self._m_Rotation) * translate(Matrix.Mat4(), self._m_Position)
        self._m_ViewMatrix = inverse(transform)
        
        self._m_ViewProjectionMatrix = self._m_ViewMatrix * self._m_ProjectionMatrix 
        
    
    def _RecalculateProjectionMatrix(self):
        pass
    
    def GetProjectionMatrix(self): return self._m_ProjectionMatrix
    def GetViewMatrix(self): return self._m_ViewMatrix
    def GetViewProjectionMatrix(self): return self._m_ViewProjectionMatrix
    def GetRotation(self): return self._m_Rotation
    def GetPosition(self): return self._m_Position
