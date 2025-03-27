import pyopencl as cl
import numpy as np
from PIL import Image
import math, threading, time
import pygame
try:
    import simplegui  # type: ignore
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


import os
os.environ["PYOPENCL_CTX"] = "0"

# ----------------- Configuration & Texture Loading -----------------

# Load the image with Pillow and convert to RGB NumPy array.
image_path = "/Users/nathanielfrimpong-santeng/codestuffs/RHUL/Software Eng/pythonProjects/GroupPythonGame/LayersNLogic/testing/testAssets/testImage3.png"

imageLinks = os.listdir(os.path.abspath("/Users/nathanielfrimpong-santeng/codestuffs/RHUL/Software Eng/pythonProjects/GroupPythonGame/LayersNLogic/testing/testAssets"))



img = Image.open(image_path)
# (Optionally resize if needed)
img = img.resize((300,300))
tex_np = np.array(img.convert("RGB"), dtype=np.uint8)
tex_height, tex_width, _ = tex_np.shape

# ----------------- Canvas & Polygon Setup -----------------

# Canvas dimensions
canvas_width, canvas_height = int(900), int(600)

# Define polygon vertices and corresponding UV coordinates.
# (For this example we use a quad split into two triangles.)
polygon_vertices = [
    (canvas_width * 0.25, canvas_height * 0.25),
    (canvas_width * 0.75, canvas_height * 0.25),
    (canvas_width * 0.75, canvas_height * 0.75),
    (canvas_width * 0.25, canvas_height * 0.75)
]
uv_coords = [(0, 0), (1, 0), (1, 1), (0, 1)]

# Split the quad into two triangles.
triangles = [
    ((polygon_vertices[0][0] + 100,polygon_vertices[0][1] + 100), (polygon_vertices[1][0] + 100,polygon_vertices[1][1] - 200), (polygon_vertices[2][0] + 100,polygon_vertices[2][1] + 100)),
    (polygon_vertices[0], polygon_vertices[2], (polygon_vertices[3][0] - 400,polygon_vertices[3][1] + 100),),
]
uv_triangles = [
    (uv_coords[0], uv_coords[1], uv_coords[2]),
    (uv_coords[0], uv_coords[2], uv_coords[3])
]

# We'll compute the texture mapping only over the polygon area.
# For simplicity, we allocate an output buffer equal to the canvas size.
# Pixels not inside the polygon will remain black.
output_buffer = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)

# ----------------- PyOpenCL Setup -----------------

# Create a PyOpenCL context and command queue.
ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

mf = cl.mem_flags
# Create a buffer for the texture (read-only).
tex_cl = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=tex_np)
# Create a buffer for the output image.
output_cl = cl.Buffer(ctx, mf.WRITE_ONLY, output_buffer.nbytes)

# We'll process each triangle separately.
# We'll pack triangle and UV data as flat float32 arrays.
def flatten_triangle(tri):
    return np.array([coord for vertex in tri for coord in vertex], dtype=np.float32)

def flatten_uv(uv_tri):
    return np.array([coord for uv in uv_tri for coord in uv], dtype=np.float32)

# ----------------- OpenCL Kernel -----------------

