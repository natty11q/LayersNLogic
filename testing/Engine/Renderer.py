# from abc import ABC, abstractmethod
# from enum import Enum
# import pygame


# import json
# import pygame

# try:
#     import simplegui # type: ignore
# except ImportError :
#     import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


# class RendererAPI(Enum):
#     SIMPLEGUI = "SimpleGUI"
#     PYGAME = "Pygame"
#     METAL = "Metal"
#     OPENGL = "OpenGL"
#     NONE = "None"

# class RenderCommand:
#     @staticmethod
#     def SetClearColor(renderer, color):
#         renderer.submit_command(RenderCommand("set_clear_color", color=color))
    
#     @staticmethod
#     def Clear(renderer):
#         renderer.submit_command(RenderCommand("clear"))
    
#     @staticmethod
#     def DrawIndexed(renderer, vertices, indices, color, layer=0):
#         renderer.submit_command(RenderCommand("draw_indexed", vertices=vertices, indices=indices, color=color, layer=layer))
    
#     def __init__(self, command_type, **kwargs):
#         self.command_type = command_type
#         self.kwargs = kwargs

# class Renderer(ABC):
#     S_RendererAPI :  RendererAPI =  RendererAPI.NONE  # Static reference to selected Renderer API

#     @abstractmethod
#     def submit_command(self, command: RenderCommand):
#         pass

# class GameObject(ABC):
#     def __init__(self, vertices, indices, color, layer=0):
#         self.vertices = vertices
#         self.indices = indices
#         self.color = color
#         self.layer = layer

#     @abstractmethod
#     def draw(self, renderer: Renderer):
#         pass

# class Polygon(GameObject):
#     def draw(self, renderer: Renderer):
#         RenderCommand.DrawIndexed(renderer, self.vertices, self.indices, self.color, self.layer)

# class Triangle(Polygon):
#     def __init__(self, v1, v2, v3, color, layer=0):
#         vertices = [v1, v2, v3]
#         indices = [0, 1, 2]
#         super().__init__(vertices, indices, color, layer)

# class LayeredRenderer(Renderer):
#     def __init__(self):
#         self.layers = {}
    
#     def submit_command(self, command: RenderCommand):
#         if command.command_type in ["draw_indexed", "draw_polygon"]:
#             layer = command.kwargs["layer"]
#             if layer not in self.layers:
#                 self.layers[layer] = []
#             self.layers[layer].append((command.kwargs["vertices"], command.kwargs.get("indices"), command.kwargs["color"]))
#         elif command.command_type == "set_clear_color":
#             self.clear_color = command.kwargs["color"]
#         elif command.command_type == "clear":
#             self.layers.clear()
    
#     def get_sorted_layers(self):
#         return sorted(self.layers.keys())

# class Window(ABC):
#     def __init__(self, width, height):
#         self.width = width
#         self.height = height
#         self.renderer = None
    
#     @abstractmethod
#     def create(self):
#         pass

#     @staticmethod
#     def CreateWindow(api: RendererAPI, width: int, height: int):
#         if api == RendererAPI.SIMPLEGUI:
#             return SimpleGUIWindow(width, height)
#         elif api == RendererAPI.PYGAME:
#             return PygameWindow(width, height)
#         else:
#             raise ValueError("Unsupported API")

# class SimpleGUIRenderer(LayeredRenderer):
#     def __init__(self):
#         super().__init__()
    
# class SimpleGUIWindow(Window):
#     def __init__(self, width, height):
#         super().__init__(width, height)
#         self.renderer = SimpleGUIRenderer()
#         Renderer.S_RendererAPI = RendererAPI.SIMPLEGUI

#     def create(self):
#         # import simplegui
#         self.frame = simplegui.create_frame("Game", self.width, self.height)
#         self.frame.set_draw_handler(self.draw)
#         self.frame.start()
    
#     def draw(self, canvas):
#         for layer in self.renderer.get_sorted_layers():
#             for vertices, indices, color in self.renderer.layers[layer]:
#                 if indices:
#                     indexed_vertices = [vertices[i] for i in indices]
#                     canvas.draw_polygon(indexed_vertices, 1, color, color)
#                 else:
#                     canvas.draw_polygon(vertices, 1, color, color)
#         self.renderer.layers.clear()

# class PygameRenderer(LayeredRenderer):
#     def __init__(self, screen):
#         super().__init__()
#         self.screen = screen
#         self.clear_color = pygame.Color(50,50,50,255)
#     def submit_command(self, command: RenderCommand):
#         super().submit_command(command)
#         if command.command_type == "set_clear_color":
#             self.clear_color = pygame.Color(*command.kwargs["color"])
#         elif command.command_type == "clear":
#             self.screen.fill(self.clear_color)
#         elif command.command_type == "draw_indexed":
#             vertices = command.kwargs["vertices"]
#             indices = command.kwargs.get("indices")
#             color = pygame.Color(*command.kwargs["color"])
#             if indices:
#                 pygame.draw.polygon(self.screen, color, [vertices[i] for i in indices])
#             else:
#                 pygame.draw.polygon(self.screen, color, vertices)

# class PygameWindow(Window):
#     def __init__(self, width, height):
#         super().__init__(width, height)
#         pygame.init()
#         self.screen = pygame.display.set_mode((width, height))
#         self.renderer = PygameRenderer(self.screen)
#         Renderer.S_RendererAPI = RendererAPI.PYGAME

#     def create(self):
#         running = True
#         clock = pygame.time.Clock()
#         while running:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False
            
#             self.renderer.submit_command(RenderCommand("clear"))
#             for layer in self.renderer.get_sorted_layers():
#                 for vertices, indices, color in self.renderer.layers[layer]:
#                     if indices:
#                         indexed_vertices = [vertices[i] for i in indices]
#                         pygame.draw.polygon(self.screen, pygame.Color(*color), indexed_vertices)
#                     else:
#                         pygame.draw.polygon(self.screen, pygame.Color(*color), vertices)
            
