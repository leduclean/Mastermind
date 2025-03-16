#!/usr/bin/env python3

LENGTH = 4
COLORS = ['R', 'V', 'B', 'J', 'N', 'M', 'O', 'G']
import itertools

# Notez que vos programmes doivent continuer à fonctionner si on change les valeurs par défaut ci-dessus


def evaluation(arg: str, ref: str) -> tuple[int, int]:
    """
    Compare deux combinaisons de couleurs et retourne le nombre de couleurs bien placées et mal placées.

    Args:
        arg (str): La combinaison proposée par le joueur.
        ref (str): La combinaison de référence à deviner.

    Returns:
        tuple[int, int]: Un tuple contenant :
            - Le nombre de couleurs bien placées.
            - Le nombre de couleurs mal placées mais présentes dans la combinaison.

    Raises:
        AssertionError: Si les deux combinaisons n'ont pas la même longueur.
    """
    assert len(arg) == len(ref), "Les deux combinaisons doivent avoir la même longueur"

    LENGTH = len(arg)
    correctly_placed = 0  # Nombre de couleurs bien placées
    incorrectly_placed = 0  # Nombre de couleurs mal placées mais présentes

    # Étape 1 : Détection des couleurs bien placées
    rest_arg = []  # Stocke les couleurs de `arg` qui ne sont pas bien placées
    rest_ref = []  # Stocke les couleurs de `ref` qui ne sont pas bien placées

    for i in range(LENGTH):
        if arg[i] == ref[i]:
            correctly_placed += 1
        else:
            rest_arg.append(arg[i])
            rest_ref.append(ref[i])

    # Étape 2 : Détection des couleurs mal placées mais présentes
    for color in rest_arg:
        if color in rest_ref:
            incorrectly_placed += 1
            rest_ref.remove(color)  # Empêche de compter une couleur plusieurs fois

    return correctly_placed, incorrectly_placed


all_permutations = set(map(''.join,itertools.product(COLORS,repeat = LENGTH))) # On convertit les tuples en chaines de caractères

def donner_possibles(tested_combination: str, associated_evaluation: tuple[int, int]) -> set[str]:
    """
    Retourne un ensemble de combinaisons possibles qui sont cohérentes avec l'évaluation donnée.

    Args:
        tested_combination (str): La combinaison testée par le joueur.
        associated_evaluation (tuple[int, int]): L'évaluation de la combinaison testée, sous forme de tuple
            (nombre de couleurs bien placées, nombre de couleurs mal placées).

    Returns:
        set[str]: Un ensemble de combinaisons possibles qui correspondent à l'évaluation donnée.
    """
    global all_permutations
    correctly_placed, incorrectly_placed = associated_evaluation

    possible_combination = set()  # Ensemble pour stocker les combinaisons possibles

    for element in all_permutations:
        # On évalue chaque combinaison dans `all_permutations` par rapport à `tested_combination`
        cplaces, iplaces = evaluation(tested_combination, element)
        # On conserve uniquement les combinaisons qui correspondent à l'évaluation donnée
        if cplaces == correctly_placed and iplaces == incorrectly_placed:
            possible_combination.add(element)

    return possible_combination


def maj_possibles(possible_combinations: set[str], tested_combination: str, associated_evaluation: tuple[int, int]) -> None:
    """
    Met à jour l'ensemble des combinaisons possibles en fonction de l'évaluation d'une combinaison testée.

    Args:
        possible_combinations (set[str]): L'ensemble actuel des combinaisons possibles.
        tested_combination (str): La combinaison testée par le joueur.
        associated_evaluation (tuple[int, int]): L'évaluation de la combinaison testée, sous forme de tuple
            (nombre de couleurs bien placées, nombre de couleurs mal placées).

    Returns:
        None: La fonction modifie directement `possible_combinations` en place.
    """
    # On génère les nouvelles combinaisons possibles basées sur l'évaluation
    new_possible_combinations = donner_possibles(tested_combination, associated_evaluation)
    # On met à jour l'ensemble des combinaisons possibles en conservant uniquement celles qui sont dans les deux ensembles
    possible_combinations.intersection_update(new_possible_combinations)


#%% Partie Test
if __name__ == "__main__":
    donner_possibles(['R', 'V', 'B', 'J'],evaluation(['R', 'V', 'B', 'J'], 'RVBR'))


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





# %%
