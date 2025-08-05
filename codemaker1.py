import sys
import random 
import common

def init():
    """
    Cette fonction, appellée à chaque début de partie, initialise un certain nombre de
    variables utilisées par le codemaker
    """
    global solution
    solution = ''.join(random.choices(common.COLORS, k=common.LENGTH))


def codemaker(combinaison):
    """
    Cette fonction corrige la combinaison proposée par le codebreaker
    (donnée en argument)
    """
    global solution
    return common.evaluation(combinaison, solution)