kernel_code = """
__kernel void map_triangle(
    __global uchar *output,
    __global const uchar *tex,
    __global const float *triangle,
    __global const float *uv_triangle,
    const int tex_width,
    const int tex_height,
    const int canvas_width,
    const int min_x,
    const int min_y,
    const int bbox_width,
    const int bbox_height)
{
    int i = get_global_id(0);
    int j = get_global_id(1);
    
    if(i >= bbox_width || j >= bbox_height)
        return;
        
    int x = min_x + i;
    int y = min_y + j;
    
    // Read triangle vertices.
    float v0x = triangle[0]; float v0y = triangle[1];
    float v1x = triangle[2]; float v1y = triangle[3];
    float v2x = triangle[4]; float v2y = triangle[5];
    
    // Compute barycentric coordinates denominator.
    float denom = (v1y - v2y) * (v0x - v2x) + (v2x - v1x) * (v0y - v2y);
    if (denom == 0.0f) return;
    
    float w0 = ((v1y - v2y) * (x - v2x) + (v2x - v1x) * (y - v2y)) / denom;
    float w1 = ((v2y - v0y) * (x - v2x) + (v0x - v2x) * (y - v2y)) / denom;
    float w2 = 1.0f - w0 - w1;
    
    // Check if (x, y) is inside the triangle.
    if(w0 < 0.0f || w1 < 0.0f || w2 < 0.0f)
        return;
    
    // Load UV coordinates for vertices.
    float uv0u = uv_triangle[0]; float uv0v = uv_triangle[1];
    float uv1u = uv_triangle[2]; float uv1v = uv_triangle[3];
    float uv2u = uv_triangle[4]; float uv2v = uv_triangle[5];
    
    // Interpolate UV.
    float u = w0 * uv0u + w1 * uv1u + w2 * uv2u;
    float v = w0 * uv0v + w1 * uv1v + w2 * uv2v;
    
    // Map UV to texture pixel coordinates.
    int tex_x = (int)(u * (tex_width - 1));
    int tex_y = (int)(v * (tex_height - 1));
    
    int tex_index = (tex_y * tex_width + tex_x) * 3;
    uchar r = tex[tex_index];
    uchar g = tex[tex_index + 1];
    uchar b = tex[tex_index + 2];
    
    // Write to output buffer.
    int out_index = (y * canvas_width + x) * 3;
    output[out_index] = r;
    output[out_index + 1] = g;
    output[out_index + 2] = b;
}
"""

prg = cl.Program(ctx, kernel_code).build()


def process_triangle(triangle, uv_triangle):
    # Compute the bounding box of the triangle.
    xs = [v[0] for v in triangle]
    ys = [v[1] for v in triangle]
    min_x = int(min(xs))
    max_x = int(max(xs))
    min_y = int(min(ys))
    max_y = int(max(ys))
    bbox_width = max_x - min_x
    bbox_height = max_y - min_y
    
    # Flatten triangle and UV data.
    tri_flat = flatten_triangle(triangle)
    uv_flat = flatten_uv(uv_triangle)
    
    triangle_cl = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=tri_flat)
    uv_triangle_cl = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=uv_flat)
    
    # Define workgroup size and global size.
    local_size = (16, 16)
    global_size = (math.ceil(bbox_width / local_size[0]) * local_size[0],
                   math.ceil(bbox_height / local_size[1]) * local_size[1])
    
    prg.map_triangle(queue, global_size, local_size,
                     output_cl, tex_cl, triangle_cl, uv_triangle_cl,
                     np.int32(tex_width), np.int32(tex_height),
                     np.int32(canvas_width),
                     np.int32(min_x), np.int32(min_y),
                     np.int32(bbox_width), np.int32(bbox_height))
    
# Run GPU computation for both triangles in a background thread.
def gpu_compute_texture():
    # Clear output buffer to black.
    global output_buffer
    output_buffer[:] = 0
    for tri, uv_tri in zip(triangles, uv_triangles):
        process_triangle(tri, uv_tri)
    # Copy the GPU buffer back to the output_buffer NumPy array.
    cl.enqueue_copy(queue, output_buffer, output_cl)
    queue.finish()
    # Signal that GPU computation is complete.
    global gpuReady
    gpuReady = True

gpuReady = False
gpu_thread = threading.Thread(target=gpu_compute_texture)
# gpu_thread.start()

# ----------------- SimpleGUI Image Wrapper -----------------

# SimpleGUICS2Pygame's draw_image expects an object of type Image.
# Since we have a pygame.Surface, we wrap it in a minimal class that provides
# the attributes "center" and "size". This is an unconventional workaround.
# Create a dummy image so we can get the expected type.
# Create a dummy image so we can get the expected base type.
from collections import OrderedDict

# Create a dummy image so we can get the expected base type and defaults.
_dummy = simplegui.load_image("")
DummyImage = type(_dummy)

