from __future__ import annotations
from dataclasses import dataclass

from ApplicationEngine.src.Graphics.Renderer.RendererAPI import *
from ApplicationEngine.src.Graphics.Renderer.RenderCommand import *


class WindowProperties:
    def __init__(self, title : str, width : int , height : int):
        self.__Title  : str  = title
        self.__Width  : int  = width
        self.__Height : int  = height
        self.__Aspectratio : float = (width / height)
    
    def AspectRatio(self):
        return self.__Aspectratio
    
    def Width(self):
        return self.__Width

    def Height(self):
        return self.__Height
    
    def Title(self):
        return self.__Title

    def __RecalculateAspectRatio(self):
        self.__Aspectratio = (self.__Width / self.__Height)

    def SetWidth(self, newW : int):
        self.__Width = newW
        self.__RecalculateAspectRatio()
    
    def SetHeight(self, newH : int):
        self.__Height = newH
        self.__RecalculateAspectRatio()
    
    def SetTitle(self, newT : str):
        self.__Title = newT

class Window(ABC):
    
    @dataclass
    class WindowData:
        Title   : str = ""
        Width   : float = 0
        Height  : float = 0
        AspectRatio : float = False
        VSync   : bool = False
        # Keys    : dict [int , bool] = {}
    
    def __init__(self, props : WindowProperties):
        self._Data : Window.WindowData = Window.WindowData()
        
        self._Data.Title   = props.Title()
        self._Data.Width   = props.Width()
        self._Data.Height  = props.Height()
        self._Data.AspectRatio = props.AspectRatio()
        self._Data.VSync
        
        self.__m_Window = None
    
    @abstractmethod
    def Run(self):
        pass
        
    
    @staticmethod
    def CreateWindow(Props : WindowProperties) -> Window:
        if RendererAPI.GetAPI() == RendererAPI.API.SimpleGui:
            from ApplicationEngine.Platform.Simplegui.Window.SimpleGuiWindow import SimpleGUIWindow
            RenderCommand.s_RendererAPI = SimpleGUiRendererAPI()
            return SimpleGUIWindow(Props)
        else:
            print("RENDERING API NOT SUPPORTED YET")
            raise Exception()
        
    
    
    def OnUpdate(self) -> None: ...

    def GetWidth(self) -> float: ...
    def GetHeight(self) -> float: ...
    def GetAspectRatio(self) -> float: ...
    
    
    def SetVsync(self) -> None: ...
    def ISVsync(self) -> bool: ...
    
    def GetNativeWindow(self) -> None: ...