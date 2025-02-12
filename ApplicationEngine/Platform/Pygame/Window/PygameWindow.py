from ApplicationEngine.include.Window.Window import Window , WindowProperties
import pygame
class GraphicsContext: ...

class PygameWindow(Window):
    pygameIsInit : bool = False
    
    class WindowData:
        Title   : str = ""
        Width   : float = 0
        Height  : float = 0
        AspectRatio : bool = False
        VSync   : bool = False
        Keys    : dict [int , bool] = {}
    
    def __init__(self, props : WindowProperties):
        self._m_windowProperties : WindowProperties = props
        self._m_window  : pygame.surface.Surface = pygame.display.set_mode((self._m_windowProperties.Width(),self._m_windowProperties.Height()))
        self._m_context : GraphicsContext = GraphicsContext()
    
    def CreateWindow(self, Props : WindowProperties):
        return PygameWindow(Props)