from __future__ import annotations

import json
import os , sys
# import pkg_resources


# OLD_WD =  os.getcwd()


FOLDERPATH = os.path.dirname(os.path.abspath(__file__)) 
# PathToJson = pkg_resources.resource_filename('LNLLogger','LNLLoggerModule/Settings/LNLLoggerSettings.json')
PathToJson = "ApplicationEngine/Settings/Logger/LNLLoggerSettings.json"

# os.chdir(FOLDERPATH)

LNL_LOGGER_DATA : dict = {"Test " : 1}

def ResetJson():
    # print("CWDTEST" , os.getcwd())
    global LNL_LOGGER_DATA
    with open(PathToJson, 'r') as file:
        LNL_LOGGER_DATA = json.load(file)

def RefreshLogger():
    """Resets the state of the logger by checking the json"""
    # print("before :" , LNL_LOGGER_DATA)
    # WRAPPER = [LNL_LOGGER_DATA]
    ResetJson()
    # print("after : ",LNL_LOGGER_DATA)



RefreshLogger()

# os.chdir(OLD_WD)


def printCol(debugLevel : str):
    col = LNL_LOGGER_DATA["LNL_DEBUG_COLOUR"][debugLevel]
    print("\033[", col , end = "" , sep = "")
    

def Display(*text, sep = " ", end = "\n", file = None, flush = False):
    for statement in text:
        print(statement , end = sep , file = file , flush = flush)
    print("" , end = end, file = file , flush = flush)

def cascadeMkdir(path : str):
    if not os.path.exists(os.path.dirname(os.path.abspath(path))):
        cascadeMkdir(os.path.dirname(os.path.abspath(path)))
    os.mkdir(os.path.abspath(path))
    # print(path)
    


def WriteTofile(*text, sep = " ", end = "\n", file = ""):
    if not os.path.exists(os.path.dirname(os.path.abspath(file))):
        cascadeMkdir(os.path.dirname(os.path.abspath(file)))
    
    # os.path.dirname(os.path.abspath(file))
    
    with open( os.path.abspath(file) , 'a') as logOutput:
        for statement in text:
            logOutput.write(f"{statement}{sep}")
        logOutput.write(end)


