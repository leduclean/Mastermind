#!/usr/bin/env python3

LENGTH = 5
COLORS = ['R', 'V', 'B', 'J', 'N', 'M', 'O', 'G']
import itertools

# Notez que vos programmes doivent continuer à fonctionner si on change les valeurs par défaut ci-dessus


def evaluation(arg, ref):
    assert len(arg) == len(ref), "Les deux combinaisons doivent avoir la même longueur"

    LENGTH = len(arg)
    correctly_placed = 0
    incorrectly_placed = 0

    # Étape 1 : Détection des bien placés
    rest_arg = []
    rest_ref = []

    for i in range(LENGTH):
        # assert arg[i] in COLORS, "Les couleurs en entré doivent être dans les couleurs disponibles"
        if arg[i] == ref[i]:
            correctly_placed += 1
        else:
            rest_arg.append(arg[i])
            rest_ref.append(ref[i])

    # Étape 2 : Détection des mal placés (présents mais mal placés)
    for color in rest_arg:
        if color in rest_ref:
            incorrectly_placed += 1
            rest_ref.remove(color)  # Empêche de compter une couleur plusieurs fois

    return correctly_placed , incorrectly_placed


#TO DO : Ajouter doc string et meilleur commentaires et tt

def donner_possibles(tested_combination: str, associated_evaluation: tuple) -> set:
    correctly_placed , incorrectly_placed = associated_evaluation
    #Faire un ensemble avec toutes les possibilites,
    all_permutations = set(map(''.join,itertools.product(COLORS,repeat = LENGTH))) # On convertit les tuples en chaines de caractères
    #Maintenant on va supprimer les combinaisons qui sont pas possibles et apres on aura l ensemble des combinaisons finales

    possible_combination = set()

    for element in all_permutations :
        #On regarde si le nombre de meme couleur, si c'est egal a bien_places+ mal_places c'est deja bien
        #Ensuite on regarde si le nombre de meme places = nombre bien places
        cplaces, iplaces = evaluation(tested_combination, element)
        if cplaces == correctly_placed and iplaces == incorrectly_placed:
            possible_combination.add(element)

    #print(liste_return)
    return possible_combination

# To DO : Commentaires
def maj_possibles(possible_combinations, tested_combination, associated_evaluation):
    new_possible_combinations = donner_possibles(tested_combination, associated_evaluation)
    possible_combinations.intersection_update(new_possible_combinations) # mets a jour directement le set avant le .intersectionupdate

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
