from Game.src.GameComponents.Environement.EnvironmentObject import * 

class Box(EnvironmentObject2D):
    def __init__(self,dimensions : Vec2 = Vec2(1,1)):
        super().__init__() 
        self.dimensions = dimensions * WorldGrid.GRID_SIZE
        

    
