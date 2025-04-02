from __future__ import annotations
from ApplicationEngine.include.Maths.Vector.Vector import Vec2
from ApplicationEngine.src.Graphics.SpriteAnimationClass import Vec2
from Game.src.GameComponents.Entities.EntityClass import *
from Game.src.GameComponents.Environement.Attributes.CanTravelThroughPortals import Vec2
from Game.src.GameComponents.Environement.Environment import Vec2
from Game.src.GameComponents.Environement.Portal import Vec2


class Enemy(Entity):
    def __init__(self, dimensions: Vec2, position: Vec2 = Vec2(0,0) , mass : float =10, name: str = ""):
        super().__init__(dimensions, position, mass, name)





class Tier1Enemy(Enemy):
    def __init__(self, dimensions: Vec2 = Vec2(WorldGrid.GRID_SIZE,WorldGrid.GRID_SIZE), position: Vec2 = Vec2(), mass=10, name: str = ""):
        super().__init__(dimensions, position, mass, name)

        tex = LNLEngine.Texture("Game/Assets/Sprites/tier1bug.png", True)
        self.sprite = LNLEngine.Sprite(tex , self.body.position - (dimensions / 2), WorldGrid.GRID_SIZE, WorldGrid.GRID_SIZE)



        self.attack = 1


    def _OnUpdate(self, deltatime: float):
        self.body.linearVelocity += Vec2(math.sin(LNLEngine.Temporal.LLEngineTime.Time() * 2), math.sin(LNLEngine.Temporal.LLEngineTime.Time() * random.randint(0,5)) * 10)
        self.sprite.SetPos(self.body.getPosition() - Vec2(self.sprite.spriteHeight/2,self.sprite.spriteWidth/2))

    def Draw(self):
        self.sprite.Draw()

class Tier2Enemy(Enemy):
    def __init__(self, dimensions: Vec2, position: Vec2 = Vec2(), mass=10, name: str = ""):
        super().__init__(dimensions, position, mass, name)



class Tier3nemy(Enemy):
    def __init__(self, dimensions: Vec2, position: Vec2 = Vec2(), mass=10, name: str = ""):
        super().__init__(dimensions, position, mass, name)