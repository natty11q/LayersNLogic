from ApplicationEngine.src.Graphics.Renderer.Buffer import *



class SimpleGuiVertexBuffer(VertexBuffer):
    def __init__(self, vertices : list[float] , size : int):
        self._m_RendererID = 0
        self._m_Layout : BufferLayout = BufferLayout()
    
    def GetLayout(self) -> BufferLayout:
        return self._m_Layout
    def SetLayout(self, layout : BufferLayout):
        self._m_Layout = layout

class SimpleGuiIndexBuffer(VertexBuffer):
    def __init__(self, indices : list[int] , size : int):
        self._m_RendererID = 0
        self._m_Count = 0
    
    def GetCount(self):
        return self._m_Count