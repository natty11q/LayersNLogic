try:
    import simplegui # type: ignore
except ImportError :
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# Global variables
WIDTH, HEIGHT = 400, 300
radius = 20
position = [WIDTH // 2, HEIGHT // 2]
velocity = 0
acceleration = 0.5  # Acceleration when a key is pressed
deceleration = 0.1  # Friction when no key is pressed

# Key handlers
def keydown(key):
    global velocity
    if key == simplegui.KEY_MAP['right']:
        velocity += acceleration
    elif key == simplegui.KEY_MAP['left']:
        velocity -= acceleration

def keyup(key):
    global velocity
    if key in (simplegui.KEY_MAP['right'], simplegui.KEY_MAP['left']):
        pass  # No direct effect, handled in the update step

# Timer handler (physics update)
def update():
    global position, velocity
    position[0] += velocity
    
    # Apply deceleration (friction) if not pressing keys
    if velocity > 0:
        velocity = max(0, velocity - deceleration)
    elif velocity < 0:
        velocity = min(0, velocity + deceleration)
    
    # Wrap around the canvas
    if position[0] < -radius:
        position[0] = WIDTH + radius
    elif position[0] > WIDTH + radius:
        position[0] = -radius

# Draw handler
def draw(canvas):
    canvas.draw_circle(position, radius, 1, "Black", "White")

# Create frame
frame = simplegui.create_frame("Wheel Motion", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# Start update timer
timer = simplegui.create_timer(50, update)
timer.start()

# Start frame
frame.start()
