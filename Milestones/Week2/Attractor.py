 # type: ignore
import random
# import time
# import json

from Vector import Vector

try:
    import simplegui # type: ignore
except ImportError :
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui



def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def rand_col():
    return rgb_to_hex((random.randint(0,255), random.randint(0,255), random.randint(0,255)))


DRAG_COEF = 0.001

class GameTime:
    DeltaTime : float = 1/60

class Ball:
    def __init__(self, position : Vector, vel, radius, color):
        self._radius = radius
        self._position : Vector = position
        self._velocity : Vector = vel
        self._acceleration = Vector()
        self._colour = color
        self._Mass = 1
    
    
    def ApplyImpulse(self, impulse :  Vector):
        self._velocity += impulse.divide(self._Mass)
    
    def SetColour(self, newCol):
        self._colour = newCol
    
    def Update(self):
        self._velocity.add( self._acceleration.multiply(GameTime.DeltaTime) )
        # dragDirection : Vector = self._velocity.get_normalized() * -1
        # dragStrength : float  = self._velocity.length_squared() * DRAG_COEF
        # self._velocity.subtract( dragDirection * dragStrength )
        self._position.add( self._velocity )
        
        if self._radius > 1:
            self._radius -= 1
    
    
            
    def Draw(self, canvas : simplegui.Canvas):
        canvas.draw_circle((self._position.x, self._position.y), self._radius, 2, self._colour, self._colour)
        
    
    def GetKinetic(self):
        return 0.5 * self._Mass * self._velocity.length_squared()

    def SetAcceleration(self , newAcc : Vector):
        self._acceleration = newAcc

    def GetPosition(self):
        return self._position
    
    def SetPosition(self, newPos : Vector):
        self._position = newPos

class Attractor(Ball):
    def __init__(self, position):
        super().__init__(position, Vector(), 20, "red")
    
    def Draw(self, canvas : simplegui.Canvas): 
        canvas.draw_circle((self._position.x, self._position.y), self._radius, 2, "red", "black")
        



WIDTH = 600
HEIGHT = 400
balls :  list [Ball]= []
GRAVITY_STRENGTH = 10
ATTRACTOR : Attractor | None = None

def add_ball():
    pos = Vector(WIDTH / 2, HEIGHT / 2)
    vel = Vector(random.uniform(-5, 5), random.uniform(-5, 5))
    radius = random.randint(10, 50)
    color = rand_col()
    new_ball = Ball(pos, vel, radius, color)
    balls.append(new_ball)

def timer_handler():
    add_ball()

def draw(canvas):
    global balls, ATTRACTOR
    x = 0
    for i in range(len(balls) - x):
        ball = balls[i]
        if ATTRACTOR:
            dirVec = ATTRACTOR.GetPosition() - ball.GetPosition()
            ball.SetAcceleration( 
                                dirVec.normalize().multiply( GRAVITY_STRENGTH/(dirVec.length_squared()) )
                            )
        
        ball.Update()
        ball.Draw(canvas)
        if ATTRACTOR:
            ATTRACTOR.Draw(canvas)

def click(pos):
    global ATTRACTOR
    if not ATTRACTOR:
        ATTRACTOR = Attractor(Vector(pos[0], pos[1]))
    
    ATTRACTOR.SetPosition(Vector(pos[0], pos[1]))
    # print(f"Attractor set at: {pos}")

frame = simplegui.create_frame("Multiple Balls", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(click)


timer = simplegui.create_timer(100, timer_handler)
timer.start()

frame.start()


