#!/usr/bin/env python3
import importlib

from . import common


# TODO: change comments to English
def get_codebreaker_module(version: int):
    """Dynamically imports the codebreaker module for the given version."""
    try:
        return importlib.import_module(f"app.mastermind.codebreaker{version}")
    except ImportError:
        raise ValueError(f"Module codebreaker{version} not found.")


def get_codemaker_module(version: int):
    """Dynamically imports the codemaker module for the given version."""
    try:
        return importlib.import_module(f"app.mastermind.codemaker{version}")
    except ImportError:
        raise ValueError(f"Module codemaker{version} not found.")


def check_compatibility(codemaker_version: int, codebreaker_version: int):
    """
    Checks that the codemaker/codebreaker pair is compatible.
    Raises an error if you try to play with codemaker0 and codebreaker2,
    as codebreaker2 requires a full evaluation.
    """

    if (codemaker_version, codebreaker_version) == (0, 2):
        raise ValueError(
            "Incompatibility detected: codebreaker2 requires a full evaluation and cannot be used with codemaker0."
        )


def play(
    codemaker_version: int,
    codebreaker_version: int,
    reset_solution=True,
    quiet=False,
    output=print,
    get_input=None,
) -> int:
    """
    Plays a game for a given codebreaker.

    This is an automatic mode, get_input stays None, and the codebreaker generates its combinations.
    """
    check_compatibility(codemaker_version, codebreaker_version)
    codemaker_module = get_codemaker_module(codemaker_version)
    codebreaker_module = get_codebreaker_module(codebreaker_version)

    if reset_solution:
        codemaker_module.init()
    codebreaker_module.init()

    ev = None
    nbr_of_try = 0

    if not quiet:
        output(
            "Combinations of size {} with available colors: {}".format(
                common.LENGTH, common.COLORS
            )
        )

    while True:
        # If get_input is defined, use it to get the input,
        # otherwise, the codebreaker automatically generates its combination.
        if get_input is not None:
            combination = get_input(ev)
        else:
            combination = codebreaker_module.codebreaker(ev)

        ev = codemaker_module.codemaker(combination)
        nbr_of_try += 1

        if not quiet:
            output(
                "Attempt {}: {} ({} correct, {} incorrect)".format(
                    nbr_of_try, combination, ev[0], ev[1]
                )
            )

        if ev[0] >= common.LENGTH:
            if not quiet:
                output(
                    "Congratulations! Found {} in {} attempts".format(
                        combination, nbr_of_try
                    )
                )
            return nbr_of_try


class FileLogger:
    """
    Logger that writes messages to a text file.
    """

    def __init__(self, log_file: str):
        # The log file is constructed from the provided path and name.
        self.log_file = f"app\\logs\\{log_file}.txt"

    def __call__(self, message: str):
        # Opens the file in "append" mode to add the message with a newline.
        with open(self.log_file, "a") as f:
            f.write(message + "\n")


def play_log(
    codemaker_version,
    codebreaker_version: int,
    log_file: str,
    reset_solution=True,
    quiet=False,
    output_func=None,
    human_solution=False,
) -> int:
    """
    Plays a game for a codebreaker with the solution already initialized.
    The codebreaker is reset for each game, while the codemaker keeps the solution.

    The output (logs) is done via the output function passed as a parameter.
    By default, if no function is provided, the logs are written to a text file using FileLogger.
        int: number of attempts made.
    """
    check_compatibility(codemaker_version, codebreaker_version)

    if not human_solution:
        codemaker_module = get_codemaker_module(codemaker_version)
        # Reset the solution and codebreaker
        if reset_solution:
            codemaker_module.init()

    codebreaker_module = get_codebreaker_module(codebreaker_version)
    codebreaker_module.init()

    if output_func is None:
        output_func = FileLogger(log_file)

    ev = None
    nbr_of_try = 0

    if not quiet:
        print(
            "Combinations of size {}, available colors {}".format(
                common.LENGTH, common.COLORS
            )
        )

    while True:
        combination = codebreaker_module.codebreaker(ev)
        ev = (
            common.evaluation(combination, human_solution)
            if human_solution
            else codemaker_module.codemaker(combination)
        )
        nbr_of_try += 1

        # Log the output via output_func
        output_func(combination)
        output_func(f"{ev[0]},{ev[1]}")

        if not quiet:
            print(f"Attempt {nbr_of_try}: {combination} ({ev[0]},{ev[1]})")

        if ev[0] >= common.LENGTH:
            if not quiet:
                print(f"Congratulations! Found {combination} in {nbr_of_try} attempts")
            return nbr_of_try


# To avoid executing these functions during imports
if __name__ == "__main__":
    print("This play.py file is executed directly.")
    # call functions here
    play_log(0, 2, "none")
