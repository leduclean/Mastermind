import random

# We use a relative import (`from . import common`)
# to ensure the module is correctly imported,
# regardless of how the application is executed with Flask.
# This avoids errors related to absolute imports.
from . import common


def init():
    """
    This function is called at the beginning of each game
    and initializes variables used by the codemaker.
    """
    global solution
    solution = "".join(random.choices(common.COLORS, k=common.LENGTH))


def codemaker(combination):
    """
    This function evaluates the combination proposed by the codebreaker.

    Args:
        combination (str): The combination provided by the codebreaker.

    Returns:
        tuple[int, int]: The result of the evaluation.
    """
    global solution
    return common.evaluation(combination, solution)
