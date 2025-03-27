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

import numpy as np
from PIL import Image



from ApplicationEngine.Logger.LNLEngineLogger import *



def get_file_contents(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        LNL_LogEngineError(f"File not found: {file_path}")
        return ""