import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np


# Initialize Pygame and set up an OpenGL context
pygame.init()
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 2)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
pygame.display.set_caption("OpenGL in Pygame (macOS-compatible)")

# Print the OpenGL version
print(glGetString(GL_VERSION).decode())

# Vertex and fragment shaders
vertex_shader = """
#version 410 core
layout(location = 0) in vec3 position;
void main()
{
    gl_Position = vec4(position, 1.0);
}
"""

fragment_shader = """
#version 410 core
out vec4 color;
void main()
{
    color = vec4(1.0, 0.5, 0.2, 1.0);
}
"""


vao = glGenVertexArrays(1)
glBindVertexArray(vao)

# Compile shaders
program = compileProgram(
    compileShader(vertex_shader, GL_VERTEX_SHADER),
    compileShader(fragment_shader, GL_FRAGMENT_SHADER)
)

# Set up vertex data (a simple triangle)
vertices = np.array([
    [ 0.0,  0.5, 0.0],
    [-0.5, -0.5, 0.0],
    [ 0.5, -0.5, 0.0]
], dtype=np.float32)

# Create a VAO and VBO
vao = glGenVertexArrays(1)
vbo = glGenBuffers(1)

glBindVertexArray(vao)

glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

# Specify the layout of the vertex data
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
glEnableVertexAttribArray(0)

glBindBuffer(GL_ARRAY_BUFFER, 0)
glBindVertexArray(0)

# Main render loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False

    glClear(GL_COLOR_BUFFER_BIT)
    glUseProgram(program)
    
    glBindVertexArray(vao)
    glDrawArrays(GL_TRIANGLES, 0, 3)
    glBindVertexArray(0)

    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()