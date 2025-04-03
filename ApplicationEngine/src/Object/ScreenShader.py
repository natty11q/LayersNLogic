from ApplicationEngine.include.Common import *
from ApplicationEngine.include.Maths.Maths import *
from ApplicationEngine.src.Event.Event import Event
from ApplicationEngine.src.Graphics.Renderer.Renderer import *

from ApplicationEngine.src.Object.ObjectClass import GameObject

from ApplicationEngine.src.Core.Utility.Temporal import *
from ApplicationEngine.src.Core.Mouse import *

class ScreenShader(GameObject):

    def __init__(self, VertexShader : str | None = None, FragmentShader : str | None = None, VertexShaderIsPath : bool = False, FragmentShaderIsPath : bool = False , texture : Texture | None = None):
        super().__init__()
        vertices = [
            # Positions        # UVs
            -1.0, -1.0, 0.0,   0.0, 0.0,  # Bottom-left
             1.0, -1.0, 0.0,   1.0, 0.0,  # Bottom-right
            -1.0,  1.0, 0.0,   0.0, 1.0,  # Top-left
             1.0,  1.0, 0.0,   1.0, 1.0   # Top-right
        ]

        indices = [
            0, 1, 2,
            1, 3, 2
        ]

        self.VertexArray = VertexArray.Create()

        vb = VertexBuffer.Create(vertices, sizeof(c_float)*len(vertices))

        bufferLayout = BufferLayout(
            [
                BufferElement("a_Pos", ShaderDataType.Vec3),
                BufferElement("a_TexCoord", ShaderDataType.Vec2)
            ]
        )

        vb.SetLayout(bufferLayout)

        self.VertexArray.AddVertexBuffer(vb)



        ib = IndexBuffer.Create(indices, len(indices))

        self.VertexArray.SetIndexBuffer(ib)


        self.DefaultVertexShader = """
            #version 330 core

            layout(location = 0) in vec3 a_Pos;
            layout(location = 1) in vec2 a_TexCoord;

            out vec2 CurrentPosition;
            out vec2 TextureCoordinate;

            void main()
            {
                CurrentPosition = a_Pos.xy;
                TextureCoordinate = a_TexCoord;
                gl_Position = vec4(a_Pos, 1.0);
            }
        """
       

#         DefaultFragmentShader = """
# #version 330 core

# out vec4 FragColor;

# in vec2 CurrentPosition;
# in vec2 TextureCoordinate;

# uniform sampler2D diffuse0;
# uniform float HudOpacity;
# uniform float Time;

# // (width, Height)
# uniform vec2 Dimensions;

# // (W/H)
# uniform float aspectRatio;



# vec4 RenderHudTextrue()
# {
#     return texture(diffuse0,TextureCoordinate) * vec4(1.0f,1.0f,1.0f,HudOpacity);
# }


# void main() {
#     FragColor = vec4(1.0 * ((cos(Time) + 1.0) / 2) ,0.0,0.0, 1.0);
# }
#        """




        # DefaultFragmentShader = get_file_contents("ApplicationEngine/src/Object/Shaders/ScreenShaderBackground.frag")

        if VertexShader:
            if VertexShaderIsPath:
                self.VertexShader = get_file_contents(VertexShader)
            else:
                self.VertexShader = VertexShader
        else:
            self.VertexShader = self.DefaultVertexShader


        if FragmentShader:
            if FragmentShaderIsPath:
                self.FragmentShader = get_file_contents(FragmentShader)
            else:
                self.FragmentShader = FragmentShader
        else:
            self.FragmentShader = get_file_contents("ApplicationEngine/src/Object/Shaders/ScreenShaderRaymarch.frag")


        self.Shader = Shader(self.VertexShader, self.FragmentShader)

        self.hasTexture = False

        if texture:
            self.Texture = texture
            self.hasTexture = True


        self.Campos_xy = Vec2()
    

    # def _OnEvent(self, event: Event):
    #     DefaultFragmentShader = get_file_contents("ApplicationEngine/src/Object/Shaders/ScreenShaderRaymarch.frag")
    #     self.Shader.RecompileShader(self.DefaultVertexShader, DefaultFragmentShader)

    def SetUniformFloat(self, type : ShaderDataType , name : str, value ):
        ...

    def Draw(self):

        self.Shader.Bind()
        

        self.Shader.SetUniformFloat("HudOpacity", 1.0)
        self.Shader.SetUniformFloat("Time", LLEngineTime.Time())
        self.Shader.SetUniformVec2("Dimensions", Vec2(900, 600)) # temporary Values , TODO : make it get the canvas dimensions
        self.Shader.SetUniformVec2("Campos_XY", self.Campos_xy) # temporary Values , TODO : make it get the canvas dimensions
        
        self.Shader.SetUniformFloat("aspectRatios", 900/600) # temporary Values , TODO : make it get the canvas dimensions


# uniform vec3 iResolution; // viewport resolution (in pixels)
# uniform float iTime;      // shader playback time (in seconds)
# uniform vec4 iMouse;      // mouse pixel coords. xy: current pos (when clicked)
# uniform int iFrame;       // shader playback frame


# for parity with shader toy

        self.Shader.SetUniformVec3("iResolution", Vec3(900, 600, (900/600)))
        self.Shader.SetUniformFloat("iTime", LLEngineTime.Time())
        mpos = Mouse.GetPos()
        mpressed = Mouse.GetPressed()
        self.Shader.SetUniformVec4("iMouse", Vec4(mpos.x, mpos.y, mpos.x, mpos.y))
        self.Shader.SetUniformInt("iFrame", LLEngineTime.FrameCount())


        if self.hasTexture:
            self.Texture.Bind()
            self.Shader.SetUniformInt("diffuse0", 0)
            self.Shader.SetUniformInt("texture0", 0)
        
        Renderer.Submit(self.Shader, self.VertexArray)