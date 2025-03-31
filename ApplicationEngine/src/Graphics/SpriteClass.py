from ApplicationEngine.src.Object.ObjectClass import GameObject

from ApplicationEngine.src.Core.Utility.Temporal import *
from ApplicationEngine.src.Graphics.Renderer.Renderer import *

from ApplicationEngine.include.Maths.Maths import *



class Sprite(GameObject):
    s_SpriteShader : Shader | None = None

    def __init__(self, SpriteSheet : Texture, position : Vec2 , width : float, height : float, UVs : tuple[Vec2, Vec2] = (Vec2(0.0,1.0), Vec2(1.0,0.0)) ):
        super().__init__()

        from ApplicationEngine.src.Core.Game import Game

        self.GameWindow = Game.Get().GetWindow()

        self.spriteWidth  : float = width
        self.spriteHeight : float = height
        self.spriteAspectRatio : float = width / height


        self.UVCache = UVs


        UV0 = UVs[0].get_p()
        UV1 = (UVs[1][0], UVs[0][1])
        UV2 = (UVs[0][0], UVs[1][1])
        UV3 = UVs[1].get_p()
        
        vertices = [
            # Positions        # UVs
            -1.0, -1.0,   UV2[0], UV2[1],  # Bottom-left
             1.0, -1.0,   UV3[0], UV3[1],  # Bottom-right
            -1.0,  1.0,   UV0[0], UV0[1],  # Top-left
             1.0,  1.0,   UV1[0], UV1[1]   # Top-right
        ]

        

        indices = [
            0, 1, 2,
            1, 3, 2
        ]


        self.VertexArray = VertexArray.Create()
        vb = VertexBuffer.Create(vertices, sizeof(c_float)*len(vertices))

        bufferLayout = BufferLayout(
            [
                BufferElement("a_Pos", ShaderDataType.Vec2),
                BufferElement("a_TexCoord", ShaderDataType.Vec2)
            ]
        )

        vb.SetLayout(bufferLayout)
        self.VertexArray.AddVertexBuffer(vb)

        ib = IndexBuffer.Create(indices, len(indices))
        self.VertexArray.SetIndexBuffer(ib)


        SPRITE_VERTEX_SHADER = """
            #version 330 core

            layout(location = 0) in vec2 a_Pos;
            layout(location = 1) in vec2 a_TexCoord;

            uniform vec2 u_SpritePosition;
            uniform float u_SpriteRotation;
            uniform vec2 u_SpriteDimensions;
            uniform vec2 u_ScreenDimensions;
            uniform float u_AspectRatio;

            uniform mat4 u_ViewProjection;

            out vec2 CurrentPosition;
            out vec2 TextureCoordinate;

            void main()
            {
                vec2 pos = a_Pos;

                float Cosr = cos(u_SpriteRotation);
                float Sinr = sin(u_SpriteRotation);

                mat2 rotationMatrix = mat2(Cosr, -Sinr, Sinr,  Cosr);

                //Apply the rotation
                pos = rotationMatrix * pos;
                // u_ScreenDimensions = rotationMatrix * u_ScreenDimensions;

                float scale_x = u_SpriteDimensions.x / u_ScreenDimensions.x;
                float scale_y = u_SpriteDimensions.y / u_ScreenDimensions.y;

                
                vec2 transformed_position = vec2(pos.x + 1.0, pos.y - 1.0); // transform top left to origin for scaling
                transformed_position = vec2(transformed_position.x * scale_x , transformed_position.y * scale_y);

                vec2 Transform = vec2(u_SpritePosition.x / u_ScreenDimensions.x, -u_SpritePosition.y / u_ScreenDimensions.y);

                transformed_position = transformed_position + (Transform * 2.0);
                transformed_position = transformed_position + vec2(-1.0, +1.0); // undo initial transform   


                CurrentPosition = transformed_position;
                TextureCoordinate = a_TexCoord;
                gl_Position = u_ViewProjection * vec4(CurrentPosition, 0.0 , 1.0);
            }
        """
        SPRITE_FRAGMENT_SHADER = """
            #version 330 core

            out vec4 FragColor;


            in vec2 CurrentPosition;
            in vec2 TextureCoordinate;

            uniform sampler2D SpriteSheet;
            uniform int flipped_lr;


            vec4 RenderSprite()
            {
                vec2 modUV = vec2( (1.0 - TextureCoordinate.x * flipped_lr + (TextureCoordinate.x) * (1 - flipped_lr) ), TextureCoordinate.y);
                return texture(SpriteSheet,modUV);
            }


            void main()
            {
                vec4 col = RenderSprite();
                // if (col.x > 0.95 && col.y > 0.95 && col.z > 0.95) discard;
                FragColor = col;
                // FragColor = vec4(0.5f);
            }
        """

        if not Sprite.s_SpriteShader:
            Sprite.s_SpriteShader = Shader(SPRITE_VERTEX_SHADER, SPRITE_FRAGMENT_SHADER)
        self.SheetTexture : Texture = SpriteSheet

        self.flipped_lr = False
        self.flipped_ud = False

        self.SpritePos : Vec2 = position
        self.SpriteRot : float = 0.0 # rotation in radians

    def SetPos(self, position : Vec2): self.SpritePos = position
    def SetRot(self, rotation : float): self.SpriteRot = rotation
    def SetWidth(self, new_W : float): self.spriteWidth = new_W
    def SetHeight(self, new_H : float): self.spriteHeight = new_H



    def copy(self):
        return Sprite(self.SheetTexture, self.SpritePos, self.spriteWidth, self.spriteHeight, self.UVCache)


    def Flip_lr(self):
        self.flipped_lr = not self.flipped_lr

    def Flip_ud(self):
        self.flipped_ud = not self.flipped_ud
    
    
    def Draw(self):
        w_width   = self.GameWindow.GetWidth()
        w_height  = self.GameWindow.GetHeight()

        if Sprite.s_SpriteShader:
            Sprite.s_SpriteShader.Bind()


            Sprite.s_SpriteShader.SetUniformVec2("u_SpritePosition", self.SpritePos)
            Sprite.s_SpriteShader.SetUniformFloat("u_SpriteRotation", self.SpriteRot)

            Sprite.s_SpriteShader.SetUniformVec2("u_SpriteDimensions", Vec2(self.spriteWidth, self.spriteHeight))
            Sprite.s_SpriteShader.SetUniformVec2("u_ScreenDimensions", Vec2(w_width, w_height))
            Sprite.s_SpriteShader.SetUniformFloat("u_AspectRatio", (w_width/w_height))

            Sprite.s_SpriteShader.SetUniformInt("flipped_lr", int(self.flipped_lr))
            
            self.SheetTexture.Bind()
            Sprite.s_SpriteShader.SetUniformInt("SpriteSheet", 0)

            if self.SheetTexture.hasTransparent:
                RenderCommand.Enable(GL_BLEND)
                Renderer.CustomRendererCommand(glBlendFunc, [GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA])
                Renderer.CustomRendererCommand(glDepthMask, [GL_FALSE])
                
            Renderer.SubmitImidiate(Sprite.s_SpriteShader, self.VertexArray)

            if self.SheetTexture.hasTransparent:
                Renderer.CustomRendererCommand(glDepthMask, [GL_TRUE])
                RenderCommand.Disable(GL_BLEND)