# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 12:46:54 2025

@author: Simon
"""
# We use a relative import (`from . import common`)
# to ensure that the module is imported correctly,
# regardless of how the application is run with Flask.
# This avoids issues related to absolute imports.
from . import common


def check_codemaker(log_file: str) -> bool:
    """Ensure the codemaker has not cheated during the game.

    Args:
        log_file (str): The log file of the played game.

    Raises:
        IndexError: If the log file is empty.
        ValueError: If the last line is not in the correct format.
        ValueError: In case the evaluation format is incorrect.

    Returns:
        bool: False if cheating or invalid format is detected, otherwise True.
    """
    with open(log_file, "r") as log:
        lines = log.readlines()

        # If the file is empty, raise an error.
        if not lines:
            raise IndexError("Empty log file.")

        # If the number of lines is odd, then the format is invalid.
        if len(lines) % 2 != 0:
            return False

        # Convert the last line to a tuple for comparison.
        try:
            last_eval = tuple(map(int, lines[-1].strip().strip("()").split(",")))
        except Exception as e:
            raise ValueError("Invalid format for the last line.") from e

        # If the last evaluation does not match (4, 0), return False.
        if last_eval != (4, 0):
            return False

        # Retrieve the cleaned solution from the second-to-last line.
        solution = lines[-2].strip()

        # Process each pair of lines (tried combination and its evaluation).
        for i in range(0, len(lines) - 1, 2):
            tried = lines[i].strip()
            try:
                # Convert the evaluation from the next line into a tuple
                # after removing the parentheses.
                ev = tuple(map(int, lines[i + 1].strip().strip("()").split(",")))
            except Exception as e:
                raise ValueError("Invalid evaluation format in log.") from e

            # If the evaluation does not match the expected evaluation, return False.
            if ev != common.evaluation(tried, solution):
                return False

    return True
