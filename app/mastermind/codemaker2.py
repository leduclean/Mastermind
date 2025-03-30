# -*- coding: utf-8 -*-
import itertools
import random

from . import common, past_evaluations

possible_combinations = set()
permanent_combinations = set()
solution = ""


def init():
    """
    Initializes global variables at the beginning of each game.

    This function is called at the start of each game to:
    - Generate a new random solution.
    - Initialize the set of possible combinations.
    - Copy this set into `permanent_combinations` for future reference.
    """
    global solution, possible_combinations, permanent_combinations
    # Generates a random solution by choosing colors from `common.COLORS`
    solution = "".join(random.choices(common.COLORS, k=common.LENGTH))
    # Generates all possible permutations of color combinations
    possible_combinations = set(
        map("".join, itertools.product(common.COLORS, repeat=common.LENGTH))
    )
    # Copies `possible_combinations` into `permanent_combinations` for future reference
    permanent_combinations = possible_combinations.copy()

    if (
        past_evaluations.LENGTH != common.LENGTH
        or past_evaluations.LENGTH != common.LENGTH
    ):
        past_evaluations.reset_dict()


def codemaker(combination: str) -> tuple:
    """
    Main function of the codemaker. It updates possible combinations and selects a new
    solution that is difficult for the codebreaker to find.

    Args:
        combination (str): The combination proposed by the codebreaker.

    Returns:
        tuple[int, int]: The evaluation of the proposed combination, in the format
            (number of well-placed colors, number of misplaced colors).
    """
    global solution, permanent_combinations, possible_combinations

    # Evaluates the proposed combination against the current solution
    ev = common.evaluation(combination, solution)
    # Updates possible combinations based on the evaluation
    common.maj_possibles(possible_combinations, combination, ev)

    # Dictionary to store evaluation results and avoid redundant calculations
    best_combination = None  # Best combination found
    max_worst_case = -float("inf")  # Maximum worst-case size

    # Iterates through all possible combinations to find the one that maximizes the worst case
    for test_combination in possible_combinations:
        # Dictionary to group combinations by evaluation result
        evaluation_groups = {}

        for comb in permanent_combinations:
            # Checks if the evaluation has already been computed
            if (test_combination, comb) not in past_evaluations.dict_backtracking or (
                comb,
                test_combination,
            ) not in past_evaluations.dict_backtracking:
                # Computes the evaluation between `test_combination` and `comb`
                eval_result = common.evaluation(test_combination, comb)
                past_evaluations.dict_backtracking[(test_combination, comb)] = (
                    eval_result
                )
                past_evaluations.dict_backtracking[comb, test_combination] = eval_result
            else:
                # Retrieves the precomputed evaluation
                if (test_combination, comb) in past_evaluations.dict_backtracking:
                    eval_result = past_evaluations.dict_backtracking[
                        (test_combination, comb)
                    ]
                else:
                    eval_result = past_evaluations.dict_backtracking[
                        (comb, test_combination)
                    ]

            # Adds the combination to the corresponding evaluation group
            if eval_result not in evaluation_groups:
                evaluation_groups[eval_result] = []
            evaluation_groups[eval_result].append(comb)

        # Determines the size of the largest evaluation group (worst case)
        worst_case = max(len(group) for group in evaluation_groups.values())

        # If this combination increases the worst-case size, choose it
        if worst_case > max_worst_case:
            best_combination = test_combination
            max_worst_case = worst_case

    # Updates the solution with the best-found combination
    solution = best_combination
    # Prints the new solution (for debugging or verification)
    # print(solution)
    return ev
