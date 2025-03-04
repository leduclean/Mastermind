#!/usr/bin/env python3

LENGTH = 4
COLORS = ['R', 'V', 'B', 'J', 'N', 'M', 'O', 'G']
import itertools

# Notez que vos programmes doivent continuer à fonctionner si on change les valeurs par défaut ci-dessus


def evaluation(arg, ref):
    assert len(arg) == len(ref), "Les deux combinaisons doivent avoir la même longueur"

    LENGTH = len(arg)
    bien_places = 0
    mal_places = 0

    # Étape 1 : Détection des bien placés
    reste_arg = []
    reste_ref = []

    for i in range(LENGTH):
        # assert arg[i] in COLORS, "Les couleurs en entré doivent être dans les couleurs disponibles"
        if arg[i] == ref[i]:
            bien_places += 1
        else:
            reste_arg.append(arg[i])
            reste_ref.append(ref[i])

    # Étape 2 : Détection des mal placés (présents mais mal placés)
    for couleur in reste_arg:
        if couleur in reste_ref:
            mal_places += 1
            reste_ref.remove(couleur)  # Empêche de compter une couleur plusieurs fois

    return bien_places, mal_places

"""
argument = ['E', 'G', 'Y', 'L', 'C']
ref = ['B', 'V', 'E', 'A', 'O']

evaluation(argument,ref)

argument = ['W', 'Q', 'A', 'T', 'N', 'S', 'C', 'I', 'E']
ref = ['Y', 'Q', 'H', 'G', 'D', 'T', 'J', 'J', 'I']

evaluation(argument,ref)


argument = ['Y', 'M', 'C', 'Y', 'S']
ref = ['Z', 'R', 'I', 'L', 'C']
evaluation(argument,ref)


argument = ['M', 'J', 'C', 'D', 'Y', 'O', 'T']
ref = ['T', 'M', 'K', 'Y', 'L', 'Q', 'J']
evaluation(argument,ref)

argument = ['E', 'G', 'N', 'F', 'H', 'C', 'J', 'V', 'U', 'N']
ref = ['U', 'S', 'S', 'S', 'I', 'Y', 'M', 'H', 'C', 'F']
evaluation(argument,ref)

argument = ['J', 'C', 'O', 'C', 'T', 'B']
ref = ['V', 'B', 'E', 'X', 'Q', 'G']
evaluation(argument,ref)
"""
