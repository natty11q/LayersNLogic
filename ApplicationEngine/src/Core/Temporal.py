import include.Common as Common
import src.Core.utility as Utility

import time




class Time:

#------------- private:

    # inner class for timer
    class __Timer:
        def __init__(self, Duration, usesScaledTime, endCall, endArgs, frameCall, frameArgs, callOnPhysicsThread):
            self.__paused   : bool  = False
            self.__time     : float = 0
            self.__hasEnd   : bool  = (Duration != -1)
            self.__Duration : float = Duration
            
            self.__Finished : bool = False
            
            self.__usesScaledTime : bool = usesScaledTime
            
            self.__endCall : function = endCall
            self.__endArgs : list = endArgs
            
            self.__frameCall : function = frameCall
            self.__frameCall : list = frameArgs
            
            self.__isPhysTimer : bool = callOnPhysicsThread
        
        def Update(self, dt):
            self.__time += dt
            if self.__time > self.__Duration:
                self.__time = self.__Duration
            
            self.__OnUpdate()
        
        def __OnUpdate(self):
            self.__frameCall(*self.__frameArgs)
        
        def __OnTermination(self):
            self.__endCall(*self.__endArgs)

        def IsComplete(self):
            self.__Finished = (self.__Duration < self.__time) * self.__hasEnd
            return self.__Finished



        def Terminate(self):
            self.__OnTermination
        
        def Increment(self, Deltatime, timeScale):
            if self.__usesScaledTime:
                self.__time += Deltatime
            else:
                self.__time += Deltatime * timeScale
            
            self.__Finished = (self.__Duration < self.__time) * self.__hasEnd

        
        def Pause(self):
            self.__paused = True
        
        def UnPause(self):
            self.__paused = False
        
        def IsPaused(self):
            return self.__paused
        
        def IsPhysTimer(self):
            return self.__isPhysTimer



#==================================================
    
    __BASE_TIME_SCALE : float = 1.0
    __TimeScale : float = __BASE_TIME_SCALE
    
    __Deltatime : float = 0
    __ScaledDeltatime   : float  = 0
    
    __TotalElapsedTime  : float  = 0
    __ScaledElapsedTime : float  = 0
    
    
    __BASE_TICK_RATE : float = 60
    __TickRate : int = 60
    
    
    
    __TickCount : int = 0
    __FrameCount : int = 0
    
    __FPS : float = 0
    __FPS_CACHE : list [float] = [] # used to store the recent frame render times to find the current frame rate as an average
    __FPS_CACHE_SIZE : int = 120 # how many of the previous frames are we measuring

    

    __MAX_TIME_SCALE : float = 2 ** 32
    __MAX_TICK_RATE : float = 2 ** 32
    
    __MIN_TIME_SCALE : float = 0.0
    __MIN_TICK_RATE : float = 0.0
    
    
    __TARGET_FRAME_RATE : float = 120
    __V_SYNC : bool = False

# init as this so that the first frame has a deltatime of 0 instead of a large number (due to time.time() - 0 on frame 1)
    __frameStart    : float  = time.time()
    __frameEnd      : float  = time.time()
    
    
    # timers are handled with ids
    # Note :: Ids should never change until the function is complete
    __Timers : dict = {}


    
    def __UpdateTimers():
        for timer in Time.__Timers.values():
            if not timer.IsPhysTimer():
                timer.Update(Time.__Deltatime)

    def __UpdatePhysicsTimers():
        for timer in Time.__Timers.values():
            if timer.IsPhysTimer():
                timer.Update(Time.__Deltatime)
    
    def __UpdateFPS():
        if len(Time.__FPS_CACHE) < Time.__FPS_CACHE_SIZE:
            Time.__FPS_CACHE.append(Time.__Deltatime)
        else:
            Time.__FPS = 1 / (sum(Time.__FPS_CACHE) / Time.__FPS_CACHE_SIZE) # caclulate average frames per second
            Time.__FPS_CACHE = []
        
#--------------- public

    def TimeScale() -> float:
        return Time.__TimeScale
    def ScaledDeltaTime() -> float:
        return Time.__ScaledDeltatime
    def DeltaTime() -> float:
        return Time.__Deltatime
    def Time() -> float:
        return Time.__TotalElapsedTime
    def ScaledTime() -> float:
        return Time.__ScaledElapsedTime
    def FPS() -> float:
        return Time.__FPS
    def FrameCount() -> int:
        return Time.__FrameCount
    def TickCount() -> int:
        return Time.__TickCount
    def IsVsync() -> bool:
        return Time.__V_SYNC
    def TimeScale() -> float:
        return Time.__TimeScale
    
    
    def SetTimeScale(scale : float) -> None:
        Time.__TimeScale = scale
    def SetPhysicsTickRate(newRate : float) -> None:
        if newRate > Time.__MIN_TICK_RATE and newRate < Time.__MAX_TICK_RATE:
            Time.__TickRate = newRate
            return
        
        Time.__TickRate = Time.__BASE_TICK_RATE
    def SetVSync(VS):
        Time.__V_SYNC = VS
    
    


    def Update() -> None:
        Time.__frameEnd = time.time()

        Time.__Deltatime        = Time.__frameEnd - Time.__frameStart
        Time.__ScaledDeltatime  = Time.__Deltatime * Time.__TimeScale
        Time.__TotalElapsedTime     += Time.__Deltatime
        Time.__ScaledElapsedTime    += Time.__ScaledDeltatime


        Time.__frameStart = time.time()

        
        
        Time.__UpdateFPS()
        Time.__UpdateTimers()
    
    def PhysicsUpdate() -> None:
        Time.__UpdatePhysicsTimers()
    
    
    def StartTimerMs(duration = -1, usesScaledTime = False, endCall =  Utility.nullFunc, endArgs = [], frameCall = Utility.nullFunc, frameArgs = [], callOnPhysicsThread = False) -> int:
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
        
        TimerID = Utility.FindLowestAvailableFreeInt(Time.__Timers)
        Time.__Timers[TimerID] = Time.__Timer(Duration= (duration / 1000), usesScaledTime= usesScaledTime, endCall= endCall, endArgs= endArgs, frameCall= frameCall, frameArgs= frameArgs, callOnPhysicsThread= callOnPhysicsThread)
        
        return TimerID


    def StartTimerS(duration = -1, usesScaledTime = False, endCall =  Utility.nullFunc, endArgs = [], frameCall = Utility.nullFunc, frameArgs = [], callOnPhysicsThread = False) -> int:
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
        
        TimerID = Utility.FindLowestAvailableFreeInt(Time.__Timers)
        Time.__Timers[TimerID] = Time.__Timer(Duration= duration, usesScaledTime= usesScaledTime, endCall= endCall, endArgs= endArgs, frameCall= frameCall, frameArgs= frameArgs, callOnPhysicsThread= callOnPhysicsThread)
        
        return TimerID


#provide an interface for the timers
    
    def EndTimer(ID : str) -> None:
        if ID not in Time.__Timers.keys():
            return
        Time.__Timers[ID].Terminate()
        del Time.__Timers[ID]
    
    
    def PauseTimer(ID : str) -> None:
        if ID not in Time.__Timers.keys():
            return
        Time.__Timers[ID].Pause()
    
    def UnPauseTimer(ID : str) -> None:
        if ID not in Time.__Timers.keys():
            return
        Time.__Timers[ID].UnPause()
    
    def IsTimerPaused(ID : str) -> None:
        if ID not in Time.__Timers.keys():
            return
        Time.__Timers[ID].IsPaused()

