from ApplicationEngine.src.Graphics.Renderer.RendererAPI import *


from ApplicationEngine.Platform.Simplegui.Renderer.SimpleGuiRendererAPI import SimpleGUiRendererAPI
from ApplicationEngine.Platform.Pygame.Renderer.PygameRendererAPI import PygameRendererAPI


class RenderCommand():
    
    # TODO : change api settings to be in 1 location only.
    s_RendererAPI : RendererAPI = SimpleGUiRendererAPI()
    
    @staticmethod
    def PushLayer(layer : Layer):
        RenderCommand.s_RendererAPI.PushLayer(layer)
        
    @staticmethod
    def PopLayer():
        RenderCommand.s_RendererAPI.PopLayer()
    
    @staticmethod
    def PushOverlay(layer : Layer):
        RenderCommand.s_RendererAPI.PushOverlay(layer)
    
    @staticmethod
    def PopOverlay():
        RenderCommand.s_RendererAPI.PopOverlay()
    
    
    @staticmethod
    def SetClearColour( col : Vec4 ) -> None:
        RenderCommand.s_RendererAPI.SetClearColour(col)


    @staticmethod
    def CustomRendererCommand(command, args : list) -> None:
        RenderCommand.s_RendererAPI.CustomRendererCommand(command, args)
    
    @staticmethod
    def Clear( value : int = 0) -> None:
        RenderCommand.s_RendererAPI.Clear(value)
    
    @staticmethod
    def Enable( value : int = 0) -> None:
        RenderCommand.s_RendererAPI.Enable(value)
    
    @staticmethod
    def Disable( value : int = 0) -> None:
        RenderCommand.s_RendererAPI.Disable(value)
    
    @staticmethod
    def DrawIndexed( shader: Shader, vertexArray : VertexArray) -> None:
        RenderCommand.s_RendererAPI.DrawIndexed(shader, vertexArray)
    

    @staticmethod
    def BindShader(ID : int) -> None:
        return RenderCommand.s_RendererAPI.BindShader(ID)

    @staticmethod
    def GetUniformLocation(ID : int, UniformName : str) -> int:
        return RenderCommand.s_RendererAPI.GetUniformLocation(ID, UniformName)
    
    
    @staticmethod
    def SetUniformInt(UniformLocation : int, value : int) -> None:
        RenderCommand.s_RendererAPI.SetUniformInt(UniformLocation, value)
    
    @staticmethod
    def SetUniformFloat(UniformLocation : int, value : float) -> None:
        RenderCommand.s_RendererAPI.SetUniformFloat(UniformLocation, value)
    
    
    @staticmethod
    def SetUniformVec2(UniformLocation : int, value : Vec2) -> None:
        RenderCommand.s_RendererAPI.SetUniformVec2(UniformLocation, value)
    
    
    @staticmethod
    def SetUniformVec3(UniformLocation : int, value : Vec3) -> None:
        RenderCommand.s_RendererAPI.SetUniformVec3(UniformLocation, value)
    
    
    @staticmethod
    def SetUniformVec4(UniformLocation : int, value : Vec4) -> None:
        RenderCommand.s_RendererAPI.SetUniformVec4(UniformLocation, value)
    
    
    @staticmethod
    def SetUniformMat2(UniformLocation : int, value : Matrix.Mat2) -> None:
        RenderCommand.s_RendererAPI.SetUniformMat2(UniformLocation, value)
    
    
    @staticmethod
    def SetUniformMat3(UniformLocation : int, value : Matrix.Mat3) -> None:
        RenderCommand.s_RendererAPI.SetUniformMat3(UniformLocation, value)
    
    
    @staticmethod
    def SetUniformMat4(UniformLocation : int, value : Matrix.Mat4) -> None:
        RenderCommand.s_RendererAPI.SetUniformMat4(UniformLocation, value)
    
    
    @staticmethod
    def DrawTriangle(VertexPositions : list [Vec2], colour : Vec4):
        RenderCommand.s_RendererAPI.DrawTriangle(VertexPositions, colour)
    
    @staticmethod
    def DrawCircle(Position : Vec2, colour : Vec4):
        RenderCommand.s_RendererAPI.DrawCircle(Position, colour)
    
    @staticmethod
    def BindTexture(tex_id : int):
        RenderCommand.s_RendererAPI.BindTexture(tex_id)

    @staticmethod
    def DrawText(text : str, position : Vec2,  size : int, colour : Vec3):
        RenderCommand.s_RendererAPI.DrawText(text,position,size, colour)


    @staticmethod
    def Draw(*args):
        RenderCommand.s_RendererAPI.Draw(*args)