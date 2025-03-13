class Event:
    def __init__(self, name : str):
        self._m_name : str = name
        self._m_handled : bool = False


    def GetName(self):
        return self._m_name
    
    def Handled(self):
        return self._m_handled


class EventDispatcher:
   

    def __init__(self):
        self.__m_EventListeners : list[function] = []
        self.__m_NextListenerID = 0
    
    def AddEventListener(self, listener : function) -> int:
        self.__m_EventListeners.append(listener)

        handle = self.__m_NextListenerID
        self.__m_NextListenerID += 1

        return handle


    def RemoveEventListener(self, handle : int):
        if handle < len(self.__m_EventListeners):
            self.__m_EventListeners.pop(handle)
            self.__m_NextListenerID -= 1
    
    def sendEvent(self, event : Event):
        for listener in self.__m_EventListeners:
            if not event.Handled():
                listener(event)