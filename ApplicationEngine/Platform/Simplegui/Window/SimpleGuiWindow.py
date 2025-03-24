from ApplicationEngine.include.Window.Window import WindowProperties , Window

from ApplicationEngine.src.Graphics.Renderer.RendererAPI import RendererAPI
from ApplicationEngine.Platform.Simplegui.Renderer.SimpleGuiRendererAPI import SimpleGUiRendererAPI

from ApplicationEngine.src.Graphics.Renderer.Renderer import Renderer

from ApplicationEngine.src.Event.EventHandler import * 


from ApplicationEngine.src.Core.Keys import * 


try:
    import simplegui # type: ignore
except ImportError :
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui # type: ignore
    
    
import pygame


class SimpleGUIWindow(Window):
    def __init__(self, props : WindowProperties):
        super().__init__(props)
        
        self.frame : simplegui.Frame = simplegui.create_frame(self._Data.Title, self._Data.Width, self._Data.Height)
        pygame.event.post(pygame.event.Event(pygame.ACTIVEEVENT, gain=1, state=6))

        self.frame.set_draw_handler(self.SimpleGuiUpdate)

        self.frame.set_keydown_handler(self.KeyDownHandler)
        self.frame.set_keyup_handler(self.KeyUpHandler)
        # self.frame.set_mouseclick_handler(self.MouseReleasedHandler)
        # self.frame.set_mousedrag_handler(self.MouseDraggedHandler)


        # self.frame.set_mousemove_handler(self.MouseMovedHandler) # type: ignore

        pygame.mixer.init()

        self.windowEvents = pygame.event.get()
        # self.firstclick = False
        # self.mousePos : tuple[int, int] = (-1,-1)
        
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
        self.pygame_event_callback()
        Renderer.Draw(canvas)
        self.windowEvents = pygame.event.get()
        

    def pygame_event_callback(self):
        for event in self.windowEvents:
            if (event.type == pygame.QUIT):  # pylint: disable=no-member  # noqa
                    self.frame.stop()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("mbtn down", event.pos, event.button , event.touch)
                e = MouseButtonDownEvent()
                e.button = event.button
                e.x = event.pos[0] - self.frame._canvas_x_offset
                e.y = event.pos[1] - self.frame._canvas_y_offset
                print("modPos down", e.x, e.y)
                sendEvent(e)
                # self.firstclick = True

            elif event.type == pygame.MOUSEBUTTONUP:
                print("mbtn up", event.pos, event.button , event.touch)
                e = MouseButtonUpEvent()
                e.button = event.button
                e.x = event.pos[0] - self.frame._canvas_x_offset
                e.y = event.pos[1] - self.frame._canvas_y_offset
                sendEvent(e)
                print("modPos up", e.x, e.y)
            
            elif event.type == pygame.MOUSEMOTION:
                e = MouseMovedEvent()
                e.x = event.pos[0] - self.frame._canvas_x_offset
                e.y = event.pos[1] - self.frame._canvas_y_offset
                sendEvent(e)
                print("modPos moved", e.x, e.y)

            elif event.type == pygame.KEYDOWN:
                e = KeyDownEvent()
                # print("keydown" , event.key, event.mod, event.unicode, event.scancode, pygame.key.name(event.key))
            
                # TODO Find a better Solution to this
                e.keycode = KEY_MAP.get(pygame.key.name(event.key), KEY_MAP.get(pygame.key.name(event.key).upper(), event.key))
                sendEvent(e)
            
            elif event.type == pygame.KEYUP:
                e = KeyUpEvent()
                # print("keydown" , event.key, event.mod, event.unicode, event.scancode, pygame.key.name(event.key))
            
                # TODO Find a better Solution to this
                e.keycode = KEY_MAP.get(pygame.key.name(event.key), KEY_MAP.get(pygame.key.name(event.key).upper(), event.key))
                sendEvent(e)

    def InputHandler(self, etype: str, values: list)-> None:
        if etype == "keyDown":
            e = KeyDownEvent()
            e.keycode = values[0]
            sendEvent(e)

        elif etype == "keyUp":
            e = KeyUpEvent()
            e.keycode = values[0]
            sendEvent(e)



        # elif etype == "mouseReleased":
        #     e = MouseButtonUpEvent()
        #     e.button = 1
        #     sendEvent(e)

        # elif etype == "mouseDragged":
        #     if not self.firstclick:
        #         e = MouseButtonDownEvent()
        #         e.button = 1
        #         sendEvent(e)
        #         self.firstclick = True
        
        # elif etype == "mouseMoved":
        #     self.mousePos = values[0]
        #     e = MouseMovedEvent()
        #     e.x = values[0][0]
        #     e.y = values[0][1]
        #     sendEvent(e)



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