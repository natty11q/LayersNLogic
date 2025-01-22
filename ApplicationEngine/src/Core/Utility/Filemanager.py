from include.Common import *




class EngineFileManager:
    __EnginePaths : {str , os.path} = {
        "EngineRoot" : "./",
        "EngineSettingsRoot" : "./"
    }
    
    def SetEnginePath(pathName, pathDir):
        EngineFileManager.__EnginePaths[pathName] = pathDir

    def GetEnginePath(pathName , default = None):
        if pathName in EngineFileManager.__EnginePaths:
            return EngineFileManager.__EnginePaths[pathName]
        return default
    


    GamePaths : {str , os.path} = {}