class LNLDebugLogger:
    
    s_EngineLogger  : LNLDebugLogger
    s_GameLogger    : LNLDebugLogger
    
    def __init__(self , prefix : str = LNL_LOGGER_DATA["DEFAULT_PREFIX"], OutFile = LNL_LOGGER_DATA.get("LOG_FILE_PATH", None)):
        self.__CURRENT_DEBUG_MINIMUM = LNL_LOGGER_DATA["LNL_CURRENT_DEBUG_MINIMUM_LEVEL"]
        self.__LOG_COLOUR = LNL_LOGGER_DATA.get("LNL_LOG_COLOUR", True)
        self.DEBUG_ACTIVE = LNL_LOGGER_DATA.get("LNL_DEBUG", False)
        self.prefix = prefix
        self.FileOutput = OutFile
        self.LogToFile = False if OutFile is None else LNL_LOGGER_DATA.get("LOG_TO_FILE", False)
        
        
        self.LogTime = False
        self.setup()

    def setLoggerPrefix(self, newPrefix):
        self.prefix = newPrefix
    
    def getPrefix(self):
        return self.prefix
    
    def setFileOutputDestination(self, dest : str):
        self.FileOutput = dest
        self.LogToFile  = False if dest == None else True
    
    
    def setup(self):
        pass

    def setDebugMinimum(self ,level : int):
        self.__CURRENT_DEBUG_MINIMUM = level
    
    def getDebugMinimum(self):
        return self.__CURRENT_DEBUG_MINIMUM
        
    
    def setLogColourState(self, doCol : bool):
        self.__LOG_COLOUR = doCol
    
    def getLogColourState(self):
        return self.__LOG_COLOUR
        
    def turnLoggerOn(self):
        self.DEBUG_ACTIVE = True
        
    def turnLoggerOff(self):
        self.DEBUG_ACTIVE = False
        
    def WriteTofile(self, *text, sep = " ", end = "\n", file = ""):
        if not os.path.exists(os.path.dirname(os.path.abspath(file))):
            os.mkdir(os.path.dirname(os.path.abspath(file)))
            
        with open( os.path.abspath(file) , 'a') as logOutput:
            logOutput.write(f"[{self.prefix}]: ")
            for statement in text:
                logOutput.write(f"{statement}{sep}")
            logOutput.write(end)

    def LNL_LogTrace(self, *text, sep = " ", end = "\n", file = None, flush = False):
        if file is None:
            file = self.FileOutput
            
        if not self.DEBUG_ACTIVE:
            return
        
        if self.__CURRENT_DEBUG_MINIMUM <= LNL_LOGGER_DATA["LNL_DEBUG_MINIMUM_LEVEL"]["Trace"]:
            if self.__LOG_COLOUR:
                printCol("Trace")
            if self.prefix != None:
                print(f"[{self.prefix}]", end = ": ")
            Display(*text , sep= sep , end = "" , file = None , flush = flush)
            filetext = list(text)
            filetext.insert(0,self.prefix)
            WriteTofile(*filetext , sep=sep , end=end , file=file)
            if self.__LOG_COLOUR:
                print("\033[0m" , end = end, file = None , flush = flush)

    def LNL_LogInfo(self, *text, sep = " ", end = "\n", file = None, flush = False):
        if file is None:
            file = self.FileOutput
            
        if not self.DEBUG_ACTIVE:
            return
        
        if self.__CURRENT_DEBUG_MINIMUM <= LNL_LOGGER_DATA["LNL_DEBUG_MINIMUM_LEVEL"]["Info"]:
            if self.__LOG_COLOUR:
                printCol("Info")
            if self.prefix != None:
                print(f"[{self.prefix}]", end = ": ")
            Display(*text , sep= sep , end = "" , file = None , flush = flush)
            filetext = list(text)
            filetext.insert(0,self.prefix)
            WriteTofile(*filetext , sep=sep , end=end , file=file)
            if self.__LOG_COLOUR:
                print("\033[0m" , end = end, file = None , flush = flush)

    def LNL_LogWarning(self, *text, sep = " ", end = "\n", file = None, flush = False):
        if file is None:
            file = self.FileOutput
            
        if not self.DEBUG_ACTIVE:
            return
        
        if self.__CURRENT_DEBUG_MINIMUM <= LNL_LOGGER_DATA["LNL_DEBUG_MINIMUM_LEVEL"]["Warning"]:
            if self.__LOG_COLOUR:
                printCol("Warning")
            if self.prefix != None:
                print(f"[{self.prefix}]", end = ": ")
            Display(*text , sep= sep , end = "" , file = None , flush = flush)
            filetext = list(text)
            filetext.insert(0,self.prefix)
            WriteTofile(*filetext , sep=sep , end=end , file=file)
            if self.__LOG_COLOUR:
                print("\033[0m" , end = end, file = None , flush = flush)
    def LNL_LogError(self, *text, sep = " ", end = "\n", file = None, flush = False):
        if file is None:
            file = self.FileOutput
            
        if not self.DEBUG_ACTIVE:
            return
        
        if self.__CURRENT_DEBUG_MINIMUM <= LNL_LOGGER_DATA["LNL_DEBUG_MINIMUM_LEVEL"]["Error"]:
            if self.__LOG_COLOUR:
                printCol("Error")
            if self.prefix != None:
                print(f"[{self.prefix}]", end = ": ")
            Display(*text , sep= sep , end = "" , file = None , flush = flush)
            filetext = list(text)
            filetext.insert(0,self.prefix)
            WriteTofile(*filetext , sep=sep , end=end , file=file)
            if self.__LOG_COLOUR:
                print("\033[0m" , end = end, file = None , flush = flush)
        
    def LNL_LogFatal(self, *text, sep = " ", end = "\n", file = None, flush = False):
        if file is None:
            file = self.FileOutput
            
        if not self.DEBUG_ACTIVE:
            return
        
        if self.__CURRENT_DEBUG_MINIMUM <= LNL_LOGGER_DATA["LNL_DEBUG_MINIMUM_LEVEL"]["Fatal"]:
            if self.__LOG_COLOUR:
                printCol("Fatal")
            if self.prefix != None:
                print(f"[{self.prefix}]", end = ": ")
            Display(*text , sep= sep , end = "" , file = None , flush = flush)
            filetext = list(text)
            filetext.insert(0,self.prefix)
            WriteTofile(*filetext , sep=sep , end=end , file=file)
            if self.__LOG_COLOUR:
                print("\033[0m" , end = end, file = None , flush = flush)






