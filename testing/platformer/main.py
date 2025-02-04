import PySimpleGUI as sg
import time

# Constants
WINDOW_SIZE = (400, 300)
PLAYER_SIZE = (20, 20)
GRAVITY = 0.00981
JUMP_STRENGTH = -8
MOVE_SPEED = 5
FLOOR_Y = 0 # Adjusting for PySimpleGUI's coordinate system

# Initialize player
player_x = 50
player_y = 300
velocity_x = 0
velocity_y = 0

friction = 0.8
max_velocity_x = 300

# Create window with a frame
layout = [[sg.Frame("Game", [[sg.Graph(WINDOW_SIZE, (0, 0), WINDOW_SIZE, background_color='white', key='-GRAPH-')]], key='-FRAME-')]]
window = sg.Window("Platformer", layout, finalize=True, return_keyboard_events=True)
graph = window['-GRAPH-']

# Main game loop
running = True
while running:
    start_time = time.time()
    event, values = window.read(timeout=0)  # Approx. 60 FPS
    
    if event == sg.WIN_CLOSED or event == 'Exit':
        running = False
        break
    
    # Handle input
    if event == 'a':
        velocity_x -= MOVE_SPEED
    if event == 'd':
        velocity_x += MOVE_SPEED
    if event == ' ' and player_y == FLOOR_Y:
        velocity_y = JUMP_STRENGTH
    
    # Apply gravity
    velocity_y -= GRAVITY  # Reverse direction since PySimpleGUI's Y-axis increases upwards
    player_y += velocity_y

    # Collision with the ground
    if player_y < FLOOR_Y:
        player_y = FLOOR_Y
        velocity_y = 0
    
    if abs(velocity_x) > max_velocity_x:
        velocity_x = max_velocity_x * (velocity_x / abs(velocity_x))
    
    if velocity_x > 0:
        if abs(velocity_x) > friction:
            velocity_x = 0
        else:
            velocity_x -= friction * (velocity_x / abs(velocity_x))
    
    player_x += velocity_x
    # Draw the player
    graph.erase()
    graph.draw_rectangle((player_x, player_y), (player_x + PLAYER_SIZE[0], player_y + PLAYER_SIZE[1]), fill_color='blue')
    
    # Debugging output
    print(f'Player Position: ({player_x}, {player_y}), Velocity Y: {velocity_y}')
    
    # Control frame rate
    elapsed_time = time.time() - start_time
    # time.sleep(max(0, 0.016 - elapsed_time))

window.close()
