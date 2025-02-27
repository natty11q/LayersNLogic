from ApplicationEngine.src.Graphics.Renderer.RendererAPI import *
from ApplicationEngine.src.Core.Utility.CoreUtility import *
from ApplicationEngine.src.Core.Utility.Temporal import LLEngineTime

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
        ...
    
    
    def Clear(self, value : int = 0) -> None:
        self.__DrawQueue.clear()
    
    def Enable(self, value : int = 0) -> None:
        self.__RenderSettings |= value
        
        
        
        self.wfMode = self.__RenderSettings & SimpleGUiRendererAPI.RenderSettings.LL_SG_WIREFRAME_MODE_ENABLED
    
    def Disable(self, value : int = 0) -> None:
        pass
    
    
    
    ## TODO : change vertex argument to be a proper Vertex array instead. [ X ]
    ## TODO : finish the VA class [X] alongside SHADER CLASSES [ ]
    ## TODO : Implement Shader!!
    ## TODO : Add implementation that follows the buffer layout and draws triangles using the vertices
    def DrawIndexed(self,VertexArray : VertexArray) -> None:
        VBuffers : list[VertexBuffer] = VertexArray.GetVetexBuffers()
        IBuffers : IndexBuffer = VertexArray.GetIndexBuffer()
        
        
        RawVertices : list[Vector.Vec4] = []
        Colours : list[Vector.Vec4] = []
        for Vbuffer in VBuffers:
            
            vertexComponent : list[Vector.Vec4]= []
            
            bufferVertices = Vbuffer.GetVertices()
            layout = Vbuffer.GetLayout()
            
            elements : list [BufferElement] = layout.getElements()
            stride = layout.GetStride()
            
            for element in elements:
                if element.Name.lower() in ["a_position", "a_pos"]:

                    vIndex = element.Offset
                    while (vIndex <= Vbuffer.GetSize()):
                        vert = []
                        for j in range(element.Size):
                            vert.append(bufferVertices[vIndex + j])
                            
                        if element.Size <= 4: # if it isnt <= 4 then something has gone wrong
                            vertexComponent.append(Vector.Vec4(*vert))
                        vIndex += stride
                
                elif element.Name.lower() in ["a_colour", "a_col", "a_color"]:
                    CIndex = element.Offset
                    while (vIndex <= Vbuffer.GetSize()):
                        col = []
                        for j in range(element.Size):
                            col.append(bufferVertices[CIndex + j])      
                        if element.Size <= 4: # if it isnt <= 4 then something has gone wrong
                            Colours.append(Vector.Vec4(*col))
                        vIndex += stride
                    CIndex += stride

            RawVertices += vertexComponent

        
        self.__DrawQueue.append(
            {
                "type" : CommandType.DrawIndexed,
                "vertices" : RawVertices,
                "indices" : VertexArray.GetIndexBuffer().GetIndices(),
                "colours" : Colours
            }
        )

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
                "type" : CommandType.DrawTriangle,
                "vertices" : VertexPositions,
                "indices" : [0 , 1 , 2],
                "colour" : colour.toVec3().get_p()
            }
        )
    
    def DrawCircle(self, Position : Vector.Vec2, colour : Vector.Vec4) -> None: ...
            
    def Draw(self, *args):
        canvas : simplegui.Canvas = args[0]
        LLEngineTime.Update()
        
        for layer in RendererAPI._LayerStack:
            layer.OnUpdate()
        # input()
        
        for element in self.__DrawQueue:
            
            if element["type"] == CommandType.DrawTriangle:
                vertices : list [Vector.Vector] = element["vertices"]
                indices : list [int]= element["indices"]
                color = element["colour"]
                indexed_vertices = [(vertices[i].get_p()[0], vertices[i].get_p()[1]) for i in indices]
                
                if self.wfMode:
                    canvas.draw_polygon(indexed_vertices, 1, rgb_to_hex(color),None)
                else:
                    canvas.draw_polygon(indexed_vertices, 1, rgb_to_hex(color),rgb_to_hex(color))
        


            if element["type"] == CommandType.DrawIndexed:
                vertices : list [Vector.Vector] = element["vertices"]
                idices  : list[int] = element["indices"]
                colours : list[Vector.Vec4] = element["colours"]