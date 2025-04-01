from __future__ import annotations

# imports
from ApplicationEngine.include.Common import *
from ApplicationEngine.include.Maths.Maths import *
from ApplicationEngine.include.Window.Window import *
from ApplicationEngine.src.Object.Object import *
from ApplicationEngine.src.Graphics.Graphics import *
import ApplicationEngine.src.Core.Utility.Temporal as Temporal


from ApplicationEngine.src.Core.Keys import *

from ApplicationEngine.src.Core.SceneManager import *
from ApplicationEngine.src.Event.EventHandler import *


from ApplicationEngine.src.Core.Mouse import *
from ApplicationEngine.src.Core.Keys import *


# import pygame

from ApplicationEngine.src.Physics.LNL_Physics import *

# import _tkinter
# import PySimpleGUI as simplegui
# try:
#     import simplegui # noqa
# except ImportError :
#     import SimpleGUICS2Pygame.simpleguics2pygame as simplegui



# class TestCube(GameObject):
#     def __init__(self):
#         self.Vertices = []
#         self.indices = []

#         self.position : Vector.Vec3 = Vector.Vec3()

#     def Draw(self, window : Window):
#         pass
    
#     def Update(self):
#         return super().Update()



# WINDOW_SIZE = (900, 600)
# PLAYER_SIZE = (20, 20)
# player_x = 50
# player_y = 300

class EngineSettings:
    SETTINGS_DATA = {

    }

    OUTPUT_DIR = ""
    AUTOSAVE_TIMEOUT_S  = 0
    AUTOSAVE_TIME_MAX_S = 60

    @staticmethod
    def Get() -> str | float | int:
        return 0 

    @staticmethod
    def Set() -> None:
        ...
    

    @staticmethod
    def Save() -> bool:
        success = True

        ...

        return success

    @staticmethod
    def Load() -> bool:
        success = True

        ...

        return success
    

    @staticmethod
    def Update(deltatime : float) -> None:
        EngineSettings.AUTOSAVE_TIMEOUT_S -= deltatime
        if EngineSettings.AUTOSAVE_TIMEOUT_S > 0:
            return

        LNL_LogEngineTrace("Auto Saving Engine Settings")

        EngineSettings.AUTOSAVE_TIMEOUT_S = EngineSettings.AUTOSAVE_TIME_MAX_S

class Game:
    
    __s_Instance : Game
    
    @staticmethod
    def CreateGame(gameclass) -> Game:
        if not issubclass(gameclass, Game):
            LNL_LogEngineFatal(f"GAME PROVIDIED : {gameclass} , IS NOT A SUBCLASS OF THE GAME CLASS")
            raise Exception()
        
        Game.__s_Instance = gameclass()
        return Game.__s_Instance
    
    
    
    def __init__(self):
        self.__IsRunning : bool = False
        self._window : Window




        Mouse.Init()
        Keys.Init()

        
        # layout = [[]] # clear layout
        # # layout = [[simplegui.Frame("Game", [[simplegui.Graph((900, 600), (0, 0), (900, 600), background_color='white', key='-GRAPH-')]], key='-FRAME-')]] # clear layout
        # layout = [[simplegui.Graph(WINDOW_SIZE, (WINDOW_SIZE[0], 0), (0, WINDOW_SIZE[1]), background_color='white', key='-GRAPH-')]] # clear layout
        
        
        # # layout = [[simplegui.Frame("Game", [[simplegui.Graph(WINDOW_SIZE, (WINDOW_SIZE[0], 0), (0, WINDOW_SIZE[1]), background_color='white', key='-GRAPH-')]], key='-FRAME-')]]
        # self.__window : simplegui.Window = simplegui.Window("Base Window", layout, finalize=True, return_keyboard_events=True)
        # self.__window.set_size(WINDOW_SIZE)
        
        
        self.__PhysicsThread : threading.Thread
        self.__InputThread : threading.Thread
        
        Temporal.LLEngineTime.CapFramerate()
        Temporal.LLEngineTime.SetTargetFramerate(120)
        
        self._m_SceneManager : SceneManager = SceneManager()

        # self._m_PhysicsSystem2D : PhysicsSystem2D = PhysicsSystem2D(Vec2(0.0, -9.81 * 30))
        self._m_PhysicsSystem2D : PhysicsSystem2D = PhysicsSystem2D(Vec2(0.0, 9.81 * 400))
        AddEventListener(self.__HandleEvents)

        self.saveDir : str = ""

        
        Game.__s_Instance = self
    
    
    @staticmethod
    def Get() -> Game:
        return Game.__s_Instance
    
    def GetWindow(self) -> Window:
        return self._window
    
    def GetSceneManager(self) -> SceneManager:
        return self._m_SceneManager
    
    def GetPhysicsSystem2D(self):
        return self._m_PhysicsSystem2D

    def Run(self):
        self.stop_event_Phys = threading.Event()
        self.stop_event_Inp  = threading.Event()

        self.__PhysicsThread : threading.Thread  = threading.Thread(target = self.__PhysicsMainloop, args=())
        self.__InputThread : threading.Thread = threading.Thread(target= self.input_listener, args=())
        
        self.__StartPhysicsThread()
        # self.__startInputThread()
        
        
        if Renderer.GetAPI() != RendererAPI.API.SimpleGui:
            self.__IsRunning = True
        
        self._window.Run()
        self.__MainLoop()
    
    
    def input_listener(self):
        LLEngineTime.CustomSleep()

    def Quit(self):
        # handle everything that needs to be done before closing
        self.Save()
        self.__IsRunning = False


    def Save(self):
        outpuData = {}

    def Load(self, jsonPath : str):
        path = os.path.abspath(jsonPath)
        jsonData : dict = {}
        if os.path.exists(path):
            with open(path, "r") as leveldata:
                jsonData = json.load(leveldata)
            
            self.saveDir = path
        else:
            LNL_LogEngineError(f"Failed to load Scene Data from path : {jsonPath}, path does not exist!")
            return

        startupSceneName : str = jsonData.get("StartupScene", None)
        exists = False
        firstSceneName = ""
        for scene in jsonData.get("Scenes", []):
            s = Scene(scene["name"])
            self._OnSceneLoad(scene, s)
            self._m_SceneManager.AddScene(s)
            
            if scene["name"] == startupSceneName: 
                exists = True

            if firstSceneName == "":
                firstSceneName = scene["name"]
            
            if startupSceneName is None:
                startupSceneName = scene["name"]
                exists = True
        
        if not exists:
            LNL_LogEngineWarning(f"Scene name :  {startupSceneName} , is not a scene in leveldata, selecting :  {firstSceneName}")
            startupSceneName = firstSceneName
        
        self._m_SceneManager.SetActiveScene(startupSceneName)

    def LoadEngineSettings(self, jsonPath : str):
        path = os.path.abspath(jsonPath)
        jsonData : dict = {}
        if os.path.exists(path):
            with open(path, "r") as leveldata:
                jsonData = json.load(leveldata)
            
            self.saveDir = path
        else:
            LNL_LogEngineError(f"Failed to load Settings Data from path : {jsonPath}, path does not exist!")
            return
        


        #TODO : impl


    def SaveSettings(self):
        ...

    def _OnSceneLoad(self, sceneData : dict, scene : Scene): ...




