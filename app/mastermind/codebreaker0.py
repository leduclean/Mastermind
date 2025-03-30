#!/usr/bin/env python3

import random

# We use a relative import (`from . import common`)
# to ensure the module is correctly imported,
# regardless of how the application is executed with Flask.
# This prevents errors related to absolute imports.
from . import common


def init():
    """
    A function that does nothing... for this trivial version.
    For more advanced codebreakers, this is where you can initialize
    variables at the beginning of each game.
    """
    return


def codebreaker(evaluation_p: tuple):
    """
    The argument evaluation_p is the evaluation received for the last
    proposed combination (and is None if it's the first move of the game).
    This trivial version does not use this information, as it plays randomly.
    """
    return "".join(random.choices(common.COLORS, k=common.LENGTH))
