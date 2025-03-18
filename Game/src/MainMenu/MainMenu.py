sys.path.append(os.path.join(os.path.dirname(__file__),'..','Level'))
import Level
import sys
import os
import ApplicationEngine.AppEngine as LNLEngine
try:
    import simplegui # type: ignore
    
except ImportError :
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

class GameMenu:
    def __init__(self, width=600, height=400):
        self.WIDTH = width
        self.HEIGHT = height
        self.BG_COLOUR = "black"  # Placeholder background 
        self.TITLE = "Layers and Logic " 
        # Load images
        self.start_button_image = simplegui.load_image('startbutton.png')
        self.start_button_hover_image = simplegui.load_image('startbuttonhover.png')

        # Track hover state
        self.start_button_hover = False
 
        # Button properties
        self.BUTTON_WIDTH = 150
        self.BUTTON_HEIGHT = 50
        self.START_BUTTON_POS = (self.WIDTH // 2 - self.BUTTON_WIDTH // 2, self.HEIGHT // 2)
        self.QUIT_BUTTON_POS = (self.WIDTH // 2 - self.BUTTON_WIDTH // 2, self.HEIGHT // 2 + 80)

        # Create frame
        self.frame = simplegui.create_frame("Home Menu", self.WIDTH, self.HEIGHT)

        # Set handlers
        self.frame.set_draw_handler(self.draw)
        self.frame.set_mouseclick_handler(self.mouse_click)
        self.frame.set_canvas_background(self.BG_COLOUR)

    def start_game(self):
        print("Starting level...")
        try:
            level_instance = Level.LNL_Level()
            level_instance.run()
        except AttributeError:
            print("Error: 'Level' class or 'run()' method not found in level module.")
        

    def quit_game(self):
        #Quit game button to be implemented later
        print("Quit button pressed")

    def level_select(self):
        ...

    def draw(self, canvas):
        # Menu
        canvas.draw_text(self.TITLE, (self.WIDTH // 3, self.HEIGHT // 4), 36, "White")
        
        # Draw buttons
        self.draw_button(canvas, self.START_BUTTON_POS, self.start_button_hover,self.start_button_image,self.start_button_hover_image)
        self.draw_button(canvas, self.QUIT_BUTTON_POS, "Quit", "Red")

    def draw_button(self, canvas, position, text, is_hovered, default_image, hover_image):
        x, y = position
        img = hover_image if is_hovered else default_image
        canvas.draw_image(img, 
                    (img.get_width() // 2, img.get_height() // 2),  # Image center
                    (img.get_width(), img.get_height()),             # Image size
                    (x + self.BUTTON_WIDTH // 2, y + self.BUTTON_HEIGHT // 2),  
                    (self.BUTTON_WIDTH, self.BUTTON_HEIGHT)) 

        text_x = x + self.BUTTON_WIDTH // 4
        text_y = y + self.BUTTON_HEIGHT // 1.5
        canvas.draw_text(text, (text_x, text_y), 24, "White")

    def mouse_click(self, pos):
        #Click handler
        x, y = pos

        # Check if Start button is clicked
        if (self.START_BUTTON_POS[0] <= x <= self.START_BUTTON_POS[0] + self.BUTTON_WIDTH and
            self.START_BUTTON_POS[1] <= y <= self.START_BUTTON_POS[1] + self.BUTTON_HEIGHT):
            self.start_game()

        # Check if Quit button is clicked
        if (self.QUIT_BUTTON_POS[0] <= x <= self.QUIT_BUTTON_POS[0] + self.BUTTON_WIDTH and
            self.QUIT_BUTTON_POS[1] <= y <= self.QUIT_BUTTON_POS[1] + self.BUTTON_HEIGHT):
            self.quit_game()

    def mouse_move(self, pos):
        x, y = pos

    # Track hover state for Start button
        self.start_button_hover = (
            self.START_BUTTON_POS[0] <= x <= self.START_BUTTON_POS[0] + self.BUTTON_WIDTH and
            self.START_BUTTON_POS[1] <= y <= self.START_BUTTON_POS[1] + self.BUTTON_HEIGHT
        )

    def run(self):
        self.frame.start()


# Create and run the menu
menu = GameMenu()
menu.run()
