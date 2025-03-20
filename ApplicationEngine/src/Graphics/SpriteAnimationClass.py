
from ApplicationEngine.src.Graphics.SpriteClass import * 




class SpriteAnimation:

    def __init__(self, sprites : list[Sprite] , framerate : float = 24, repeat = False , startingSpriteIdx = 0, endingSpriteIndiex = None):
        self.sprites : list[Sprite] = sprites
        self.spriteTTL = 1.0 / framerate
        self.spriteInitIdx = startingSpriteIdx
        self.spriteIdx = startingSpriteIdx
        self.currentSprite = self.sprites[self.spriteIdx]
        self.repeat = repeat
        self.complete = False

    # def Update(self, dt : float):
    #     self.spriteTTL -= dt
    #     if self.spriteTTL <= 0.0:
    #         self.spriteIdx += 1
    #         # if self.spriteIdx == self