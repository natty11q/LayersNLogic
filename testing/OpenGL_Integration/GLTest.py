import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np

# Initialize Pygame & OpenGL
pygame.init()
pygame.display.set_mode((600, 400), DOUBLEBUF | OPENGL)

# === GLSL Shaders ===
VERTEX_SHADER = """
#version 330 core
layout(location = 0) in vec2 aPos;
void main() {
    gl_Position = vec4(aPos, 0.0, 1.0);
}
"""

FRAGMENT_SHADER = """
#version 330 core
out vec4 FragColor;
void main() {
    FragColor = vec4(0.2, 0.8, 0.3, 1.0);  // Green color
}
"""

# === Shader & Buffer Setup ===
def create_shader_program():
    shader = compileProgram(
        compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
        compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
    )
    return shader

def create_square():
    vertices = np.array([
        -0.5, -0.5,
         0.5, -0.5,
         0.5,  0.5,
        -0.5,  0.5,
    ], dtype=np.float32)

    indices = np.array([
        0, 1, 2,
        2, 3, 0
    ], dtype=np.uint32)

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)

# === Draw Handler ===
def draw(canvas):
    # Render with OpenGL
    glClear(GL_COLOR_BUFFER_BIT)
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
    pygame.display.flip()
    
    # Capture the OpenGL output
    size = (300, 400)
    pixels = glReadPixels(0, 0, size[0], size[1], GL_RGBA, GL_UNSIGNED_BYTE)
    surface = pygame.image.fromstring(pixels, size, "RGBA")
    surface = pygame.transform.flip(surface, False, True)

    # Convert to SimpleGUI image
    image = simplegui._load_local_image(surface)

    # Draw with SimpleGUI
    canvas.draw_image(image, (150, 200), (300, 400), (150, 200), (300, 400))
    canvas.draw_circle((450, 200), 80, 5, "Red", "Blue")

# === Main Setup ===
def main():
    shader = create_shader_program()
    glUseProgram(shader)
    create_square()

    frame = simplegui.create_frame("SimpleGUI + OpenGL", 600, 400)
    frame.set_draw_handler(draw)
    frame.start()

main()
