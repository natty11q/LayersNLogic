from ApplicationEngine.include.Maths.Maths import *
from ApplicationEngine.src.Graphics.Renderer.Renderer import Renderer
from ApplicationEngine.src.Event.EventHandler import *



class UIElement:
    def __init__(self, *eat_args, **eat_kwargs):
        self._Position : Vec2 = Vec2()
        self._RelativePosition : Vec2 = Vec2()
        self.Z_index : int = 0
