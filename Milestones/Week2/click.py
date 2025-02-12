from Vector import Vector
import math
import random

try:
    import simplegui # type: ignore
except ImportError :
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

WINDOW_SIZE = (900, 600)
BALL_RADIUS = 20
BALL_COLOR = "Blue"




class GameTime:
    DeltaTime : float = 1/60

class Ball:
    def __init__(self, position : Vector, vel : Vector, radius : float, color : str):
        self._position : Vector = position
        self._velocity : Vector = vel
        self._acceleration : Vector = Vector()
        self._radius : float = radius
        self._colour = color
        self._Mass = 1
    
    
    def ApplyImpulse(self, impulse :  Vector):
        self._velocity += impulse.divide(self._Mass)
    
    def SetColour(self, newCol):
        self._colour = newCol
    
    def Update(self):
        self._velocity.add( self._acceleration.multiply(GameTime.DeltaTime) )
        self._position.add( self._velocity )

    
    
            
    def Draw(self, canvas : simplegui.Canvas): 
        canvas.draw_circle((self._position.x, self._position.y), self._radius, 2, self._colour, self._colour)
        
    
    def GetKinetic(self):
        return 0.5 * self._Mass * self._velocity.length_squared()

    def SetAcceleration(self , newAcc : Vector):
        self._acceleration = newAcc

    def SetVelocity(self , newVel : Vector):
        self._velocity = newVel

    def GetPosition(self):
        return self._position
    
    def SetPosition(self, newPos : Vector):
        self._position = newPos
        
    def is_inside(self, pos):
        return math.sqrt((self._position.x - pos[0])**2 + (self._position.y - pos[1])**2) <= self._radius

class Mouse:
    def __init__(self):
        self.position = None
    
    def click_handler(self, pos):
        self.position = pos
    
    def click_pos(self):
        pos = self.position
        self.position = None
        return pos

class Interaction:
    def __init__(self, ball, mouse):
        self.ball: Ball = ball
        self.mouse = mouse
    
    def draw(self, canvas):
        self.ball.Update()
        self.ball.Draw(canvas)
        click = self.mouse.click_pos()
        if click:
            if self.ball.is_inside(click):
                self.ball.SetVelocity( Vector(random.randint(-25,25), random.randint(-25,25)) )
            else:
                self.ball.SetVelocity( Vector() )
                self.ball.SetPosition( Vector(click[0],click[1]) )

ball = Ball(Vector(450, 300),Vector() , BALL_RADIUS, BALL_COLOR)
mouse = Mouse()
interaction = Interaction(ball, mouse)

frame = simplegui.create_frame("Ball Interaction", WINDOW_SIZE[0], WINDOW_SIZE[1])
frame.set_draw_handler(interaction.draw)
frame.set_mouseclick_handler(mouse.click_handler)

frame.start()
