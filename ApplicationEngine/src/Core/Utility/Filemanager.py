from include.Common import *




class EngineFileManager:
    __EnginePaths : dict [str , str] = {
        "EngineRoot" : "./",
        "EngineSettingsRoot" : "./"
    }
    GamePaths : dict [str , str] = {}

    
    @staticmethod
    def SetEnginePath(pathName : str, pathDir : str):
        EngineFileManager.__EnginePaths[pathName] = pathDir

    @staticmethod
    def GetEnginePath(pathName : str , default : str | None = None):
        if pathName in EngineFileManager.__EnginePaths:
            return EngineFileManager.__EnginePaths[pathName]
        return default
    
