from __future__ import annotations

from ApplicationEngine.src.Graphics.Renderer import *


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

class Window:
    
    
    def CreateWindow(self, Props : WindowProperties) ->  Window: ...
    
    
    def OnUpdate(self) -> None: ...

    def GetWidth(self) -> float: ...
    def GetHeight(self) -> float: ...
    def GetAspectRatio(self) -> float: ...
    
    
    def SetVsync(self) -> None: ...
    def ISVsync(self) -> bool: ...
    
    def GetNativeWindow(self) -> None: ...