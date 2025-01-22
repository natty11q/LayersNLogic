# imports
from include.Common import *
import src.Core.Utility.Temporal as Temporal


class Game:
    def __init__(self):
        self.IsRunning = True
        

    def Run(self):
        self.__Update()
# protected :
    def _OnUpdate(self) -> None:
        pass

    def _OnEvent(self , event) -> None:
        pass

# private :
    def __Update(self):
        x = 2400
        while self.IsRunning:
            Temporal.Time.Update()
            # print(f"dt  : {Temporal.Time.DeltaTime()}")
            # print(f"tet : {Temporal.Time.Time()}\n")
            if x == 0:
                self.IsRunning = False
            x -= 1
            
            self._OnUpdate()
        print(f"fps : {Temporal.Time.FPS()}\n")

