# -*- coding: utf-8 -*-

import random
import common  # N'utilisez pas la syntaxe "form random import XXX"
import itertools

possible_combinations=[]
def init():
    #Initialise l'ensemble des valeurs possibles
    global possible_combinations
    possible_combinations=itertools.permutations(common.COLORS,common.LENGTH)



def codebreaker(evaluation_p):
    """
    L'argument evaluation_p est l'évaluation qu'on reçoit pour la dernière
    combinaison qu'on a proposée (et vaut None si c'est le premier coup de la
    partie). Cette version triviale n'utilise pas cette information, puisqu'elle joue au hasard.
    """
    
    global possible_combinations
    
    to_try = random.choice(list(possible_combinations))
    common.maj_possibles(possible_combinations, to_try, evaluation_p)
    
    return to_try

