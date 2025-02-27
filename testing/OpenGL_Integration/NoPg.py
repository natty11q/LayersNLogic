import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np

# Initialize GLUT (for windowless rendering)
glutInit()

# Set up an OpenGL context
def setup_opengl():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

# Draw a square with OpenGL
def draw_square():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glBegin(GL_QUADS)
    glColor3f(0.0, 1.0, 0.0)  # Green color
    glVertex2f(-0.5, -0.5)
    glVertex2f(0.5, -0.5)
    glVertex2f(0.5, 0.5)
    glVertex2f(-0.5, 0.5)
    glEnd()

    glFlush()

# SimpleGUI draw handler
def draw(canvas):
    draw_square()
    
    # Use SimpleGUI to draw a circle
    canvas.draw_circle((400, 200), 80, 5, "Red", "Blue")

# Main setup
def main():
    setup_opengl()

    # Start the SimpleGUI frame
    frame = simplegui.create_frame("SimpleGUI + OpenGL", 800, 400)
    frame.set_draw_handler(draw)
    frame.start()

main()
