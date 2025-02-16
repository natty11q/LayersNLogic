from ApplicationEngine.include.Common import *
from ApplicationEngine.include.Window.Window import *
from ApplicationEngine.src.Graphics.Renderer.RenderCommand import *

class Renderer:
    
    __Objects = []
    
    @staticmethod
    def Submit(renderWindow : Window):
        pass
    
    @staticmethod
    def BeginScene(renderWindow : Window, camera):
        pass
   
    @staticmethod
    def EndScene():
        pass
    
    @staticmethod
    def SubmitImidiate():
        pass
    
    @staticmethod
    def PushLayer(layer : Layer):
        RenderCommand.PushLayer(layer)
        
    @staticmethod
    def PopLayer():
        RenderCommand.PopLayer()
    
    @staticmethod
    def PushOverlay(layer : Layer):
        RenderCommand.PushOverlay(layer)
    
    @staticmethod
    def PopOverlay():
        RenderCommand.PopOverlay()
    
    @staticmethod
    def SetClearColour( col : Vector.Vec4 ) -> None:
        RenderCommand.SetClearColour(col)
    
    @staticmethod
    def Clear( value : int = 0) -> None:
        RenderCommand.Clear(value)
    
    @staticmethod
    def Enable( value : int = 0) -> None:
        RenderCommand.Enable(value)
    
    @staticmethod
    def Disable( value : int = 0) -> None:
        RenderCommand.Disable(value)
    
    @staticmethod
    def DrawIndexed(VertexArray) -> None:
        RenderCommand.DrawIndexed(VertexArray)
    
    @staticmethod
    def GetUniformLocation(ID : int, UniformName : str) -> None:
        RenderCommand.GetUniformLocation(ID, UniformName)
    
    
    @staticmethod
    def SetUniformInt(UniformLocation : int, value : int) -> None:
        RenderCommand.SetUniformInt(UniformLocation, value)
    
    
    @staticmethod
    def SetUniformVec2(UniformLocation : int, value : Vector.Vec2) -> None:
        RenderCommand.SetUniformVec2(UniformLocation, value)
    
    
    @staticmethod
    def SetUniformVec3(UniformLocation : int, value : Vector.Vec3) -> None:
        RenderCommand.SetUniformVec3(UniformLocation, value)
    
    
    @staticmethod
    def SetUniformVec4(UniformLocation : int, value : Vector.Vec4) -> None:
        RenderCommand.SetUniformVec4(UniformLocation, value)
    
    
    @staticmethod
    def SetUniformMat2(UniformLocation : int, value : Matrix.Mat2) -> None:
        RenderCommand.SetUniformMat2(UniformLocation, value)
    
    
    @staticmethod
    def SetUniformMat3(UniformLocation : int, value : Matrix.Mat3) -> None:
        RenderCommand.SetUniformMat3(UniformLocation, value)
    
    
    @staticmethod
    def SetUniformMat4(UniformLocation : int, value : Matrix.Mat4) -> None:
        RenderCommand.SetUniformMat4(UniformLocation, value)
    
    
    @staticmethod
    def DrawTriangle(VertexPositions : list [Vector.Vec2], colour : Vector.Vec4):
        RenderCommand.DrawTriangle(VertexPositions, colour)
    
    @staticmethod
    def DrawCircle(Position : Vector.Vec2, colour : Vector.Vec4):
        RenderCommand.DrawCircle(Position, colour)
        
    @staticmethod
    def Draw(*args):
        RenderCommand.Draw(*args)
    
    @staticmethod
    def GetAPI():
        return RendererAPI.GetAPI()