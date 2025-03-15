from ApplicationEngine.src.Graphics.Renderer.RendererAPI import *
from ApplicationEngine.src.Core.Utility.CoreUtility import *
from ApplicationEngine.src.Core.Utility.Temporal import LLEngineTime

try:
    import simplegui # type: ignore
except ImportError :
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


from ApplicationEngine.Logger.LNLEngineLogger import *

# from ApplicationEngine.src.Graphics.Renderer.ShaderProgram import Shader


from collections import OrderedDict
import glfw
from OpenGL.GL import * # type: ignore
from OpenGL.GL.shaders import compileProgram, compileShader

import pygame



_dummy = simplegui.load_image("")
DummyImage  = type(_dummy)
class SimpleGUIImageWrapper(DummyImage):# type: ignore
    def __init__(self, surface):
        self._pygame_surface = surface
        self.center = (surface.get_width() / 2, surface.get_height() / 2)
        self.size = (surface.get_width(), surface.get_height())
        self._pygamesurfaces_cached = OrderedDict()
        self._pygamesurfaces_cached_clear = lambda: self._pygamesurfaces_cached.clear()
        self._pygamesurfaces_cache_max_size = getattr(_dummy, "_pygamesurfaces_cache_default_max_size", 50)
        self._draw_count = 0




