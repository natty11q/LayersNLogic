import ApplicationEngine.AppEngine as LNLEngine 
from ApplicationEngine.include.Maths.Maths import *

gameWindow = LNLEngine.Game.Get().GetWindow()
windowWidth = gameWindow.GetWidth() 
windowHeight = gameWindow.GetHeight()
windowWidthGrace = windowWidth * 1.1 - (windowWidth * 0.05)  
windowHeightGrace = windowHeight * 1.1 - (windowHeight * 0.05)

class WorldObject(LNLEngine.GameObject):
    def __init__(self,width : float, height : float):
        super().__init__() 
        self.width = width 
        self.height = height 
        self.onScreen = True 

        self.boundingBox = {"tl" : self._World_Position.xy,"tr" : Vec2(self._World_Position.x + width,self._World_Position.y),"bl": Vec2(self._World_Position.x,self._World_Position.y + height), "br": Vec2(self._World_Position.x + width,self._World_Position.y + height)}
         
    def _OnUpdate(self, deltatime: float):
        if  (self._World_Position.x >= 0 and \
            self._World_Position.x <= windowWidthGrace and \
            self._World_Position.y >= 0 and \
            self._World_Position.y <= windowHeightGrace):
            self.onScreen = True
        else:
            self.onScreen = False

        
        

