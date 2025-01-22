from include.Common import *

# used as default for some functions that take in lambdas / function ptrs
def nullFunc() -> None:
    return

def FindLowestAvailableFreeInt(data : dict , start : int = 0) -> int:
    """Gets the next free integer value in a dictionary,
    used to check a dictionary for the lowest available free integer

    Args:
        data (dict): the data that we are loking for the value in
        start (int): the first value that should be checked as free
    Returns:
        int: lowest free integer found
    """
    
    pass






## filehandling wrappers and utiliity

def LoadJson(pathToJson):
    """loads a json file into mem as a dictionary

    Args:
        pathToJson String / pathlike: path to destination json

    Returns:
        dict : json data
    """
    JsOut = None # init as none instead of an empty json for external error handling

    with open(pathToJson , "r") as jsonFile:
        JsOut = json.load(jsonFile)

    return JsOut