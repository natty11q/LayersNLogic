from ApplicationEngine.include.Window.Window import WindowProperties , Window

from ApplicationEngine.src.Graphics.Renderer.RendererAPI import RendererAPI
from ApplicationEngine.Platform.Simplegui.Renderer.SimpleGuiRendererAPI import SimpleGUiRendererAPI

from ApplicationEngine.src.Graphics.Renderer.Renderer import Renderer



try:
    import simplegui # type: ignore
except ImportError :
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui # type: ignore
    
    

class SimpleGUIWindow(Window):
    def __init__(self, props : WindowProperties):
        super().__init__(props)
        
        self.frame : simplegui.Frame = simplegui.create_frame(self._Data.Title, self._Data.Width, self._Data.Height)
        self.frame.set_draw_handler(Renderer.Draw)
        
    def Run(self):
        self.frame.start()
    
    def _OnUpdate(self) -> None: ...

    def GetWidth(self) -> float:    return self._Data.Width
    def GetHeight(self) -> float:   return self._Data.Height
    def GetAspectRatio(self) -> float:  return self._Data.AspectRatio
    
    
    def SetVsync(self, state :  bool) -> None:
        self._Data.VSync = state

    def ISVsync(self) -> bool:
        return self._Data.VSync
    
    def GetNativeWindow(self) -> object:
        return self.frame