import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import ApplicationEngine.AppEngine as LNLEngine


class DoomExample(LNLEngine.Game):
    def __init__(self):
        super().__init__()

    def _OnUpdate(self):
        return super()._OnUpdate()


if __name__ == "__main__":
    gameInst = DoomExample()
    gameInst.Run()