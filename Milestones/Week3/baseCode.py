try:
    import simplegui # type: ignore
except ImportError :
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# Some constants
CANVAS_DIMS = (600, 400)

# IMG = simplegui.load_image('./coach_wheel-512.png')
IMG = simplegui.load_image('/Users/nathanielfrimpong-santeng/codestuffs/RHUL/Software Eng/pythonProjects/GroupPythonGame/LayersNLogic/Milestones/Week3/coach_wheel-512.png')
IMG_CENTRE = (256, 256)
IMG_DIMS = (512, 512)

STEP = 0.5

# Global variables
img_dest_dim = (128,128)
img_pos = [CANVAS_DIMS[0]/2, 2*CANVAS_DIMS[1]/3.]
img_rot = 0

# Drawing handler
def draw(canvas):
    global img_rot
    img_rot += STEP
    canvas.draw_image(IMG, IMG_CENTRE, IMG_DIMS, img_pos, img_dest_dim, img_rot)


# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("A wheel", CANVAS_DIMS[0], CANVAS_DIMS[1])
frame.set_canvas_background('#2C6A6A')
frame.set_draw_handler(draw)


# Start the frame animation
frame.start()