class Log:
    __s_EngineLogger  :  LNLDebugLogger
    __s_GameLogger    :  LNLDebugLogger


    @staticmethod
    def Init():
        Log.__s_EngineLogger  = LNLDebugLogger("LOGIC-ENGINE", "./Game/LogicEngineOut/LoggerOutput/log.txt")        
        Log.__s_GameLogger    = LNLDebugLogger("LAYERS-N-LOGIC-GAME", "./Game/Layers_N_Logic_Game/LoggerOutput/log.txt")        

    @staticmethod
    def GetEngineLogger() -> LNLDebugLogger : return Log.__s_EngineLogger
    @staticmethod
    def GetGameLogger() -> LNLDebugLogger : return Log.__s_GameLogger












###     if not defined then dont bother printing anything

# create seperate logs for engine and game for better error handling.
def LNL_LogEngineTrace(*text, sep = " ", end = "\n", file = None, flush = False): ...
def LNL_LogEngineInfo(*text, sep = " ", end = "\n", file = None, flush = False): ...
def LNL_LogEngineWarning(*text, sep = " ", end = "\n", file = None, flush = False): ...
def LNL_LogEngineError(*text, sep = " ", end = "\n", file = None, flush = False): ...
def LNL_LogEngineFatal(*text, sep = " ", end = "\n", file = None, flush = False): ...

def LNL_LogTrace(*text, sep = " ", end = "\n", file = None, flush = False): ...
def LNL_LogInfo(*text, sep = " ", end = "\n", file = None, flush = False): ...
def LNL_LogWarning(*text, sep = " ", end = "\n", file = None, flush = False): ...
def LNL_LogError(*text, sep = " ", end = "\n", file = None, flush = False): ...
def LNL_LogFatal(*text, sep = " ", end = "\n", file = None, flush = False): ...





