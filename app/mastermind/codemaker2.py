# -*- coding: utf-8 -*-
import random 
from . import common
from . import past_evaluations
import itertools


possible_combinations = set()
permanent_combinations = set()
solution = ""

def init():
    """
    Initialise les variables globales au début de chaque partie.

    Cette fonction est appelée à chaque début de partie pour :
    - Générer une nouvelle solution aléatoire.
    - Initialiser l'ensemble des combinaisons possibles.
    - Copier cet ensemble dans `permanent_combinations` pour référence future.
    """
    global solution, possible_combinations, permanent_combinations
    # Génère une solution aléatoire en choisissant des couleurs parmi `common.COLORS`
    solution = ''.join(random.choices(common.COLORS, k=common.LENGTH))
    # Génère toutes les permutations possibles de combinaisons de couleurs
    possible_combinations = set(map(''.join, itertools.product(common.COLORS, repeat=common.LENGTH)))
    # Copie de `possible_combinations` dans `permanent_combinations` pour référence future
    permanent_combinations = possible_combinations.copy()
    
    if past_evaluations.LENGTH != common.LENGTH or past_evaluations.LENGTH != common.LENGTH :
        past_evaluations.reset_dict()
    
    
    
def codemaker(combination: str) -> tuple:
    """
    Fonction principale du codemaker. Elle met à jour les combinaisons possibles et choisit une nouvelle solution
    difficile à trouver pour le codebreaker.

    Args:
        combination (str): La combinaison proposée par le codebreaker.

    Returns:
        tuple[int, int]: L'évaluation de la combinaison proposée, sous forme de tuple
            (nombre de couleurs bien placées, nombre de couleurs mal placées).
    """
    global solution, permanent_combinations, possible_combinations
    
    # Évalue la combinaison proposée par rapport à la solution actuelle
    ev = common.evaluation(combination, solution)
    # Met à jour les combinaisons possibles en fonction de l'évaluation
    common.maj_possibles(possible_combinations, combination, ev)
    
    # Dictionnaire pour stocker les résultats d'évaluation et éviter les calculs redondants
    
    best_combination = None  # Meilleure combinaison trouvée
    max_worst_case = -float('inf')  # Taille maximale du pire cas
    
    # Parcourt toutes les combinaisons possibles pour trouver celle qui maximise le pire cas
    for test_combination in possible_combinations:
        # Dictionnaire pour regrouper les combinaisons par résultat d'évaluation
        evaluation_groups = {}

        for comb in permanent_combinations:
            # Vérifie si l'évaluation a déjà été calculée
            if (test_combination, comb) not in past_evaluations.dict_backtracking or (comb, test_combination) not in past_evaluations.dict_backtracking:
                # Calcule l'évaluation entre `test_combination` et `comb`
                eval_result = common.evaluation(test_combination, comb)
                past_evaluations.dict_backtracking[(test_combination, comb)] = eval_result
                past_evaluations.dict_backtracking[comb,test_combination] = eval_result
            else:
                # Récupère l'évaluation déjà calculée
                if (test_combination,comb) in past_evaluations.dict_backtracking :
                    
                    
                    eval_result = past_evaluations.dict_backtracking[(test_combination, comb)]
                else :
                    eval_result = past_evaluations.dict_backtracking[(comb,test_combination)]
            
            # Ajoute la combinaison au groupe correspondant à son évaluation
            if eval_result not in evaluation_groups:
                evaluation_groups[eval_result] = []
            evaluation_groups[eval_result].append(comb)
        
        # Détermine la taille du plus grand groupe d'évaluations (pire cas)
        worst_case = max(len(group) for group in evaluation_groups.values())
        
        # Si cette combinaison augmente la taille du pire cas, on la choisit
        if worst_case > max_worst_case:
            best_combination = test_combination
            max_worst_case = worst_case
    
    # Met à jour la solution avec la meilleure combinaison trouvée
    solution = best_combination
    # Affiche la nouvelle solution (pour débogage ou vérification)
    print(solution)
    return ev


""" Version d'avant
def codemaker(combinaison):
    #On va prendre la combinaison dans les combinaisons possibles qui fait en sorte que lorsque qu'on choisit un element aleatoire, il y a aura le plus grand
    #nombre de nouvelles solutions
    
    
    #Initialisation comme dans codemaker1
    global solution
    ev = common.evaluation(combinaison, solution)
    common.maj_possibles(possible_combinations, combinaison, ev)
    
    
    #Partie Rouerie
    
    #Creation d'un dictionnaire pour associer les nouvelles solutions avec leur moyenne de taille de nouvelles solutions possibles avec chaque element de possible combinations
    dictionnary_best_solution = dict()
    
    for new_solution in possible_combinations :
        
        list_length_new_possible_combinations = []
        
        for new_tested_combination in possible_combinations :
            
            temp_possibles_combinations = possible_combinations.copy() # Niveau complexite c'est vraiment pas fou
            new_ev = common.evaluation(new_solution,new_tested_combination)
            common.maj_possibles(temp_possibles_combinations, new_tested_combination, new_ev)
            
            #On ajoute a une liste toutes les longueurs possibles avec chaque elements testables
            list_length_new_possible_combinations.append(len(temp_possibles_combinations))
        
        #On prend ensuite la moyenne
        average_new_possible_combinations = sum(list_length_new_possible_combinations) / len(list_length_new_possible_combinations)
    
        #On ajoute au dictionnaire avec la nouvelle solution envisagée (en tuple sinon ca marche pas en tant que cle)
        dictionnary_best_solution[tuple(new_solution)] = average_new_possible_combinations
    
    
    
    #On prend celui avec le plus grand nombre de solutions envisagées
    solution =  list(max(dictionnary_best_solution, key = dictionnary_best_solution.get))
    
    return ev
            
""" 
    

    