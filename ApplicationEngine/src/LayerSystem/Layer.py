from ApplicationEngine.src.Event.EventHandler import *



class Layer:
    def __init__(self , name = "Layer"):
        self.__Name : str = name
        self.__Active : bool = True

        AddEventListener(self.OnEvent)


#protected:

#public:
    def OnUpdate(self,  deltatime : float):
        pass
    
    def OnAttach(self):
        pass
    
    def OnDetach(self):
        pass
    
    def OnGuiRender(self):
        pass

    def OnEvent(self , event : Event):
        pass

    def Update(self,  deltatime : float):
        pass
    
    def GetName(self) -> str:
        return self.__Name
    
    def Activate(self) -> None:
        self.__Active = True
    
    def Deactivate(self) -> None:
        self.__Active = False