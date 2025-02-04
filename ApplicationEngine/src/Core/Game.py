# imports
from include.Common import *
from include.Maths.Maths import *
from src.Graphics.Renderer import *
from ApplicationEngine.src.Object.Object import *
import src.Core.Utility.Temporal as Temporal




import _tkinter
import PySimpleGUI as simplegui
# try:
#     import simplegui # noqa
# except ImportError :
#     import SimpleGUICS2Pygame.simpleguics2pygame as simplegui



class TestCube(GameObject):
    def __init__(self):
        self.Vertices = []
        self.indices = []
    
    def Draw(self):
        pass
    
    def Update(self):
        return super().Update()



WINDOW_SIZE = (900, 600)
PLAYER_SIZE = (20, 20)
player_x = 50
player_y = 300


class Game:
    def __init__(self):
        self.__IsRunning = True
        
        
        layout = [[]] # clear layout
        # layout = [[simplegui.Frame("Game", [[simplegui.Graph((900, 600), (0, 0), (900, 600), background_color='white', key='-GRAPH-')]], key='-FRAME-')]] # clear layout
        layout = [[simplegui.Graph(WINDOW_SIZE, (WINDOW_SIZE[0], 0), (0, WINDOW_SIZE[1]), background_color='white', key='-GRAPH-')]] # clear layout
        
        
        # layout = [[simplegui.Frame("Game", [[simplegui.Graph(WINDOW_SIZE, (WINDOW_SIZE[0], 0), (0, WINDOW_SIZE[1]), background_color='white', key='-GRAPH-')]], key='-FRAME-')]]
        self.__window : simplegui.Window = simplegui.Window("Base Window", layout, finalize=True, return_keyboard_events=True)
        self.__window.set_size(WINDOW_SIZE)
        
        
        self.__PhysicsThread : threading.Thread  = threading.Thread(target = self.__PhysicsMainloop, args=(), daemon=True)
        self.__InputThread : threading.Thread = threading.Thread(target=self.input_listener, args=(self.__window,), daemon=True)
        
        
        self.__col = "blue"
        # Create a frame called "A canvas " with dimensions 400 x200
        # self.frame = simplegui.create_frame("A canvas ", 400, 200)

    def Run(self):
        self.__StartPhysicsThread()
        
        
        self.__MainLoop()
    
    def Save():
        pass
    
    def Quit(self):
        # handle everything that needs to be done before closing
        self.Save()
        self.__IsRunning = False











# protected :
    def _OnUpdate(self) -> None:
        """game based render updates should be handled here"""
        pass
    
    def _OnPhysicsUpdate(self) -> None:
        print("Physics update called")

    def _OnEvent(self , event, values) -> None:
        pass
    
    def __StartPhysicsThread(self):
        self.__PhysicsThread.start()


    def input_listener(self, window : simplegui.Window):
        while True:
            # print("listening")
            
            event, values = window.read(timeout= 8)
            self.__HandleEvents(event , values)
            window.write_event_value("-INPUT-", event)  # Send event to main loop






# private :
    def __PhysicsMainloop(self):
        while True:
            self._OnPhysicsUpdate()
            Temporal.time.sleep(1 / Temporal.Time.TickRate())

    def __HandleEvents(self, event, values = {}):
        # print("called")

        if event == simplegui.WIN_CLOSED or event == 'Exit':	# if user closes window or clicks cancel
            self.__IsRunning = False
            
        if event == 'a':
            self.__col = "green"

        self._OnEvent(event , values)
        
        

    def __MainLoop(self):
        # x = 2400
        
        
        Temporal.Time.CapFramerate()
        
        Temporal.Time.SetTargetFramerate(120)
        
        
        
        while self.__IsRunning:
            Temporal.Time.Update()
        
            event, values = self.__window.Read(timeout=8)
            self.__HandleEvents(event , values)
            if (not self.__IsRunning): break
            
            # if x == 0:
            #     self.__IsRunning = False
            # x -= 1
            
            # self.frame.set_canvas_background(f'rgb(math.sin(Temporal.Time.Time()) * 30,20,30)')
            # self.__window.BackgroundColor = f'rgb(0,0,0)'
            # print(f"dt  : {Temporal.Time.DeltaTime()}")
            # print(f"tet : {Temporal.Time.Time()}\n")
            # self.__window.TKroot.configure(bg=f'rgb(math.sin(Temporal.Time.Time()) * 30,20,30)')
            # self.__window['-BACKGROUND-'].update(background_color= f'rgb({int(math.sin(Temporal.Time.Time())) * 30},20,30)')

            

            self._OnUpdate()
            self.__window['-GRAPH-'].erase()
            self.__window['-GRAPH-'].TKCanvas.create_rectangle(player_x, player_y, player_x + PLAYER_SIZE[0], player_y + PLAYER_SIZE[1], fill=self.__col)
            # self.__window['-GRAPH-'].draw_rectangle((WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2), ((WINDOW_SIZE[0] / 2) + PLAYER_SIZE[0], (WINDOW_SIZE[1] / 2) + PLAYER_SIZE[1]) , fill_color='blue')
            self.__window.refresh()

            # self.frame.start()
        print(f"fps : {Temporal.Time.FPS()}\n")
        # self.frame.stop()
        self.__window.close()



# simplegui.Graph.DrawPolygon

