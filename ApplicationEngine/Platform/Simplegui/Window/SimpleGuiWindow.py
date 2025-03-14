from ApplicationEngine.include.Window.Window import WindowProperties , Window

from ApplicationEngine.src.Graphics.Renderer.RendererAPI import RendererAPI
from ApplicationEngine.Platform.Simplegui.Renderer.SimpleGuiRendererAPI import SimpleGUiRendererAPI

from ApplicationEngine.src.Graphics.Renderer.Renderer import Renderer

from ApplicationEngine.src.Event.EventHandler import * 


try:
    import simplegui # type: ignore
except ImportError :
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui # type: ignore
    
    

class SimpleGUIWindow(Window):
    def __init__(self, props : WindowProperties):
        super().__init__(props)
        
        self.frame : simplegui.Frame = simplegui.create_frame(self._Data.Title, self._Data.Width, self._Data.Height)
        self.frame.set_draw_handler(self.SimpleGuiUpdate)

        self.frame.set_keydown_handler(self.KeyDownHandler)
        self.frame.set_keyup_handler(self.KeyUpHandler)
        self.frame.set_mouseclick_handler(self.MouseReleasedHandler)
        self.frame.set_mousedrag_handler(self.MouseDraggedHandler)
        # self.frame.set_mousemove_handler(self.MouseMovedHandler) # type: ignore

        self.firstclick = False
        self.mousePos : tuple[int, int] = (-1,-1)
        
    def Run(self):
        self.frame.start()
    
    def _OnUpdate(self) -> None: ...

    def GetWidth(self) -> float:    return self._Data.Width
    def GetHeight(self) -> float:   return self._Data.Height
    def GetAspectRatio(self) -> float:  return self._Data.AspectRatio
    
    def OnInput(self): ...


    def SetVsync(self, state :  bool) -> None:
        self._Data.VSync = state

    def ISVsync(self) -> bool:
        return self._Data.VSync
    
    def GetNativeWindow(self) -> object:
        return self.frame

    def SimpleGuiUpdate(self, canvas: simplegui.Canvas):
        Renderer.Draw(canvas)



    def InputHandler(self, etype: str, values: list)-> None:
        if etype == "keyDown":
            e = KeyDownEvent()
            e.keycode = values[0]
            sendEvent(e)

        elif etype == "keyUp":
            e = KeyUpEvent()
            e.keycode = values[0]
            sendEvent(e)

        elif etype == "mouseReleased":
            e = MouseButtonUpEvent()
            e.button = 1
            sendEvent(e)

        elif etype == "mouseDragged":
            if not self.firstclick:
                e = MouseButtonDownEvent()
                e.button = 1
                sendEvent(e)
                self.firstclick = True
        
        elif etype == "mouseMoved":
            self.mousePos = values[0]
            e = MouseMovedEvent()
            e.x = values[0][0]
            e.y = values[0][1]
            sendEvent(e)



    def KeyDownHandler(self, key : int):
        self.InputHandler("keyDown", [key])
    def KeyUpHandler(self, key : int):
        self.InputHandler("keyUp", [key])
    def MouseReleasedHandler(self, position : tuple[int, int]):
        self.InputHandler("mouseReleased", [position])
    def MouseDraggedHandler(self, position : tuple[int, int]):
        self.InputHandler("mouseDragged", [position])
    def MouseMovedHandler(self, position : tuple[int, int]):
        self.InputHandler("mouseMoved", [position])