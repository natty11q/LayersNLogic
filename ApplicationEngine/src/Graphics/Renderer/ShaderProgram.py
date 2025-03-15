from ApplicationEngine.include.Common import *
from ApplicationEngine.include.Maths.Maths import *
from ApplicationEngine.src.Graphics.Renderer.RenderCommand import RenderCommand


from OpenGL.GL import * # type: ignore


class Shader:
    def __init__(self, vertexSource, fragmentSource):
        self._m_RendererID : int = 0
        self._m_uniformNameHash_ : dict[str , int] = {}

        self.RecompileShader(vertexSource, fragmentSource)

    @staticmethod
    def CreateShaderFromFile(vertexFile: str, fragmentFile: str ):
        resource_path = "../../../../"  # Replace with actual resource path
        
        # Check if vertex file exists
        if not (os.path.exists(vertexFile) or os.path.exists(os.path.join(resource_path, vertexFile))):
            LNL_LogEngineError(f"Could not resolve shader from source: {vertexFile}\nTried: {vertexFile} , {os.path.join(resource_path, vertexFile)}")
            return None
        
        # Check if fragment file exists
        elif not (os.path.exists(fragmentFile) or os.path.exists(os.path.join(resource_path, fragmentFile))):
            LNL_LogEngineError(f"Could not resolve shader from source: {fragmentFile}\nTried: {fragmentFile} , {os.path.join(resource_path, fragmentFile)}")
            return None

        # Read the file contents for vertex and fragment shaders
        vertex_src = get_file_contents(vertexFile)
        fragment_src = get_file_contents(fragmentFile)

        return Shader(vertex_src, fragment_src)


    def RecompileShader(self, vertex_source, fragment_source):
    # ----------------------- create vertex shader ----------------------------

        vertex_shader = glCreateShader(GL_VERTEX_SHADER)

        # ensure that the shader is NULL terminated
        source = vertex_source.encode('utf-8')
        glShaderSource(vertex_shader, 1, [source], None)

        glCompileShader(vertex_shader)

        success = glGetShaderiv(vertex_shader, GL_COMPILE_STATUS)
        if not success:
            maxlen = glGetShaderiv(vertex_shader, GL_INFO_LOG_LENGTH)
            info_log = glGetShaderInfoLog(vertex_shader, maxlen)
            LNL_LogEngineError(f"\nVERTEX SHADER FAILURE: {info_log.decode('utf-8')}")

            glDeleteShader(vertex_shader)
            return

        # ----------------------- create fragment shader ----------------------------

        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)

        # ensure that the shader is NULL terminated
        source = fragment_source.encode('utf-8')
        glShaderSource(fragment_shader, 1, [source], None)

        glCompileShader(fragment_shader)

        success = glGetShaderiv(fragment_shader, GL_COMPILE_STATUS)
        if not success:
            maxlen = glGetShaderiv(fragment_shader, GL_INFO_LOG_LENGTH)
            info_log = glGetShaderInfoLog(fragment_shader, maxlen)
            LNL_LogEngineError(f"\nFRAGMENT SHADER FAILURE: {info_log.decode('utf-8')}")

            glDeleteShader(fragment_shader)
            glDeleteShader(vertex_shader)
            return

        # Create shader program
        self._m_RendererID = glCreateProgram() # type: ignore

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
            return

        # Detach shaders after linking
        glDetachShader(self._m_RendererID, vertex_shader)
        glDetachShader(self._m_RendererID, fragment_shader)

        return self._m_RendererID


    def Bind(self):
        glUseProgram(self._m_RendererID)
    def UnBind(self):
        glUseProgram(0)
    def Delete(self): ...



    def SetUniformFloat(self, name : str, val :  float ):
        RenderCommand.SetUniformFloat(self._getUniformLocation(name), val) 
    def SetUniforInt(self, name : str, val: int):
        RenderCommand.SetUniformInt(self._getUniformLocation(name), val) 

    
    def SetUniformVec2(self, name : str, vec : Vec2):
        RenderCommand.SetUniformVec2(self._getUniformLocation(name), vec) 

    def SetUniformVec3(self, name : str, vec : Vec3):
        RenderCommand.SetUniformVec3(self._getUniformLocation(name), vec) 

    def SetUniformVec4(self, name : str, vec : Vec4):
        RenderCommand.SetUniformVec4(self._getUniformLocation(name), vec) 
    


    def SetUniformMatrix2(self, name : str, mat : Mat2):
        RenderCommand.SetUniformMat2(self._getUniformLocation(name), mat) 
    
    def SetUniformMatrix3(self, name : str, mat : Mat3):
        RenderCommand.SetUniformMat3(self._getUniformLocation(name), mat)

    def SetUniformMatrix4(self, name : str, mat : Mat4):
        RenderCommand.SetUniformMat4(self._getUniformLocation(name), mat) 


    def Get_id(self) -> int: return self._m_RendererID

    def _getUniformLocation(self, uniformName : str):
        retVal : int= 0
        if uniformName in self._m_uniformNameHash_:
            retVal = self._m_uniformNameHash_[uniformName]
        else:
            retVal = RenderCommand.GetUniformLocation(self._m_RendererID, uniformName)
            self._m_uniformNameHash_[uniformName] = retVal
        return retVal
