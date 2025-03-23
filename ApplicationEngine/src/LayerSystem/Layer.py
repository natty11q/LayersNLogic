from ApplicationEngine.src.Event.EventHandler import *



class Layer:
    def __init__(self , name = "Layer"):
        self.__Name : str = name
        self.__Active : bool = True

        AddEventListener(self.OnEvent)

    def __init_subclass__(cls, **kwargs):
        """removes the need to super init every layer in the game code"""
        
        super().__init_subclass__(**kwargs)
        
        # Store the original __init__ of the subclass
        original_init = cls.__init__

        def new_init(self, *args, **kwargs):
            # Call Base class __init__ first
            super(cls, self).__init__()

            # Call the subclass's original __init__
            original_init(self, *args, **kwargs)

        cls.__init__ = new_init  # Override the subclass's __init__


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