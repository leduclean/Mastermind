import itertools

from . import common  # Do not use the syntax "from random import XXX"
from . import past_evaluations

permanent_combinations = set()
possible_combinations = set()
last_guess = None
Optimization = True


def first_guess():
    """
    Generates the first guess using a cyclic pattern of colors.

    Returns:
        str: A combination of colors as the first guess.
    """
    # Initialize the guess
    guess = []

    # Add colors in a cyclic manner to the guess, ensuring the length is met
    for i in range(common.LENGTH):
        guess.append(common.COLORS[i % len(common.COLORS)])

    # Join the list into a string and return as the guess
    return "".join(guess)


def init():
    """
    Initializes the set of possible values at the start of each game.
    Also resets the evaluation dictionary if needed.
    """
    global possible_combinations, permanent_combinations, last_guess
    possible_combinations = set(
        map("".join, itertools.product(common.COLORS, repeat=common.LENGTH))
    )
    permanent_combinations = possible_combinations.copy()
    last_guess = None

    # Reset past evaluations if the stored length does not match the current game length
    if (
        past_evaluations.LENGTH != common.LENGTH
        or past_evaluations.LENGTH != common.LENGTH
    ):
        past_evaluations.reset_dict()


def codebreaker(evaluation_p: tuple) -> str:
    """
    Generates a combination to try, minimizing the solution space in the worst-case scenario.

    Args:
        evaluation_p (tuple[int, int] | None): The evaluation of the last proposed combination.
            If this is the first attempt, `evaluation_p` is `None`.

    Returns:
        str: A combination chosen to minimize the worst-case solution space.
    """
    global possible_combinations, permanent_combinations, last_guess, Optimization  # Global variables

    if evaluation_p is not None:
        # Updates the set of possible combinations based on the previous evaluation
        common.maj_possibles(possible_combinations, last_guess, evaluation_p)

    best_combination = None  # Best combination found
    min_worst_case = float("inf")  # Minimum size of the worst case

    # Find the combination that minimizes the worst-case scenario
    if Optimization:
        if last_guess is None:
            last_guess = first_guess()
            return last_guess

    for test_combination in permanent_combinations:
        # Dictionary to group combinations by evaluation result
        evaluation_groups = {}

        for comb in possible_combinations:
            # Check if the evaluation has already been calculated
            if (test_combination, comb) not in past_evaluations.dict_backtracking or (
                comb,
                test_combination,
            ) not in past_evaluations.dict_backtracking:
                # Compute the evaluation between `test_combination` and `comb`
                eval_result = common.evaluation(test_combination, comb)
                past_evaluations.dict_backtracking[(test_combination, comb)] = (
                    eval_result
                )
                past_evaluations.dict_backtracking[(comb, test_combination)] = (
                    eval_result
                )
            else:
                # Retrieve the previously calculated evaluation
                if (test_combination, comb) in past_evaluations.dict_backtracking:
                    eval_result = past_evaluations.dict_backtracking[
                        (test_combination, comb)
                    ]
                else:
                    eval_result = past_evaluations.dict_backtracking[
                        (comb, test_combination)
                    ]

            # Add the combination to the group corresponding to its evaluation
            if eval_result not in evaluation_groups:
                evaluation_groups[eval_result] = []
            evaluation_groups[eval_result].append(comb)

        # Determine the size of the largest evaluation group (worst case)
        worst_case = max(len(group) for group in evaluation_groups.values())

        # If this combination reduces the search space more than the previous best, choose it
        if worst_case < min_worst_case:
            best_combination = comb
            min_worst_case = worst_case

    # Save the last attempted combination
    last_guess = best_combination
    # Return the best combination found
    return best_combination
