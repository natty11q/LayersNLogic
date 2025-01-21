from include.Common import *



class EngineFileManager:
    __EnginePaths : {str , os.path} = {}
    def SetEnginePath(pathName, pathDir):
        EngineFileManager.__EnginePaths[pathName] = pathDir

    def GetEnginePath(pathName):
        if pathName in EngineFileManager.__EnginePaths:
            return EngineFileManager.__EnginePaths[pathName]
        return None
    


    GamePaths : {str , os.path} = {}