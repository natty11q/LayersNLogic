from __future__ import annotations

from ApplicationEngine.src.Graphics.Renderer.Buffer import *



class VertexArray:
    
    def Bind(self): ...
    def UnBind(self): ...
    
    def AddVertexBuffer(self, vertexBuffer : VertexBuffer): ...
    def SetIndexBuffer(self, indexBuffer : IndexBuffer): ...
    
    
    def GetVetexBuffers(self) -> list[VertexBuffer]: ...
    def GetIndexBuffer(self) -> IndexBuffer: ...
    
    @staticmethod
    def Create() -> VertexArray:
        from ApplicationEngine.src.Graphics.Renderer.Renderer import Renderer , RendererAPI
        api = Renderer.GetAPI()
        match api:
            case RendererAPI.API.NoAPI:
                from ApplicationEngine.Platform.Simplegui.Renderer.SimpleGuiVertexArray import SimpleGuiVertexArray
                return SimpleGuiVertexArray()
            case _:
                print(f"Unimplemented Api for vertex array : {api}")
                raise Exception()