from include.Common import *
from include.Window.Window import *
from src.Graphics.Renderer.RendererAPI import *

class Renderer:
    
    __Objects = []
    
    @staticmethod
    def Submit(renderWindow : Window):
        pass
    
    @staticmethod
    def BeginScene(renderWindow : Window, camera):
        pass
   
    @staticmethod
    def EndScene():
        pass
    
    @staticmethod
    def SubmitImidiate():
        pass

    @staticmethod
    def DrawIndexed():
        pass
    
    @staticmethod
    def GetAPI():
        return RendererAPI.GetAPI()