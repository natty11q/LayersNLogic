import ApplicationEngine.include.Common as Common # type: ignore noqa
import ApplicationEngine.src.Core.Utility.CoreUtility as Utility


from ApplicationEngine.src.Core.Utility.Filemanager import * 


import time
from typing import Callable


class LLEngineTime:

#------------- private:

    # inner class for timer
    class __Timer:
        def __init__(self, Duration : float, usesScaledTime : bool, endCall : Callable[[list [object]], None], endArgs : list [object], frameCall : Callable[[list [object]], None], frameArgs : list [object], callOnPhysicsThread : bool):
            self.__paused   : bool  = False
            self.__time     : float = 0
            self.__hasEnd   : bool  = (Duration != -1)
            self.__Duration : float = Duration
            
            self.__Finished : bool = False
            
            self.__usesScaledTime : bool = usesScaledTime
            
            self.__endCall : Callable[[list], None] = endCall       # type: ignore
            self.__endArgs : list = endArgs                         # type: ignore
            
            self.__frameCall : Callable[[list], None] = frameCall   # type: ignore
            self.__frameArgs : list = frameArgs                     # type: ignore
            
            self.__isPhysTimer : bool = callOnPhysicsThread
        
        def Update(self, dt : float):
            self.__time += dt
            if self.__time > self.__Duration:
                self.__time = self.__Duration
            
            self.__OnUpdate()
        
        def __OnUpdate(self):
            self.__frameCall(*self.__frameArgs)       # type: ignore
        
        def __OnTermination(self):
            self.__endCall(*self.__endArgs)           # type: ignore

        def IsComplete(self):
            self.__Finished = bool((self.__Duration < self.__time) * self.__hasEnd) # unnecessary conversion , i know dw
            return self.__Finished



        def Terminate(self):
            self.__OnTermination
        
        def Increment(self, Deltatime : float, timeScale : float):
            if self.__usesScaledTime:
                self.__time += Deltatime
            else:
                self.__time += Deltatime * timeScale
            
            self.__Finished = bool((self.__Duration < self.__time) * self.__hasEnd)

        
        def Pause(self):
            self.__paused = True
        
        def UnPause(self):
            self.__paused = False
        
        def IsPaused(self):
            return self.__paused
        
        def IsPhysTimer(self):
            return self.__isPhysTimer



#==================================================
    __TimeSettings = Utility.LoadJson( os.path.join( str(EngineFileManager.GetEnginePath("EngineSettingsRoot")) , "Graphics/graphicsSettings.json") ) 
    
    
    __BASE_TIME_SCALE : float = __TimeSettings.get("BASE_TIME_SCALE",1)         # type: ignore
    __TimeScale : float = __BASE_TIME_SCALE
    
    __Deltatime : float = 0
    __ScaledDeltatime   : float  = 0
    
    __TotalElapsedTime  : float  = 0
    __ScaledElapsedTime : float  = 0
    
    
    __BASE_TICK_RATE : float = __TimeSettings.get("BASE_TICK_RATE",60)          # type: ignore
    __TickRate : float = __BASE_TICK_RATE
    
    
    
    __TickCount : int = 0
    __FrameCount : int = 0
    
    __FPS : float = 0
    __FPS_CACHE : list [float] = [] # used to store the recent frame render times to find the current frame rate as an average
    __FPS_CACHE_SIZE : int = 120 # how many of the previous frames are we measuring

    

    __MAX_TIME_SCALE : float = 2 ** 32
    __MAX_TICK_RATE : float = 2 ** 32
    
    __MIN_TIME_SCALE : float = 0.0
    __MIN_TICK_RATE : float = 0.0
    
    
    __b_FRAMERATE_UNCAPPED = True
    __f_TARGET_FRAME_RATE : float = __TimeSettings.get("STARTING_TARGET_FRAMERATEE",120) # type: ignore
    __b_V_SYNC : bool = False

# init as this so that the first frame has a deltatime of 0 instead of a large number (due to time.time() - 0 on frame 1)
    __frameStart    : float  = time.process_time()
    __frameEnd      : float  = time.process_time()
    
    # timers are handled with ids
    # Note :: Ids should never change until the function is complete
    __Timers : dict [int , __Timer] = {}

    __FRAME_SLEEP_ALLOWANCE = 0.0005 / 1000  # slight reduction in waiting time to get as close to target framerate as possible