#             pygame.display.flip()
#             clock.tick(60)
        
#         pygame.quit()

# # Example Usage
# game_window = Window.CreateWindow(RendererAPI.SIMPLEGUI, 400, 300)
# game_window.create()
# RenderCommand.SetClearColor(game_window.renderer, (255, 255, 255))
# RenderCommand.Clear(game_window.renderer)
# triangle1 = Triangle((50, 50), (100, 50), (75, 100), (255, 0, 0), layer=1)
# triangle2 = Triangle((60, 60), (110, 60), (85, 110), (0, 0, 255), layer=0)
# triangle1.draw(game_window.renderer)
# triangle2.draw(game_window.renderer)



from abc import ABC, abstractmethod
from enum import Enum
import pygame

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


class RendererAPI(Enum):
    SIMPLEGUI = "SimpleGUI"
    PYGAME = "Pygame"
    METAL = "Metal"
    OPENGL = "OpenGL"

class RenderCommand:
    @staticmethod
    def SetClearColor(renderer, color):
        renderer.submit_command(RenderCommand("set_clear_color", color=color))
    
    @staticmethod
    def Clear(renderer):
        renderer.submit_command(RenderCommand("clear"))
    
    @staticmethod
    def DrawIndexed(renderer, vertices, indices, color):
        renderer.submit_command(RenderCommand("draw_indexed", vertices=vertices, indices=indices, color=color))
    
    def __init__(self, command_type, **kwargs):
        self.command_type = command_type
        self.kwargs = kwargs

class Renderer(ABC):
    S_RendererAPI = None  # Static reference to selected Renderer API

    @abstractmethod
    def submit_command(self, command: RenderCommand):
        pass

class GameObject(ABC):
    def __init__(self, vertices, indices, color):
        self.vertices = vertices
        self.indices = indices
        self.color = color

    @abstractmethod
    def draw(self, renderer: Renderer):
        pass

class Polygon(GameObject):
    def draw(self, renderer: Renderer):
        RenderCommand.DrawIndexed(renderer, self.vertices, self.indices, self.color)

class Triangle(Polygon):
    def __init__(self, v1, v2, v3, color):
        vertices = [v1, v2, v3]
        indices = [0, 1, 2]
        super().__init__(vertices, indices, color)

class SimpleGUIRenderer(Renderer):
    def __init__(self):
        self.commands = []
    
    def submit_command(self, command: RenderCommand):
        self.commands.append(command)
    
    def draw(self, canvas):
        # canvas.draw_polygon([(20,20),(30,50),(10,60)], 1, "red","yellow")
        
        # print(self.commands)
        for layer in layers:
            layer.OnUpdate()
        # input()
        for command in self.commands:
            if command.command_type == "draw_indexed":
                vertices = command.kwargs["vertices"]
                indices = command.kwargs["indices"]
                color = command.kwargs["color"]
                indexed_vertices = [vertices[i] for i in indices]
                canvas.draw_polygon(indexed_vertices, 1, rgb_to_hex(color),rgb_to_hex(color))
        self.commands.clear()

class Window(ABC):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.renderer = None
    
    @abstractmethod
    def create(self):
        pass
    @abstractmethod
    def Run(self):
        pass

    @staticmethod
    def CreateWindow(api: RendererAPI, width: int, height: int):
        if api == RendererAPI.SIMPLEGUI:
            return SimpleGUIWindow(width, height)
        elif api == RendererAPI.PYGAME:
            return PygameWindow(width, height)
        else:
            raise ValueError("Unsupported API")

class SimpleGUIWindow(Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.renderer = SimpleGUIRenderer()
        Renderer.S_RendererAPI = RendererAPI.SIMPLEGUI
    
    def create(self):
        try:
            import simplegui # type: ignore
        except ImportError :
            import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

        self.frame = simplegui.create_frame("Game", self.width, self.height)
        self.frame.set_draw_handler(self.renderer.draw)
    
    def Run(self):
        self.frame.start()
        

class PygameRenderer(Renderer):
    def __init__(self, screen):
        self.screen = screen
        self.commands = []
    
    def submit_command(self, command: RenderCommand):
        self.commands.append(command)
    
    def draw(self):
        # pygame.draw.polygon(self.screen, color, indexed_vertices)
        for command in self.commands:
            if command.command_type == "clear":
                self.screen.fill((255, 255, 255))
            elif command.command_type == "draw_indexed":
                vertices = command.kwargs["vertices"]
                indices = command.kwargs["indices"]
                color = command.kwargs["color"]
                indexed_vertices = [vertices[i] for i in indices]
                pygame.draw.polygon(self.screen, color, indexed_vertices)
        self.commands.clear()

class PygameWindow(Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.renderer = PygameRenderer(self.screen)
        Renderer.S_RendererAPI = RendererAPI.PYGAME

    def create(self):
        ...
    def Run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.renderer.draw()
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()
        
# Example Usage
game_window = Window.CreateWindow(RendererAPI.SIMPLEGUI, 400, 300)
game_window.create()
RenderCommand.SetClearColor(game_window.renderer, (255, 255, 255))
RenderCommand.Clear(game_window.renderer)
triangle1 = Triangle((50, 50), (100, 50), (75, 100), (255, 0, 0))
triangle2 = Triangle((60, 60), (110, 60), (85, 110), (0, 0, 255))
triangle3 = Triangle((20,20),(30,50),(10,60), (0, 255, 0))
triangle1.draw(game_window.renderer)
triangle2.draw(game_window.renderer)
triangle3.draw(game_window.renderer)
game_window.Run()