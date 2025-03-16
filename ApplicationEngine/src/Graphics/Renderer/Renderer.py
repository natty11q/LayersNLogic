from ApplicationEngine.include.Common import *
from ApplicationEngine.src.Graphics.Renderer.RenderCommand import *
from ApplicationEngine.src.Graphics.Renderer.VertexArray import *
from ApplicationEngine.src.Graphics.Camera.Camera import *


    
    
    
    
from ApplicationEngine.src.Graphics.Renderer.ShaderProgram import Shader
class Renderer:
    
    __Objects = []
    

    @staticmethod
    def BeginScene(camera : Camera):
        pass 
   
    @staticmethod
    def EndScene():
        pass
    
    @staticmethod
    def Submit(shader : Shader, vertexArray: VertexArray):
        #modify for defered rendering
        RenderCommand.DrawIndexed(shader, vertexArray)
    

    @staticmethod
    def SubmitImidiate(shader : Shader, vertexArray: VertexArray):
        vertexArray.Bind()
        RenderCommand.DrawIndexed(shader,vertexArray)
    
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
    def SetClearColour( col : Vec4 ) -> None:
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
    def DrawIndexed(shader : Shader, VertexArray : VertexArray) -> None:
        RenderCommand.DrawIndexed(shader, VertexArray)
    
    @staticmethod
    def GetUniformLocation(ID : int, UniformName : str) -> int:
        return RenderCommand.GetUniformLocation(ID, UniformName)
    
    
    @staticmethod
    def SetUniformInt(UniformLocation : int, value : int) -> None:
        RenderCommand.SetUniformInt(UniformLocation, value)

    @staticmethod
    def SetUniformFloat(UniformLocation : int, value : float) -> None:
        RenderCommand.SetUniformFloat(UniformLocation, value)
    
    
    @staticmethod
    def SetUniformVec2(UniformLocation : int, value : Vec2) -> None:
        RenderCommand.SetUniformVec2(UniformLocation, value)
    
    
    @staticmethod
    def SetUniformVec3(UniformLocation : int, value : Vec3) -> None:
        RenderCommand.SetUniformVec3(UniformLocation, value)
    
    
    @staticmethod
    def SetUniformVec4(UniformLocation : int, value : Vec4) -> None:
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
    def DrawTriangle(VertexPositions : list [Vec2], colour : Vec4):
        RenderCommand.DrawTriangle(VertexPositions, colour)
    
    @staticmethod
    def DrawCircle(Position : Vec2, colour : Vec4):
        RenderCommand.DrawCircle(Position, colour)
        
    @staticmethod
    def Draw(*args):
        RenderCommand.Draw(*args)
    
    @staticmethod
    def GetAPI():
        return RendererAPI.GetAPI()