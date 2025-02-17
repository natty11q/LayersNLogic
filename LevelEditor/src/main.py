## ============================== setup ===================================
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from ApplicationEngine.include.Maths.Vector.Vector import Vec2, Vec4
import ApplicationEngine.AppEngine as LNLEngine
## ============================= App Code =================================



class LayersAndLogicLevelEditor(LNLEngine.Game):
    def __init__(self):
        super().__init__()
        


if __name__ == "__main__":
    LevelEditor = LNLEngine.Game.CreateGame(LayersAndLogicLevelEditor)
    LevelEditor.Run()