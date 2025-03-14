from ApplicationEngine.include.Common import *
# from ApplicationEngine.include.Maths.Maths import *
# from ApplicationEngine.include.Window.Window import *
from ApplicationEngine.src.Object.Object import *
# from ApplicationEngine.src.Graphics.Renderer.Renderer import *
# import ApplicationEngine.src.Core.Utility.Temporal as Temporal


class Scene:
    def __init__(self, name):
        self.name = name
        self.objects : list[GameObject] = []  # List of GameObject instances

    def AddObject(self, obj):
        self.objects.append(obj)

    def Update(self, dt):
        for obj in self.objects:
            obj.Update(dt)
    
    def PhysicsUpdate(self, tickTime):
        for obj in self.objects:
            obj.PhysicsUpdate(tickTime)

    def Draw(self):
        for obj in self.objects:
            obj.Draw()