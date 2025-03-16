# -*- coding: utf-8 -*-

import random
import itertools
# On utilise un import relatif (`from . import common`)  
# pour s'assurer que le module est bien importé,  
# peu importe comment l'application est exécutée avec Flask.  
# Cela évite les erreurs liées aux imports absolus.  
from . import common  # N'utilisez pas la syntaxe "form random import XXX"


possible_combinations = set()
last_guess = None

possible_combinations = set()
last_guess = None

def init():
    #Initialise l'ensemble des valeurs possibles
    global possible_combinations, last_guess
    possible_combinations = set(map(''.join, itertools.product(common.COLORS, repeat = common.LENGTH)))
    last_guess = None


def codebreaker(evaluation_p: tuple) -> str:
    """
    Génère une combinaison à essayer en fonction de l'évaluation précédente.

    Args:
        evaluation_p (tuple[int, int] | None): L'évaluation de la dernière combinaison proposée.
            Si c'est le premier essai, `evaluation_p` est `None`.

    Returns:
        str: Une combinaison à essayer, choisie aléatoirement parmi les combinaisons possibles restantes.
    """
    global possible_combinations, last_guess 
    
    if evaluation_p is not None:
        # Met à jour l'ensemble des combinaisons possibles en fonction de l'évaluation précédente
        common.maj_possibles(possible_combinations, last_guess, evaluation_p)
        
    # Choisit une combinaison aléatoire parmi les combinaisons possibles restantes
    to_try = random.choice(list(possible_combinations))
    # Sauvegarde la dernière combinaison essayée
    last_guess = to_try
    # Retourne la combinaison choisie
    return to_try
