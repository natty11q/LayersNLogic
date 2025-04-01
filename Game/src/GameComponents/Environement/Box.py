from Game.src.GameComponents.Environement.EnvironmentObject import * 


class Box(EnvironmentObject2D):
    boxTexture = LNLEngine.Texture("",False)
    def __init__(self,mass : float ,dimensions : Vec2 = Vec2(1,1)):
        super().__init__(mass = mass) 
        self.dimensions = dimensions * WorldGrid.GRID_SIZE  
        self.sprite = LNLEngine.Sprite(Box.boxTexture, self.body.position - self.dimensions/2, self.dimensions.x, self.dimensions.y)
        

 


    
