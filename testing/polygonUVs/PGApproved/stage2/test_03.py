import numpy as np
import time
import pygame
try:
    import simplegui  # type: ignore
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import ctypes

# Canvas dimensions
canvas_width, canvas_height = 900, 600

# Global variables for OpenGL objects
shader_program = None       # for drawing the triangle
quad_shader_program = None  # for drawing the textured quad
vao = None                  # triangle VAO
quad_vao = None             # quad VAO
fbo = None
fbo_texture = None

frame = simplegui.create_frame("OpenGL FBO Rendering", canvas_width, canvas_height, 0)
# pygame.init()
# Request an OpenGL 3.3 Core context.


pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
pygame.display.gl_set_attribute(pygame.GL_SWAP_CONTROL, 1)


# Create an OpenGL display.
pygame.display.set_mode((canvas_width, canvas_height), pygame.OPENGL | pygame.DOUBLEBUF, vsync= 1)


frame._pygame_surface = pygame.display.get_surface()
# Monkey-patch update() so that any call with rectangle arguments calls flip().
def opengl_update(rect=None):
    pygame.display.flip()
pygame.display.update = opengl_update

def init_gl():
    global shader_program, vao, fbo, fbo_texture, quad_shader_program, quad_vao

    # --- Shader for rendering the triangle into the FBO ---
    vertex_shader_source = """
    #version 330 core
    layout(location = 0) in vec2 position;
    layout(location = 1) in vec3 inColor;
    out vec3 fragColor;
    void main(){
        fragColor = inColor;
        gl_Position = vec4(position, 0.0, 1.0);
    }
    """
    fragment_shader_source = """
    #version 330 core
    in vec3 fragColor;
    out vec4 color;
    void main(){
        color = vec4(fragColor, 1.0);
    }
    """

        # Triangle vertices: each with (position, color)
    vertices = np.array([
        -0.8, -0.8,  1.0, 0.0, 0.0,  # Bottom-left: red
         0.8, -0.8,  0.0, 1.0, 0.0,  # Bottom-right: green
         0.0,  0.8,  0.0, 0.0, 1.0   # Top: blue
    ], dtype=np.float32)

    
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    print(glGetError())

    shader_program = compileProgram(
        compileShader(vertex_shader_source, GL_VERTEX_SHADER),
        compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)
    )
    

    
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 5 * vertices.itemsize, ctypes.c_void_p(0))
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 5 * vertices.itemsize,
                          ctypes.c_void_p(2 * vertices.itemsize))
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)
    
    # --- Create the FBO and attach a texture ---
    fbo = glGenFramebuffers(1)
    glBindFramebuffer(GL_FRAMEBUFFER, fbo)
    fbo_texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, fbo_texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, canvas_width, canvas_height,
                 0, GL_RGB, GL_UNSIGNED_BYTE, None)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, fbo_texture, 0)
    if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
        print("Error: Framebuffer is not complete!")
    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    
    # --- Shader for rendering the FBO texture as a full-screen quad ---
    quad_vertex_shader = """
    #version 330 core
    layout(location = 0) in vec2 position;
    layout(location = 1) in vec2 texCoord;
    out vec2 TexCoord;
    void main(){
        TexCoord = texCoord;
        gl_Position = vec4(position, 0.0, 1.0);
    }
    """
    quad_fragment_shader = """
    #version 330 core
    in vec2 TexCoord;
    out vec4 FragColor;
    uniform sampler2D screenTexture;
    void main(){
        FragColor = texture(screenTexture, TexCoord);
    }
    """
    
    
    quad_vao = glGenVertexArrays(1)
    glBindVertexArray(quad_vao)


    quad_shader_program = compileProgram(
        compileShader(quad_vertex_shader, GL_VERTEX_SHADER),
        compileShader(quad_fragment_shader, GL_FRAGMENT_SHADER)
    )
    
    # Full-screen quad vertices: position (x,y) and texture coordinates (u,v)
    quadVertices = np.array([
        # First triangle
        -1.0, -1.0,  0.0, 0.0,
         1.0, -1.0,  1.0, 0.0,
         1.0,  1.0,  1.0, 1.0,
        # Second triangle
        -1.0, -1.0,  0.0, 0.0,
         1.0,  1.0,  1.0, 1.0,
        -1.0,  1.0,  0.0, 1.0,
    ], dtype=np.float32)
    
    quad_vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, quad_vbo)
    glBufferData(GL_ARRAY_BUFFER, quadVertices.nbytes, quadVertices, GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4 * quadVertices.itemsize, ctypes.c_void_p(0))
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * quadVertices.itemsize, ctypes.c_void_p(2 * quadVertices.itemsize))
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

def render_to_fbo():
    """Renders the triangle to the offscreen framebuffer."""
    glBindFramebuffer(GL_FRAMEBUFFER, fbo)
    glViewport(0, 0, canvas_width, canvas_height)
    # glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    
    glBindVertexArray(vao)
    glUseProgram(shader_program)
    glDrawArrays(GL_TRIANGLES, 0, 3)
    glBindVertexArray(0)
    glUseProgram(0)
    glFlush()
    glBindFramebuffer(GL_FRAMEBUFFER, 0)

def render_quad():
    """Renders the FBO texture as a full-screen quad to the default framebuffer."""
    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    glViewport(0, 0, canvas_width, canvas_height)
    glClearColor(0.2, 0.2, 0.2, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    
    glUseProgram(quad_shader_program)
    glBindVertexArray(quad_vao)
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, fbo_texture)
    # Set uniform "screenTexture" to texture unit 0.
    glUniform1i(glGetUniformLocation(quad_shader_program, "screenTexture"), 0)
    
    glDrawArrays(GL_TRIANGLES, 0, 6)
    glBindVertexArray(0)
    glUseProgram(0)
    glFlush()

def draw(canvas: simplegui.Canvas):
    # Render your scene (triangle) into the FBO.
    render_to_fbo()
    # Then render the FBO texture as a full-screen quad.
    render_quad()
    # Swap buffers.
    pygame.display.flip()

# Create a SimpleGUI frame.
frame.set_draw_handler(draw)
# Remove extra UI elements.
frame._hide_controlpanel = True
frame._canvas_border_size = 0
frame._canvas_x_offset = 0
frame._canvas_y_offset = 0
frame._border_size = 0
# frame._pygame_surface = pygame.display.get_surface()

init_gl()
frame.start()
