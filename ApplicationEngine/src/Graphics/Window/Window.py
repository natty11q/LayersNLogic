from src.Core.Utility.CoreUtility import *


class Window:
    def __init__(self, width, height):
        self.__width  = width
        self.__height = height

        self.__FrameBufferSizeCallBack : function = nullFunc
            # the frame buffer size callback is set by the user from the game code and takes in
            # the argument of the pointer to the current window object.
            # It is called every time the window is resized.
            
        self.__KeyCallback : function = nullFunc
        
        
        
        self.__NativeWindow = None


    def Update(self):
        pass
    
    
    def __resetFrameBuffer(self):
        """ """
       
        self.__FrameBufferSizeCallBack(self)
    
    def SetWidth(self, newW):
        self.__width = newW
        
    def SetHeight(self, newH):
        self.__height = newH
    
