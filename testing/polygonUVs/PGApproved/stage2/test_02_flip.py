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
from collections import OrderedDict

# Canvas dimensions
canvas_width, canvas_height = 900, 600

# Global variables for OpenGL objects
shader_program = None
vao = None
fbo = None
fbo_texture = None
wrapped_image = None

pygame.init()
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)


def init_gl():
    """Initializes shaders, buffers, and the FBO."""
    global shader_program, vao, fbo, fbo_texture

    # Create shaders
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
        // color = vec4(fragColor, 1.0);
        color = vec4(1.0, 0.0, 0.5, 1.0);
    }
    """

    # Define triangle vertices: each vertex has (x, y, r, g, b)
    vertices = np.array([
        -0.8, -0.8,  1.0, 0.0, 0.0,  # Bottom-left, red
         0.8, -0.8,  0.0, 1.0, 0.0,  # Bottom-right, green
         0.0,  0.8,  0.0, 0.0, 1.0   # Top, blue
    ], dtype=np.float32)

    # Create Vertex Array Object and Vertex Buffer Object.
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    shader_program = compileProgram(compileShader(vertex_shader_source, GL_VERTEX_SHADER),
                                    compileShader(fragment_shader_source, GL_FRAGMENT_SHADER))

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    # Attribute 0: vertex position (2 floats)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 5 * vertices.itemsize, ctypes.c_void_p(0))
    # Attribute 1: vertex colour (3 floats)
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 5 * vertices.itemsize,
                          ctypes.c_void_p(2 * vertices.itemsize))

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    # Create the FBO and its attached texture.
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

def render_to_fbo():
    """Renders the triangle to the offscreen framebuffer."""
    glBindFramebuffer(GL_FRAMEBUFFER, fbo)
    glViewport(0, 0, canvas_width, canvas_height)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    glBindVertexArray(vao)
    glUseProgram(shader_program)
    glDrawArrays(GL_TRIANGLES, 0, 3)
    glBindVertexArray(0)
    glUseProgram(0)
    glFinish()

    glBindFramebuffer(GL_FRAMEBUFFER, 0)


# --- SimpleGUI Image Wrapper ---
# SimpleGUICS2Pygame's draw_image expects an image-like object with attributes "center" and "size".
_dummy = simplegui.load_image("")
DummyImage = type(_dummy)
class SimpleGUIImageWrapper(DummyImage):
    def __init__(self, surface):
        self._pygame_surface = surface
        self.center = (surface.get_width() / 2, surface.get_height() / 2)
        self.size = (surface.get_width(), surface.get_height())
        self._pygamesurfaces_cached = OrderedDict()
        self._pygamesurfaces_cached_clear = lambda: self._pygamesurfaces_cached.clear()
        self._pygamesurfaces_cache_max_size = getattr(_dummy, "_pygamesurfaces_cache_default_max_size", 50)
        self._draw_count = 0



def update_wrapped_image():
    """Reads the FBO contents and wraps it in a SimpleGUI-compatible image."""
    global wrapped_image, fbo
    # Bind the FBO and read its pixels
    glBindFramebuffer(GL_FRAMEBUFFER, fbo)
    # Read pixels in GL_RGB format as unsigned bytes.

    glViewport(0, 0, canvas_width, canvas_height)
    data = glReadPixels(0, 0, canvas_width, canvas_height, GL_RGB, GL_UNSIGNED_BYTE)

    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    # Convert to a NumPy array then reshape to image dimensions
    image_array = np.frombuffer(data, dtype=np.uint8).reshape(canvas_height, canvas_width, 3)
    # OpenGL's origin is bottom-left, so flip vertically.
    image_array = np.flipud(image_array)
    # Create a pygame surface; note pygame expects (width, height, channels)
    surf = pygame.surfarray.make_surface(np.transpose(image_array, (1, 0, 2)))
    wrapped_image = SimpleGUIImageWrapper(surf)


# --- Draw Handler ---
def draw(canvas: simplegui.Canvas):
    start_time = time.time()
    # Render the triangle to the FBO via OpenGL
    render_to_fbo()
    # Update our image wrapper with the new frame
    update_wrapped_image()
    # Draw the rendered image onto the SimpleGUI canvas
    if wrapped_image:
        canvas._background_pygame_color = pygame.Color(255, 0 , 0)

        canvas.draw_image(wrapped_image,
                          wrapped_image.center,
                          wrapped_image.size,
                          (canvas_width / 2, canvas_height / 2),
                          wrapped_image.size)
    else:
        canvas.draw_text("Rendering...", (canvas_width // 2 - 50, canvas_height // 2), 20, "White")
    # Optionally, print frame timing
    # print("Frame rate:", 1 / (time.time() - start_time))

# --- SimpleGUI Frame Setup ---
frame = simplegui.create_frame("OpenGL FBO Rendering", canvas_width, canvas_height, 0)
frame.set_draw_handler(draw)

# Remove extra UI elements.
frame._hide_controlpanel = True
frame._canvas_border_size = 0
frame._canvas_x_offset = 0
frame._canvas_y_offset = 0
frame._border_size = 0

# # Set the pygame display mode with OpenGL and double buffering.
# pygame.display.set_mode((int(frame._canvas_x_offset + canvas_width + frame._canvas_border_size + frame._border_size),
#                         int(frame._canvas_y_offset + canvas_height + frame._canvas_border_size + frame._border_size)),
#                         simplegui.Frame._pygame_mode_flags | pygame.OPENGL | pygame.DOUBLEBUF,
#                         simplegui.Frame._pygame_mode_depth, vsync=1)
pygame.display.set_mode((canvas_width, canvas_height),
                        simplegui.Frame._pygame_mode_flags | pygame.OPENGL | pygame.DOUBLEBUF,
                        simplegui.Frame._pygame_mode_depth, vsync=1)

frame._pygame_surface = pygame.display.get_surface()

def opengl_update(rect=None):
    pygame.display.flip()

pygame.display.update = opengl_update


# Initialize our OpenGL objects (after the context is created).

init_gl()

frame.start()
