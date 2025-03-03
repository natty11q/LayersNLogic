# pip install SimpleGUICS2Pygame Pillow numpy numba pygame


try:
    import simplegui  # type: ignore
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from PIL import Image
import numpy as np
from numba import cuda
import math
import pygame  # We’ll use pygame.surfarray to create a surface from our NumPy array

# -------- Configuration and Setup --------

# Load the texture image with PIL and convert to a NumPy array.
image_path = "/Users/nathanielfrimpong-santeng/codestuffs/RHUL/Software Eng/pythonProjects/GroupPythonGame/LayersNLogic/testing/testAssets/grid.png"  # update with your local absolute path

img = Image.open(image_path)
img = img.resize((300, 300))
tex_np = np.array(img.convert("RGB"), dtype=np.uint8)
tex_height, tex_width, _ = tex_np.shape

# Canvas dimensions
canvas_width, canvas_height = 600, 400

# Create an output buffer (canvas) as a NumPy array (initialized to black).
output_buffer = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)

# Define the quad (polygon) vertices and corresponding UV coordinates.
# Vertices are given as (x, y) coordinates.
polygon_vertices = np.array([[200, 100],
                             [400, 100],
                             [350, 300],
                             [250, 300]], dtype=np.float32)

# UV coordinates for each vertex (range 0 to 1)
uv_coords = np.array([[0, 0],
                      [1, 0],
                      [1, 1],
                      [0, 1]], dtype=np.float32)

# Split the quad into two triangles:
# Triangle 1: vertices 0,1,2 and Triangle 2: vertices 0,2,3.
triangles = [polygon_vertices[[0, 1, 2]], polygon_vertices[[0, 2, 3]]]
uv_triangles = [uv_coords[[0, 1, 2]], uv_coords[[0, 2, 3]]]

# -------- GPU Kernel Definition --------

@cuda.jit
def map_triangle_kernel(output, triangle, uv_triangle, tex, tex_width, tex_height, min_x, min_y):
    """
    For each pixel in the bounding box of the triangle,
    compute barycentric coordinates. If the point is inside the triangle,
    interpolate UV coordinates and write the corresponding texture color to the output.
    """
    i = cuda.threadIdx.x + cuda.blockIdx.x * cuda.blockDim.x #type: ignore
    j = cuda.threadIdx.y + cuda.blockIdx.y * cuda.blockDim.y #type: ignore

    # Map thread indices to canvas coordinates
    x = min_x + i
    y = min_y + j

    # Check bounds
    if x >= output.shape[1] or y >= output.shape[0]:
        return

    # Read triangle vertices.
    v0x = triangle[0, 0]; v0y = triangle[0, 1]
    v1x = triangle[1, 0]; v1y = triangle[1, 1]
    v2x = triangle[2, 0]; v2y = triangle[2, 1]

    # Compute denominator of barycentric coordinates.
    denom = (v1y - v2y) * (v0x - v2x) + (v2x - v1x) * (v0y - v2y)
    if denom == 0:
        return

    # Compute barycentrics.
    w0 = ((v1y - v2y) * (x - v2x) + (v2x - v1x) * (y - v2y)) / denom
    w1 = ((v2y - v0y) * (x - v2x) + (v0x - v2x) * (y - v2y)) / denom
    w2 = 1.0 - w0 - w1

    # Check if (x,y) is inside the triangle.
    if w0 < 0 or w1 < 0 or w2 < 0:
        return

    # Interpolate UV coordinates.
    u = w0 * uv_triangle[0, 0] + w1 * uv_triangle[1, 0] + w2 * uv_triangle[2, 0]
    v = w0 * uv_triangle[0, 1] + w1 * uv_triangle[1, 1] + w2 * uv_triangle[2, 1]

    # Map UV to texture pixel coordinates.
    tex_x = int(u * (tex_width - 1))
    tex_y = int(v * (tex_height - 1))

    # Fetch color from texture.
    r = tex[tex_y, tex_x, 0]
    g = tex[tex_y, tex_x, 1]
    b = tex[tex_y, tex_x, 2]

    # Write the color to the output buffer.
    output[y, x, 0] = r
    output[y, x, 1] = g
    output[y, x, 2] = b

# -------- CPU Helper Function to Launch Kernel --------

def process_triangle(triangle, uv_triangle):
    # Compute the bounding box of the triangle.
    min_x = int(np.min(triangle[:, 0]))
    max_x = int(np.max(triangle[:, 0]))
    min_y = int(np.min(triangle[:, 1]))
    max_y = int(np.max(triangle[:, 1]))
    width = max_x - min_x
    height = max_y - min_y

    # Define CUDA block and grid sizes.
    blockdim = (16, 16)
    griddim = (math.ceil(width / blockdim[0]), math.ceil(height / blockdim[1]))

    # Launch the kernel.
    map_triangle_kernel[griddim, blockdim](output_buffer, triangle, uv_triangle, tex_np, tex_width, tex_height, min_x, min_y) #type: ignore

# Process each triangle on the GPU.
for tri, uv_tri in zip(triangles, uv_triangles):
    process_triangle(tri, uv_tri)

# Convert the output buffer (NumPy array) into a pygame surface.
# Note: pygame.surfarray.make_surface expects the array shape (width, height, channels),
# so we transpose the output buffer.
output_surface = pygame.surfarray.make_surface(np.transpose(output_buffer, (1, 0, 2)))

# -------- Draw Handler --------

def draw(canvas):
    # Draw the textured quad (as produced in output_surface) onto the canvas.
    # We position it at the center of the canvas.
    canvas.draw_image(output_surface,
                      (output_surface.get_width()/2, output_surface.get_height()/2),
                      (output_surface.get_width(), output_surface.get_height()),
                      (canvas_width/2, canvas_height/2),
                      (output_surface.get_width(), output_surface.get_height()))
    # Also draw the polygon outline for reference.
    for i in range(len(polygon_vertices)):
        v1 = polygon_vertices[i]
        v2 = polygon_vertices[(i + 1) % len(polygon_vertices)]
        canvas.draw_line((v1[0], v1[1]), (v2[0], v2[1]), 2, "White")

# -------- Create Frame and Run --------

frame = simplegui.create_frame("GPU Accelerated UV Mapping", canvas_width, canvas_height)
frame.set_draw_handler(draw)
frame.start()
