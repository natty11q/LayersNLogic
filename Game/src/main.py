## ============================== setup ===================================
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from ApplicationEngine.include.Maths.Maths import *
import ApplicationEngine.AppEngine as LNLEngine
## ============================= App Code =================================


from Game.src.GameComponents.Player.PlayerClass import *

import math


# from Game.src.MainMenu.MainMenuLayer import *
from Game.src.MainMenu.MainMenuScene import *
from Game.src.World.World import *

class MovingSquare(LNLEngine.Quad):
    def __init__(self, topLeft: LNLEngine.Vec2, width: float, height: float, colour: LNLEngine.Vec4):
        super().__init__(topLeft, width, height, colour)
        self.RestPos : LNLEngine.Vec2 = topLeft
        
    def _OnUpdate(self, deltatime: float):
        self._topLeft = Vec2( self.RestPos.x + ( 300 * math.cos(LNLEngine.LLEngineTime.Time() * 2) ), self.RestPos.y + ( 300 * math.sin(LNLEngine.LLEngineTime.Time() * 2) ))



class Cube(LNLEngine.GameObject):
    def __init__(self, scale : float= 1, rotation : Quat.Quat = Quat.Quat() ,position : Vec3 = Vec3(0,0,-100)):
        super().__init__()

        VERTEX_SHADER = """
            #version 330 core
            layout(location = 0) in vec3 a_Pos;
            layout(location = 1) in vec3 a_Col;
            layout(location = 2) in vec3 a_Normal;

            out vec3 vertexColor;
            void main() {
                vertexColor = a_Col;
                gl_Position = vec4(a_Pos, 1.0);
            }
        """
        FRAGMENT_SHADER = """
            #version 330 core
            in vec3 vertexColor;
            out vec4 FragColor;
            void main() {
                FragColor = vec4(vertexColor, 1.0);
            }
        """
        self.shader : LNLEngine.Shader = LNLEngine.Shader(VERTEX_SHADER, FRAGMENT_SHADER)

        self.m_vertexArray = LNLEngine.VertexArray.Create()

        self.baseVertices = [ 
            # position          # colour        # normal
            # face 1 (front face)
            -0.5,-0.5,-0.5,     0.0,0.0,1.0,        0.0,0.0,-1.0,        
             0.5,-0.5,-0.5,     0.0,0.0,1.0,        0.0,0.0,-1.0,        
             0.5, 0.5,-0.5,     0.0,0.0,1.0,        0.0,0.0,-1.0,       
            -0.5, 0.5,-0.5,     0.0,0.0,1.0,        0.0,0.0,-1.0,       

            # face 2 (let face)
            -0.5,-0.5,0.5,      0.0,1.0,0.0,        -1.0,0.0,-0.0,        
            -0.5,-0.5,-0.5,     0.0,1.0,0.0,        -1.0,0.0,-0.0,        
            -0.5,0.5,-0.5,      0.0,1.0,0.0,        -1.0,0.0,-0.0,        
            -0.5,0.5,0.5,       0.0,1.0,0.0,        -1.0,0.0,-0.0,        
            
            # face 3 (top face)
            -0.5, 0.5,-0.5,     1.0,0.0,0.0,         0.0,1.0,-0.0,       
            0.5, 0.5,-0.5,      1.0,0.0,0.0,         0.0,1.0,-0.0,        
            0.5, 0.5,0.5,       1.0,0.0,0.0,         0.0,1.0,-0.0,        
            -0.5, 0.5,0.5,      1.0,0.0,0.0,         0.0,1.0,-0.0,        
            
            # face 4 (bottom face)
            -0.5, -0.5,0.5,     1.0,0.0,1.0,        0.0,-1.0,-0.0,        
            0.5, -0.5,0.5,      1.0,0.0,1.0,        0.0,-1.0,-0.0,        
            0.5, -0.5,-0.5,     1.0,0.0,1.0,        0.0,-1.0,-0.0,       
            -0.5, -0.5,-0.5,    1.0,0.0,1.0,        0.0,-1.0,-0.0,       

            # face 5 (right face)
            0.5,-0.5,-0.5,      0.0,1.0,1.0,        1.0,0.0,-0.0,        
            0.5,-0.5,0.5,       0.0,1.0,1.0,        1.0,0.0,-0.0,        
            0.5,0.5,0.5,        0.0,1.0,1.0,        1.0,0.0,-0.0,        
            0.5,0.5,-0.5,       0.0,1.0,1.0,        1.0,0.0,-0.0,        

            # face 6 (back face)
            0.5,-0.5,0.5,       1.0,1.0,0.0,        1.0,0.0,1.0,        
             -0.5,-0.5,0.5,     1.0,1.0,0.0,        1.0,0.0,1.0,       
             -0.5, 0.5,0.5,     1.0,1.0,0.0,        1.0,0.0,1.0,        
            0.5, 0.5,0.5,       1.0,1.0,0.0,        1.0,0.0,1.0,   
        ]

        VertexBuffer = LNLEngine.VertexBuffer.Create(self.baseVertices, len(self.baseVertices))

        self.layout = LNLEngine.BufferLayout(
            [
                LNLEngine.BufferElement("a_pos", LNLEngine.ShaderDataType.Vec3),
                LNLEngine.BufferElement("a_col", LNLEngine.ShaderDataType.Vec3),
                LNLEngine.BufferElement("a_normal", LNLEngine.ShaderDataType.Vec3)
            ]
        )

        VertexBuffer.SetLayout(self.layout)
        self.m_vertexArray.AddVertexBuffer(VertexBuffer)



        indices = [
            0,1,2,
            2,3,0,
              
            4,5,6,
            6,7,4,
              
            8,9,10,
            10,11,8,
              
            12,13,14,
            14,15,12,
              
            16,17,18,
            18,19,16,
              
            20,21,22,
            22,23,20
        ]
        
        self.IndexBuffer = LNLEngine.IndexBuffer.Create(indices , len(indices))

        self.m_vertexArray.SetIndexBuffer(self.IndexBuffer)

    

        self.translate = Matrix.translate(Mat4(), position)
        self.rotate = rotation
        self.scale = Mat4() * scale

    def _OnUpdate(self, deltatime : float):
        transformedVertices = self.baseVertices

        vec = [0.0, 0.0, 0.0]
        for i in range(len(transformedVertices)):
            
            
            if i % 9 < 3:
                vec[0] = transformedVertices[i]

                if i % 9 == 2:

                    # LNLEngine.LNL_LogTrace(toMat4(self.rotate))
                    
                    transform : Mat4 = (self.scale * self.translate * toMat4(self.rotate))
                    position : Vec4 =   Vec4(*vec) * transform
                
                    for i in range(3):
                        j = 2 - i
                        transformedVertices[i - j] = position[i]
        
        # LNLEngine.LNL_LogEngineTrace(self.baseVertices)
        # LNLEngine.LNL_LogEngineInfo(transformedVertices)

        self.m_vertexArray = LNLEngine.VertexArray.Create()
        
        VertexBuffer = LNLEngine.VertexBuffer.Create(transformedVertices, len(transformedVertices))
        VertexBuffer.SetLayout(self.layout)

        self.m_vertexArray.AddVertexBuffer(VertexBuffer)
        self.m_vertexArray.SetIndexBuffer(self.IndexBuffer)



    def Draw(self):
        # LNLEngine.Renderer.Submit(self.m_vertexArray)
        LNLEngine.Renderer.DrawIndexed(self.shader, self.m_vertexArray)


