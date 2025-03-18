from ApplicationEngine.src.Object.ObjectClass import GameObject

from ApplicationEngine.src.Core.Utility.Temporal import *
from ApplicationEngine.src.Graphics.Renderer.Renderer import *

from ApplicationEngine.include.Maths.Maths import *



class Sprite(GameObject):
    def __init__(self, SpriteSheet : Texture, position : Vec2 , width : float, height : float, UVs : tuple[Vec2, Vec2] = (Vec2(0.0,1.0), Vec2(1.0,0.0)) ):
        from ApplicationEngine.src.Core.Game import Game

        self.GameWindow = Game.Get().GetWindow()

        self.spriteWidth  : float = width
        self.spriteHeight : float = height
        self.spriteAspectRatio : float = width / height





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
            uniform vec2 u_SpriteDimensions;
            uniform vec3 u_ScreenDimensions;

            out vec2 CurrentPosition;
            out vec2 TextureCoordinate;

            void main()
            {
                float scale_x = u_SpriteDimensions.x / u_ScreenDimensions.x;
                float scale_y = u_SpriteDimensions.y / u_ScreenDimensions.y;

                
                vec2 transformed_position = vec2(a_Pos.x + 1.0, a_Pos.y - 1.0); // transform top left to origin for scaling
                transformed_position = vec2(transformed_position.x * scale_x , transformed_position.y * scale_y);

                vec2 Transform = vec2(u_SpritePosition.x / u_ScreenDimensions.x, -u_SpritePosition.y / u_ScreenDimensions.y);

                transformed_position = transformed_position + Transform;
                transformed_position = transformed_position + vec2(-1.0, +1.0); // undo initial transform   


                CurrentPosition = transformed_position;
                TextureCoordinate = a_TexCoord;
                gl_Position = vec4(transformed_position, 0.0 , 1.0);
            }
        """
        SPRITE_FRAGMENT_SHADER = """
            #version 330 core

            out vec4 FragColor;


            in vec2 CurrentPosition;
            in vec2 TextureCoordinate;

            uniform sampler2D SpriteSheet;

            vec4 RenderSprite()
            {
                return texture(SpriteSheet,TextureCoordinate);
            }


            void main()
            {
                vec4 col = RenderSprite();
                if (col.x > 0.95 && col.y > 0.95 && col.z > 0.95) discard;
                FragColor = col;
                // FragColor = vec4(0.5f);
            }
        """


        self.SpriteShader : Shader = Shader(SPRITE_VERTEX_SHADER, SPRITE_FRAGMENT_SHADER)
        self.SheetTexture : Texture = SpriteSheet

        self.SpritePos : Vec2 = position

    def SetPos(self, position : Vec2): self.SpritePos = position
    def SetWidth(self, new_W : float): self.spriteWidth = new_W
    def SetHeight(self, new_H : float): self.spriteHeight = new_H
    
    
    def Draw(self):
        w_width   = self.GameWindow.GetWidth()
        w_height  = self.GameWindow.GetHeight()

        self.SpriteShader.Bind()


        self.SpriteShader.SetUniformVec2("u_SpritePosition", self.SpritePos)
        self.SpriteShader.SetUniformVec2("u_SpriteDimensions", Vec2(self.spriteWidth, self.spriteHeight))
        self.SpriteShader.SetUniformVec3("u_ScreenDimensions", Vec3(w_width, w_height, (w_width/w_height)))

        self.SheetTexture.Bind()
        self.SpriteShader.SetUniformInt("SpriteSheet", 0)

        Renderer.Submit(self.SpriteShader, self.VertexArray)