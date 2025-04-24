#!/usr/bin/env python3

import itertools

# Are you testing the graphical interface?
# The interface will automatically handle changes to the game settings.
# You can change the code length (LENGTH) up to a maximum of 8,
# but you may only reduce the number of colors.

# Are you testing the function implementations?
# You’re free to adjust the game settings


# ============= GAME PARAMETERS =============

LENGTH = 4  # Max allowed value is 8 for graphic interphace
COLORS = ["R", "V", "B", "J", "N", "M", "O", "G"]

# ============================================


def verif_combination(combination: str):
    """Verifies the validity of the combination entered by the user.

    Args:
        combination (str): combination entered by the user

    Returns:
        str/None: error message if there is an error, else: None
    """
    if len(combination) != LENGTH:
        return f"invalid combination : length {len(combination)} supposed to be {LENGTH}"
    for c in combination:
        if c not in COLORS:
            return f"invalid combination : color {c} doesn't exist"
    return None  # No error

def evaluation(arg: str, ref: str) -> tuple[int, int]:
    """
    Compares two color combinations and returns the number of well-placed and misplaced colors.

    Args:
        arg (str): The combination proposed by the player.
        ref (str): The reference combination to be guessed.

    Returns:
        tuple[int, int]: A tuple containing:
            - The number of well-placed colors.
            - The number of misplaced colors (colors present but in the wrong position).

    Raises:
        AssertionError: If the two combinations do not have the same length.
    """
    error_arg = verif_combination(arg)
    error_ref = verif_combination(ref)

    if error_arg:
        raise AssertionError(error_arg)
    if error_ref:
        raise AssertionError(error_ref)

    LENGTH = len(arg)
    correctly_placed = 0  # Number of well-placed colors
    incorrectly_placed = 0  # Number of misplaced but present colors

    # Step 1: Detect well-placed colors
    rest_arg = []  # Store colors from `arg` that are not well-placed
    rest_ref = []  # Store colors from `ref` that are not well-placed

    for i in range(LENGTH):
        if arg[i] == ref[i]:
            correctly_placed += 1
        else:
            rest_arg.append(arg[i])
            rest_ref.append(ref[i])

    # Step 2: Detect misplaced but present colors
    for color in rest_arg:
        if color in rest_ref:
            incorrectly_placed += 1
            rest_ref.remove(color)  # Prevent counting a color more than once

    return correctly_placed, incorrectly_placed


all_permutations = set(
    map("".join, itertools.product(COLORS, repeat=LENGTH))
)  # Convert tuples to strings


def donner_possibles(tested_combination: str, associated_evaluation: tuple[int, int]) -> set[str]:
    """
    Returns a set of possible combinations that are consistent with the given evaluation.

    Args:
        tested_combination (str): The combination tested by the player.
        associated_evaluation (tuple[int, int]): The evaluation of the tested combination, as a tuple
            (number of well-placed colors, number of misplaced colors).

    Returns:
        set[str]: A set of possible combinations that match the given evaluation.
    """
    global all_permutations
    correctly_placed, incorrectly_placed = associated_evaluation

    possible_combination = set()  # Set to store the possible combinations

    for element in all_permutations:
        # Evaluate each combination in `all_permutations` against `tested_combination`
        cplaces, iplaces = evaluation(tested_combination, element)
        # Keep only the combinations that match the given evaluation
        if cplaces == correctly_placed and iplaces == incorrectly_placed:
            possible_combination.add(element)

    return possible_combination


def maj_possibles(possible_combinations: set[str], tested_combination: str, associated_evaluation: tuple[int, int]) -> None:
    """
    Updates the set of possible combinations based on the evaluation of a tested combination.

    Args:
        possible_combinations (set[str]): The current set of possible combinations.
        tested_combination (str): The combination tested by the player.
        associated_evaluation (tuple[int, int]): The evaluation of the tested combination, as a tuple
            (number of well-placed colors, number of misplaced colors).

    Returns:
        None: The function updates `possible_combinations` in place.
    """
    # Generate new possible combinations based on the evaluation
    new_possible_combinations = donner_possibles(
        tested_combination, associated_evaluation
    )
    # Update the set of possible combinations by keeping only those present in both sets
    possible_combinations.intersection_update(new_possible_combinations)
