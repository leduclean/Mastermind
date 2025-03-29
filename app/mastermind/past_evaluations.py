from . import common

dict_backtracking = dict()
LENGTH = 0
COLORS = []


def reset_dict():
    global dict_backtracking, LENGTH, COLORS
    LENGTH = common.LENGTH
    COLORS = common.LENGTH
    dict_backtracking = dict()
