import itertools

from . import common  # N'utilisez pas la syntaxe "form random import XXX"
from . import past_evaluations

permanent_combinations = set()
possible_combinations = set()
last_guess = None
Optimization = True


def first_guess():
    # Initialize the guess
    guess = []

    # Add colors in a cyclic manner to the guess, ensuring the length is met
    for i in range(common.LENGTH):
        guess.append(common.COLORS[i % len(common.COLORS)])

    # Join the list into a string and return as the guess
    return "".join(guess)


def init():
    # Initialise l'ensemble des valeurs possibles
    global possible_combinations, permanent_combinations, last_guess
    possible_combinations = set(
        map("".join, itertools.product(common.COLORS, repeat=common.LENGTH))
    )
    permanent_combinations = possible_combinations.copy()
    last_guess = None
    if (
        past_evaluations.LENGTH != common.LENGTH
        or past_evaluations.LENGTH != common.LENGTH
    ):
        past_evaluations.reset_dict()


def codebreaker(evaluation_p: tuple) -> str:
    """
    Génère une combinaison à essayer en minimisant l'espace des solutions possibles dans le pire des cas.

    Args:
        evaluation_p (tuple[int, int] | None): L'évaluation de la dernière combinaison proposée.
            Si c'est le premier essai, `evaluation_p` est `None`.

    Returns:
        str: Une combinaison à essayer, choisie pour minimiser l'espace des solutions possibles dans le pire des cas.
    """
    global possible_combinations, permanent_combinations, last_guess, Optimization  # Variables globales

    if evaluation_p is not None:
        # Met à jour l'ensemble des combinaisons possibles en fonction de l'évaluation précédente
        common.maj_possibles(possible_combinations, last_guess, evaluation_p)

    best_combination = None  # Meilleure combinaison trouvée
    min_worst_case = float("inf")  # Taille minimale du pire cas

    # Parcourt toutes les combinaisons dans `permanent_combinations` pour trouver celle qui minimise le pire cas
    if Optimization == True:
        if last_guess == None:

            last_guess = first_guess()
            return last_guess

    for test_combination in permanent_combinations:
        # Dictionnaire pour regrouper les combinaisons par résultat d'évaluation
        evaluation_groups = {}

        for comb in possible_combinations:
            # Vérifie si l'évaluation a déjà été calculée
            if (test_combination, comb) not in past_evaluations.dict_backtracking or (
                comb,
                test_combination,
            ) not in past_evaluations.dict_backtracking:
                # Calcule l'évaluation entre `test_combination` et `comb`
                eval_result = common.evaluation(test_combination, comb)
                past_evaluations.dict_backtracking[(test_combination, comb)] = (
                    eval_result
                )
                past_evaluations.dict_backtracking[(comb, test_combination)] = (
                    eval_result
                )
            else:

                # Récupère l'évaluation déjà calculée
                if (test_combination, comb) in past_evaluations.dict_backtracking:

                    eval_result = past_evaluations.dict_backtracking[
                        (test_combination, comb)
                    ]
                else:
                    eval_result = past_evaluations.dict_backtracking[
                        (comb, test_combination)
                    ]

            # Ajoute la combinaison au groupe correspondant à son évaluation
            if eval_result not in evaluation_groups:
                evaluation_groups[eval_result] = []
            evaluation_groups[eval_result].append(comb)

        # Détermine la taille du plus grand groupe d'évaluations (pire cas)
        worst_case = max(len(group) for group in evaluation_groups.values())

        # Si cette combinaison réduit l'espace plus que la précédente, on la choisit
        if worst_case < min_worst_case:
            best_combination = comb
            min_worst_case = worst_case

    # Sauvegarde la dernière combinaison essayée
    last_guess = best_combination
    # Retourne la meilleure combinaison trouvée
    return best_combination
