# Group name - app name - Nathaniel Frimpong-Santeng - [14-01-2025]
#
# this is the file that is included into the game project and allows for interfacing between the game and the engine
#
#   
#
#
#
#


import os, sys
EngineRoot : os.path = os.path.dirname( os.path.dirname( __file__ ) )
sys.path.append(EngineRoot)

import src.Core.Utility.CoreUtility as Utility
from src.Core.Utility.Filemanager import *

EngineFileManager.SetEnginePath("EngineRoot" , EngineRoot)
EngineFileManager.SetEnginePath("EngineBase" , os.path.join( EngineFileManager.GetEnginePath("EngineRoot"), "ApplicationEngine") )
EngineFileManager.SetEnginePath("EngineSettingsRoot" , os.path.join( EngineFileManager.GetEnginePath("EngineBase") , "Settings"))

print ("ESR : ", EngineFileManager.GetEnginePath("EngineSettingsRoot"))

from src.Core.Core import *


# for testing
if __name__ == "__main__":
    gameInst = Game()
    gameInst.Run()
    
    
    
    # import random
    # try:
    #     import simplegui # noqa
    # except ImportError :
    #     import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

    # def randCol ():
    #     r = random.randrange (0, 256)
    #     g = random.randrange (0, 256)
    #     b = random.randrange (0, 256)
    #     return 'rgb('+str(r)+ ','+str(g)+ ','+str(b)+ ')'

    # # Drawing handler :
    # # this function is called 60 times per second
    # def draw(canvas):
    #     frame.set_canvas_background(randCol())

    # # Create a frame and assign the callback to the event handler
    # frame = simplegui.create_frame(" Colours ", 400 , 200)
    # frame.set_draw_handler(draw)

    # # Start the frame animation
    # frame.start ()