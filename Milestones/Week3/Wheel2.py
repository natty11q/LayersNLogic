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
rotation = 0  # Rotation angle of the wheel
rotation_speed = 0.1  # Speed at which the wheel rotates

# Load sprite image
wheel_image = simplegui.load_image('http://www.cs.rhul.ac.uk/courses/CS1830/sprites/coach_wheel-512.png')  # Replace with actual URL
image_size = (100, 100)  # Adjust based on actual sprite size

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
    global position, velocity, rotation
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
    
    # Update rotation
    if velocity != 0:
        rotation += (velocity / radius) * rotation_speed

# Draw handler
def draw(canvas : simplegui.Canvas):
    global rotation
    canvas.draw_image(wheel_image, (image_size[0] / 2, image_size[1] / 2), image_size,
                      position, (radius * 2, radius * 2), rotation)

# Create frame
frame = simplegui.create_frame("Wheel Motion", WIDTH, HEIGHT)
frame.set_canvas_background('#2C6A6A')
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# Start update timer
timer = simplegui.create_timer(50, update)
timer.start()

# Start frame
frame.start()
