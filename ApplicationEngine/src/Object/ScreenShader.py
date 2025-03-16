from ApplicationEngine.include.Common import *
from ApplicationEngine.include.Maths.Maths import *
from ApplicationEngine.src.Graphics.Renderer.Renderer import *

from ApplicationEngine.src.Object.ObjectClass import GameObject

from ApplicationEngine.src.Core.Utility.Temporal import *

class ScreenShader(GameObject):

    def __init__(self):
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


        DefaultVertexShader = """
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





        DefaultFragmentShader = get_file_contents("ApplicationEngine/src/Object/Shaders/ScreenShaderRaymarch.frag")
        # DefaultFragmentShader = get_file_contents("ApplicationEngine/src/Object/Shaders/ScreenShaderBackground.frag")

        self.Shader = Shader(DefaultVertexShader, DefaultFragmentShader)

        self.Texture = Texture("ApplicationEngine/src/Object/Textures/testImage3.png")
    


    def Draw(self):

        self.Shader.Bind()
        

        self.Shader.SetUniformFloat("HudOpacity", 1.0)
        self.Shader.SetUniformFloat("Time", LLEngineTime.Time())
        self.Shader.SetUniformVec2("Dimensions", Vec2(900, 600)) # temporary Values , TODO : make it get the canvas dimensions
        
        self.Shader.SetUniformFloat("aspectRatios", 900/600) # temporary Values , TODO : make it get the canvas dimensions

        self.Texture.Bind()
        self.Shader.SetUniforInt("texture0", 0)
        
        Renderer.Submit(self.Shader, self.VertexArray)