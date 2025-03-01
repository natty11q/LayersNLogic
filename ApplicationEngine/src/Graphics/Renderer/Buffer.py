from __future__ import annotations

from ApplicationEngine.include.Common import *
from ApplicationEngine.include.Maths.Maths import *


import OpenGL.GL


class ShaderDataType(Enum):
    NoData  = auto()
    Float   = auto()
    Vec2    = auto()
    Vec3    = auto()
    Vec4    = auto()
    Mat3    = auto()   
    Mat4    = auto()
    Int     = auto()
    Int2    = auto()
    Int3    = auto()
    Int4    = auto()
    UInt    = auto()
    UInt2   = auto()
    UInt3   = auto()
    UInt4   = auto()
    Bool    = auto()


def SizeOfShaderDataType(type : ShaderDataType):
    match type:
        case ShaderDataType.Float:      return 1  * sizeof(c_float);
        case ShaderDataType.Vec2:       return 2  * sizeof(c_float);
        case ShaderDataType.Vec3:       return 3  * sizeof(c_float);
        case ShaderDataType.Vec4:       return 4  * sizeof(c_float);
        case ShaderDataType.Mat3:       return 9  * sizeof(c_float);
        case ShaderDataType.Mat4:       return 16 * sizeof(c_float);

        case ShaderDataType.Int:        return 1  * sizeof(c_int);
        case ShaderDataType.Int2:       return 2  * sizeof(c_int);
        case ShaderDataType.Int3:       return 3  * sizeof(c_int);
        case ShaderDataType.Int4:       return 4  * sizeof(c_int);

        case ShaderDataType.UInt:       return 1  * sizeof(c_uint);
        case ShaderDataType.UInt2:      return 2  * sizeof(c_uint);
        case ShaderDataType.UInt3:      return 3  * sizeof(c_uint);
        case ShaderDataType.UInt4:      return 4  * sizeof(c_uint);

        case ShaderDataType.Bool:       return 1  * sizeof(c_bool);
        case _:
            # assert(false && "unknown ShaderType"); return 0;
            assert(False , "unknown ShaderType") # type: ignore
            return 0


class BufferElement:
    
    
    
    def __init__(self , Name : str, Type : ShaderDataType, Normalized : bool = False):
        self.Name : str = Name
        self.Type : ShaderDataType  = Type
        self.Offset : int = 0
        self.Size : int = SizeOfShaderDataType(Type)
        self.Normalized : bool = Normalized
        
    
    
    ## TODO : modify to reference the actual enum as a change in the values may break the program for OpenGl 
    def GetGLBaseType(self) -> int:
        """returns the value for the OPENGL enum variants"""
        
        match self.Type:
            case ShaderDataType.Float:      return OpenGL.GL.GL_FLOAT;
            case ShaderDataType.Vec2:       return OpenGL.GL.GL_FLOAT;
            case ShaderDataType.Vec3:       return OpenGL.GL.GL_FLOAT;
            case ShaderDataType.Vec4:       return OpenGL.GL.GL_FLOAT;
            case ShaderDataType.Mat3:       return OpenGL.GL.GL_FLOAT;
            case ShaderDataType.Mat4:       return OpenGL.GL.GL_FLOAT;

            case ShaderDataType.Int:        return OpenGL.GL.GL_INT;
            case ShaderDataType.Int2:       return OpenGL.GL.GL_INT;
            case ShaderDataType.Int3:       return OpenGL.GL.GL_INT;
            case ShaderDataType.Int4:       return OpenGL.GL.GL_INT;

            case ShaderDataType.UInt:       return OpenGL.GL.GL_UNSIGNED_INT;
            case ShaderDataType.UInt2:      return OpenGL.GL.GL_UNSIGNED_INT;
            case ShaderDataType.UInt3:      return OpenGL.GL.GL_UNSIGNED_INT;
            case ShaderDataType.UInt4:      return OpenGL.GL.GL_UNSIGNED_INT;

            case ShaderDataType.Bool:       return OpenGL.GL.GL_BOOL;
            case _:
                # assert(false && "unknown ShaderType"); return 0;
                assert(False , "unknown ShaderType") # type: ignore
                return 0
        
    def GetComponentCount(self) -> int:
        """get the number of components in a datatype"""
        match self.Type:
            case ShaderDataType.Float:      return 1;
            case ShaderDataType.Vec2:       return 2;
            case ShaderDataType.Vec3:       return 3;
            case ShaderDataType.Vec4:       return 4;
            case ShaderDataType.Mat3:       return 9;
            case ShaderDataType.Mat4:       return 16;

            case ShaderDataType.Int:        return 1;
            case ShaderDataType.Int2:       return 2;
            case ShaderDataType.Int3:       return 3;
            case ShaderDataType.Int4:       return 4;

            case ShaderDataType.UInt:       return 1;
            case ShaderDataType.UInt2:      return 2;
            case ShaderDataType.UInt3:      return 3;
            case ShaderDataType.UInt4:      return 4;

            case ShaderDataType.Bool:       return 1;
            case _:
                # assert(false && "unknown ShaderType"); return 0;
                assert(False , "unknown ShaderType") # type: ignore
                return 0


class BufferLayout:
    def __init__(self, elements : list [BufferElement] = []):
        self._m_Elements : list[BufferElement] = elements
        self._m_Stride  : int = 0

        self.__CalculateOffsetAndStride()
        
    
    def getElements(self) -> list[BufferElement]:
        return self._m_Elements
    
    def GetStride(self):
        return self._m_Stride
    
    def __iter__(self):
        for element in self._m_Elements:
            yield element
    
    def __CalculateOffsetAndStride(self):
        
        offset = 0
        self._m_Stride = 0
        
        for element in self._m_Elements:
            element.Offset = offset;
            offset += element.Size;
            self._m_Stride += element.Size;




class VertexBuffer(ABC):
    def __init__(self):
        self._vertices : list[float] = []
        self._size = 0
    
    def Bind(self): ...
    def UnBind(self): ...

    def SetLayout(self, layout : BufferLayout): ...
    def GetLayout(self) -> BufferLayout: ...
    
    
    def GetVertices(self) -> list[float]: return self._vertices
    def GetSize(self) -> int: return self._size

    @staticmethod
    def Create(vertices : list [float] , size : int) -> VertexBuffer:
        from ApplicationEngine.src.Graphics.Renderer.Renderer import Renderer, RendererAPI
        match (Renderer.GetAPI()):
            case RendererAPI.API.SimpleGui:
                from ApplicationEngine.Platform.Simplegui.Renderer.SimpleGuiBuffer import SimpleGuiVertexBuffer
                return SimpleGuiVertexBuffer(vertices, size)
            
            case _ :
                raise NotImplemented      
    


class IndexBuffer(ABC):
    def __init__(self):
        self._indices : list[int] = []
        self._size = 0

    def Bind(self): ...
    def UnBind(self): ...

    def GetCount(self) -> int: ...



    def GetIndices(self) -> list[int]: return self._indices
    def GetSize(self) -> int: return self._size

    @staticmethod
    def Create(indices : list [int], size : int) -> IndexBuffer:
        from ApplicationEngine.src.Graphics.Renderer.Renderer import Renderer, RendererAPI
        match (Renderer.GetAPI()):
            case RendererAPI.API.SimpleGui:
                from ApplicationEngine.Platform.Simplegui.Renderer.SimpleGuiBuffer import SimpleGuiIndexBuffer
                return SimpleGuiIndexBuffer(indices, size)
            
            case _ :
                raise NotImplemented