from include.Common import *
from include.Maths.Maths import *


class RendererAPI(ABC): ## abstract class only
    
    class API(Enum):
        NoAPI       = auto()
        Pygame      = auto()
        OpenGl      = auto()
        Metal       = auto()
        
        SimpleGui   = auto()
        PySimpleGui = auto()
        
    
    @staticmethod
    @abstractmethod
    def SetClearColour( col : Vector.Vec4 ) -> None:
        pass
    
    @staticmethod
    @abstractmethod
    def Clear( value : int = 0) -> None:
        pass
    
    @staticmethod
    @abstractmethod
    def Enable( value : int = 0) -> None:
        pass
    
    @staticmethod
    @abstractmethod
    def DrawIndexed(VertexArray) -> None:
        pass
    
    @staticmethod
    @abstractmethod
    def GetUniformLocation(ID : int, UniformName : str) -> None:
        pass
    
    
    @staticmethod
    @abstractmethod
    def SetUniformInt(UniformLocation : int, value : int) -> None:
        pass
    
    
    @staticmethod
    @abstractmethod
    def SetUniformVec2(UniformLocation : int, value : Vector.Vec2) -> None:
        pass
    
    
    @staticmethod
    @abstractmethod
    def SetUniformVec3(UniformLocation : int, value : Vector.Vec3) -> None:
        pass
    
    
    @staticmethod
    @abstractmethod
    def SetUniformVec4(UniformLocation : int, value : Vector.Vec4) -> None:
        pass
    
    
    @staticmethod
    @abstractmethod
    def SetUniformMat2(UniformLocation : int, value : Matrix.Mat2) -> None:
        pass
    
    
    @staticmethod
    @abstractmethod
    def SetUniformMat3(UniformLocation : int, value : Matrix.Mat3) -> None:
        pass
    
    
    @staticmethod
    @abstractmethod
    def SetUniformMat4(UniformLocation : int, value : Matrix.Mat4) -> None:
        pass
    
    
    
    
    
    @staticmethod
    def GetAPI() -> API:
        return RendererAPI.__s_API
    
    # __s_API : API = API.NoAPI
    __s_API : API = API.SimpleGui