class SimpleGUIImageWrapper(DummyImage): #type: ignore
    def __init__(self, surface):
        self._pygame_surface = surface
        self.center = (surface.get_width() / 2, surface.get_height() / 2)
        self.size = (surface.get_width(), surface.get_height())
        # Use an OrderedDict to mimic the caching structure.
        self._pygamesurfaces_cached = OrderedDict()
        self._pygamesurfaces_cached_clear = lambda: self._pygamesurfaces_cached.clear()
        # Set the cache max size from the dummy image, if available.
        self._pygamesurfaces_cache_max_size = getattr(_dummy, "_pygamesurfaces_cache_default_max_size", 50)
        # Add the _draw_count attribute required by draw_image.
        self._draw_count = 0



# Initially, our wrapped image is empty.
wrapped_image = None

def update_wrapped_image():
    global wrapped_image
    # pygame.surfarray.make_surface expects an array with shape (width, height, channels),
    # so we need to transpose our output_buffer.
    print(output_buffer)
    input()
    surf = pygame.surfarray.make_surface(np.transpose(output_buffer, (1, 0, 2)))
    wrapped_image = SimpleGUIImageWrapper(surf)

# ----------------- Draw Handler -----------------

switchTimer = 2
switchTimerMax = 10
frames = 0


imgID = 0

def draw(canvas: simplegui.Canvas):
    global switchTimer, switchTimerMax,imgID, img, triangles, output_buffer, tex_height, tex_width, tex_np, output_cl, tex_cl

    gpu_compute_texture()
    startTime = time.time()


    triangles = [
        ((polygon_vertices[0][0] + 100,polygon_vertices[0][1] + (200 * math.sin(frames / 20))), (polygon_vertices[1][0] + 100,polygon_vertices[1][1] - 200), (polygon_vertices[2][0] + 100,polygon_vertices[2][1] + 100)),
        (polygon_vertices[0], polygon_vertices[2], (polygon_vertices[3][0] - 400,polygon_vertices[3][1] + 100),),
    ]



    
    switchTimer -= 1
    print("st : ", switchTimer)
    if switchTimer == 0:
        imgID = (imgID + 1) % (len(imageLinks) - 1)
        switchTimer= switchTimerMax
        img = Image.open(os.path.abspath("testing/testAssets/" + imageLinks[imgID]))
        print("img : ", imageLinks[imgID])
        # (Optionally resize if needed)
        # img = img.resize((300,300))
        tex_np = np.array(img.convert("RGB"), dtype=np.uint8)
        tex_height, tex_width, _ = tex_np.shape

        output_buffer = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)

        tex_cl = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=tex_np)
        # Create a buffer for the output image.
        output_cl = cl.Buffer(ctx, mf.WRITE_ONLY, output_buffer.nbytes)

        # print(output_buffer)


    # Draw polygon outline.
    for i in range(len(polygon_vertices)):
        v1 = polygon_vertices[i]
        v2 = polygon_vertices[(i + 1) % len(polygon_vertices)]
        canvas.draw_line(v1, v2, 2, "White")
    
    # Once GPU computation is ready, update the wrapped image and draw it.
    if gpuReady:
        update_wrapped_image()
        if wrapped_image:
            canvas.draw_image(wrapped_image,
                              wrapped_image.center,
                              wrapped_image.size,
                              (canvas_width / 2, canvas_height / 2),
                              wrapped_image.size)
    else:
        canvas.draw_text("Computing texture on GPU...", (canvas_width // 2 - 100, canvas_height // 2), 20, "White")
    
    endTime = time.time()
    print("Frame rate:", 1 / (endTime - startTime))

# ----------------- SimpleGUI Frame Setup -----------------

frame = simplegui.create_frame("GPU-Accelerated UV Mapping", canvas_width, canvas_height, 0)
frame.set_draw_handler(draw)

# Remove extra UI elements.
frame._hide_controlpanel = True
frame._canvas_border_size = 0
frame._canvas_x_offset = 0
frame._canvas_y_offset = 0
frame._border_size = 0

# (Optional) Set pygame display to borderless if supported.
import pygame
frame._pygame_surface = pygame.display.set_mode(
    (int(frame._canvas_x_offset + canvas_width + frame._canvas_border_size + frame._border_size),
     int(frame._canvas_y_offset + canvas_height + frame._canvas_border_size + frame._border_size)),
    simplegui.Frame._pygame_mode_flags,
    simplegui.Frame._pygame_mode_depth)

frame.start()
