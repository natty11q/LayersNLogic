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
EngineRoot : os.path = os.path.abspath( os.path.abspath( __file__ ) )
sys.path.append(EngineRoot)


from src.Core.Core import *

EngineFileManager.SetEnginePath("EngineRoot" , EngineRoot)






# for testing
if __name__ == "__main__":
    gameInst = Game()
    gameInst.Run()