if LNL_LOGGER_DATA["LNL_DEBUG"]:
    if LNL_LOGGER_DATA["LNL_CURRENT_DEBUG_MINIMUM_LEVEL"]  <= LNL_LOGGER_DATA["LNL_DEBUG_MINIMUM_LEVEL"]["Trace"]:
        def LNL_LogEngineTrace(*text, sep = " ", end = "\n", file = None, flush = False):
            Log.GetEngineLogger().LNL_LogTrace(*text, sep=sep, end=end, file=file, flush=flush)
    if LNL_LOGGER_DATA["LNL_CURRENT_DEBUG_MINIMUM_LEVEL"]  <= LNL_LOGGER_DATA["LNL_DEBUG_MINIMUM_LEVEL"]["Info"]:
        def LNL_LogEngineInfo(*text, sep = " ", end = "\n", file = None, flush = False):
            Log.GetEngineLogger().LNL_LogInfo(*text, sep=sep, end=end, file=file, flush=flush)

    if LNL_LOGGER_DATA["LNL_CURRENT_DEBUG_MINIMUM_LEVEL"]  <= LNL_LOGGER_DATA["LNL_DEBUG_MINIMUM_LEVEL"]["Warning"]:
        def LNL_LogEngineWarning(*text, sep = " ", end = "\n", file = None, flush = False):
            Log.GetEngineLogger().LNL_LogWarning(*text, sep=sep, end=end, file=file, flush=flush)

    if LNL_LOGGER_DATA["LNL_CURRENT_DEBUG_MINIMUM_LEVEL"]  <= LNL_LOGGER_DATA["LNL_DEBUG_MINIMUM_LEVEL"]["Error"]:
        def LNL_LogEngineError(*text, sep = " ", end = "\n", file = None, flush = False):
            Log.GetEngineLogger().LNL_LogError(*text, sep=sep, end=end, file=file, flush=flush)
    
    if LNL_LOGGER_DATA["LNL_CURRENT_DEBUG_MINIMUM_LEVEL"]  <= LNL_LOGGER_DATA["LNL_DEBUG_MINIMUM_LEVEL"]["Fatal"]:       
        def LNL_LogEngineFatal(*text, sep = " ", end = "\n", file = None, flush = False):
            Log.GetEngineLogger().LNL_LogFatal(*text, sep=sep, end=end, file=file, flush=flush)



    if LNL_LOGGER_DATA["LNL_CURRENT_DEBUG_MINIMUM_LEVEL"]  <= LNL_LOGGER_DATA["LNL_DEBUG_MINIMUM_LEVEL"]["Trace"]:
        def LNL_LogTrace(*text, sep = " ", end = "\n", file = None, flush = False):
            Log.GetGameLogger().LNL_LogTrace(*text, sep=sep, end=end, file=file, flush=flush)

    if LNL_LOGGER_DATA["LNL_CURRENT_DEBUG_MINIMUM_LEVEL"]  <= LNL_LOGGER_DATA["LNL_DEBUG_MINIMUM_LEVEL"]["Info"]:
        def LNL_LogInfo(*text, sep = " ", end = "\n", file = None, flush = False):
            Log.GetGameLogger().LNL_LogInfo(*text, sep=sep, end=end, file=file, flush=flush)

    if LNL_LOGGER_DATA["LNL_CURRENT_DEBUG_MINIMUM_LEVEL"]  <= LNL_LOGGER_DATA["LNL_DEBUG_MINIMUM_LEVEL"]["Warning"]:
        def LNL_LogWarning(*text, sep = " ", end = "\n", file = None, flush = False):
            Log.GetGameLogger().LNL_LogWarning(*text, sep=sep, end=end, file=file, flush=flush)

    if LNL_LOGGER_DATA["LNL_CURRENT_DEBUG_MINIMUM_LEVEL"]  <= LNL_LOGGER_DATA["LNL_DEBUG_MINIMUM_LEVEL"]["Error"]:
        def LNL_LogError(*text, sep = " ", end = "\n", file = None, flush = False):
            Log.GetGameLogger().LNL_LogError(*text, sep=sep, end=end, file=file, flush=flush)

    if LNL_LOGGER_DATA["LNL_CURRENT_DEBUG_MINIMUM_LEVEL"]  <= LNL_LOGGER_DATA["LNL_DEBUG_MINIMUM_LEVEL"]["Fatal"]:
        def LNL_LogFatal(*text, sep = " ", end = "\n", file = None, flush = False):
            Log.GetGameLogger().LNL_LogFatal(*text, sep=sep, end=end, file=file, flush=flush)




















# #if debug is defined as true then call displays
#     if LNL_LOGGER_DATA["LNL_CURRENT_DEBUG_MINIMUM_LEVEL"]  <= LNL_LOGGER_DATA["LNL_DEBUG_MINIMUM_LEVEL"]["Trace"]:
#         def LNL_LogTrace(*text, sep = " ", end = "\n", file = None, flush = False):
#             if LNL_LOGGER_DATA["LNL_LOG_COLOUR"]:
#                 printCol("Trace")
#             WriteTofile(*text , sep= sep , end = end , file = LNL_LOGGER_DATA["LOG_FILE_PATH"])
#             Display(*text , sep= sep , end = "" , file = file , flush = flush)
#             if LNL_LOGGER_DATA["LNL_LOG_COLOUR"]:
#                 print("\033[0m" , end = end, file = file , flush = flush)
    
#     if LNL_LOGGER_DATA["LNL_CURRENT_DEBUG_MINIMUM_LEVEL"]  <= LNL_LOGGER_DATA["LNL_DEBUG_MINIMUM_LEVEL"]["Info"]:
#         def LNL_LogInfo(*text, sep = " ", end = "\n", file = None, flush = False):
#             if LNL_LOGGER_DATA["LNL_LOG_COLOUR"]:
#                 printCol("Info")
#             WriteTofile(*text , sep= sep , end = end , file = LNL_LOGGER_DATA["LOG_FILE_PATH"])
#             Display(*text , sep= sep , end = "" , file = file , flush = flush)
#             if LNL_LOGGER_DATA["LNL_LOG_COLOUR"]:
#                 print("\033[0m" , end = end, file = file , flush = flush)
    