class TestPhysicsObject(LNLEngine.GameObject2D):
    def __init__(self, position: LNLEngine.Vec2 = Vec2(), mass: float = 100):
        super().__init__(position, mass)

        LNLEngine.Renderer.SetClearColour(LNLEngine.Vec4(0.15,0.1,0.2,1.0))

        VERTEX_SHADER = """
            #version 330 core
            layout(location = 0) in vec3 a_Pos;
            layout(location = 1) in vec3 a_Col;
            layout(location = 2) in vec3 a_Normal;

            uniform vec3 worldPosition;

            out vec3 vertexColor;
            void main() {
                vertexColor = a_Col;
                gl_Position = vec4(a_Pos + worldPosition, 1.0);
            }
        """
        FRAGMENT_SHADER = """
            #version 330 core
            in vec3 vertexColor;
            out vec4 FragColor;
            void main() {
                FragColor = vec4(vertexColor, 1.0);
            }
        """
        self.shader : LNLEngine.Shader = LNLEngine.Shader(VERTEX_SHADER, FRAGMENT_SHADER)

        self.m_vertexArray = LNLEngine.VertexArray.Create()

        vertices = [ 
            # position          # colour        # normal
            -0.5, -0.5, 0.0,    0.3, 0.2, 0.8,  0.0, 0.0, 1.0,
             0.5, -0.5, 0.0,    0.8, 0.2, 0.3,  0.0, 0.0, 1.0,
             0.5,  0.5, 0.0,    0.3, 0.8, 0.2,  0.0, 0.0, 1.0,
            -0.5,  0.5, 0.0,    0.7, 0.4, 0.8,  0.0, 0.0, 1.0
            ]
        
        VertexBuffer = LNLEngine.VertexBuffer.Create(vertices, LNLEngine.sizeof(LNLEngine.c_float) * len(vertices))

        layout = LNLEngine.BufferLayout(
            [
                LNLEngine.BufferElement("a_pos", LNLEngine.ShaderDataType.Vec3),
                LNLEngine.BufferElement("a_col", LNLEngine.ShaderDataType.Vec3),
                LNLEngine.BufferElement("a_normal", LNLEngine.ShaderDataType.Vec3)
            ]
        )
        VertexBuffer.SetLayout(layout)
        self.m_vertexArray.AddVertexBuffer(VertexBuffer)


        indices = [0 ,1 ,2, 
                   2 ,3 ,0]
        
        IndexBuffer = LNLEngine.IndexBuffer.Create(indices , len(indices))

        self.m_vertexArray.SetIndexBuffer(IndexBuffer)

        LNLEngine.Game.Get().GetPhysicsSystem2D().addRigidbody(self.body, True)


    
    def Draw(self):

        self.shader.Bind()
        self.shader.SetUniformVec3("worldPosition",Vec3( *( self.body.getPosition() / 1000 ) .get_p() ))
        LNLEngine.Renderer.Submit(self.shader ,self.m_vertexArray)

