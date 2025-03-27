from ApplicationEngine.src.Graphics.Renderer.Buffer import VertexBuffer, IndexBuffer
from ApplicationEngine.src.Graphics.Renderer.VertexArray import VertexArray


from OpenGL.GL import * # type: ignore
from OpenGL.GL.shaders import compileProgram, compileShader

class SimpleGuiVertexArray(VertexArray):
    def __init__(self) -> None:
        super().__init__()
        self._m_VertexBuffers : list[VertexBuffer] = []
        self._m_IndexBuffer : IndexBuffer
        self._m_RendererID : int = glGenVertexArrays(1)

    def Bind(self):
        glBindVertexArray(self._m_RendererID)
    
    def UnBind(self):
        glBindVertexArray(0)
    
    def AddVertexBuffer(self, vertexBuffer : VertexBuffer):
        
        glBindVertexArray(self._m_RendererID)
        vertexBuffer.Bind()
        
        index = 0
        layout = vertexBuffer.GetLayout()
        
        for element in layout:
            glEnableVertexAttribArray(index)
            glVertexAttribPointer(index, element.GetComponentCount(), 
                                  element.GetGLBaseType(), 
                                  GL_FALSE, layout.GetStride(), 
                                  ctypes.c_void_p(element.Offset))
            index += 1
            
        self._m_VertexBuffers.append(vertexBuffer)
    
    def SetIndexBuffer(self, indexBuffer : IndexBuffer):
        glBindVertexArray(self._m_RendererID)
        indexBuffer.Bind()
        self._m_IndexBuffer = indexBuffer
    
    def GetVetexBuffers(self): return self._m_VertexBuffers
    def GetIndexBuffer(self): return self._m_IndexBuffer