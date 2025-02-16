from ApplicationEngine.include.Common import *

# class __Timer : ...

# used as default for some functions that take in lambdas / function ptrs
def nullFunc(*eatArgs : ..., **eatKewargs : ...) -> None: # type: ignore noqa
    return


def FindLowestAvailableFreeInt(data : dict [int , object], start : int = 0) -> int:
    """Gets the next free integer value in a dictionary,
    used to check a dictionary for the lowest available free integer

    Args:
        data (dict): the data that we are loking for the value in
        start (int): the first value that should be checked as free
    Returns:
        int: lowest free integer found
    """
    
    return 0






## filehandling wrappers and utiliity

def LoadJson(pathToJson : str) -> dict [str, object] | None:
    """Loads a json file into mem as a dictionary

    Args:
        pathToJson String / pathlike: path to destination json

    Returns:
        dict : json data
    """
    if (not os.path.exists(pathToJson)):
        print("Failed to load json from path : ", pathToJson , "  |  " ,os.path.abspath(pathToJson))
        return {}
    
    with open(pathToJson , "r") as jsonFile:
        JsOut = json.load(jsonFile)

    return JsOut


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb