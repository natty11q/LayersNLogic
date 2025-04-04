from ApplicationEngine.src.Graphics.Renderer.RendererAPI import *
from ApplicationEngine.src.Core.Utility.CoreUtility import *
from ApplicationEngine.src.Core.Utility.Temporal import LLEngineTime

try:
    import simplegui # type: ignore
except ImportError :
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


from ApplicationEngine.Logger.LNLEngineLogger import *

from ApplicationEngine.src.Graphics.Renderer.ShaderProgram import Shader
from ApplicationEngine.src.Graphics.Renderer.Texture import Texture


from collections import OrderedDict
import glfw
from OpenGL.GL import * # type: ignore

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
        self._DrawQueue : list [list] = []
        self.__RenderSettings : int = 0

        self.wrappedImage = None
        self.fbo : int = -1
        self.fbo_texture = None

        self.init_gl()

        self.TRIANGLE_VERTEX_SHADER_SRC = """
        #version 330 core
        layout(location = 0) in vec3 aPos;
        uniform vec3 uColour;

        out vec3 vertexColor;
        void main() {
            gl_Position = vec4(aPos, 1.0);
            vertexColor = uColour;
        }
        """

        self.TRIANGLE_FRAGMENT_SHADER_SRC = """
        #version 330 core
        in vec3 vertexColor;
        out vec4 FragColor;
        void main() {
            FragColor = vec4(vertexColor, 1.0);
        }
        """

        self.triangleShader : Shader | None = None
    
    
    # def mouse_callback(self, window, button, action, mods):
    #     ...


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
        window = glfw.create_window(900, 600, "OpenGL with GLFW", None, None)
        if not window:
            glfw.terminate()
            return

        # Make the window's context current
        glfw.make_context_current(window)

        # self.TriangleVao = -1
        # self.TriangleVbo = -1
        
        
        glViewport(0, 0, 900, 600) # default values
        
        
        
        self.fbo = glGenFramebuffers(1)
        self.fbo_texture = glGenTextures(1)
        
        
        self.SetupFbo(900, 600)

        

        # ----------------------------

        
        

    def CustomRendererCommand(self, command, args : list):
            # {
            #     "type" : CommandType.CustomCommand,
            #     "func" : command,
            #     "args" : args
            # }

        self._DrawQueue.append(
            [
                CommandType.CustomCommand,
                command,
                args
            ]
        )

    
    def SetClearColour(self, col : Vec4) -> None:
            # {
            #     "type" : CommandType.SetClearColour,
            #     "colour" : col
            # }        
        glClearColor(*col.get_p())
        self._DrawQueue.append(
            [
                CommandType.SetClearColour,
                col
            ]
        )
    
    
    def Clear(self, value : int = 0) -> None:
            # {
            #     "type" : CommandType.Clear,
            # }
        self._DrawQueue.clear()
        self._DrawQueue.append(
            [
                CommandType.Clear,
            ]
        )

    
    def Enable(self, value : int = 0) -> None:
        self.__RenderSettings |= value
        # {
        #         "type" : CommandType.Enable,
        #         "value" : value
        # }
        self._DrawQueue.append(
            [
                CommandType.Enable,
                value
            ]
        )
        
    def Disable(self, value : int = 0) -> None:
        self.__RenderSettings ^= value
        # {
        #     "type" : CommandType.Disable,
        #     "value" : value
        # }
        self._DrawQueue.append(
            [
                CommandType.Disable,
                value
            ]
        )    
    
    
    ## TODO : change vertex argument to be a proper Vertex array instead. [ X ]
    ## TODO : finish the VA class [X] alongside SHADER CLASSES [X]
    ## TODO : Implement Shader [X]!!
    ## TODO : Add implementation that follows the buffer layout and draws triangles using the vertices [x]
    ## COMPLETE !!

    def DrawIndexed(self, shader: Shader, VertexArray : VertexArray) -> None:
        
        # {
        #     "type" : CommandType.DrawIndexed,
        #     "vertexArray" : VertexArray,
        #     "shader" : shader
        # }
        self._DrawQueue.append(
            [
                CommandType.DrawIndexed,
                VertexArray,
                shader
            ]
        )

    def BindShader(self, ID) -> None:
        glUseProgram(ID) # <= important to bind here also for getting uniform locations ingame

        # {
        #     "type" : CommandType.BindShader,
        #     "ID" : ID
        # }
        self._DrawQueue.append(
            [
                CommandType.BindShader,
                ID
            ]
        )

    # TODO : Change this to return int
    def GetUniformLocation(self, ID : int, UniformName : str) -> int:
        return glGetUniformLocation(ID, UniformName)
    

    def SetUniformInt(self, UniformLocation : int, value : int) -> None:
        # {
        #     "type" : CommandType.SetUniformInt,
        #     "uniformLocation" : UniformLocation,
        #     "value" : value
        # }
        self._DrawQueue.append(
            [
                CommandType.SetUniformInt,
                UniformLocation,
                value
            ]
        )
    def SetUniformFloat(self, UniformLocation : int, value : float) -> None:
        # {
        #     "type" : CommandType.SetUniformFloat,
        #     "uniformLocation" : UniformLocation,
        #     "value" : value
        # }
        self._DrawQueue.append(
            [
                CommandType.SetUniformFloat,
                UniformLocation,
                value
            ]
        )
    
    
    def SetUniformVec2(self, UniformLocation : int, value : Vec2) -> None:
        # {
        #     "type" : CommandType.SetUniformVec2,
        #     "uniformLocation" : UniformLocation,
        #     "value" : value.get_p()
        # }
        self._DrawQueue.append(
            [
                CommandType.SetUniformVec2,
                UniformLocation,
                value.get_p()
            ]
        )
        # glUniform2f(UniformLocation, value[0], value[1])
    
    
    def SetUniformVec3(self, UniformLocation : int, value : Vec3) -> None:
        # {
        #     "type" : CommandType.SetUniformVec3,
        #     "uniformLocation" : UniformLocation,
        #     "value" : value.get_p()
        # }
        self._DrawQueue.append(
            [
                CommandType.SetUniformVec3,
                UniformLocation,
                value.get_p()
            ]
        )
        # glUniform3f(UniformLocation, value[0], value[1], value[2])
    
    
    def SetUniformVec4(self, UniformLocation : int, value : Vec4) -> None:
        # {
        #     "type" : CommandType.SetUniformVec4,
        #     "uniformLocation" : UniformLocation,
        #     "value" : value.get_p()
        # }
        self._DrawQueue.append(
            [
                CommandType.SetUniformVec4,
                UniformLocation,
                value.get_p()
            ]
        )
        # glUniform4f(UniformLocation, value[0], value[1], value[2], value[3])

    
    
    def SetUniformMat2(self, UniformLocation : int, value : Mat2) -> None:
        # {
        #     "type" : CommandType.SetUniformMat2,
        #     "uniformLocation" : UniformLocation,
        #     "transpose" : GL_FALSE,
        #     "value" : value.nparr()
        # }
        self._DrawQueue.append(
            [
                CommandType.SetUniformMat2,
                UniformLocation,
                GL_FALSE,
                value.nparr()
            ]
        )
        # glUniformMatrix2fv(UniformLocation, 1, GL_FALSE, value.nparr())
    
    
    def SetUniformMat3(self, UniformLocation : int, value : Mat3) -> None:
        # {
        #     "type" : CommandType.SetUniformMat3,
        #     "uniformLocation" : UniformLocation,
        #     "transpose" : GL_FALSE,
        #     "value" : value.nparr()
        # }
        self._DrawQueue.append(
            [
                CommandType.SetUniformMat3,
                UniformLocation,
                GL_FALSE,
                value.nparr()
            ]
        )
        # glUniformMatrix3fv(UniformLocation, 1, GL_FALSE, value.nparr())
    

    def SetUniformMat4(self, UniformLocation : int, value : Mat4) -> None:
        # {
        #     "type" : CommandType.SetUniformMat4,
        #     "uniformLocation" : UniformLocation,
        #     "transpose" : GL_FALSE,
        #     "value" : value.nparr()
        # }
        self._DrawQueue.append(
            [
                CommandType.SetUniformMat4,
                UniformLocation,
                GL_FALSE,
                value.nparr()
            ]
        )
        # glUniformMatrix4fv(UniformLocation, 1, GL_FALSE, value.nparr())
    

    def BindTexture(self, tex_id : int):
        # {
        #     "type" : CommandType.BindTexture,
        #     "tex_id" : tex_id
        # }
        self._DrawQueue.append(
            [
                CommandType.BindTexture,
                tex_id
            ]
        )

    
    ## TODO : Decide if this shiould be extended to an SGUICOmmand Class instead of using raw Dicts | Done [ ]
    ## TODO : Command Type cna use an enum instead of the strings for faster lookup
    ## (can use an int and the two instead of an o(n) string comparison every frame) |  Done : [ x ]

    def DrawTriangle(self, VertexPositions : list [Vec2], colour : Vec4) -> None:
        # {
        #     "type" : CommandType.DrawTriangle,
        #     "vertices" : VertexPositions,
        #     "indices" : [0 , 1 , 2],
        #     "colour" : colour.toVec3()
        # }
        self._DrawQueue.append(
            [
                CommandType.DrawTriangle,
                VertexPositions,
                [0 , 1 , 2],
                colour.toVec3()
            ]
        )
    
    def DrawCircle(self, Position : Vec2, colour : Vec4) -> None: ...


    def DrawText(self, text : str, position : Vec2,  size : int, colour : Vec3):
        self._DrawQueue.append(
            [
                CommandType.DrawText,
                text,
                position.get_p(),
                size,
                colour.get_p()
            ]
        )
    

    def SetupFbo(self, width, height):
        # glDeleteTextures(1, [self.fbo_texture])
        glViewport(0, 0, width, height)

        # self.fbo = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        # self.fbo_texture = glGenTextures(1)

        # recalc the fbo texture in case of window resize
        glBindTexture(GL_TEXTURE_2D, self.fbo_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                    0, GL_RGB, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.fbo_texture, 0)

        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            LNL_LogEngineError("Error: Framebuffer is not complete!")
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
    


    def updateWrappedImage(self, width, height):
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        data = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        image_array = np.frombuffer(data, dtype=np.uint8).reshape(height, width, 3)# type: ignore
        # OpenGL's origin is bottom-left, so flip vertically.

        image_array = np.flipud(image_array)
        
        # Create a pygame surface; note pygame expects (width, height, channels)
        surf = pygame.surfarray.make_surface(np.transpose(image_array, (1, 0, 2)))
        self.wrappedImage = SimpleGUIImageWrapper(surf)





    def Draw(self, *args):
        # glViewport(0,0,900,600)
        canvas : simplegui.Canvas = args[0]
        LLEngineTime.Update()
        # self.pygame_event_callback()
        
        # self.SetupFbo(canvas._width, canvas._height)
        for layer in RendererAPI._LayerStack:
            layer.OnUpdate(LLEngineTime.DeltaTime())
 
        postQueue = []





        for element in self._DrawQueue:
            eType = element[0]


            # ======== shaders ====

            if eType == CommandType.BindShader:
                glUseProgram(element[1])

            elif eType == CommandType.SetUniformInt:
                glUniform1i(element[1], element[2])
            elif eType == CommandType.SetUniformFloat:
                glUniform1f(element[1], element[2])



            elif eType == CommandType.SetUniformVec2:
                x, y =  element[2]
                glUniform2f(element[1],x , y)

            elif eType == CommandType.SetUniformVec3:
                x, y, z = element[2]
                glUniform3f(element[1], x, y, z)

            elif eType == CommandType.SetUniformVec4:
                x, y, z, w =  element[2]
                glUniform4f(element[1], x, y, z, w)


            elif eType == CommandType.SetUniformMat2:
                glUniformMatrix2fv(element[1], 1, element[2], element[3])
            elif eType == CommandType.SetUniformMat3:
                glUniformMatrix3fv(element[1], 1, element[2], element[3])
            elif eType == CommandType.SetUniformMat4:
                glUniformMatrix4fv(element[1], 1, element[2], element[3])






            # =========
            
            if eType == CommandType.Enable:
                glEnable(element[1])
                self.__RenderSettings |= element[1]
            
            elif eType == CommandType.Disable:
                glDisable(element[1])
                self.__RenderSettings ^= element[1]
            
            elif eType == CommandType.CustomCommand:
                glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)

                element[1](*element[2])
                
                glBindFramebuffer(GL_FRAMEBUFFER, 0)
            
            elif eType == CommandType.Clear:
                glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) #type: ignore
                glBindFramebuffer(GL_FRAMEBUFFER, 0)
            
            elif eType == CommandType.SetClearColour:
                col : Vec4 = element[1]

            elif eType == CommandType.BindTexture:
                tex_id = element[1]
                glActiveTexture(GL_TEXTURE0)
                glBindTexture(GL_TEXTURE_2D, tex_id)
            
            elif eType == CommandType.DrawTriangle:
                vertices : list [Vec2 | Vec3 | Vec4] = element[1]
                indices : list [int]= element[2]
                tricol : Vec3 = element[3]

                p_indexed_vertices : list[tuple[float, float, float]] = [(normalisePos(vertices[i].get_p(), canvas._width, canvas._height)) for i in indices]
                
                indexed_vertices = np.array(p_indexed_vertices, dtype=np.float32).flatten()
                
                
                vao = glGenVertexArrays(1)
                glBindVertexArray(vao)
        

                vbo = glGenBuffers(1)
                glBindBuffer(GL_ARRAY_BUFFER, vbo)

                # Upload the vertex data to the GPU
                glBufferData(GL_ARRAY_BUFFER, indexed_vertices.nbytes, indexed_vertices, GL_STATIC_DRAW)

                # Enable the vertex attribute for position (location = 0 in shader)
                glEnableVertexAttribArray(0)
                glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 4, ctypes.c_void_p(0))

                if not self.triangleShader:
                    self.triangleShader = Shader(self.TRIANGLE_VERTEX_SHADER_SRC,self.TRIANGLE_FRAGMENT_SHADER_SRC)




                glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
                
                # Use a simple shader program (make sure your shader is active)
                self.triangleShader.Bind()  # Ensure `shader_program` is set before calling this function

                # Set the color uniform (assuming the shader has a 'uColour' uniform)
                self.triangleShader.SetUniformVec3("uColour", tricol.divide(255))
                # if color_location != -1:
                #     glUniform3f(color_location, *color)
                # else:
                #     LNL_LogEngineWarning("Uniform 'uColour' not found in the shader!")

                # Draw the triangle
                glDrawArrays(GL_TRIANGLES, 0, 3)

                # Cleanup
                glBindBuffer(GL_ARRAY_BUFFER, 0)
                glBindVertexArray(0)
                glDeleteBuffers(1, [vbo])
                glDeleteVertexArrays(1, [vao])

                glBindFramebuffer(GL_FRAMEBUFFER, 0)


            elif eType == CommandType.DrawIndexed:
                vertexArray : VertexArray = element[1]
                shader : Shader = element[2]

                glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)

                shader.Bind()
                vertexArray.Bind()
                glDrawElements(GL_TRIANGLES, vertexArray.GetIndexBuffer().GetCount(), GL_UNSIGNED_INT , None)

                glBindFramebuffer(GL_FRAMEBUFFER, 0)

            elif eType == CommandType.DrawText:
                postQueue.append(element)

        self.updateWrappedImage(canvas._width, canvas._height)
        if self.wrappedImage:
            canvas.draw_image(self.wrappedImage,
                            self.wrappedImage.center,
                            self.wrappedImage.size,
                            (canvas._width / 2, canvas._height / 2),
                            self.wrappedImage.size)
            
        else:
            canvas.draw_text("Rendering...", (canvas._width // 2 - 50, canvas._height // 2), 20, "White")

        for element in postQueue:
            eType = element[0]

            if eType == CommandType.DrawText:
                canvas.draw_text(element[1],element[2],element[3], rgb_to_hex(element[4]))


# from normalised coord system to screenspace
def denormalisePos(vertex : tuple[float, float], w , h) -> tuple[float, float]:
    # LNL_LogEngineInfo(vertex)
    return ( ((vertex[0] + 1) / 2) * w,  h - ((vertex[1] + 1) / 2) * h )

def normalisePos(position : tuple[float, ...], screen_width, screen_height) -> tuple[float, float, float]:
    """
    Converts a screen-space position (pixels) into normalized OpenGL coordinates (-1 to 1)
    and flips the Y-axis.

    Parameters:
    - position: Tuple (x, y) in pixel coordinates
    - screen_width: Screen width in pixels
    - screen_height: Screen height in pixels

    Returns:
    - Tuple (nx, ny) in normalized device coordinates (-1 to 1)
    """
    x, y = position
    
    # Convert to normalized coordinates (-1 to 1)
    nx = (x / screen_width) * 2 - 1  # Normalize X
    ny = 1 - (y / screen_height) * 2  # Normalize Y (flips it)

    return (nx, ny , 0.0)