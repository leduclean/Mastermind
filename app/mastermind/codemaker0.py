#!/usr/bin/env python3
import random
import sys

# On utilise un import relatif (`from . import common`)
# pour s'assurer que le module est bien importé,
# peu importe comment l'application est exécutée avec Flask.
# Cela évite les erreurs liées aux imports absolus.
from . import common


def init():
    """
    Cette fonction, appellée à chaque début de partie, initialise un certain nombre de
    variables utilisées par le codemaker
    """
    global solution
    solution = "".join(random.choices(common.COLORS, k=common.LENGTH))


def evaluation_partielle(solution, combinaison):
    """
    Cette fonction n'est pas correcte, elle n'implémente qu'une évaluation partielle
    """
    if len(solution) != len(combinaison):
        sys.exit("Erreur : les deux combinaisons n'ont pas la même longueur")
    bp = 0  # Nombre de plots bien placés
    for i in range(len(solution)):
        if solution[i] == combinaison[i]:
            bp += 1
    return (bp, 0)


def codemaker(combinaison):
    """
    Cette fonction corrige la combinaison proposée par le codebreaker
    (donnée en argument)
    """
    global solution
    return evaluation_partielle(solution, combinaison)
