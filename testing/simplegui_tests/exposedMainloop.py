
import math
import time


try:
    import simplegui # type:  ignore 
except ImportError :
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


# Constants
WIDTH, HEIGHT = 400, 400
FPS = 60  # Target frames per second

# Global Variables
t = 0.0  # Time tracker for sine wave
running = True  # Control loop execution

# Event handlers
def draw(canvas):
    global t
    # Generate a smooth color transition using sine function
    sin_val = (math.sin(t) + 1) / 2  # Normalize to range [0,1]
    color_intensity = int(sin_val * 255)
    
    # Create an RGB color with varying intensity (R component)
    color = f'rgb({color_intensity}, 50, 150)'
    
    # Draw background
    canvas.draw_polygon([(0, 0), (WIDTH, 0), (WIDTH, HEIGHT), (0, HEIGHT)], 1, color, color)

def stop():
    """Stop the main loop."""
    global running
    running = False

# Create frame
frame = simplegui.create_frame("Sine Color Window", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.add_button("Stop", stop)

# Start the frame but don't rely on its built-in loop
frame.start()

# **Exposed Main Loop**
while running:
    print("lloopp")
    # frame._canvas._trigger_repaint()  # Force redraw
    t += 0.05  # Adjust speed of sine wave animation
    time.sleep(1 / FPS)  # Control frame rate