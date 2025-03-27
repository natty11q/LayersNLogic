from ApplicationEngine.include.Common import *
from ApplicationEngine.include.Maths.Maths import *

from ApplicationEngine.src.LayerSystem.LayerSystem import *

from ApplicationEngine.src.Graphics.Renderer.VertexArray import *

from ApplicationEngine.src.Graphics.Renderer.ShaderProgram import *
from ApplicationEngine.src.Graphics.Renderer.Texture import *


from OpenGL.GL import * # type: ignore

class RenderSettings:
        #TODO : change values to use opengl enum values so that it works with glEnable
        LL_SG_TRANSPARENCY_ENABLLED     : int = 1
        LL_SG_WIREFRAME_MODE_ENABLED    : int = 2

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
    BindTexture     = auto()
    CustomCommand   = auto()

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
    def SetClearColour(self, col : Vec4 ) -> None: ...

    @abstractmethod
    def Clear(self, value : int = 0) -> None: ...
    
    @abstractmethod
    def CustomRendererCommand(self, command, args : list) -> None: ...
   
    @abstractmethod
    def Enable(self, value : int = 0) -> None: ...
    
    @abstractmethod
    def Disable(self, value : int = 0) -> None: ...
    
    @abstractmethod
    def DrawIndexed(self, shader: Shader, VertexArray : VertexArray) -> None: ...
    
    @abstractmethod
    def GetUniformLocation(self, ID : int, UniformName : str) -> int: ...
    
    @abstractmethod
    def SetUniformInt(self, UniformLocation : int, value : int) -> None: ...

    @abstractmethod
    def SetUniformFloat(self, UniformLocation : int, value : float) -> None: ...
    
    @abstractmethod
    def SetUniformVec2(self, UniformLocation : int, value : Vec2) -> None: ...
    
    @abstractmethod
    def SetUniformVec3(self, UniformLocation : int, value : Vec3) -> None: ...
    
    @abstractmethod
    def SetUniformVec4(self, UniformLocation : int, value : Vec4) -> None: ...
    
    @abstractmethod
    def SetUniformMat2(self, UniformLocation : int, value : Matrix.Mat2) -> None: ...
    
    @abstractmethod
    def SetUniformMat3(self, UniformLocation : int, value : Matrix.Mat3) -> None: ...
    
    @abstractmethod
    def SetUniformMat4(self, UniformLocation : int, value : Matrix.Mat4) -> None: ...
    
    @abstractmethod
    def DrawTriangle(self, VertexPositions : list [Vec2], colour : Vec4): ...
    
    @abstractmethod
    def DrawCircle(self, Position : Vec2, colour : Vec4): ...

    @abstractmethod
    def BindTexture(self, tex_id : int): ...
    
    @abstractmethod
    def Draw(self, *args): ...
    
    @staticmethod
    def GetAPI() -> API:
        return RendererAPI.__s_API
    
    # __s_API : API = API.NoAPI
    __s_API : API = API.SimpleGui