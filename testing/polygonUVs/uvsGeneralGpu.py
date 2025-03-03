import pyopencl as cl
import numpy as np
from PIL import Image
import math
import pygame
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# -------- Load and Prepare Texture --------

image_path = "/Users/nathanielfrimpong-santeng/codestuffs/RHUL/Software Eng/pythonProjects/GroupPythonGame/LayersNLogic/testing/testAssets/testImage3.png"
img = Image.open(image_path)
img = img.resize((300, 300))
tex_np = np.array(img.convert("RGB"), dtype=np.uint8)
tex_height, tex_width, _ = tex_np.shape

# -------- Canvas and Output Buffer --------

canvas_width, canvas_height = 600, 400
# Output buffer: shape (canvas_height, canvas_width, 3)
output_buffer = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)

# -------- Define Triangle and UV Coordinates --------

# For demonstration, we work with a single triangle from a split quad.
# Triangle vertices (x, y)
triangle = np.array([[200, 100],
                     [400, 100],
                     [350, 300]], dtype=np.float32)
# Corresponding UV coordinates (range 0 to 1)
uv_triangle = np.array([[0, 0],
                        [1, 0],
                        [1, 1]], dtype=np.float32)

# Compute the bounding box of the triangle.
min_x = int(np.min(triangle[:, 0]))
max_x = int(np.max(triangle[:, 0]))
min_y = int(np.min(triangle[:, 1]))
max_y = int(np.max(triangle[:, 1]))
bbox_width = max_x - min_x
bbox_height = max_y - min_y

# Flatten the triangle and uv arrays for OpenCL.
triangle_flat = triangle.flatten().astype(np.float32)
uv_triangle_flat = uv_triangle.flatten().astype(np.float32)

# -------- Setup PyOpenCL --------

# Create a context and command queue.
ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

mf = cl.mem_flags
tex_cl = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=tex_np)
output_cl = cl.Buffer(ctx, mf.WRITE_ONLY, output_buffer.nbytes)
triangle_cl = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=triangle_flat)
uv_triangle_cl = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=uv_triangle_flat)

# -------- OpenCL Kernel Code --------

kernel_code = """
__kernel void map_triangle(
    __global uchar *output,
    __global const uchar *tex,
    __global const float *triangle,
    __global const float *uv_triangle,
    int tex_width,
    int tex_height,
    int canvas_width,
    int min_x,
    int min_y,
    int bbox_width,
    int bbox_height)
{
    int i = get_global_id(0);
    int j = get_global_id(1);
    
    if (i >= bbox_width || j >= bbox_height)
        return;
        
    int x = min_x + i;
    int y = min_y + j;
    
    // Load triangle vertices: each vertex has (x, y)
    float v0x = triangle[0]; float v0y = triangle[1];
    float v1x = triangle[2]; float v1y = triangle[3];
    float v2x = triangle[4]; float v2y = triangle[5];
    
    // Compute barycentric coordinates denominator.
    float denom = (v1y - v2y) * (v0x - v2x) + (v2x - v1x) * (v0y - v2y);
    if (denom == 0.0f) return;
    
    float w0 = ((v1y - v2y) * (x - v2x) + (v2x - v1x) * (y - v2y)) / denom;
    float w1 = ((v2y - v0y) * (x - v2x) + (v0x - v2x) * (y - v2y)) / denom;
    float w2 = 1.0f - w0 - w1;
    
    // Check if point (x, y) is inside the triangle.
    if (w0 < 0.0f || w1 < 0.0f || w2 < 0.0f) return;
    
    // Load uv coordinates for vertices.
    float uv0u = uv_triangle[0]; float uv0v = uv_triangle[1];
    float uv1u = uv_triangle[2]; float uv1v = uv_triangle[3];
    float uv2u = uv_triangle[4]; float uv2v = uv_triangle[5];
    
    // Interpolate UV coordinates.
    float u = w0 * uv0u + w1 * uv1u + w2 * uv2u;
    float v = w0 * uv0v + w1 * uv1v + w2 * uv2v;
    
    // Map UV to texture coordinates.
    int tex_x = (int)(u * (tex_width - 1));
    int tex_y = (int)(v * (tex_height - 1));
    
    int tex_index = (tex_y * tex_width + tex_x) * 3;
    uchar r = tex[tex_index];
    uchar g = tex[tex_index + 1];
    uchar b = tex[tex_index + 2];
    
    // Write the color to the output buffer.
    int out_index = (y * canvas_width + x) * 3;
    output[out_index] = r;
    output[out_index + 1] = g;
    output[out_index + 2] = b;
}
"""

prg = cl.Program(ctx, kernel_code).build()

# -------- Execute the Kernel --------

global_size = (bbox_width, bbox_height)
prg.map_triangle(queue, global_size, None,
                 output_cl, tex_cl, triangle_cl, uv_triangle_cl,
                 np.int32(tex_width), np.int32(tex_height),
                 np.int32(canvas_width),
                 np.int32(min_x), np.int32(min_y),
                 np.int32(bbox_width), np.int32(bbox_height))

# Copy the results back to output_buffer.
cl.enqueue_copy(queue, output_buffer, output_cl)
queue.finish()

# -------- Create Pygame Surface from Output Buffer --------

# pygame.surfarray.make_surface expects (width, height, channels), so transpose the array.
output_surface = pygame.surfarray.make_surface(np.transpose(output_buffer, (1, 0, 2)))

ImageType = None #type: ignore
for key, val in simplegui.__dict__.items():
    if key.lower() == "image" and isinstance(val, type):
        ImageType = val
        break

# If not found, create a dummy base class.
if ImageType is None:
    class ImageType:
        pass

# Create a wrapper that satisfies the expected interface.
class MyImageWrapper(ImageType): #type: ignore
    def __init__(self, surface):
        # Store the pygame.Surface (from your GPU code, for example)
        self._pygame_surface = surface
        self.center = (surface.get_width() / 2, surface.get_height() / 2)
        self.size = (surface.get_width(), surface.get_height())


# Wrap your pygame surface:
wrapped_image = MyImageWrapper(
    output_surface
)

# -------- SimpleGUI Draw Handler --------

def draw(canvas):
    # Draw the output surface (the textured triangle) onto the canvas.
    canvas.draw_image(
        wrapped_image,
        (wrapped_image.center[0], wrapped_image.center[1]),
        (wrapped_image.size[0], wrapped_image.size[1]),
        (canvas_width/2, canvas_height/2),
        (wrapped_image.size[0], wrapped_image.size[1])
    )
    # Optionally, draw triangle outlines for debugging.
    pts = [(200, 100), (400, 100), (350, 300)]
    for i in range(len(pts)):
        canvas.draw_line(pts[i], pts[(i + 1) % len(pts)], 2, "White")

frame = simplegui.create_frame("PyOpenCL UV Mapping", canvas_width, canvas_height)
frame.set_draw_handler(draw)
frame.start()