# protected :
    def _OnUpdate(self, deltatime : float) -> None:
        """game based render updates should be handled here"""
        pass
    
    def _OnPhysicsUpdate(self) -> None:
        #TODO: add seperate deltatime for physics system.
        Temporal.LLEngineTime.PhysicsUpdate()
        self._m_SceneManager.PhysicsUpdate(Temporal.LLEngineTime.TickDelta())
        
        self._m_PhysicsSystem2D.update(Temporal.LLEngineTime.TickDelta())
        # LNL_LogEngineTrace("Physics update called")

    def _OnEvent(self , event  : Event) -> None:...
        # LNL_LogEngineTrace(f"Event occured of type : {event.GetName()}")
    
    def __StartPhysicsThread(self):
        self.__PhysicsThread.start()

    def __startInputThread(self):
        self.__InputThread.start()

    # def input_listener(self, window : Window) -> None:
    #     while True:
    #         pass






# private :
    def __PhysicsMainloop(self):
        while not self.stop_event_Phys.is_set():
            self._OnPhysicsUpdate()
            Temporal.time.sleep(1 / Temporal.LLEngineTime.TickRate())

    def __HandleEvents(self, event : Event):
        

        # if event == simplegui.WIN_CLOSED or event == 'Exit':	# if user closes window or clicks cancel
        #     self.__IsRunning = False
            
        # if event == 'a':
        #     self.__col = "green"

        self._OnEvent(event)
        
        

    def __MainLoop(self):
        # x = 2400
        
        
        
        
        
        
        while self.__IsRunning:
            Temporal.LLEngineTime.Update()
        
            # event, values = self._window.Read(timeout=8)
            # self.__HandleEvents(event , values)
            # if (not self.__IsRunning): break
            
            # # if x == 0:
            # #     self.__IsRunning = False
            # # x -= 1
            
            # # self.frame.set_canvas_background(f'rgb(math.sin(Temporal.Time.Time()) * 30,20,30)')
            # # self.__window.BackgroundColor = f'rgb(0,0,0)'
            # # print(f"dt  : {Temporal.Time.DeltaTime()}")
            # # print(f"tet : {Temporal.Time.Time()}\n")
            # # self.__window.TKroot.configure(bg=f'rgb(math.sin(Temporal.Time.Time()) * 30,20,30)')
            # # self.__window['-BACKGROUND-'].update(background_color= f'rgb({int(math.sin(Temporal.Time.Time())) * 30},20,30)')

            
            # self.__HandleEvents()
            self._OnUpdate(Temporal.LLEngineTime.DeltaTime())
            # self._window['-GRAPH-'].erase()
            # self._window['-GRAPH-'].TKCanvas.create_rectangle(player_x, player_y, player_x + PLAYER_SIZE[0], player_y + PLAYER_SIZE[1], fill=self.__col)
            # # self.__window['-GRAPH-'].draw_rectangle((WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2), ((WINDOW_SIZE[0] / 2) + PLAYER_SIZE[0], (WINDOW_SIZE[1] / 2) + PLAYER_SIZE[1]) , fill_color='blue')
            # self._window.refresh()

            # self.frame.start()
        # print(f"fps : {Temporal.Time.FPS()}\n")
        # self.frame.stop()
        # self._window.close()

        self.stop_event_Phys.set()
        self.stop_event_Inp.set()

        self.__PhysicsThread.join()
        # self.__InputThread.join()

        LNL_LogEngineInfo("Application quit success")



# simplegui.Graph.DrawPolygon

