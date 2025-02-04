class Window:
    def __init__(self):
        self.__window = None

class SGWindow(Window):
    def __init__(self , layout):
        super().__init__()
        
        self.__windowLayout = [].append(layout)
        self.__window = None
    
    def GetWidth(self) -> float:
        pass
    
    def GetHeight(self) -> float:
        pass
    
    def GetAspectRatio(self) -> float:
        pass
    
    def SetVsync(self, vsync) -> None:
        pass
    
    def IsVsync(self, vsync) -> None:
        pass
    
    def GetNative(self) -> Window:
        return self.__window
    
    
    
    
    
    def _OnUpdate(self) -> None:
        pass
    
    
    def __sub_init(xself) -> None: ... 