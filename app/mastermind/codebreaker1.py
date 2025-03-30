import random

# We use a relative import (`from . import common`)
# to ensure the module is correctly imported,
# regardless of how the application is executed with Flask.
# This prevents errors related to absolute imports.
from . import common

tried = set()


def init():
    """
    Initializes the set of attempted combinations at the start of each game.
    """
    global tried
    tried.clear()


def codebreaker(evaluation_p: tuple) -> str:
    """
    Generates a random combination that has not been attempted before.

    Args:
        evaluation_p (tuple[int, int]): The previous evaluation of the proposed combination.
            This argument is included for compatibility with test functions,
            but it is not used in this implementation.

    Returns:
        str: A random combination that has not been attempted before.
    """
    global tried  # Set of previously attempted combinations

    while True:
        # Generate a random combination by selecting colors from `common.COLORS`
        to_try = "".join(random.choices(common.COLORS, k=common.LENGTH))

        # Check if the combination has not been attempted before
        if to_try not in tried:
            # Add the combination to the set of attempted combinations
            tried.add(to_try)
            # Return the untried combination
            return to_try
