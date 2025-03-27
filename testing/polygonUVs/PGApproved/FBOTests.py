import os, math, time, ctypes
import numpy as np
import pygame
from PIL import Image

try:
    import simplegui  # type: ignore
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram

# ----------------- Context & Window Setup -----------------
pygame.init()
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

canvas_width, canvas_height = 900, 600
screen = pygame.display.set_mode((canvas_width, canvas_height), pygame.OPENGL | pygame.DOUBLEBUF)
pygame.display.set_caption("Shader Render to Surface")
print("OpenGL version:", glGetString(GL_VERSION).decode())

# ----------------- Shader Setup -----------------
vertex_shader_source = """
#version 330 core
in vec2 position;
in vec2 texCoord;
out vec2 vTexCoord;
void main() {
    gl_Position = vec4(position, 0.0, 1.0);
    vTexCoord = texCoord;
}
"""

fragment_shader_source = """
#version 330 core
in vec2 vTexCoord;
out vec4 fragColor;
uniform sampler2D textureSampler;
void main() {
    fragColor = texture(textureSampler, vTexCoord);
}
"""

def create_shader_program():
    vs = compileShader(vertex_shader_source, GL_VERTEX_SHADER)
    fs = compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)
    return compileProgram(vs, fs)


# ----------------- VAO & Buffer Setup -----------------
# Create a dummy VAO first (required for core profile during shader validation).
dummy_vao = glGenVertexArrays(1)
glBindVertexArray(dummy_vao)
glBindVertexArray(0)

# Full-screen quad: positions in NDC and corresponding UV coordinates.
quad_vertices = np.array([
    # x,    y,     u,    v
    -1.0, -1.0,   0.0,  0.0,
     1.0, -1.0,   1.0,  0.0,
     1.0,  1.0,   1.0,  1.0,
    -1.0,  1.0,   0.0,  1.0,
], dtype=np.float32)
quad_indices = np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32)


vao = glGenVertexArrays(1)
# glBindVertexArray(vao)

vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, quad_vertices.nbytes, quad_vertices, GL_STATIC_DRAW)

ebo = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, quad_indices.nbytes, quad_indices, GL_STATIC_DRAW)

glBindVertexArray(vao)
shader_program = create_shader_program()

# Define vertex attributes
pos_loc = glGetAttribLocation(shader_program, "position")
glEnableVertexAttribArray(pos_loc)
glVertexAttribPointer(pos_loc, 2, GL_FLOAT, GL_FALSE, 4 * quad_vertices.itemsize, ctypes.c_void_p(0))

tex_loc = glGetAttribLocation(shader_program, "texCoord")
glEnableVertexAttribArray(tex_loc)
glVertexAttribPointer(tex_loc, 2, GL_FLOAT, GL_FALSE, 4 * quad_vertices.itemsize, ctypes.c_void_p(2 * quad_vertices.itemsize))

# IMPORTANT: Keep the VAO bound during validation

# ----------------- Texture Setup -----------------
# Load image with Pillow.
image_path = "/Users/nathanielfrimpong-santeng/codestuffs/RHUL/Software Eng/pythonProjects/GroupPythonGame/LayersNLogic/testing/testAssets/goik.png"  # Update with your image path
img = Image.open(image_path)
tex_np = np.array(img.convert("RGB"), dtype=np.uint8)
tex_height, tex_width, _ = tex_np.shape

texture_id = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texture_id)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, tex_width, tex_height, 0, GL_RGB, GL_UNSIGNED_BYTE, tex_np)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
glBindTexture(GL_TEXTURE_2D, 0)

# ----------------- Framebuffer Setup -----------------
# Create an offscreen framebuffer that matches the canvas size.
fbo = glGenFramebuffers(1)
glBindFramebuffer(GL_FRAMEBUFFER, fbo)
render_texture = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, render_texture)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, canvas_width, canvas_height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, render_texture, 0)
if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
    print("Framebuffer is not complete!")
glBindFramebuffer(GL_FRAMEBUFFER, 0)

# ----------------- Rendering Functions -----------------
def render_offscreen():
    glBindFramebuffer(GL_FRAMEBUFFER, fbo)
    glViewport(0, 0, canvas_width, canvas_height)
    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT)
    
    glUseProgram(shader_program)
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    tex_uniform = glGetUniformLocation(shader_program, "textureSampler")
    glUniform1i(tex_uniform, 0)
    
    glBindVertexArray(vao)
    glDrawElements(GL_TRIANGLES, len(quad_indices), GL_UNSIGNED_INT, None)
    glBindVertexArray(0)
    
    glBindTexture(GL_TEXTURE_2D, 0)
    glUseProgram(0)
    glFlush()  # Ensure commands are executed
    glBindFramebuffer(GL_FRAMEBUFFER, 0)

def read_offscreen():
    glBindFramebuffer(GL_FRAMEBUFFER, fbo)
    pixels = glReadPixels(0, 0, canvas_width, canvas_height, GL_RGB, GL_UNSIGNED_BYTE)
    # print(pixels)
    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    image = np.frombuffer(pixels, dtype=np.uint8).reshape((canvas_height, canvas_width, 3))
    image = np.flipud(image)
    return image

# ----------------- SimpleGUI Image Wrapper -----------------
from collections import OrderedDict
_dummy = simplegui.load_image("")
DummyImage = type(_dummy)
class SimpleGUIImageWrapper(DummyImage):  # type: ignore
    def __init__(self, surface):
        self._pygame_surface = surface
        self.center = (surface.get_width() / 2, surface.get_height() / 2)
        self.size = (surface.get_width(), surface.get_height())
        self._pygamesurfaces_cached = OrderedDict()
        self._pygamesurfaces_cached_clear = lambda: self._pygamesurfaces_cached.clear()
        self._pygamesurfaces_cache_max_size = getattr(_dummy, "_pygamesurfaces_cache_default_max_size", 50)
        self._draw_count = 0

wrapped_image = None
def update_image_wrapper():
    global wrapped_image
    img_data = read_offscreen()
    # pygame.surfarray.make_surface expects shape (width, height, channels) so transpose the array.
    surf = pygame.surfarray.make_surface(np.transpose(img_data, (1, 0, 2)))
    wrapped_image = SimpleGUIImageWrapper(surf)

# ----------------- Draw Handler -----------------
def draw(canvas: simplegui.Canvas):
    render_offscreen()
    update_image_wrapper()
    if wrapped_image:
        canvas.draw_image(wrapped_image, wrapped_image.center, wrapped_image.size,
                          (canvas_width/2, canvas_height/2), wrapped_image.size)
    else:
        canvas.draw_text("Rendering...", (canvas_width//2-50, canvas_height//2), 20, "White")
    print("Frame rendered offscreen.")

import pygame
frame = simplegui.create_frame("Shader Render to Pygame Surface", canvas_width, canvas_height, 0)
frame.set_draw_handler(draw)
frame._hide_controlpanel = True
frame._canvas_border_size = 0
frame._canvas_x_offset = 0
frame._canvas_y_offset = 0
frame._border_size = 0
frame._pygame_surface = pygame.display.set_mode((canvas_width, canvas_height),
                                                  simplegui.Frame._pygame_mode_flags,
                                                  simplegui.Frame._pygame_mode_depth)
frame.start()
