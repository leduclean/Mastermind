#!/usr/bin/env python3
# Using a relative import (`from . import common`)
# to ensure the module is correctly imported, regardless of how the application is executed with Flask.
# This prevents issues related to absolute imports.
from . import common


def init():
    """Initialization function (currently does nothing)."""
    return


def codemaker(combination):
    """Prompts the user to manually evaluate a proposed combination.

    Args:
        combination (str): The combination proposed by the codebreaker.

    Returns:
        tuple: A tuple (bp, mp) where:
            - bp (int): Number of well-placed plots.
            - mp (int): Number of misplaced plots.
    """
    print("Proposed combination: {}".format(combination))

    # Get the number of well-placed plots
    while True:
        try:
            bp = int(input("Enter number of well-placed plots: "))
            if 0 <= bp <= common.LENGTH:
                break
            print("Invalid value (must be between 0 and {}).".format(common.LENGTH))
        except ValueError:
            continue

    # Get the number of misplaced plots
    while True:
        try:
            mp = int(input("Enter number of misplaced plots: "))
            if 0 <= mp <= common.LENGTH:
                break
            print("Invalid value (must be between 0 and {}).".format(common.LENGTH))
        except ValueError:
            continue

    return bp, mp
