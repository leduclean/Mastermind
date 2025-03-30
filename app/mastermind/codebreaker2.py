# -*- coding: utf-8 -*-

import itertools
import random

# We use a relative import (`from . import common`)
# to ensure the module is correctly imported,
# regardless of how the application is executed with Flask.
# This prevents errors related to absolute imports.
from . import common  # Do not use the syntax "from random import XXX"

possible_combinations = set()
last_guess = None


def init():
    """
    Initializes the set of possible combinations at the start of each game.
    """
    global possible_combinations, last_guess
    possible_combinations = set(
        map("".join, itertools.product(common.COLORS, repeat=common.LENGTH))
    )
    last_guess = None


def codebreaker(evaluation_p: tuple) -> str:
    """
    Generates a combination to try based on the previous evaluation.

    Args:
        evaluation_p (tuple[int, int] | None): The evaluation of the last proposed combination.
            If this is the first attempt, `evaluation_p` is `None`.

    Returns:
        str: A combination to try, randomly chosen from the remaining possible combinations.
    """
    global possible_combinations, last_guess

    if evaluation_p is not None:
        # Updates the set of possible combinations based on the previous evaluation
        common.maj_possibles(possible_combinations, last_guess, evaluation_p)

    # Chooses a random combination from the remaining possible combinations
    to_try = random.choice(list(possible_combinations))
    # Saves the last attempted combination
    last_guess = to_try
    # Returns the chosen combination
    return to_try
