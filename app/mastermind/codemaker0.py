#!/usr/bin/env python3
import random
import sys

# We use a relative import (`from . import common`)
# to ensure the module is correctly imported,
# regardless of how the application is executed with Flask.
# This avoids errors related to absolute imports.
from . import common


def init():
    """
    This function is called at the beginning of each game
    and initializes several variables used by the codemaker.
    """
    global solution
    solution = "".join(random.choices(common.COLORS, k=common.LENGTH))


def partial_evaluation(solution, combination):
    """
    This function is incorrect as it only implements a partial evaluation.

    Args:
        solution (str): The secret code.
        combination (str): The combination proposed by the codebreaker.

    Returns:
        tuple[int, int]: A tuple containing the number of well-placed pegs
                         and a placeholder zero (since the function is incomplete).
    """
    if len(solution) != len(combination):
        sys.exit("Error: The two combinations do not have the same length.")

    bp = 0  # Number of well-placed pegs
    for i in range(len(solution)):
        if solution[i] == combination[i]:
            bp += 1

    return (bp, 0)


def codemaker(combination):
    """
    This function evaluates the combination proposed by the codebreaker.

    Args:
        combination (str): The combination provided by the codebreaker.

    Returns:
        tuple[int, int]: The result of the evaluation.
    """
    global solution
    return partial_evaluation(solution, combination)
