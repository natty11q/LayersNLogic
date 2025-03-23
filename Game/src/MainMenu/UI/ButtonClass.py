


from ApplicationEngine.include.Maths.Maths import *
import ApplicationEngine.AppEngine as LNLEngine



# TODO: modify to exist inside the engine as a child og the UI ELEMENT class
class Menu_Button(LNLEngine.GameObject):
    """Button class for Button ui elements

    Args:
        width: float, button width
    """
    def __init__(self, width : float, height : float,
                position : Vec2,
                baseSpritePath  : str, 
                hoverSpritePath : str | None = None):
        
    
        self.basePosition       : Vec2 = position
        self.currentPosition    : Vec2 = position
        self.targetPosition     : Vec2 = position

        self.ButtonAtive = False # wether the button is accesable EG If the play has unlocked that option yet or not

        self.width          : float = width 
        self.currentWidth   : float = width


        self.prevWidth   : float = width # cache the width and height (reesize optimisation)

        self.height         : float = height
        self.currentHeight  : float = height

        self.prevHeight   : float = height # cache the width and height (reesize optimisation)



        # TODO : decide if the button action should be handled here or outside the class
        self.OnClickHandles : list = [] # a list contatining the actions that occur when the button is pressed
        self.nextButtonId   : int = 0



        self.hovered  : bool = False # if the mouse is hovered over the specified target
        self.selected : bool = False # if the button had the keydown event above it
        self.pressed  : bool = False # if the button was pressed on this frame




        tex             : LNLEngine.Texture = LNLEngine.Texture(baseSpritePath)
        self.BaseSprite : LNLEngine.Sprite = LNLEngine.Sprite(tex, self.currentPosition, self.width, self.height)
        


        self.HoverSprite : LNLEngine.Sprite | None = None
        if hoverSpritePath:
            tex : LNLEngine.Texture = LNLEngine.Texture(hoverSpritePath)
            self.HoverSprite = LNLEngine.Sprite(tex, self.currentPosition, self.width, self.height)


        



    def _OnUpdate(self, deltatime: float):

        if self.pressed:
            LNL_LogEngineInfo("button pressed : ", self.id)
            self.OnButtonPress()
        
        self.pressed = False
        self.hovered = False # reset the state of the button if not active

        
        
        
        
        if self.Overlap():
            self.hovered = True


        if self.currentWidth != self.prevWidth:
            self.BaseSprite.SetWidth(self.currentWidth)
        if self.currentHeight != self.prevHeight:
            self.BaseSprite.SetHeight(self.currentHeight)


        self.BaseSprite.SetPos(self.currentPosition)
        if self.HoverSprite:
            self.HoverSprite.SetPos(self.currentPosition)


    def _OnEvent(self, event: LNLEngine.Event):
        if event.GetName() == "MouseButtonDown" and event.button == 1:
            self.selected = False
            if self.Overlap():
                self.selected = True

            pos = LNLEngine.Mouse.GetPos()
            LNL_LogError(pos , "btn pos : ", self.currentPosition,
                         self.currentPosition + Vec2(self.width, self.height))

        if event.GetName() == "MouseButtonUp" and event.button == 1:
            if self.hovered and self.selected:
                self.pressed = True
            self.selected = False


    def Draw(self):
        self.BaseSprite.Draw()
        if self.HoverSprite and self.hovered:
            self.HoverSprite.Draw()


    def AddOnClickkHandler(self, onClick, args : list) -> int:
        self.OnClickHandles[self.nextButtonId] = [onClick, args]
        self.nextButtonId += 1
        return self.nextButtonId -1


    def Overlap(self):
        pos = LNLEngine.Mouse.GetPos()
        if  pos[0] >= self.currentPosition[0] and pos[0] <= self.currentPosition[0] + self.currentWidth\
            and pos[1] >= self.currentPosition[1] and pos[1] <= self.currentPosition[1] + self.currentHeight:
             
            return True


        
        return False

    def OnButtonPress(self):
        for handleData in self.OnClickHandles:
            handleData[0]( *(handleData[1]) )