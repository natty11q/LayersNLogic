try:
    import simplegui  # type: ignore
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from PIL import Image
import time

from numba import njit, prange
import numpy as np


# Load an image
image_path = "/Users/nathanielfrimpong-santeng/codestuffs/RHUL/Software Eng/pythonProjects/GroupPythonGame/LayersNLogic/testing/testAssets/testImage3.png"
# image_path = "/Users/nathanielfrimpong-santeng/codestuffs/RHUL/Software Eng/pythonProjects/GroupPythonGame/LayersNLogic/testing/testAssets/lowResTest.png"
img = Image.open(image_path)

# Resize image if needed
# img = img.resize((300, 300))
image_data = img.convert("RGB")

# imgw, imgh = (img.width/ 1.5, img.height/ 1.5)
imgPos = (0, 0)
# Canvas size
canvas_width, canvas_height = 900 * 1.3, 600 * 1.3
imgw, imgh = (canvas_width, canvas_height)

# Polygon vertices and UV coordinates
polygon_vertices = [ imgPos, (imgw, imgPos[1]), (imgw, imgh), (imgPos[0], imgh) ]
uv_coords = [(0, 0), (1, 0), (1, 1), (0, 1)]

# Split polygon into two triangles
triangles = [
    (polygon_vertices[0], polygon_vertices[1], polygon_vertices[2]),
    (polygon_vertices[0], polygon_vertices[2], polygon_vertices[3]),
]

uv_triangles = [
    (uv_coords[0], uv_coords[1], uv_coords[2]),
    (uv_coords[0], uv_coords[2], uv_coords[3]),
]


def get_color_from_uv(u, v):
    """Get pixel color from UV coordinates."""
    x = int(u * (img.width - 1))
    y = int(v * (img.height - 1))
    pixelCol = image_data.getpixel((x, y))

    r, g, b = (10, 10, 10)
    if isinstance(pixelCol, tuple):
        r, g, b = pixelCol
    return f"rgb({r},{g},{b})"


def barycentric_coords(p, a, b, c):
    """Compute barycentric coordinates for point p inside triangle (a, b, c)."""
    detT = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
    alpha = ((b[1] - c[1]) * (p[0] - c[0]) + (c[0] - b[0]) * (p[1] - c[1])) / detT
    beta = ((c[1] - a[1]) * (p[0] - c[0]) + (a[0] - c[0]) * (p[1] - c[1])) / detT
    gamma = 1 - alpha - beta
    return alpha, beta, gamma


def is_point_in_triangle(alpha, beta, gamma):
    """Check if a point is inside the triangle using barycentric coords."""
    return 0 <= alpha <= 1 and 0 <= beta <= 1 and 0 <= gamma <= 1



@njit(parallel=True)
def draw(canvas):
    # Draw the polygon outline
    
    startTime = time.time()

    for i in range(len(polygon_vertices)):
        v1 = polygon_vertices[i]
        v2 = polygon_vertices[(i + 1) % len(polygon_vertices)]
        canvas.draw_line(v1, v2, 2, "White")

    # Fill the triangles with UV-mapped pixels
    step = 1  # Smaller step for pixel-perfect fill

    for tri, uv_tri in zip(triangles, uv_triangles):
        (v0, v1, v2), (uv0, uv1, uv2) = tri, uv_tri

        # Find the bounding box for the triangle
        min_x = int(min(v0[0], v1[0], v2[0]))
        max_x = int(max(v0[0], v1[0], v2[0]))
        min_y = int(min(v0[1], v1[1], v2[1]))
        max_y = int(max(v0[1], v1[1], v2[1]))

        # Loop through the bounding box
        for x in range(min_x, max_x, step):
            for y in range(min_y, max_y, step):
                alpha, beta, gamma = barycentric_coords((x, y), v0, v1, v2)

                if is_point_in_triangle(alpha, beta, gamma):
                    # Interpolate UVs
                    u = alpha * uv0[0] + beta * uv1[0] + gamma * uv2[0]
                    v = alpha * uv0[1] + beta * uv1[1] + gamma * uv2[1]

                    # Get the texture color
                    color = get_color_from_uv(u, v)

                    # Draw a small filled rectangle (pixel)
                    canvas.draw_polygon(
                        [(x, y), (x + step, y), (x + step, y + step), (x, y + step)],
                        1,
                        color,
                        color,
                    )
    endtimeTime = time.time()

    print("time taken for frame = ", endtimeTime - startTime)



# Create frame and set draw handler
frame = simplegui.create_frame("UV Mapping with Local Image", canvas_width, canvas_height, 0)
# frame.set_canvas_background("Black")
frame.set_draw_handler(draw)


frame._canvas_border_size
frame._hide_controlpanel = True
frame._canvas_border_size = 0 
frame._canvas_x_offset = 0
frame._canvas_y_offset = 0
frame._border_size = 0



import pygame
frame._pygame_surface = pygame.display.set_mode(
            ((frame._canvas_x_offset + canvas_width +
              frame._canvas_border_size + frame._border_size),
             (frame._canvas_y_offset + canvas_height +
              frame._canvas_border_size + frame._border_size)),
            simplegui.Frame._pygame_mode_flags,
            simplegui.Frame._pygame_mode_depth)


# Start frame
frame.start()
