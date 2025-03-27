try:
    import simplegui  # type: ignore
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from PIL import Image
import time, threading
import numpy as np

# Load an image
image_path = "/Users/nathanielfrimpong-santeng/codestuffs/RHUL/Software Eng/pythonProjects/GroupPythonGame/LayersNLogic/testing/testAssets/testImage3.png"
img = Image.open(image_path)
# Optionally resize if needed
# img = img.resize((300, 300))
image_data = img.convert("RGB")

# Canvas size
canvas_width, canvas_height = int(900 * 1), int(600 * 1)
imgw, imgh = (canvas_width / 2, canvas_height / 2)
imgPos = (canvas_width / 2 ** 1.5, canvas_height / 2 ** 1.5)

# Polygon vertices and UV coordinates
polygon_vertices = [ imgPos, (imgw, imgPos[1]), (imgw, imgh), (imgPos[0], imgh) ]
uv_coords = [(0, 0), (1, 0), (1, 1), (0, 1)]

# Split polygon into two triangles
triangles = [
    ((polygon_vertices[0][0] + 100,polygon_vertices[0][1] + 100), (polygon_vertices[1][0] + 100,polygon_vertices[1][1] - 200), (polygon_vertices[2][0] + 100,polygon_vertices[2][1] + 100)),
    (polygon_vertices[0], polygon_vertices[2], polygon_vertices[3]),
]

uv_triangles = [
    (uv_coords[0], uv_coords[1], uv_coords[2]),
    (uv_coords[0], uv_coords[2], uv_coords[3]),
]

# Global container for precomputed pixel data.
# Each element is a list: [polygon (list of 4 tuples), line thickness, fill color, outline color]
texture0 = []
tex0Ready = False 

def get_color_from_uv(u, v):
    """Get pixel color from UV coordinates as an 'rgb(r,g,b)' string."""
    x = int(u * (img.width - 1))
    y = int(v * (img.height - 1))
    pixelCol = image_data.getpixel((x, y))
    # Default color if pixelCol is not a tuple.
    r, g, b = (10, 10, 10)
    if isinstance(pixelCol, tuple):
        r, g, b = pixelCol
    return f"rgb({r},{g},{b})"

def barycentric_coords(p, a, b, c):
    """Compute barycentric coordinates for point p inside triangle (a, b, c)."""
    detT = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
    if detT == 0:
        return 0.0, 0.0, 0.0
    alpha = ((b[1] - c[1]) * (p[0] - c[0]) + (c[0] - b[0]) * (p[1] - c[1])) / detT
    beta = ((c[1] - a[1]) * (p[0] - c[0]) + (a[0] - c[0]) * (p[1] - c[1])) / detT
    gamma = 1 - alpha - beta
    return alpha, beta, gamma

def is_point_in_triangle(alpha, beta, gamma):
    """Check if a point is inside the triangle using barycentric coordinates."""
    return (alpha >= 0 and beta >= 0 and gamma >= 0)



texSize = 0


def loadTexture():
    global tex0Ready, texture0, texSize
    step = 1  # pixel step for fine-grained fill

    # Process each triangle.
    for tri, uv_tri in zip(triangles, uv_triangles):
        (v0, v1, v2) = tri
        (uv0, uv1, uv2) = uv_tri

        # Compute bounding box of the triangle.
        min_x = int(min(v0[0], v1[0], v2[0]))
        max_x = int(max(v0[0], v1[0], v2[0]))
        min_y = int(min(v0[1], v1[1], v2[1]))
        max_y = int(max(v0[1], v1[1], v2[1]))

        # Loop over bounding box pixels.
        for x in range(min_x, max_x, step):
            for y in range(min_y, max_y, step):
                alpha, beta, gamma = barycentric_coords((x, y), v0, v1, v2)
                if is_point_in_triangle(alpha, beta, gamma):
                    # Interpolate UV coordinates.
                    u = alpha * uv0[0] + beta * uv1[0] + gamma * uv2[0]
                    v = alpha * uv0[1] + beta * uv1[1] + gamma * uv2[1]
                    # Get the color from the texture.
                    color = get_color_from_uv(u, v)
                    # Store the pixel's polygon (as a small quad), line thickness, and colors.
                    # Here we store the quad corners.
                    pixel_quad = [(x, y), (x + step, y), (x + step, y + step), (x, y + step)]
                    texture0.append([pixel_quad, 1, color, color])
    texSize = len(texture0)
    tex0Ready = True

# Run loadTexture in a background thread so as not to block the main thread.
texture_thread = threading.Thread(target=loadTexture)
texture_thread.start()



pixelLimit = 2**18
currentPixelIdx = 0
lastPixelIndex = 0
def draw(canvas: simplegui.Canvas):

    global pixelLimit
    global currentPixelIdx
    global lastPixelIndex

    startTime = time.time()

    # Draw polygon outline.
    for i in range(len(polygon_vertices)):
        v1 = polygon_vertices[i]
        v2 = polygon_vertices[(i + 1) % len(polygon_vertices)]
        canvas.draw_line(v1, v2, 2, "White")

    # Draw the texture once it is ready.


    if tex0Ready:
        # print(currentPixelId)
        currentPixelIdx = currentPixelIdx  % texSize
        lastPixelIndex = currentPixelIdx
        complete = pixelLimit
        while complete > 0 and (pixelLimit - complete) < texSize:
            pixel = texture0[currentPixelIdx]
            # pixel[0] is the list of vertices; pixel[1] is thickness;
            # pixel[2] is fill color; pixel[3] is outline color.
            # canvas.draw_polygon(pixel[0],1, pixel[2], pixel[2])
            canvas.draw_point(pixel[0][0],pixel[2])
            # print(f"update :  {pixel[0][0]}")
        
            currentPixelIdx = ((currentPixelIdx + 1) % (texSize - 1))
            # print(f"CPI : {currentPixelIdx}")
            # print(f"TS : {texSize}")
            complete -= 1
        texture_thread.join()
    else:
        canvas.draw_text("Loading texture...", (canvas_width//2 - 50, canvas_height//2), 20, "White")

    endTime = time.time()
    print("FR =", 1 / (endTime - startTime))

# Create frame and set draw handler.
frame = simplegui.create_frame("UV Mapping with Local Image", canvas_width, canvas_height, 0)
frame.set_draw_handler(draw)

# Remove control panel and borders (as much as possible with SimpleGUI).
frame._hide_controlpanel = True
frame._canvas_border_size = 0
frame._canvas_x_offset = 0
frame._canvas_y_offset = 0
frame._border_size = 0

# (Optional) Set pygame display to borderless if supported by your version.
import pygame
frame._pygame_surface = pygame.display.set_mode(
    (int(frame._canvas_x_offset + canvas_width + frame._canvas_border_size + frame._border_size),
     int(frame._canvas_y_offset + canvas_height + frame._canvas_border_size + frame._border_size)),
    simplegui.Frame._pygame_mode_flags,
    simplegui.Frame._pygame_mode_depth)

frame.start()
