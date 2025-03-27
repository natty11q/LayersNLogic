from ApplicationEngine.src.Event.Event import * 

class WindowResizeEvent(Event):
    def __init__(self):
        super().__init__("WindowResize")
        self.width = 0
        self.height = 0

class WindowMinimisedEvent(Event):
    def __init__(self):
        super().__init__("WindowMinimised")

class WindowMaximisedEvent(Event):
    def __init__(self):
        super().__init__("WindowMaximised")

class WindowFocusLostEvent(Event):
    def __init__(self):
        super().__init__("WindowFocousLostEvent")

class WindowFocusGainedEvent(Event):
    def __init__(self):
        super().__init__("WindowFocousGainedEvent")

class WindowClosedEvent(Event):
    def __init__(self):
        super().__init__("WindowClose")

class WindowRestoredEvent(Event):
    def __init__(self):
        super().__init__("WindowRestored")

class WindowRestoredDownEvent(Event):
    def __init__(self):
        super().__init__("WindowRestoredDown")

