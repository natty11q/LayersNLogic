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
    fragColor = vec4(fragColor, 1.0);
}
"""

def create_shader_program():
    vs = compileShader(vertex_shader_source, GL_VERTEX_SHADER)
    fs = compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)
    program = compileProgram(vs, fs)
    
    if not glGetProgramiv(program, GL_LINK_STATUS):
        print("Shader program linking failed!")
        print(glGetProgramInfoLog(program).decode())
    
    return program

# ----------------- VAO & Buffer Setup -----------------
quad_vertices = np.array([
    -1.0, -1.0,   0.0,  0.0,   
     1.0, -1.0,   1.0,  0.0,   
     1.0,  1.0,   1.0,  1.0,   
    -1.0,  1.0,   0.0,  1.0    
], dtype=np.float32)

quad_indices = np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32)

vao = glGenVertexArrays(1)
glBindVertexArray(vao)

vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, quad_vertices.nbytes, quad_vertices, GL_STATIC_DRAW)

ebo = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, quad_indices.nbytes, quad_indices, GL_STATIC_DRAW)

shader_program = create_shader_program()

pos_loc = glGetAttribLocation(shader_program, "position")
glEnableVertexAttribArray(pos_loc)
glVertexAttribPointer(pos_loc, 2, GL_FLOAT, GL_FALSE, 4 * quad_vertices.itemsize, ctypes.c_void_p(0))

tex_loc = glGetAttribLocation(shader_program, "texCoord")
glEnableVertexAttribArray(tex_loc)
glVertexAttribPointer(tex_loc, 2, GL_FLOAT, GL_FALSE, 4 * quad_vertices.itemsize, ctypes.c_void_p(2 * quad_vertices.itemsize))

glBindVertexArray(0)

# ----------------- Texture Setup -----------------
image_path = "/Users/nathanielfrimpong-santeng/codestuffs/RHUL/Software Eng/pythonProjects/GroupPythonGame/LayersNLogic/testing/testAssets/goik.png"
img = Image.open(image_path)
tex_np = np.array(img.convert("RGB"), dtype=np.uint8)
tex_height, tex_width, _ = tex_np.shape

texture_id = glGenTextures(1)
if texture_id == 0:
    print("Failed to generate texture!")

glBindTexture(GL_TEXTURE_2D, texture_id)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, tex_width, tex_height, 0, GL_RGB, GL_UNSIGNED_BYTE, tex_np)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
glGenerateMipmap(GL_TEXTURE_2D)
glBindTexture(GL_TEXTURE_2D, 0)

# ----------------- Framebuffer Setup -----------------
fbo = glGenFramebuffers(1)
glBindFramebuffer(GL_FRAMEBUFFER, fbo)
render_texture = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, render_texture)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, canvas_width, canvas_height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, render_texture, 0)

glBindFramebuffer(GL_FRAMEBUFFER, 0)

# ----------------- Rendering Functions -----------------
def render_offscreen():
    global fbo, vao, shader_program, texture_id
    glBindFramebuffer(GL_FRAMEBUFFER, fbo)
    glViewport(0, 0, canvas_width, canvas_height)
    glClearColor(0.5, 0, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT)
    glUseProgram(shader_program)
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBindVertexArray(vao)
    glDrawElements(GL_TRIANGLES, len(quad_indices), GL_UNSIGNED_INT, None)
    glBindVertexArray(0)
    glBindTexture(GL_TEXTURE_2D, 0)
    glUseProgram(0)
    glFinish()
    glBindFramebuffer(GL_FRAMEBUFFER, 0)

def read_offscreen():
    # image = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)
    glBindFramebuffer(GL_FRAMEBUFFER, fbo)
    pixels = glReadPixels(0, 0, canvas_width, canvas_height, GL_RGB, GL_UNSIGNED_BYTE)
    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    image = np.frombuffer(pixels, dtype=np.uint8).reshape((canvas_height, canvas_width, 3))
    image = np.flipud(image)
    return image

# Test function
def test_framebuffer():
    render_offscreen()
    image = read_offscreen()

    print("Framebuffer test - Mean color:", np.mean(image, axis=(0, 1)))

test_framebuffer()

def run_framebuffer_test():
    print("Running framebuffer test...")
    render_offscreen()
    img = read_offscreen()
    test_pixel = img[canvas_height // 2, canvas_width // 2]
    expected_color = np.array([255, 0, 0], dtype=np.uint8)
    assert np.array_equal(test_pixel, expected_color), f"Framebuffer test failed: {test_pixel} != {expected_color}"
    print("Framebuffer test passed!")

# ----------------- SimpleGUI Integration -----------------
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
    surf = pygame.surfarray.make_surface(np.transpose(img_data, (1, 0, 2)))
    wrapped_image = SimpleGUIImageWrapper(surf)

def draw(canvas: simplegui.Canvas):
    global wrapped_image
    render_offscreen()
    update_image_wrapper()
    if wrapped_image:
        canvas.draw_image(wrapped_image,
                          wrapped_image.center,
                          wrapped_image.size,
                          (canvas_width/2, canvas_height/2), wrapped_image.size)
    else:
        canvas.draw_text("Rendering...", (canvas_width//2-50, canvas_height//2), 20, "White")

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



pygame.quit()
