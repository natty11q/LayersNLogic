## ============================== setup ===================================
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from ApplicationEngine.include.Maths.Maths import *
import ApplicationEngine.AppEngine as LNLEngine
## ============================= App Code =================================


import math


from Game.src.MainMenu.MainMenuScene import *
from Game.src.MainGame.MainScene import *
from Game.src.MainGame.IntroScene import *

class TestLayer(LNLEngine.Layer):
    def __init__(self, name="TestLayer"):
        super().__init__(name)
        self.SceneManager = LNLEngine.Game.Get().GetSceneManager()

        self.SceneManager.AddScene(MainMenuScene())
        self.SceneManager.AddScene(IntroScene())
        self.SceneManager.AddScene(MainScene())


        self.SceneManager.SetActiveScene("MainMenu")



    def OnEvent(self, event: LNLEngine.Event):...

    def OnUpdate(self, deltatime : float):
        self.SceneManager.Update(deltatime)

class PortalsDemo(LNLEngine.Game):
    def __init__(self):
        super().__init__()
        
        LNLEngine.Game.CreateGameWindow("PortalsDemo", 900, 600)
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

            startupLevelName : str = sceneData.get("startupLevel", "")
            # startupLevelID : int = -1
            exists = False
            # firstLevelID : int = 0
            firstLevelName = ""

            for i in range(len(s_levels)):

                gameLevelData = s_levels[i]
                l = LNLEngine.Level(gameLevelData.get("name", scene.name + "_Level_" + str(i)))

                for s_envElement in gameLevelData.get("environment", []):
                    c_type = "environment"

                
                scene.GetLevelManager().addLevel(l)


                if gameLevelData["name"] == startupLevelName: 
                    # startupLevelID = i
                    exists = True

                if firstLevelName == "":
                    firstLevelName = gameLevelData["name"]
                
                if startupLevelName == "":
                    startupLevelName = gameLevelData["name"]
                    # startupLevelID = i
                    exists = True
            
            if not exists:
                LNLEngine.LNL_LogWarning(f"Level name :  {startupLevelName} , is not a level in leveldata, selecting :  {firstLevelName}")
                startupLevelName = firstLevelName
                # startupLevelID = firstLevelID

            scene.GetLevelManager().SetActiveLevel(startupLevelName)



                
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