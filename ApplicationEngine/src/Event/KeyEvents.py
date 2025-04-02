from ApplicationEngine.src.Event.Event import * 

class KeyDownEvent(Event):
    def __init__(self):
        super().__init__("KeyDown")
        self.type = LNL_EventType.KeyDown
        self.keycode = -1 # The ASCII of the key that was Pressed Down


class KeyUpEvent(Event):
    def __init__(self):
        super().__init__("KeyUp")
        self.type = LNL_EventType.KeyUp
        self.keycode = -1 # The ASCII of the key that was Released