#     if LNL_LOGGER_DATA["LNL_CURRENT_DEBUG_MINIMUM_LEVEL"]  <= LNL_LOGGER_DATA["LNL_DEBUG_MINIMUM_LEVEL"]["Warning"]:
#         def LNL_LogWarning(*text, sep = " ", end = "\n", file = None, flush = False):
#             if LNL_LOGGER_DATA["LNL_LOG_COLOUR"]:
#                 printCol("Warning")
#             WriteTofile(*text , sep= sep , end = end , file = LNL_LOGGER_DATA["LOG_FILE_PATH"])
#             Display(*text , sep= sep , end = "" , file = file , flush = flush)
#             if LNL_LOGGER_DATA["LNL_LOG_COLOUR"]:
#                 print("\033[0m" , end = end, file = file , flush = flush)
                
#     if LNL_LOGGER_DATA["LNL_CURRENT_DEBUG_MINIMUM_LEVEL"]  <= LNL_LOGGER_DATA["LNL_DEBUG_MINIMUM_LEVEL"]["Error"]:
#         def LNL_LogError(*text, sep = " ", end = "\n", file = None, flush = False):
#             if LNL_LOGGER_DATA["LNL_LOG_COLOUR"]:
#                 printCol("Error")
#             WriteTofile(*text , sep= sep , end = end , file = LNL_LOGGER_DATA["LOG_FILE_PATH"])
#             Display(*text , sep= sep , end = "" , file = file , flush = flush)
#             if LNL_LOGGER_DATA["LNL_LOG_COLOUR"]:
#                 print("\033[0m" , end = end, file = file , flush = flush)
    
#     if LNL_LOGGER_DATA["LNL_CURRENT_DEBUG_MINIMUM_LEVEL"]  <= LNL_LOGGER_DATA["LNL_DEBUG_MINIMUM_LEVEL"]["Fatal"]:
#         def LNL_LogFatal(*text, sep = " ", end = "\n", file = None, flush = False):
#             if LNL_LOGGER_DATA["LNL_LOG_COLOUR"]:
#                 printCol("Fatal")
#             WriteTofile(*text , sep= sep , end = end , file = LNL_LOGGER_DATA["LOG_FILE_PATH"] )
#             Display(*text , sep= sep , end = "" , file = None , flush = flush)
#             if LNL_LOGGER_DATA["LNL_LOG_COLOUR"]:
#                 print("\033[0m" , end = end, file = file , flush = flush)










Log.Init()

if __name__ == "__main__":
    
    TestLogger = LNLDebugLogger("DebugLogger")
    
    def testing():  # only defined if running this file
        word = "Variables"
        LNL_LogTrace("Simple && trace Test")
        LNL_LogInfo(f"Fstring && Info Test")
        LNL_LogWarning(f"f string with {word} && Warning Test")
        LNL_LogError("string as ","multiple arguments" , "&&" , "Error Test")
        LNL_LogFatal("Kwargs" , "&&" , "Fatal", "Test" , end="\n" , sep=" * ")

        LNL_LogEngineTrace("Simple && trace Test")
        LNL_LogEngineInfo(f"Fstring && Info Test")
        LNL_LogEngineWarning(f"f string with {word} && Warning Test")
        LNL_LogEngineError("string as ","multiple arguments" , "&&" , "Error Test")
        LNL_LogEngineFatal("Kwargs" , "&&" , "Fatal", "Test" , end="\n" , sep=" * ")
    
        word = "Variables"
        TestLogger.LNL_LogTrace("Simple && trace Test")
        TestLogger.LNL_LogInfo(f"Fstring && Info Test")
        TestLogger.LNL_LogWarning(f"f string with {word} && Warning Test")
        TestLogger.LNL_LogError("string as ","multiple arguments" , "&&" , "Error Test")
        TestLogger.LNL_LogFatal("Kwargs" , "&&" , "Fatal", "Test" , end="&" , sep=" * ")
    
    testing()