#========================================================================
   
    @staticmethod
    def __UpdateTimers():
        """
            Update all the timers that arent bound to a physics thread
            IE : called every render frame
        """
        for timer in LLEngineTime.__Timers.values():
            if not timer.IsPhysTimer():
                timer.Update(LLEngineTime.__Deltatime)
    @staticmethod
    def __UpdatePhysicsTimers():
        for timer in LLEngineTime.__Timers.values():
            if timer.IsPhysTimer():
                timer.Update(LLEngineTime.__Deltatime)
    @staticmethod
    def __UpdateFPS():
        if len(LLEngineTime.__FPS_CACHE) < LLEngineTime.__FPS_CACHE_SIZE:
            LLEngineTime.__FPS_CACHE.append(LLEngineTime.__Deltatime)
        else:
            LLEngineTime.__FPS = 1 / (sum(LLEngineTime.__FPS_CACHE) / LLEngineTime.__FPS_CACHE_SIZE) # caclulate average frames per second
            LLEngineTime.__FPS_CACHE = []
            print(f"fps : {LLEngineTime.FPS()}\n")
        
#--------------- public
    @staticmethod
    def TimeScale() -> float:
        return LLEngineTime.__TimeScale
    
    @staticmethod
    def ScaledDeltaTime() -> float:
        return LLEngineTime.__ScaledDeltatime
    
    @staticmethod
    def DeltaTime() -> float:
        return LLEngineTime.__Deltatime
    
    @staticmethod
    def Time() -> float:
        return LLEngineTime.__TotalElapsedTime
    
    @staticmethod
    def ScaledTime() -> float:
        return LLEngineTime.__ScaledElapsedTime
    
    @staticmethod
    def FPS() -> float:
        return LLEngineTime.__FPS
    
    @staticmethod
    def FrameCount() -> int:
        return LLEngineTime.__FrameCount
    
    @staticmethod
    def TickCount() -> int:
        return LLEngineTime.__TickCount
    
    @staticmethod
    def TickRate() -> float:
        return LLEngineTime.__BASE_TICK_RATE 
    
    @staticmethod
    def IsVsync() -> bool:
        return LLEngineTime.__b_V_SYNC
    
    @staticmethod
    def TargetFrameRate() -> float:
        return LLEngineTime.__f_TARGET_FRAME_RATE
    
    @staticmethod
    def SetTargetFramerate(framerate : float):
        if framerate > 0 + LLEngineTime.__FRAME_SLEEP_ALLOWANCE:
            LLEngineTime.__f_TARGET_FRAME_RATE = framerate
    
    ## TODO : add error handling or when an invalid value is input for the rates
    @staticmethod
    def SetTimeScale(scale : float) -> None:
        if scale < LLEngineTime.__MAX_TIME_SCALE and scale > LLEngineTime.__MIN_TIME_SCALE:
            LLEngineTime.__TimeScale = scale
    
    @staticmethod
    def SetPhysicsTickRate(newRate : float) -> None:
        if newRate > LLEngineTime.__MIN_TICK_RATE and newRate < LLEngineTime.__MAX_TICK_RATE:
            LLEngineTime.__TickRate = newRate
    
    @staticmethod    
    def SetVSync(VS : bool):
        LLEngineTime.__b_V_SYNC = VS
    
    @staticmethod
    def UnCapFramerate():
        LLEngineTime.__b_FRAMERATE_UNCAPPED = True
    
    @staticmethod
    def CapFramerate():
        LLEngineTime.__b_FRAMERATE_UNCAPPED = False

    @staticmethod
    def CustomSleep() -> bool:
        """custom sleep funciton to ensure that the program can be quit safley even if sleeping"""
        #TODO : impl
        return False

    @staticmethod
    def Update() -> None:
        
        
        # restrict the frame rate
        LLEngineTime.__frameEnd = time.process_time()
        
        # frameTime = Time.__frameEnd - Time.__frameStart
        if not LLEngineTime.__b_FRAMERATE_UNCAPPED:
            TargetFrameTime = (1/LLEngineTime.__f_TARGET_FRAME_RATE)

    
            WaitExit = False
            while time.process_time() - LLEngineTime.__frameStart < (TargetFrameTime - LLEngineTime.__FRAME_SLEEP_ALLOWANCE) and not WaitExit:
                WaitExit = LLEngineTime.CustomSleep()

        LLEngineTime.__frameEnd = time.process_time()
        LLEngineTime.__Deltatime        = LLEngineTime.__frameEnd - LLEngineTime.__frameStart
        LLEngineTime.__ScaledDeltatime  = LLEngineTime.__Deltatime * LLEngineTime.__TimeScale
        LLEngineTime.__TotalElapsedTime     += LLEngineTime.__Deltatime
        LLEngineTime.__ScaledElapsedTime    += LLEngineTime.__ScaledDeltatime

        # print("1/dt : " , ( 1 / Time.__Deltatime) , "\n")
        # print("")


        
        
        LLEngineTime.__UpdateFPS()
        LLEngineTime.__UpdateTimers()
        
        LLEngineTime.__frameStart = time.process_time()
    
    @staticmethod
    def PhysicsUpdate() -> None:
        LLEngineTime.__UpdatePhysicsTimers()
    
    
    @staticmethod
    def StartTimerMs(duration : float = -1.0, usesScaledTime : bool = False, endCall : Callable[[list [object]], None] =  Utility.nullFunc, endArgs : list [object]= [], frameCall : Callable[[list[object]], None] = Utility.nullFunc, frameArgs : list[object]= [], callOnPhysicsThread : bool= False) -> int:
        """Creates a timer in milliseconds

        Args:
            duration (int, optional): the amount of time that the timer stays active (milliseconds). Defaults to -1 (does not terminate).
            usesScaledTime  (bool, optional)): determines wether the timer is affected by the current timeescale
            endCall (function, optional): called on the frame that the timer fginishes. Defaults to nullFunction.
            endArgs (list [any], optional): arguments passed to the function that calls when the timer ends.
            frameCall (function, optional): called every frame of the timer's lifetime. Defaults to nullFunction.
            frameArgs (list [any], optional): arguments passed to the function that calls each frame.
            callOnPhysicsThread (bool, optional): determines wether the timer is called on render frames or physics ticks. Defaults to False.

        Returns:
            str: returns the id for the timer in the dictionary
        """
        
        TimerID = Utility.FindLowestAvailableFreeInt(LLEngineTime.__Timers) # type: ignore
        LLEngineTime.__Timers[TimerID] = LLEngineTime.__Timer(Duration= (duration / 1000), usesScaledTime= usesScaledTime, endCall= endCall, endArgs= endArgs, frameCall= frameCall, frameArgs= frameArgs, callOnPhysicsThread= callOnPhysicsThread)
        
        return TimerID


    @staticmethod
    def StartTimerS(duration : float = -1.0, usesScaledTime : bool = False, endCall : Callable[[list [object]], None] =  Utility.nullFunc, endArgs : list [object]= [], frameCall : Callable[[list[object]], None] = Utility.nullFunc, frameArgs : list[object]= [], callOnPhysicsThread : bool= False) -> int:
        """Creates a timer in seconds

        Args:
            duration (int, optional): the amount of time that the timer stays active (milliseconds). Defaults to -1 (does not terminate).
            usesScaledTime  (bool, optional)): determines wether the timer is affected by the current timeescale
            endCall (function, optional): called on the frame that the timer fginishes. Defaults to nullFunction.
            endArgs (list [any], optional): arguments passed to the function that calls when the timer ends.
            frameCall (function, optional): called every frame of the timer's lifetime. Defaults to nullFunction.
            frameArgs (list [any], optional): arguments passed to the function that calls each frame.
            callOnPhysicsThread (bool, optional): determines wether the timer is called on render frames or physics ticks. Defaults to False.

        Returns:
            str: returns the id for the timer in the dictionary
        """
        
        TimerID = Utility.FindLowestAvailableFreeInt(LLEngineTime.__Timers) # type: ignore
        LLEngineTime.__Timers[TimerID] = LLEngineTime.__Timer(Duration= duration, usesScaledTime= usesScaledTime, endCall= endCall, endArgs= endArgs, frameCall= frameCall, frameArgs= frameArgs, callOnPhysicsThread= callOnPhysicsThread)
        
        return TimerID


#provide an interface for the timers
    
    @staticmethod
    def EndTimer(ID : int) -> None:
        if ID not in LLEngineTime.__Timers.keys():
            return
        LLEngineTime.__Timers[ID].Terminate()
        del LLEngineTime.__Timers[ID]
    
    @staticmethod
    def PauseTimer(ID : int) -> None:
        if ID not in LLEngineTime.__Timers.keys():
            return
        LLEngineTime.__Timers[ID].Pause()
    
    @staticmethod
    def UnPauseTimer(ID : int) -> None:
        if ID not in LLEngineTime.__Timers.keys():
            return
        LLEngineTime.__Timers[ID].UnPause()

    @staticmethod    
    def IsTimerPaused(ID : int) -> None:
        if ID not in LLEngineTime.__Timers.keys():
            return
        LLEngineTime.__Timers[ID].IsPaused()

