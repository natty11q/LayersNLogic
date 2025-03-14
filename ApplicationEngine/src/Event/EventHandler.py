from ApplicationEngine.src.Event.KeyEvents import * 
from ApplicationEngine.src.Event.MouseEvents import * 
from ApplicationEngine.src.Event.WindowEvents import * 

class EventHandler:
    _s_Distpatcher = EventDispatcher()


def AddEventListener(func : Callable[[Event], None]):
    EventHandler._s_Distpatcher.AddEventListener(func)

def RemoveEventListener(handle : int):
    EventHandler._s_Distpatcher.RemoveEventListener(handle)

def sendEvent(event : Event):
    EventHandler._s_Distpatcher.SendEvent(event)
