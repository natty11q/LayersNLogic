from ApplicationEngine.include.Common import *
from ApplicationEngine.include.Maths.Maths import *

from ApplicationEngine.src.LayerSystem.LayerSystem import *

from ApplicationEngine.src.Graphics.Renderer.VertexArray import *

class CommandType(Enum):
    SetClearColour  = auto()
    Clear           = auto()
    Enable          = auto()
    Disable         = auto()
    DrawIndexed     = auto()
    GetUniformLocation = auto()
    SetUniformInt   = auto()
    SetUniformVec2  = auto()
    SetUniformVec3  = auto()
    SetUniformVec4  = auto()
    SetUniformMat2  = auto()
    SetUniformMat3  = auto()
    SetUniformMat4  = auto()
    DrawTriangle    = auto()
    DrawCircle      = auto()

class RendererAPI(ABC): ## abstract class only
    
    class API(Enum):
        NoAPI       = auto()
        Pygame      = auto()
        OpenGl      = auto()
        Metal       = auto()
        
        SimpleGui   = auto()
        PySimpleGui = auto()
        
    _LayerStack : LayerStack = LayerStack()
    
    @staticmethod
    def PushLayer(layer : Layer):
        RendererAPI._LayerStack.PushLayer(layer)
        layer.OnAttach()
    
    @staticmethod
    def PopLayer():
        RendererAPI._LayerStack.PopLayer()
        # layer.OnDetach()
    
    @staticmethod
    def PushOverlay(layer : Layer):
        RendererAPI._LayerStack.PushOverlay(layer)
        layer.OnAttach()
    
    @staticmethod
    def PopOverlay():
        RendererAPI._LayerStack.PopOverlay()
        # layer.OnDetach()
    

    @abstractmethod
    def SetClearColour(self, col : Vector.Vec4 ) -> None: ...

    @abstractmethod
    def Clear(self, value : int = 0) -> None: ...
    
    @abstractmethod
    def Enable(self, value : int = 0) -> None: ...
    
    @abstractmethod
    def Disable(self, value : int = 0) -> None: ...
    
    @abstractmethod
    def DrawIndexed(self, VertexArray : VertexArray) -> None: ...
    
    @abstractmethod
    def GetUniformLocation(self, ID : int, UniformName : str) -> None: ...
    
    @abstractmethod
    def SetUniformInt(self, UniformLocation : int, value : int) -> None: ...
    
    @abstractmethod
    def SetUniformVec2(self, UniformLocation : int, value : Vector.Vec2) -> None: ...
    
    @abstractmethod
    def SetUniformVec3(self, UniformLocation : int, value : Vector.Vec3) -> None: ...
    
    @abstractmethod
    def SetUniformVec4(self, UniformLocation : int, value : Vector.Vec4) -> None: ...
    
    @abstractmethod
    def SetUniformMat2(self, UniformLocation : int, value : Matrix.Mat2) -> None: ...
    
    @abstractmethod
    def SetUniformMat3(self, UniformLocation : int, value : Matrix.Mat3) -> None: ...
    
    @abstractmethod
    def SetUniformMat4(self, UniformLocation : int, value : Matrix.Mat4) -> None: ...
    
    @abstractmethod
    def DrawTriangle(self, VertexPositions : list [Vector.Vec2], colour : Vector.Vec4): ...
    
    @abstractmethod
    def DrawCircle(self, Position : Vector.Vec2, colour : Vector.Vec4): ...
    
    @abstractmethod
    def Draw(self, *args): ...
    
    @staticmethod
    def GetAPI() -> API:
        return RendererAPI.__s_API
    
    # __s_API : API = API.NoAPI
    __s_API : API = API.SimpleGui