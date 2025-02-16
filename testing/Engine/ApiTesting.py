import json
import pygame

try:
    import simplegui # type: ignore
except ImportError :
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# from OpenGL.GL import *
# from OpenGL.GLUT import *
# from OpenGL.GLU import *
# import pymetal

def ColToStr(col : tuple [float]) -> str:
    outcol = "RGB("
    for c in col:
        outcol += str(c * 255) + ","

    return outcol

class Renderer:
    def __init__(self, api_name):
        Renderer.__api = self.load_api(api_name)

    def load_api(self, api_name):
        if api_name == "pygame":
            return PygameRenderer()
        elif api_name == "simplegui":
            return SimpleGUIRenderer()
        # elif api_name == "opengl":
        #     return OpenGLRenderer()
        # elif api_name == "metal":
        #     return MetalRenderer()
        else:
            raise ValueError(f"Unknown rendering API: {api_name}")

    def draw_square(self, x, y, size, color):
        Renderer.__api.draw_square(x, y, size, color)
    
    @staticmethod
    def GetApi():
        return Renderer.__api
    
class Shape:
    def __init__(self):
        pass
    
    def Draw(self, canvas : simplegui.Canvas):
        pass

class Square(Shape):
    def __init__(self, pos= (0,0), sl= 2, bCol= "red", fCol= None):
        super().__init__()
        self.position = (50,50)
        self.BorderCol = 'red'
        self.FillCol = None
        self.SideLength = 20
        self.lw = 2
    
    def Draw(self, canvas : simplegui.Canvas):
        canvas.draw_polygon([
            (self.position[0],self.position[1]),
            (self.position[0] + self.SideLength, self.position[0]),
            (self.position[0] + self.SideLength, self.position[1] + self.SideLength),
            (self.position[0], 50 + self.SideLength)    ],
                            self.lw,
                            self.BorderCol,
                            self.FillCol)
    
class PygameRenderer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 400))
        pygame.display.set_caption("Pygame Renderer")

    def draw_square(self, x, y, size, color):
        pygame.draw.rect(self.screen, color, (x, y, size, size))

    def update_display(self):
        pygame.display.flip()

class SimpleGUIRenderer:
    def __init__(self):
        self.frame = simplegui.create_frame("SimpleGUI Renderer", 400, 400)
        self.draw_queue : list [Shape] = []
        self.frame.set_draw_handler(self.draw)

    def draw_square(self, x, y, size, color):
        self.draw_queue.append(Square())
        
    def draw_circle(self):
        pass
        # canvas.draw_circle((50, 50), 10, 2, "blue", "red")

    def draw(self, canvas : simplegui.Canvas):
        # canvas.draw_circle((50, 50), 10, 2, "blue", "red")
        canvas.draw_polygon([(50,50), (50 + 10, 50), (50 + 10, 50 + 10), (50, 50 + 10)],2,"red")
        for shape in self.draw_queue:
            shape.Draw(canvas)
        self.draw_queue.clear()

    def start(self):
        self.frame.start()

# class OpenGLRenderer:
#     def __init__(self):
#         glutInit()
#         glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
#         glutInitWindowSize(400, 400)
#         glutCreateWindow("OpenGL Renderer".encode("utf-8"))
#         glClearColor(0.0, 0.0, 0.0, 1.0)

#     def draw_square(self, x, y, size, color):
#         glBegin(GL_QUADS)
#         glColor3f(*color)
#         glVertex2f(x, y)
#         glVertex2f(x + size, y)
#         glVertex2f(x + size, y + size)
#         glVertex2f(x, y + size)
#         glEnd()

#     def update_display(self):
#         glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#         glutSwapBuffers()

# class MetalRenderer:
#     def __init__(self):
#         self.device = pymetal.create_system_default_device()
#         self.queue = self.device.new_command_queue()

#     def draw_square(self, x, y, size, color):
#         print(f"Drawing square at {x},{y} with size {size} in Metal")

#     def update_display(self):
#         print("Metal frame updated")

class Window:
    def __init__(self, settings_path="settings.json"):
        # with open(settings_path, "r") as f:
        #     settings = json.load(f)
        
        settings = {"rendering_api" : "simplegui"}
        self.api_name = settings["rendering_api"]
        self.renderer = Renderer(self.api_name)

    def get_renderer(self):
        return self.renderer

class GameLoop:
    def __init__(self, window):
        self.window = window
        self.renderer = window.get_renderer()
        self.running = True

    def update(self):
        self.renderer.draw_square(100, 100, 50, (1, 0, 0))
        self.renderer.draw_square(200, 200, 70, (1, 0, 0))

    def run(self):
        if self.window.api_name == "pygame":
            while self.running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                self.update()
                self.renderer.GetApi().update_display()
            pygame.quit()
        elif self.window.api_name == "simplegui":
            self.window.renderer.GetApi().start()
        elif self.window.api_name == "opengl":
            while self.running:
                self.update()
                self.renderer.GetApi().update_display()
        elif self.window.api_name == "metal":
            while self.running:
                self.update()
                self.renderer.GetApi().update_display()

if __name__ == "__main__":
    window = Window()
    game_loop = GameLoop(window)
    game_loop.run()
