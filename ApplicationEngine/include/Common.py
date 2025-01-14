import os
import sys
import json
import serial



# used as default for some functions that take in lambdas / function ptrs
def nullFunc() -> None:
    return