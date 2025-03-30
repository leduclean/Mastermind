#!/usr/bin/env python3
# Using a relative import (`from . import common`)
# to ensure the module is correctly imported, regardless of how the application is executed with Flask.
# This prevents issues related to absolute imports.
from . import common


def init():
    """Initialization function (currently does nothing)."""
    return


def codebreaker(__) -> str:
    """Prompts the user to enter a combination.

    Args:
        __: Placeholder argument for compatibility purposes.

    Returns:
        str: The valid combination entered by the user.
    """
    while True:
        combination = input("Enter combination: ")  # User input
        error_message = common.verif_combination(combination)  # Validity check

        if error_message:
            print(error_message)  # Displays error message if the combination is invalid
            continue

        return combination  # Returns the valid combination
