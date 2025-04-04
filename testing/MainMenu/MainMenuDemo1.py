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
        #Start game to be implemented later
        print("Start button pressed")

    def quit_game(self):
        #Quit game button to be implemented later
        print("Quit button pressed")

    def draw(self, canvas):
        # Menu
        canvas.draw_text(self.TITLE, (self.WIDTH // 3, self.HEIGHT // 4), 36, "White")
        
        # Draw buttons
        self.draw_button(canvas, self.START_BUTTON_POS, "Start", "Green")
        self.draw_button(canvas, self.QUIT_BUTTON_POS, "Quit", "Red")

    def draw_button(self, canvas, position, text, color):
        x, y = position
        canvas.draw_polygon([
            (x, y),
            (x + self.BUTTON_WIDTH, y),
            (x + self.BUTTON_WIDTH, y + self.BUTTON_HEIGHT),
            (x, y + self.BUTTON_HEIGHT)
        ], 2, "White", color)

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

    def run(self):
        self.frame.start()


# Create and run the menu
menu = GameMenu()
menu.run()
