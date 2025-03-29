# import ApplicationEngine.AppEngine as LNLEngine 
# from ApplicationEngine.include.Maths.Vector import *
# import numpy 
# from Game.src.GameComponents.Environement.Portal import get_edges, quad_collision


# gameWindow = LNLEngine.Game.Get().GetWindow()
# windowWidth = gameWindow.GetWidth() 
# windowHeight = gameWindow.GetHeight()
# windowWidthGrace = windowWidth * 1.1 - (windowWidth * 0.05)  
# windowHeightGrace = windowHeight * 1.1 - (windowHeight * 0.05) 
# windowDimensions = []



# class WorldObject(LNLEngine.GameObject):
#     def __init__(self,width : float, height : float):
#         super().__init__() 
#         self.width = width 
#         self.height = height 
#         self.onScreen = True  
#         self.tl = [self._World_Position.x,self._World_Position.y]
#         self.tr = [self._World_Position.x + width,self._World_Position.y] 
#         self.bl = [self._World_Position.x,self._World_Position.y + height] 
#         self.br = [self.tl[0],self.tr[1]]

#         self.boundingBox = [self.tl,self.tr,self.bl,self.br]
         
#     def overCheck(self):
#         quad1 = self.boundingBox 
#         quad2 = [[-windowWidth*0.5,0],[windowWidthGrace,0],[-windowWidth*0.5,windowHeightGrace],[windowWidthGrace,windowHeightGrace]]
#         quad_collision(quad1,quad2)
    