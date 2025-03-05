# -*- coding: utf-8 -*-
import sys
import random 
import itertools
# On utilise un import relatif (`from . import common`)  
# pour s'assurer que le module est bien importé,  
# peu importe comment l'application est exécutée avec Flask.  
# Cela évite les erreurs liées aux imports absolus.  
from . import common

possible_combinations= set()
solution = ""
def init():
    """
    Cette fonction, appellée à chaque début de partie, initialise un certain nombre de
    variables utilisées par le codemaker
    """
    global solution, possible_combinations
    solution = ''.join(random.choices(common.COLORS, k=common.LENGTH))
    possible_combinations = set(map(''.join, itertools.product(common.COLORS, repeat = common.LENGTH)))

def codemaker(combinaison):
    """
    Cette fonction corrige la combinaison proposée par le codebreaker
    (donnée en argument)
    """
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
            
    
    

    