class TestLayer(LNLEngine.Layer):
    def __init__(self, name="TestLayer"):
        super().__init__(name)
        self.gameWindow = LNLEngine.Game.Get().GetWindow()
        
        # =================================
        # testSquareWidth = 100
        # testSquareHeight = 100
        
        # self.TestSquare = MovingSquare(
        #     LNLEngine.Vec2(
        #         self.gameWindow.GetWidth() / 2 - (testSquareWidth/2),
        #         self.gameWindow.GetHeight() / 2 - (testSquareHeight/2)
        #     ),
        #     testSquareWidth, testSquareHeight,
        #     LNLEngine.Vec4(255,255,0,0)
        # )
        
        LNLEngine.Renderer.SetClearColour(LNLEngine.Vec4(0.15,0.1,0.2,1.0))

        VERTEX_SHADER = """
            #version 330 core
            layout(location = 0) in vec3 a_Pos;
            layout(location = 1) in vec3 a_Col;
            layout(location = 2) in vec3 a_Normal;

            uniform mat4 u_ViewProjection;

            out vec3 vertexColor;
            void main() {
                vertexColor = a_Col;
                gl_Position = u_ViewProjection * vec4(a_Pos, 1.0);
            }
        """
        FRAGMENT_SHADER = """
            #version 330 core
            in vec3 vertexColor;
            out vec4 FragColor;
            void main() {
                FragColor = vec4(vertexColor, 1.0);
            }
        """
        self.shader : LNLEngine.Shader = LNLEngine.Shader(VERTEX_SHADER, FRAGMENT_SHADER)

        self.m_vertexArray = LNLEngine.VertexArray.Create()

        vertices = [ 
            # position          # colour        # normal
            -0.5, -0.5, 0.0,    0.3, 0.2, 0.8,  0.0, 0.0, 1.0,
             0.5, -0.5, 0.0,    0.8, 0.2, 0.3,  0.0, 0.0, 1.0,
             0.5,  0.5, 0.0,    0.3, 0.8, 0.2,  0.0, 0.0, 1.0,
            -0.5,  0.5, 0.0,    0.7, 0.4, 0.8,  0.0, 0.0, 1.0
            ]
        
        VertexBuffer = LNLEngine.VertexBuffer.Create(vertices, LNLEngine.sizeof(LNLEngine.c_float) * len(vertices))

        layout = LNLEngine.BufferLayout(
            [
                LNLEngine.BufferElement("a_pos", LNLEngine.ShaderDataType.Vec3),
                LNLEngine.BufferElement("a_col", LNLEngine.ShaderDataType.Vec3),
                LNLEngine.BufferElement("a_normal", LNLEngine.ShaderDataType.Vec3)
            ]
        )
        VertexBuffer.SetLayout(layout)
        self.m_vertexArray.AddVertexBuffer(VertexBuffer)


        indices = [0 ,1 ,2, 
                   2 ,3 ,0]
        
        IndexBuffer = LNLEngine.IndexBuffer.Create(indices , len(indices))

        self.m_vertexArray.SetIndexBuffer(IndexBuffer)


        self.camera : LNLEngine.PesrpectiveCamera = LNLEngine.PesrpectiveCamera(self.gameWindow.GetWidth(),self.gameWindow.GetHeight())

        cube = Cube(rotation= Quat.Quat(0.33608,0.16351,0,0.92476), scale=1.5)
        # self.Cube2 = Cube()



        self.TestCamera = OrthographicCamera(-5.0, 5.0, -1.0, 1.0)




        self.player  = Player(Vec2(0,0), 70,  "player1")
        self.player.bound = True
        self.player.body.setCoefficientOfRestitution(0.1)

        # player2 = Player(Vec2(100,200), 7000, "player2")
        # player3 = Player(Vec2(300,200), 7, "player2")


        self.portal1 = Portal(Vec2(300, 500), Vec2(900, 100) , Vec4(255,150,20,255))
        self.portal2 = Portal(Vec2(0, 20), Vec2(200, 500) , Vec4(20,150,255,255))

        self.portal1.LinkPortal(self.portal2)

        # LNLEngine.Renderer.Enable(LNLEngine.RenderSettings.LL_SG_WIREFRAME_MODE_ENABLED)



        self.SceneManager = LNLEngine.Game.Get().GetSceneManager()
        
        mainScene : LNLEngine.Scene = LNLEngine.Scene("mainScene")

        # mainScene.AddObject(self.portal1)
        # mainScene.AddObject(self.portal2)

        # groundBody : LNLEngine.RigidBody2D = LNLEngine.RigidBody2D()
        # groundBody.setTransform(Vec2( self.gameWindow.GetWidth()/2, self.gameWindow.GetHeight() - 200))
        
        # # groundBody.setTransform(Vec2(0,500) )
        # # groundBody.setMass(sys.float_info.max)
        # groundBody.setMass(0.0)
        
        # groundCollieder : LNLEngine.Collider2D = LNLEngine.Box2D()
        # groundCollieder.setSize(Vec2(self.gameWindow.GetWidth() * 10, 20) )
        # groundCollieder.setRigidBody(groundBody )
        
        # groundBody.setCollider(groundCollieder)

        # # LNLEngine.Game.Get().GetPhysicsSystem2D().addRigidbody(groundBody, True)
        # LNLEngine.Game.Get().GetPhysicsSystem2D().addRigidbody(groundBody, False)

        mainScene.AddObject(self.player)
        
        # mainScene.AddObject(player2)
        # mainScene.AddObject(player3)

        # mainScene.AddObject(cube)

        # mainScene.AddObject(self.TestSquare)

        self.SceneManager.add_scene(mainScene)
        self.SceneManager.add_scene(MainMenuScene())
        self.SceneManager.set_active_scene("MainMenu")

        self.ScreenShader = LNLEngine.ScreenShader()


        tex = LNLEngine.Texture("Game/Assets/Sprites/Larx_Stand.png")
        # tex = LNLEngine.Texture("Game/Assets/Sprites/Bullet_Explode.jpeg")
        # self.spritePos = Vec3(50,290, 0)
        # self.speed = 1000
        # self.TestSprite = LNLEngine.Sprite(tex, self.spritePos.toVec2() , 200, 300)

        self.keys = {}



        bullet_tex  = LNLEngine.Texture("Game/Assets/Sprites/Bullet_Shot.jpeg", True)
        topLeft_uv = Vec2( 
                            ( (1 / 6) * 1 ), 
                            0 * 1
                        )
        bottomRight_uv = Vec2( 
                            ( (1 / 6) * 2 ), 
                            1 * 1
                        )
        self.bulletSprite = LNLEngine.Sprite(bullet_tex, self.player.body.getPosition().toVec2() , (bullet_tex.tex_width / 6) / 3, bullet_tex.tex_height / 3, (topLeft_uv, bottomRight_uv))

        self.bullet_TTL = 1
        self.bullet_TTL_MAX = 0.3

        self.bulletPos = Vec2(0,0)

        self.bulletSpeed = 2500


        self.testPhsicsComponent  = TestPhysicsObject(Vec2(-20, 700))







        self.tiles : list [GameObject] = []

        tex0 = Texture("Game/Assets/Sprites/environ/grassfull.png", True)
        tex1 = Texture("Game/Assets/Sprites/environ/rocksfull.png", True)
        chunk = TileChunk(Vec2(-10,10),Vec2(20, 10), tex0, tex1)

        self.tiles.append(chunk)
        # for i in range(20):
        #     tex = Texture("Game/Assets/Sprites/environ/grassfull.png", True)
        #     t = Tile(tex, Vec2(i, 10))
        #     self.tiles.append(t)
        # for i in range(10, 20):
        #     tex = Texture("Game/Assets/Sprites/environ/grassfull.png", True)
        #     t = Tile(tex, Vec2(i, 9))
        #     self.tiles.append(t)
        # for i in range(12, 20):
        #     tex = Texture("Game/Assets/Sprites/environ/grassfull.png", True)
        #     t = Tile(tex, Vec2(i, 8))
        #     self.tiles.append(t)

        # for i in range(20):
        #     for j in range(5):
        #         tex = Texture("Game/Assets/Sprites/environ/rocksfull.png", True)
        #         t = Tile(tex, Vec2(i, 11 + j))
        #         self.tiles.append(t)

        for tile in self.tiles:
            mainScene.AddObject(tile)
        # self.testPhsicsComponent2 = TestPhysicsObject(Vec2(-20, -400),0)




        # walktex = LNLEngine.Texture("Game/Assets/Sprites/Larx_whip.jpeg")
        # r = 12
        # c = 1
        # self.guyWalk = LNLEngine.SpriteAnimation.LoadFromSpritesheet(walktex,
        #                                                              r, c,
        #                                                              walktex.tex_width/r/0.5, walktex.tex_height / c /0.5, 
        #                                                              framerate=24,
        #                                                              repeat= True)
        # self.guyWalk.Play()

    def OnEvent(self, event: LNLEngine.Event):
        if event.GetName() == "KeyDown":
            self.keys[event.keycode] = 1


            if event.keycode == LNLEngine.KEY_MAP['f'] and self.bullet_TTL <= 0:
                self.bullet_TTL = self.bullet_TTL_MAX
                self.bulletPos = self.player.body.getPosition()

        if event.GetName() == "KeyUp":
            self.keys[event.keycode] = 0




    def OnUpdate(self, deltatime : float):

        if self.keys.get(LNLEngine.KEY_MAP['D']):
            self.TestCamera.SetPosition(self.TestCamera.GetPosition() + Vec3(5,0,0) * deltatime)
        if self.keys.get(LNLEngine.KEY_MAP['A']):
            self.TestCamera.SetPosition(self.TestCamera.GetPosition() - Vec3(5,0,0) * deltatime)
        if self.keys.get(LNLEngine.KEY_MAP['W']):
            self.TestCamera.SetPosition(self.TestCamera.GetPosition() + Vec3(0,5,0) * deltatime)
        if self.keys.get(LNLEngine.KEY_MAP['S']):
            self.TestCamera.SetPosition(self.TestCamera.GetPosition() - Vec3(0,5,0) * deltatime)
        if self.keys.get(LNLEngine.KEY_MAP['E']):
            self.TestCamera.SetOrthoRotation(self.TestCamera.GetOrthoRotation() - math.radians(5))
        if self.keys.get(LNLEngine.KEY_MAP['Q']):
            self.TestCamera.SetOrthoRotation(self.TestCamera.GetOrthoRotation() + math.radians(5))
        # if self.keys.get(LNLEngine.KEY_MAP['Z']):
        #     self.TestCamera.Set
        # if self.keys.get(LNLEngine.KEY_MAP['X']):
        #     self.TestCamera.SetOrthoRotation(self.TestCamera.GetOrthoRotation() + math.radians(5))

        if self.bullet_TTL > 0:
            self.bulletPos += Vec2(self.player.direction * self.bulletSpeed, 0) * deltatime
            self.bulletSprite.SetPos(self.bulletPos.toVec2())
            self.bullet_TTL -= deltatime

        # self.TestSprite.SetPos(self.spritePos.toVec2())

        # LNL_LogTrace("phys pos : ", self.testPhsicsComponent.body.getPosition())

        # LNLEngine.Renderer.SetClearColour(LNLEngine.Vec4(0.1,0.6,0.9,1.0))
        LNLEngine.Renderer.Clear()
        
        
        # LNLEngine.Renderer.DrawTriangle([LNLEngine.Vector.Vec2(10,10),LNLEngine.Vector.Vec2(100,50) , LNLEngine.Vector.Vec2(200,400)], LNLEngine.Vector.Vec4(100, 200, 255, 255))
        # LNLEngine.Renderer.DrawTriangle([LNLEngine.Vector.Vec2(200,10),LNLEngine.Vector.Vec2(100,800) , LNLEngine.Vector.Vec2(700,4)], LNLEngine.Vector.Vec4(100, 200, 80, 255))

        # self.player.Update()

        # print(LNLEngine.LLEngineTime.Time())
        
        # self.TestSquare.Update()
        # self.TestSquare.Draw()
        self.testPhsicsComponent.Update(deltatime)
        # self.testPhsicsComponent2.Update(deltatime)
        
        # self.guyWalk.Update(deltatime)

        # self.TestCamera.SetPosition(self.TestCamera.GetPosition() + Vec3(0.001,0.001,0))
        # self.TestCamera.SetOrthoRotation(self.TestCamera.GetOrthoRotation() + 0.01)


        # self.Cube.Update(deltatime)

        self.SceneManager.update(deltatime)


        LNLEngine.Renderer.BeginScene(self.TestCamera)
        self.ScreenShader.Draw()
        LNLEngine.Renderer.Submit(self.shader ,self.m_vertexArray)
    
        self.SceneManager.Draw()

        # self.testPhsicsComponent.Draw()
        # self.testPhsicsComponent2.Draw()
        # self.TestSprite.Draw()

        if self.bullet_TTL > 0:
            self.bulletSprite.Draw()

        # self.guyWalk.Draw()
        # self.portal1.Draw()
        # self.portal2.Draw()

        LNLEngine.Renderer.EndScene()


