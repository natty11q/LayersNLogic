import ApplicationEngine.include.Common as Common
import struct

class Time:
    TimeScale = 0
    
    Deltatime = 0
    ScaledDeltatime = 0
    
    ScaledElapsedTime = 0
    TotalElapsedTime = 0
    
    
    
    # timers are handled with ids
    # Note :: Ids should never change until the function is complete
    Timers = {}
    
    
    def StartTimerMs(end = -1, endCall = None, frameCall = None, CallOnPhysicsThread = False) -> str:
        """_summary_

        Args:
            end (int, optional): the amount of time that the timer stays active. Defaults to -1 (does not terminate).
            endCall (_type_, optional): _description_. Defaults to None.
            frameCall (_type_, optional): _description_. Defaults to None.
            CallOnPhysicsThread (bool, optional): _description_. Defaults to False.

        Returns:
            str: returns the id for the timer in the dictionary
        """
        pass


    def StartTimerS(end = -1, endCall = None, frameCall = None, CallOnPhysicsThread = False) -> str:
        """_summary_

        Args:
            end (int, optional): the amount of time that the timer stays active. Defaults to -1 (does not terminate).
            endCall (_type_, optional): _description_. Defaults to None.
            frameCall (_type_, optional): _description_. Defaults to None.
            CallOnPhysicsThread (bool, optional): _description_. Defaults to False.

        Returns:
            str: returns the id for the timer in the dictionary
        """
        pass
    
    
    def EndTimer(ID : str):
        if ID not in Time.Timers.keys():
            return
        
        


class Timer:
    def __init__(self, type : str, Duration, endCall , frameCall, CallOnPhysicsThread):
        pass
    
    def terminate():
        pass