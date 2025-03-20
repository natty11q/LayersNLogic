if __name__ == "__main__":
    import sys, os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))


from ApplicationEngine.AppEngine import * 


class UIComponent(GameObject, ABC): # type: ignore
    def __init__(self, pos : Vec2, relativePos_x : bool, relativePos_y : bool, zIndex : int = 1):
        super().__init__()



if __name__ == "__main__":
    ...