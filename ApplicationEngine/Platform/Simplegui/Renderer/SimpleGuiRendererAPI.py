from ApplicationEngine.src.Graphics.Renderer.RendererAPI import *
from ApplicationEngine.src.Object.Object import *

from ApplicationEngine.src.Core.Utility.CoreUtility import *

try:
    import simplegui # type: ignore
except ImportError :
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui



class SimpleGUiRendererAPI(RendererAPI):
    
    class RenderSettings:
        LL_SG_TRANSPARENCY_ENABLLED     : int = 1
        LL_SG_WIREFRAME_MODE_ENABLED    : int = 2
    
    def __init__(self) -> None:
        self.__DrawQueue : list [dict] = []
        self.__RenderSettings : int = 0
        
        self.wfMode = self.__RenderSettings & SimpleGUiRendererAPI.RenderSettings.LL_SG_WIREFRAME_MODE_ENABLED
    
    def SetClearColour(self, col : Vector.Vec4) -> None:
        pass
    
    
    def Clear(self, value : int = 0) -> None:
        pass
    
    def Enable(self, value : int = 0) -> None:
        self.__RenderSettings |= value
        
        
        
        self.wfMode = self.__RenderSettings & SimpleGUiRendererAPI.RenderSettings.LL_SG_WIREFRAME_MODE_ENABLED
    
    def Disable(self, value : int = 0) -> None:
        pass
    
    
    ## TODO : change vertex argument to be a proper Vertex array instead.
    #TODO : finish the VA class alongside SHADER CLASSES
    def DrawIndexed(self,VertexArray) -> None: ...


    # TODO : Change this to return int
    def GetUniformLocation(self, ID : int, UniformName : str) -> None:
        pass
    

    def SetUniformInt(self, UniformLocation : int, value : int) -> None:
        pass
    
    
    def SetUniformVec2(self, UniformLocation : int, value : Vector.Vec2) -> None:
        pass
    
    
    def SetUniformVec3(self, UniformLocation : int, value : Vector.Vec3) -> None:
        pass
    
    
    def SetUniformVec4(self, UniformLocation : int, value : Vector.Vec4) -> None:
        pass
    
    
    def SetUniformMat2(self, UniformLocation : int, value : Matrix.Mat2) -> None:
        pass
    
    
    def SetUniformMat3(self, UniformLocation : int, value : Matrix.Mat3) -> None:
        pass
    

    def SetUniformMat4(self, UniformLocation : int, value : Matrix.Mat4) -> None:
        pass
    
    
    ## TODO : Decide if this shiould be extended to an SGUICOmmand Class instead of using raw Dicts | Done [ ]
    ## TODO : Command Type cna use an enum instead of the strings for faster lookup
    ## (can use an int and the two instead of an o(n) string comparison every frame) |  Done : [ x ]

    def DrawTriangle(self, VertexPositions : list [Vector.Vec2], colour : Vector.Vec4) -> None:
        self.__DrawQueue.append(
            {
                "type" : CommandType.DrawIndexed,
                "vertices" : VertexPositions,
                "indices" : [0 , 1 , 2],
                "colour" : colour.toVec3().get_p()
            }
        )
    
    def DrawCircle(self, Position : Vector.Vec2, colour : Vector.Vec4) -> None: ...
            
    def Draw(self, canvas : simplegui.Canvas):
        for layer in RendererAPI._LayerStack:
            layer.OnUpdate()
        # input()
        
        for element in self.__DrawQueue:
            if element["type"] == CommandType.DrawIndexed:
                vertices : list [Vector.Vec2] = element["vertices"]
                indices : list [int]= element["indices"]
                color = element["colour"]
                indexed_vertices = [vertices[i].get_p() for i in indices]
                
                if self.wfMode:
                    canvas.draw_polygon(indexed_vertices, 1, rgb_to_hex(color),None)
                else:
                    canvas.draw_polygon(indexed_vertices, 1, rgb_to_hex(color),rgb_to_hex(color))