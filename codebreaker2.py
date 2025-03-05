# -*- coding: utf-8 -*-
import codemaker0
import random
import common  # N'utilisez pas la syntaxe "form random import XXX"
import itertools

possible_combinations = set()
last_guess = None

def init():
    #Initialise l'ensemble des valeurs possibles
    global possible_combinations, last_guess
    possible_combinations = set(map(''.join, itertools.product(common.COLORS, repeat = common.LENGTH)))
    last_guess = None


def codebreaker(evaluation_p: tuple) -> str:
    """
 
    """
    global possible_combinations, last_guess
    if evaluation_p is not None:
        # on filtre l'ensemble possibles selon l'évaluation du dernier coup.
        common.maj_possibles(possible_combinations, last_guess, evaluation_p)
        print(possible_combinations)
        
    # on choisi de manière aléatoire d'une combinaison parmi les possibilités restantes
    to_try = random.choice(list(possible_combinations))
    last_guess = to_try
    return to_try