class PortalsDemo(LNLEngine.Game):
    def __init__(self):
        super().__init__()
        
        props = LNLEngine.WindowProperties("PortalsDemo", 900, 600)
        self._window = LNLEngine.Window.CreateWindow(props)
        

        self.Load("Game/Data/LevelData/DemoLevelData.json")

        # LNLEngine.Renderer.PushLayer(MenuLayer())
        LNLEngine.Renderer.PushLayer(TestLayer())


    
    def _OnSceneLoad(self, sceneData: dict, scene: LNLEngine.Scene):
        if sceneData["type"] == "menu":
            LNLEngine.LNL_LogInfo("Loading scene data , found Menu")
            for element in sceneData["Elements"]:
                ...

        elif sceneData["type"] == "game":
            LNLEngine.LNL_LogInfo("Loading scene data , found game")
            




            s_levels = sceneData.get("levels" , [])

            startupLevelName : str = sceneData.get("startupLevel", None)
            # startupLevelID : int = -1
            exists = False
            # firstLevelID : int = 0
            firstLevelName = ""

            for i in range(len(s_levels)):

                gameLevelData = s_levels[i]
                l = LNLEngine.Level(gameLevelData.get("name", scene.name + "_Level_" + str(i)))

                for s_envElement in gameLevelData.get("environment", []):
                    c_type = "environment"

                    if s_envElement["type"] == "movingSquare":
                        ms = MovingSquare(
                                            Vec2(
                                                s_envElement["world_position"]["x"], 
                                                s_envElement["world_position"]["y"]
                                            ),
                                            
                                            s_envElement["width"],
                                            s_envElement["height"],
                                            Vec4(*s_envElement["colour"].values())
                                        )
                        
                        l.AddLevelComponent(c_type, ms)
                
                scene.GetLevelManager().addLevel(l)


                if gameLevelData["name"] == startupLevelName: 
                    # startupLevelID = i
                    exists = True

                if firstLevelName == "":
                    firstLevelName = gameLevelData["name"]
                
                if startupLevelName is None:
                    startupLevelName = gameLevelData["name"]
                    # startupLevelID = i
                    exists = True
            
            if not exists:
                LNLEngine.LNL_LogWarning(f"Level name :  {startupLevelName} , is not a level in leveldata, selecting :  {firstLevelName}")
                startupLevelName = firstLevelName
                # startupLevelID = firstLevelID

            scene.GetLevelManager().setActiveLevel(startupLevelName)



                
            # for i in range( len( sceneData.get("players", []) ) ):
                
            #     s_player = sceneData["players"][i]
            #     p = Player(s_player.get("name", scene.name + "_player_" + str(i) ))

            #     p._World_Position = Vec3(*s_player["world_position"].values())
            #     p.width = s_player["width"]
            #     p.height = s_player["height"]
            #     p.Colour = Vec4(*s_player["colour"].values())
                
            #     for s_p_attribute in s_player["attributes"]:
            #         if s_p_attribute == "AffectedByGravityAttribute":
            #             p.SetAttribure(AffectedByGravityAttribute)
            #         elif s_p_attribute == "CanTravelThroughPortals":
            #             p.SetAttribure(CanTravelThroughPortals)
                
            #     scene.AddObject(p)

    def _OnUpdate(self, deltatime : float):
        return super()._OnUpdate(deltatime)
    


if __name__ == "__main__":
    gameInst = LNLEngine.Game.CreateGame(PortalsDemo)
    gameInst.Run()
    gameInst.Save()