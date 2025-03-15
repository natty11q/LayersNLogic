import pygame
from OpenGL.GL import *
import numpy as np
import glfw

def opengl_to_pygame_surface(x, y, width, height):
    # Read pixel data from OpenGL framebuffer
    glReadBuffer(GL_FRONT)
    pixel_data = glReadPixels(x, y, width, height, GL_RGBA, GL_UNSIGNED_BYTE)
    
    # Create a Pygame Surface from the pixel data
    surface = pygame.image.fromstring(pixel_data, (width, height), 'RGBA', True)
    
    # Convert the Surface to match the display format
    surface = surface.convert_alpha()
    
    # Flip the Surface vertically to match OpenGL's coordinate system
    surface = pygame.transform.flip(surface, False, True)
    
    return surface

def main():
    # Initialize Pygame
    pygame.init()
    window_size = (800, 600)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption('OpenGL to Pygame Integration')

    if not glfw.init():
        return

    # Set GLFW window hints (optional)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(800, 600, "OpenGL with GLFW", None, None)
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)

    # Initialize OpenGL
    glViewport(0, 0, window_size[0], window_size[1])
    print("pre pre bogos binted0?")
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (window_size[0] / window_size[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Main loop
    print("pre bogos binted0?")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the OpenGL framebuffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -5)

        # Render a simple OpenGL triangle
        glBegin(GL_TRIANGLES)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(-1.0, -1.0, 0.0)
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(1.0, -1.0, 0.0)
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0.0, 1.0, 0.0)
        glEnd()

        # Capture OpenGL content as a Pygame Surface
        print("bogos binted0?")
        opengl_surface = opengl_to_pygame_surface(0, 0, window_size[0], window_size[1])

        print("bogos binted?")
        # Blit the OpenGL surface onto the Pygame screen
        screen.blit(opengl_surface, (0, 0))

        # Update the display
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
