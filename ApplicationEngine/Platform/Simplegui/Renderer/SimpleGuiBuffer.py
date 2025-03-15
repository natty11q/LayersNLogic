from ApplicationEngine.src.Graphics.Renderer.Buffer import *

from OpenGL.GL import * # type: ignore
from OpenGL.GL.shaders import compileProgram, compileShader


class SimpleGuiVertexBuffer(VertexBuffer):
    def __init__(self, vertices : list[float] | np.ndarray, size : int):
        if not isinstance(vertices, np.ndarray):
            self._vertices = np.array(vertices, dtype=np.float32)
        else:
            self._vertices = vertices # avoids accidental post modification of the vertex array
        
        self._size = size
        
        self._m_Layout : BufferLayout = BufferLayout()

        self._m_RendererID = glGenBuffers(1)


        glBindBuffer(GL_ARRAY_BUFFER, self._m_RendererID)
        glBufferData(GL_ARRAY_BUFFER, self._size, self._vertices, GL_STATIC_DRAW)
    


    def Bind(self):
        glBindBuffer(GL_ARRAY_BUFFER, self._m_RendererID)

    def UnBind(self):
        glBindBuffer(GL_ARRAY_BUFFER, 0)


    def GetLayout(self) -> BufferLayout:
        return self._m_Layout
    
    def SetLayout(self, layout : BufferLayout):
        self._m_Layout = layout

class SimpleGuiIndexBuffer(IndexBuffer):
    def __init__(self, indices : list[int] , count : int):
        self._indices : list[int] = indices.copy() # avoids accidental post modification of the index array
        # self._size = size
        
        self._m_Count = count
        self._m_RendererID = glGenBuffers(1)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._m_RendererID)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self._m_Count * sizeof(c_uint) ,(c_uint * len(indices))(*indices) ,GL_STATIC_DRAW)
        
    
    def GetCount(self):
        return self._m_Count
    
    def Bind(self):
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._m_RendererID)

    def UnBind(self):
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)