from ApplicationEngine.src.Graphics.Renderer.Buffer import VertexBuffer, IndexBuffer
from ApplicationEngine.src.Graphics.Renderer.VertexArray import VertexArray




class SimpleGuiVertexArray(VertexArray):
    def __init__(self) -> None:
        super().__init__()
        self._m_VertexBuffers : list[VertexBuffer] = []
        self._m_IndexBuffer : IndexBuffer
        self._m_RendererID : int = 0

    def Bind(self):
        pass
    
    def UnBind(self):
        pass
    
    def AddVertexBuffer(self, vertexBuffer : VertexBuffer):
        vertexBuffer.Bind()
        
        index = 0
        layout = vertexBuffer.GetLayout()
        
        for element in layout:
            index += 1
            
        self._m_VertexBuffers.append(vertexBuffer)
    
    def SetIndexBuffer(self, indexBuffer : IndexBuffer):
        
        indexBuffer.Bind()
        self._m_IndexBuffer = indexBuffer
    
    def GetVetexBuffers(self): return self._m_VertexBuffers
    def GetIndexBuffer(self): return self._m_IndexBuffer