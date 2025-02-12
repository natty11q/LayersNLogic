import random
from Vector import Vector


try:
    import simplegui # type: ignore
except ImportError :
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def rand_col():
    return rgb_to_hex((random.randint(0,255), random.randint(0,255), random.randint(0,255)))


class Ball:
    def __init__(self, pos, vel, radius, color):
        self.pos : Vector = pos    
        self.vel : Vector  = vel   
        self.radius = radius
        self.color = color
        
    def draw(self, canvas):
        canvas.draw_circle((self.pos.x, self.pos.y), self.radius, 2, self.color, self.color)
    
    def update(self):
        self.pos += self.vel

        if self.radius > 1:
            self.radius -= 1



WIDTH = 600
HEIGHT = 400
balls :  list [Ball]= [] 

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
    To_Discard = []
    for i in range(len(balls)):
        ball = balls[i]
        
        if ball.pos.x < 0 or ball.pos.y < 0 or ball.pos.x > WIDTH or ball.pos.y > HEIGHT:
            To_Discard.append(i)

        ball.update()
        ball.draw(canvas)

    for j in To_Discard:
        balls.pop(j)

frame = simplegui.create_frame("Multiple Balls", WIDTH, HEIGHT)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(100, timer_handler)
timer.start()

frame.start()