class SimpleGUiRendererAPI(RendererAPI):
    
    
    def __init__(self) -> None:
        self.__DrawQueue : list [dict] = []
        self.__RenderSettings : int = 0

        self.wrappedImage = None
        self.fbo : int = -1
        self.fbo_texture = None

        self.init_gl()


    def init_gl(self):
        # Initialize GLFW
        if not glfw.init():
            return
        
        # Set GLFW window hints (optional)
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)

        # Create a windowed mode window and its OpenGL context
        window = glfw.create_window(800, 600, "OpenGL with GLFW", None, None)
        if not window:
            glfw.terminate()
            return

        # Make the window's context current
        glfw.make_context_current(window)


        # ----------------------------

        
        



    
    def SetClearColour(self, col : Vec4) -> None:
        self.__DrawQueue.append(
            {
                "type" : CommandType.SetClearColour,
                "colour" : col
            }
        )
    
    
    def Clear(self, value : int = 0) -> None:
        self.__DrawQueue.append(
            {
                "type" : CommandType.Clear
            }
        )
    
    def Enable(self, value : int = 0) -> None:
        self.__RenderSettings |= value

        self.__DrawQueue.append(
            {
                "type" : CommandType.Enable,
                "value" : value
            }
        )
        
    def Disable(self, value : int = 0) -> None:
        self.__RenderSettings ^= value

        self.__DrawQueue.append(
            {
                "type" : CommandType.Disable,
                "value" : value
            }
        )    
    
    
    ## TODO : change vertex argument to be a proper Vertex array instead. [ X ]
    ## TODO : finish the VA class [X] alongside SHADER CLASSES [ ]
    ## TODO : Implement Shader!!
    ## TODO : Add implementation that follows the buffer layout and draws triangles using the vertices
    def DrawIndexed(self,VertexArray : VertexArray) -> None:
        
        self.__DrawQueue.append(
            {
                "type" : CommandType.DrawIndexed,
                "vertexArray" : VertexArray 
            }
        )

    # TODO : Change this to return int
    def GetUniformLocation(self, ID : int, UniformName : str) -> int:
        return glGetUniformLocation(ID, UniformName)
    

    def SetUniformInt(self, UniformLocation : int, value : int) -> None:
        glUniform1i(UniformLocation, value)

    def SetUniformFloat(self, UniformLocation : int, value : float) -> None:
        glUniform1f(UniformLocation, value)
    
    
    def SetUniformVec2(self, UniformLocation : int, value : Vec2) -> None:
        glUniform2f(UniformLocation, value[0], value[1])
    
    
    def SetUniformVec3(self, UniformLocation : int, value : Vec3) -> None:
        glUniform3f(UniformLocation, value[0], value[1], value[2])
    
    
    def SetUniformVec4(self, UniformLocation : int, value : Vec4) -> None:
        glUniform4f(UniformLocation, value[0], value[1], value[2], value[3])

    
    
    def SetUniformMat2(self, UniformLocation : int, value : Mat2) -> None:
        glUniformMatrix2fv(UniformLocation, 1, GL_FALSE, value.nparr())
    
    
    def SetUniformMat3(self, UniformLocation : int, value : Mat3) -> None:
        glUniformMatrix3fv(UniformLocation, 1, GL_FALSE, value.nparr())
    

    def SetUniformMat4(self, UniformLocation : int, value : Mat4) -> None:
        glUniformMatrix4fv(UniformLocation, 1, GL_FALSE, value.nparr())
    
    
    ## TODO : Decide if this shiould be extended to an SGUICOmmand Class instead of using raw Dicts | Done [ ]
    ## TODO : Command Type cna use an enum instead of the strings for faster lookup
    ## (can use an int and the two instead of an o(n) string comparison every frame) |  Done : [ x ]

    def DrawTriangle(self, VertexPositions : list [Vec2], colour : Vec4) -> None:
        self.__DrawQueue.append(
            {
                "type" : CommandType.DrawTriangle,
                "vertices" : VertexPositions,
                "indices" : [0 , 1 , 2],
                "colour" : colour.toVec3().get_p()
            }
        )
    
    def DrawCircle(self, Position : Vec2, colour : Vec4) -> None: ...




    def SetupFbo(self, width, height):
        self.fbo = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)

        self.fbo_texture = glGenTextures(1)
        # recalc the fbo texture in case of window resize
        glBindTexture(GL_TEXTURE_2D, self.fbo_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                    0, GL_RGB, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.fbo_texture, 0)

        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            print("Error: Framebuffer is not complete!")
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def updateWrappedImage(self, width, height):
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        data = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        image_array = np.frombuffer(data, dtype=np.uint8).reshape(height, width, 3)# type: ignore
        # OpenGL's origin is bottom-left, so flip vertically.

        # image_array = np.flipud(image_array)
        
        # Create a pygame surface; note pygame expects (width, height, channels)
        surf = pygame.surfarray.make_surface(np.transpose(image_array, (1, 0, 2)))
        self.wrappedImage = SimpleGUIImageWrapper(surf)





    def Draw(self, *args):
        canvas : simplegui.Canvas = args[0]
        LLEngineTime.Update()
        
        for layer in RendererAPI._LayerStack:
            layer.OnUpdate(LLEngineTime.DeltaTime())
 

        self.SetupFbo(canvas._width, canvas._height)





        for element in self.__DrawQueue:
            if element["type"] == CommandType.Enable:
                glEnable(element["value"])
                self.__RenderSettings |= element["value"]
            
            if element["type"] == CommandType.Disable:
                glDisable(element["value"])
                self.__RenderSettings ^= element["value"]
            
            if element["type"] == CommandType.Clear:
                self.__DrawQueue.clear()
                glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) #type: ignore
                glBindFramebuffer(GL_FRAMEBUFFER, 0)

            
            if element["type"] == CommandType.SetClearColour:
                col : Vec4 = element["colour"]
                glClearColor(*col.get_p())

            
            if element["type"] == CommandType.DrawTriangle:
                vertices : list [Vec2 | Vec3 | Vec4] = element["vertices"]
                indices : list [int]= element["indices"]
                color = element["colour"]
                indexed_vertices : list[tuple[float, float, float]] = [(vertices[i].get_p()[0], vertices[i].get_p()[1], 0.0) for i in indices]
                
                
                glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)

                glBegin(GL_TRIANGLES)
                for vertex in indexed_vertices:
                    glColor3f(color[0], color[1], color[3])
                    glVertex3f(vertex[0], vertex[1], vertex[2])
                glEnd()

                glBindFramebuffer(GL_FRAMEBUFFER, 0)


            if element["type"] == CommandType.DrawIndexed:
                vertexArray : VertexArray = element["vertexArray"]
                # shader : VertexArray = element["shader"]
                glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)

                vertexArray.Bind()
                glDrawElements(GL_TRIANGLES, vertexArray.GetIndexBuffer().GetCount(), GL_UNSIGNED_INT , None)

                glBindFramebuffer(GL_FRAMEBUFFER, 0)

        self.updateWrappedImage(canvas._width, canvas._height)
        if self.wrappedImage:
            canvas.draw_image(self.wrappedImage,
                            self.wrappedImage.center,
                            self.wrappedImage.size,
                            (canvas._width / 2, canvas._height / 2),
                            self.wrappedImage.size)
            
        else:
            canvas.draw_text("Rendering...", (canvas._width // 2 - 50, canvas._height // 2), 20, "White")


# from normalised coord system to screenspace
def denormalisePos(vertex : tuple[float, float], w , h) -> tuple[float, float]:
    # LNL_LogEngineInfo(vertex)
    return ( ((vertex[0] + 1) / 2) * w,  h - ((vertex[1] + 1) / 2) * h )