try:
    import simplegui  # type: ignore
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from PIL import Image
import numpy as np

# Load an image
image_path = "../testing/testAssets/grid.png"
img = Image.open(image_path)
img = img.resize((300, 300))
image_data = img.convert("RGB")

canvas_width, canvas_height = 600, 400

# Define vertices and UV coordinates
polygon_vertices = [(200, 100), (400, 100), (350, 300), (250, 300)]
uv_coords = [(0, 0), (1, 0), (1, 1), (0, 1)]

def get_color_from_uv(u, v):
    x = int(u * (img.width - 1))
    y = int(v * (img.height - 1))
    return image_data.getpixel((x, y))


def draw_triangle(canvas, v0, v1, v2, uv0, uv1, uv2):
    # Draw triangle and fill with texture
    min_x = min(v0[0], v1[0], v2[0])
    max_x = max(v0[0], v1[0], v2[0])
    min_y = min(v0[1], v1[1], v2[1])
    max_y = max(v0[1], v1[1], v2[1])
    
    for x in range(int(min_x), int(max_x)):
        for y in range(int(min_y), int(max_y)):
            # Compute barycentric coordinates
            denom = ((v1[1] - v2[1]) * (v0[0] - v2[0]) + (v2[0] - v1[0]) * (v0[1] - v2[1]))
            w0 = ((v1[1] - v2[1]) * (x - v2[0]) + (v2[0] - v1[0]) * (y - v2[1])) / denom
            w1 = ((v2[1] - v0[1]) * (x - v2[0]) + (v0[0] - v2[0]) * (y - v2[1])) / denom
            w2 = 1 - w0 - w1
            
            if w0 >= 0 and w1 >= 0 and w2 >= 0:
                # Interpolate UVs with perspective correction
                u = w0 * uv0[0] + w1 * uv1[0] + w2 * uv2[0]
                v = w0 * uv0[1] + w1 * uv1[1] + w2 * uv2[1]
                color : list[float] = get_color_from_uv(u, v)
                canvas.draw_point((x, y), f"rgb({color[0]}, {color[1]}, {color[2]})")


def draw(canvas):
    # Split the quad into two triangles
    draw_triangle(canvas, polygon_vertices[0], polygon_vertices[1], polygon_vertices[2],
                  uv_coords[0], uv_coords[1], uv_coords[2])
    draw_triangle(canvas, polygon_vertices[0], polygon_vertices[2], polygon_vertices[3],
                  uv_coords[0], uv_coords[2], uv_coords[3])

    # Draw outline
    for i in range(len(polygon_vertices)):
        v1 = polygon_vertices[i]
        v2 = polygon_vertices[(i + 1) % len(polygon_vertices)]
        canvas.draw_line(v1, v2, 2, "White")


frame = simplegui.create_frame("Perspective-Correct UV Mapping", canvas_width, canvas_height)
frame.set_draw_handler(draw)
frame.start()

# Let me know if you'd like me to tweak the code further! 🚀
