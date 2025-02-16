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