# type: ignore
 
import os
import sys
import json

# import serial
import threading

import queue

import random

from enum import Enum, auto
from abc  import ABC, abstractmethod  # enforce overriding

from ctypes import *


from ApplicationEngine.Logger.LNLEngineLogger import *