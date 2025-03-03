try:
    import simplegui  # type: ignore
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from PIL import Image
import threading

import time

# Load and prepare the texture image.
image_path = "testing/testAssets/testImage3.png"  # update with your local absolute path
img = Image.open(image_path)
img = img.resize((300, 300))
image_data = img.convert("RGB")

canvas_width, canvas_height = 600, 400

imgPos = (0, 0)
# Canvas size
canvas_width, canvas_height = 900 * 1.3, 600 * 1.3
imgw, imgh = (canvas_width, canvas_height)

# Define your quad and its UV coordinates.
polygon_vertices = [ imgPos, (imgw, imgPos[1]), (imgw, imgh), (imgPos[0], imgh) ]
uv_coords = [(0, 0), (1, 0), (1, 1), (0, 1)]

# Global variables to store the precomputed pixel data.
pixel_buffer = []  # list of tuples (x, y, color_string)
pixels_ready = False

def get_color_from_uv(u, v):
    """Convert interpolated UV coordinates to a color from the texture."""
    x = int(u * (img.width - 1))
    y = int(v * (img.height - 1))
    pixelCol = image_data.getpixel((x, y))
    
    
    r, g, b = (10, 10, 10)
    if isinstance(pixelCol, tuple):
        r, g, b = pixelCol
    return f"rgb({r},{g},{b})"

def compute_triangle_pixels(tri, uv_tri):
    """
    For a given triangle (with vertex positions and corresponding UV coordinates),
    compute a list of (x, y, color) tuples for each pixel inside the triangle.
    """
    (v0, v1, v2), (uv0, uv1, uv2) = tri, uv_tri
    local_pixels = []
    min_x = int(min(v0[0], v1[0], v2[0]))
    max_x = int(max(v0[0], v1[0], v2[0]))
    min_y = int(min(v0[1], v1[1], v2[1]))
    max_y = int(max(v0[1], v1[1], v2[1]))
    
    for x in range(min_x, max_x):
        for y in range(min_y, max_y):
            # Calculate barycentric coordinates
            denom = ((v1[1] - v2[1])*(v0[0] - v2[0]) + (v2[0] - v1[0])*(v0[1] - v2[1]))
            if denom == 0:
                continue
            w0 = ((v1[1] - v2[1])*(x - v2[0]) + (v2[0] - v1[0])*(y - v2[1])) / denom
            w1 = ((v2[1] - v0[1])*(x - v2[0]) + (v0[0] - v2[0])*(y - v2[1])) / denom
            w2 = 1 - w0 - w1

            # If the point (x, y) lies within the triangle...
            if w0 >= 0 and w1 >= 0 and w2 >= 0:
                # Interpolate the UV coordinates using barycentric weights.
                u = w0 * uv0[0] + w1 * uv1[0] + w2 * uv2[0]
                v = w0 * uv0[1] + w1 * uv1[1] + w2 * uv2[1]
                color = get_color_from_uv(u, v)
                local_pixels.append((x, y, color))
    return local_pixels

def compute_pixels_thread():
    """
    This function splits the quad (polygon) into two triangles,
    computes pixel color data for each in parallel using threads,
    and then stores the results in the global pixel_buffer.
    """
    global pixel_buffer, pixels_ready
    # Split the quad into two triangles.
    triangles = [
        (polygon_vertices[0], polygon_vertices[1], polygon_vertices[2]),
        (polygon_vertices[0], polygon_vertices[2], polygon_vertices[3])
    ]
    uv_triangles = [
        (uv_coords[0], uv_coords[1], uv_coords[2]),
        (uv_coords[0], uv_coords[2], uv_coords[3])
    ]
    local_buffer = []
    threads = []
    results = [None, None]
    
    # Worker function to compute pixels for a triangle.
    def worker(i, tri, uv_tri):
        results[i] = compute_triangle_pixels(tri, uv_tri)
    
    # Start a thread for each triangle.
    for i, (tri, uv_tri) in enumerate(zip(triangles, uv_triangles)):
        t = threading.Thread(target=worker, args=(i, tri, uv_tri))
        threads.append(t)
        t.start()
    # Wait for both threads to finish.
    for t in threads:
        t.join()
    # Combine the results.
    for res in results:
        if res:
            local_buffer.extend(res)
    pixel_buffer = local_buffer
    pixels_ready = True

# Start the background thread to compute pixel data.
threading.Thread(target=compute_pixels_thread, daemon=True).start()

def draw(canvas):
    startTime = time.time()

    # Draw the outline of the polygon.
    for i in range(len(polygon_vertices)):
        v1 = polygon_vertices[i]
        v2 = polygon_vertices[(i + 1) % len(polygon_vertices)]
        canvas.draw_line(v1, v2, 2, "White")
    
    # Once the pixel buffer is ready, draw each pixel.
    if pixels_ready:
        for (x, y, color) in pixel_buffer:
            canvas.draw_point((x, y), color)
    else:
        canvas.draw_text("Loading...", (canvas_width/2 - 50, canvas_height/2), 20, "White")
    
    endtimeTime = time.time()

    print("time taken for frame = ", endtimeTime - startTime)

frame = simplegui.create_frame("Threaded UV Mapping", canvas_width, canvas_height)
frame.set_draw_handler(draw)
frame.start()
