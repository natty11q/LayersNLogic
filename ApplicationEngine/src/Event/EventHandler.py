from ApplicationEngine.src.Event.Event import * 


class EventHandler:
    _s_Listener = EventDispatcher()


def AddEventListener(func : function):
    E