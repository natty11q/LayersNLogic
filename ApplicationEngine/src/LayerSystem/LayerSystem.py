from ApplicationEngine.src.LayerSystem.Layer import *


class LayerStack:
    def __init__(self):
        self.__Layers : list [Layer] = []
        self.__LayerTop = 0   # the position where regular layes end and overlays start
        self.__Top = 0        # the top of the entire stack
    
    def PushLayer(self , Layer : Layer):
        self.__Layers.insert(self.__LayerTop, Layer)
        self.__LayerTop += 1
        self.__Top += 1
    
    
    # TODO : DECIDE IF I WANT TO RETURN THE LAYERS AFTER THEY ARE POPPED
    def PopLayer(self):
        
        if self.__LayerTop >= 0:
            l = self.__Layers.pop(self.__LayerTop)
            del l  # explicit memory free
            
            self.__LayerTop -= 1
            self.__Top -= 1
    
    def PushOverlay(self , Layer : Layer):
        self.__Layers.append(Layer)
        self.__Top = 0

    def PopOverlay(self):
        if self.__Top > self.__LayerTop:
            self.__Layers.pop(-1) # pop last element
            self.__Top -= 1

    def __iter__(self):
        for Layer in self.__Layers:
            yield Layer