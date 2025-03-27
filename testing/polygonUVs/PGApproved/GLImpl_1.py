import os
import numpy as np
import math, time
import pygame
from PIL import Image

try:
    import simplegui  # type: ignore
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# ----------------- Configuration & Texture Loading -----------------
# Use an absolute path to your image
image_path = "/Users/nathanielfrimpong-santeng/codestuffs/RHUL/Software Eng/pythonProjects/GroupPythonGame/LayersNLogic/testing/testAssets/testImage3.png"
img = Image.open(image_path)
img = img.convert("RGB")
tex_np = np.array(img, dtype=np.uint8)
tex_height, tex_width, _ = tex_np.shape

# ----------------- Canvas Setup -----------------
canvas_width, canvas_height = 900, 600

# ----------------- OpenGL Shader Setup -----------------
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram

vertex_shader_source = """
#version 120
attribute vec2 position;
attribute vec2 texCoord;
varying vec2 vTexCoord;
void main() {
    gl_Position = vec4(position, 0.0, 1.0);
    vTexCoord = texCoord;
}
"""

fragment_shader_source = """
#version 120
varying vec2 vTexCoord;
uniform sampler2D textureSampler;
void main() {
    gl_FragColor = texture2D(textureSampler, vTexCoord);
}
"""

def create_shader_program():
    try:
        vertex_shader = compileShader(vertex_shader_source, GL_VERTEX_SHADER)
        fragment_shader = compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)
        program = compileProgram(vertex_shader, fragment_shader)
        return program
    except Exception as e:
        print("Shader compile error:", e)
        raise

shader_program = create_shader_program()

# Define a full-screen quad (NDC coordinates)
quad_vertices = np.array([
    #  x,    y,     u,    v
    -1.0, -1.0,   0.0,  0.0,
     1.0, -1.0,   1.0,  0.0,
     1.0,  1.0,   1.0,  1.0,
    -1.0,  1.0,   0.0,  1.0,
], dtype=np.float32)

quad_indices = np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32)

# Setup VAO, VBO, and EBO
vao = glGenVertexArrays(1)
glBindVertexArray(vao)

vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, quad_vertices.nbytes, quad_vertices, GL_STATIC_DRAW)

ebo = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, quad_indices.nbytes, quad_indices, GL_STATIC_DRAW)

pos_loc = glGetAttribLocation(shader_program, "position")
glEnableVertexAttribArray(pos_loc)
glVertexAttribPointer(pos_loc, 2, GL_FLOAT, GL_FALSE, 4 * quad_vertices.itemsize, ctypes.c_void_p(0))

tex_loc = glGetAttribLocation(shader_program, "texCoord")
glEnableVertexAttribArray(tex_loc)
glVertexAttribPointer(tex_loc, 2, GL_FLOAT, GL_FALSE, 4 * quad_vertices.itemsize, ctypes.c_void_p(2 * quad_vertices.itemsize))

glBindVertexArray(0)

# ----------------- Texture Setup -----------------
texture_id = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texture_id)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, tex_width, tex_height, 0, GL_RGB, GL_UNSIGNED_BYTE, tex_np)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
glBindTexture(GL_TEXTURE_2D, 0)

# ----------------- Framebuffer Setup -----------------
fbo = glGenFramebuffers(1)
glBindFramebuffer(GL_FRAMEBUFFER, fbo)
render_texture = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, render_texture)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, canvas_width, canvas_height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, render_texture, 0)
if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
    print("Framebuffer is not complete!")
glBindFramebuffer(GL_FRAMEBUFFER, 0)

# ----------------- OpenGL Rendering Function -----------------
def render_to_texture():
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

def read_rendered_texture():
    glBindFramebuffer(GL_FRAMEBUFFER, fbo)
    pixels = glReadPixels(0, 0, canvas_width, canvas_height, GL_RGB, GL_UNSIGNED_BYTE)
    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    image = np.frombuffer(pixels, dtype=np.uint8).reshape((canvas_height, canvas_width, 3))
    image = np.flipud(image)  # Flip vertically\n    return image

# ----------------- SimpleGUI Image Wrapper -----------------
from collections import OrderedDict
_dummy = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")
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
def update_wrapped_image():
    global wrapped_image
    image_data = read_rendered_texture()
    surf = pygame.surfarray.make_surface(np.transpose(image_data, (1, 0, 2)))
    wrapped_image = SimpleGUIImageWrapper(surf)

# ----------------- Draw Handler for SimpleGUI -----------------
def draw(canvas: simplegui.Canvas):
    startTime = time.time()
    render_to_texture()
    update_wrapped_image()
    if wrapped_image:
        canvas.draw_image(wrapped_image,
                          wrapped_image.center,
                          wrapped_image.size,
                          (canvas_width / 2, canvas_height / 2),
                          wrapped_image.size)
    else:
        canvas.draw_text("Rendering...", (canvas_width // 2 - 50, canvas_height // 2), 20, "White")
        endTime = time.time()
        print("Frame rate:", 1 / (endTime - startTime))

# ----------------- SimpleGUI Frame Setup -----------------
frame = simplegui.create_frame("OpenGL Shader Texture Mapping", canvas_width, canvas_height, 0)
frame.set_draw_handler(draw)

# Remove extra UI elements.
frame._hide_controlpanel = True
frame._canvas_border_size = 0
frame._canvas_x_offset = 0
frame._canvas_y_offset = 0
frame._border_size = 0

# Setup pygame display (if needed)
frame._pygame_surface = pygame.display.set_mode((canvas_width, canvas_height), simplegui.Frame._pygame_mode_flags, simplegui.Frame._pygame_mode_depth)
frame.start()
