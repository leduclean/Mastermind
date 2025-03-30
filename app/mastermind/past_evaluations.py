from . import common

dict_backtracking = {}
LENGTH = 0
COLORS = []


def reset_dict():
    """Reset the backtracking dictionary and update global parameters."""
    global dict_backtracking, LENGTH, COLORS
    LENGTH = common.LENGTH
    COLORS = common.COLORS
    dict_backtracking.clear()
