
from ApplicationEngine.src.Graphics.SpriteClass import * 




class SpriteAnimation(GameObject):

    def __init__(self,  sprites     : list[Sprite],
                        baseWidth   : int, 
                        baseHeight  : int, 
                        framerate   : float = 24, 
                        repeat      : bool = False, 
                        startingSpriteIdx   : int = 0, 
                        endingSpriteIndiex  : int | None = None, 
                        displayWhenComplete : bool = True,
                        playFromStart       : bool = False
                ):
        

        self.sprites : list[Sprite] = sprites

        self.framerate = framerate
        self.spriteTTL = 1.0 / framerate
        
        self.spriteInitIdx = startingSpriteIdx
        self.spriteEndIdx = endingSpriteIndiex if (endingSpriteIndiex is not None) else (len(self.sprites) - 1)
        self.spriteIdx = startingSpriteIdx

        self.currentSprite = self.sprites[self.spriteIdx]
        
        self.repeat = repeat
        self.complete = False
        self.playing = playFromStart

        self.displayWhenComplete = displayWhenComplete

        self.position : Vec2    = Vec2()
        self.rotation : float   = 0.0

        self.baseWidth  = baseWidth
        self.baseHeight = baseHeight

        self.fromSpritesheet = True

        self.flip_lr_onFrame = False
        self.flip_ud_onFrame = False

        self.setWidth(self.baseWidth)
        self.setHeight(self.baseHeight)
        self.setPos(self.position)
        self.setRot(self.rotation)



    @staticmethod
    def LoadFromSpritesheet(spritesheet : Texture, 
                            rows : int, cols : int,
                            
                            frame_width : int , frame_height : int ,

                            framerate   : float = 24,
                            repeat      : bool = False,
                            startingSpriteIdx   : int = 0, 
                            endingSpriteIndiex  : int | None = None, 
                            displayWhenComplete : bool = True, 
                            playFromStart       : bool = True
                    ):


        uvWidth  = 1 / rows
        uvHeight = 1 / cols


        sprites : list[Sprite] = []
        for c in range(rows):
            for r in range(rows):
                tl_uv = Vec2(uvWidth * r, uvHeight * (cols - c))
                br_uv = Vec2(uvWidth * (r + 1), uvHeight * (cols - (c + 1)))

                sprites.append(
                    Sprite( spritesheet, Vec2(), frame_width, frame_height, (tl_uv,br_uv) )
                    )

        return SpriteAnimation(sprites, frame_width, frame_height, 
                               framerate, repeat, startingSpriteIdx, 
                               endingSpriteIndiex, displayWhenComplete, playFromStart)


    def setPos(self, position : Vec2):
        self.position = position
        for sprite in self.sprites:
            sprite.SetPos(position)
        
    def setRot(self, rotation : float):
        self.rotation = rotation
        for sprite in self.sprites:
            sprite.SetRot(rotation)

    def setWidth(self, width):
        self.baseWidth = width
        for sprite in self.sprites:
            sprite.SetWidth(self.baseWidth)
    
    
    def Flip_lr(self):
        self.flip_lr_onFrame = True

   
    def Flip_ud(self):
        for sprite in self.sprites:
            sprite.Flip_ud()
        return self
    



    def setHeight(self, height):
        self.baseHeight = height
        for sprite in self.sprites:
            sprite.SetHeight(self.baseHeight)



    def Update(self, deltatime : float):
        

        if not self.playing or self.complete:
            return


        self.spriteTTL -= deltatime
        if self.spriteTTL <= 0.0:
            self.spriteIdx += 1
            self.spriteTTL = 1 / self.framerate

            if self.spriteIdx >= self.spriteEndIdx:
                if not self.repeat:
                    self.complete = True
                    self.playing = False
        self.spriteIdx = max(self.spriteIdx % (self.spriteEndIdx + 1), self.spriteInitIdx)

        self.currentSprite = self.sprites[self.spriteIdx]
    

    def Play(self):
        self.playing = True
        self.complete = False

    def Pause(self):
        self.playing = False

    def isPaused(self):
        return not self.playing
    

    

    def Draw(self):
        self.currentSprite.flipped_lr = self.flip_lr_onFrame
        self.currentSprite.Draw()

        self.flip_lr_onFrame = False
        self.flip_ud_onFrame = False
