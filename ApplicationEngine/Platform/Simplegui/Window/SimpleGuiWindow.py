from include.Window.Window import *


try:
    import simplegui # type: ignore
except ImportError :
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui # type: ignore
    
    

class SimpleGuiWindow(Window): ...