from ApplicationEngine.include.Common import *
from ApplicationEngine.include.Maths.Maths import *


from OpenGL.GL import * # type: ignore

from OpenGL.GL.shaders import compileProgram, compileShader

# TODO : change shader and Texture classes to be seperate impls eg  simpleGuiTexture: 

DEFAULT_VERT = """
    #version 330 core
    
    void main()
    {
        gl_Position = vec4(0.0f);
    }
"""

DEFAULT_FRAG = """
    #version 330 core


    out vec4 FragColour;
    void main()
    {
        FragColour = vec4(1.0, 0.5, 0.5, 1.0);
    }


"""

class Shader:
    def __init__(self, vertexSource, fragmentSource):
        self._m_RendererID : int = 0
        self._m_uniformNameHash_ : dict[str , int] = {}

        self.RecompileShader(vertexSource, fragmentSource)
    
    def __del__(self):
        self.Delete()



    @staticmethod
    def CreateShaderFromFile(vertexFile: str, fragmentFile: str ):
        resource_path = "../../../../"  # Replace with actual resource path
        
        # Check if vertex file exists
        if not (os.path.exists(vertexFile) or os.path.exists(os.path.join(resource_path, vertexFile))):
            LNL_LogEngineError(f"Could not resolve shader from source: {vertexFile}\nTried: {vertexFile} , {os.path.join(resource_path, vertexFile)}")
            return Shader(DEFAULT_VERT, DEFAULT_FRAG)
        
        # Check if fragment file exists
        elif not (os.path.exists(fragmentFile) or os.path.exists(os.path.join(resource_path, fragmentFile))):
            LNL_LogEngineError(f"Could not resolve shader from source: {fragmentFile}\nTried: {fragmentFile} , {os.path.join(resource_path, fragmentFile)}")
            return Shader(DEFAULT_VERT, DEFAULT_FRAG)

        # Read the file contents for vertex and fragment shaders
        vertex_src = get_file_contents(vertexFile)
        fragment_src = get_file_contents(fragmentFile)

        return Shader(vertex_src, fragment_src)


    def RecompileShader(self, vertex_source, fragment_source) -> int:
    # ----------------------- create vertex shader ----------------------------

        vertex_shader = glCreateShader(GL_VERTEX_SHADER)

        # ensure that the shader is NULL terminated
        source = vertex_source.encode('utf-8')
        glShaderSource(vertex_shader, source)

        glCompileShader(vertex_shader)

        success = glGetShaderiv(vertex_shader, GL_COMPILE_STATUS)
        if not success:
            maxlen = glGetShaderiv(vertex_shader, GL_INFO_LOG_LENGTH)
            info_log = glGetShaderInfoLog(vertex_shader) 
            LNL_LogEngineError(f"\nVERTEX SHADER FAILURE: {info_log.decode('utf-8')}")

            glDeleteShader(vertex_shader)
            self._m_RendererID = self.RecompileShader(DEFAULT_VERT, DEFAULT_FRAG)
            return self._m_RendererID 
        # ----------------------- create fragment shader ----------------------------

        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)

        # ensure that the shader is NULL terminated
        source = fragment_source.encode('utf-8')
        glShaderSource(fragment_shader, source)

        glCompileShader(fragment_shader)

        success = glGetShaderiv(fragment_shader, GL_COMPILE_STATUS)
        if not success:
            maxlen = glGetShaderiv(fragment_shader, GL_INFO_LOG_LENGTH)
            info_log = glGetShaderInfoLog(fragment_shader)
            LNL_LogEngineError(f"\nFRAGMENT SHADER FAILURE: {info_log.decode('utf-8')}")

            glDeleteShader(fragment_shader)
            glDeleteShader(vertex_shader)
            self._m_RendererID = self.RecompileShader(DEFAULT_VERT, DEFAULT_FRAG)
            return self._m_RendererID 
        # Create shader program
        self._m_RendererID = glCreateProgram() # type: ignore
        LNL_LogWarning("created shader with id: ", self._m_RendererID)

        glAttachShader(self._m_RendererID, vertex_shader)
        glAttachShader(self._m_RendererID, fragment_shader)

        glLinkProgram(self._m_RendererID)

        is_linked = glGetProgramiv(self._m_RendererID, GL_LINK_STATUS)

        if not is_linked:
            maxlen = glGetProgramiv(self._m_RendererID, GL_INFO_LOG_LENGTH)
            info_log = glGetProgramInfoLog(self._m_RendererID, maxlen)
            LNL_LogEngineError(f"\nSHADER LINK FAILURE: {info_log.decode('utf-8')}")

            glDeleteProgram(self._m_RendererID)
            glDeleteShader(fragment_shader)
            glDeleteShader(vertex_shader)
            
            self._m_RendererID = self.RecompileShader(DEFAULT_VERT, DEFAULT_FRAG)
            return self._m_RendererID 

        # Detach shaders after linking
        glDetachShader(self._m_RendererID, vertex_shader)
        glDetachShader(self._m_RendererID, fragment_shader)

        # glDeleteShader(self._m_RendererID)

        return self._m_RendererID


    def Bind(self):
        from ApplicationEngine.src.Graphics.Renderer.RenderCommand import RenderCommand
        RenderCommand.BindShader(self._m_RendererID)
        # glUseProgram(self._m_RendererID)
    def UnBind(self):
        glUseProgram(0)
    def Delete(self):
        glDeleteProgram(self._m_RendererID)
    
    
    def SetUniformFloat(self, name : str, val :  float ):
        from ApplicationEngine.src.Graphics.Renderer.RenderCommand import RenderCommand
        RenderCommand.SetUniformFloat(self._getUniformLocation(name), val) 
    
    def SetUniformInt(self, name : str, val: int):
        from ApplicationEngine.src.Graphics.Renderer.RenderCommand import RenderCommand
        RenderCommand.SetUniformInt(self._getUniformLocation(name), val) 

    
    def SetUniformVec2(self, name : str, vec : Vec2):
        from ApplicationEngine.src.Graphics.Renderer.RenderCommand import RenderCommand
        RenderCommand.SetUniformVec2(self._getUniformLocation(name), vec) 

    def SetUniformVec3(self, name : str, vec : Vec3):
        from ApplicationEngine.src.Graphics.Renderer.RenderCommand import RenderCommand
        RenderCommand.SetUniformVec3(self._getUniformLocation(name), vec) 

    def SetUniformVec4(self, name : str, vec : Vec4):
        from ApplicationEngine.src.Graphics.Renderer.RenderCommand import RenderCommand
        RenderCommand.SetUniformVec4(self._getUniformLocation(name), vec) 
    


    def SetUniformMatrix2(self, name : str, mat : Mat2):
        from ApplicationEngine.src.Graphics.Renderer.RenderCommand import RenderCommand
        RenderCommand.SetUniformMat2(self._getUniformLocation(name), mat) 
    
    def SetUniformMatrix3(self, name : str, mat : Mat3):
        from ApplicationEngine.src.Graphics.Renderer.RenderCommand import RenderCommand
        RenderCommand.SetUniformMat3(self._getUniformLocation(name), mat)

    def SetUniformMatrix4(self, name : str, mat : Mat4):
        from ApplicationEngine.src.Graphics.Renderer.RenderCommand import RenderCommand
        RenderCommand.SetUniformMat4(self._getUniformLocation(name), mat) 


    def Get_id(self) -> int: return self._m_RendererID

    def _getUniformLocation(self, uniformName : str):
        from ApplicationEngine.src.Graphics.Renderer.RenderCommand import RenderCommand
        retVal : int= 0
        if uniformName in self._m_uniformNameHash_:
            retVal = self._m_uniformNameHash_[uniformName]
        else:
            retVal = RenderCommand.GetUniformLocation(self._m_RendererID, uniformName)
            self._m_uniformNameHash_[uniformName] = retVal
        return retVal
