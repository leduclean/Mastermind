import matplotlib.pyplot as plt  # Import Matplotlib for visualization

from .play import get_codemaker_module, play


def show_histogram(codemaker_version: int, codebreaker_version: int, nbr_of_game: int):
    """
    Displays a histogram of the number of attempts required for a given version of a codebreaker
    to find the solution. Each game resets the codemaker to obtain a new solution.
    """
    if nbr_of_game <= 0:
        raise ValueError("Number of games must be positive.")

    results = []
    codemaker_module = get_codemaker_module(codemaker_version)

    for _ in range(nbr_of_game):
        codemaker_module.init()  # Generate a new solution for each game
        results.append(play(codemaker_version, codebreaker_version, False, True))

    plt.style.use("seaborn-v0_8-darkgrid")
    plt.hist(
        results,
        bins=range(min(results), max(results) + 2),
        align="left",
        edgecolor="black",
        color="skyblue",
    )
    plt.xlabel("Number of Attempts")
    plt.ylabel("Frequency")
    plt.title(
        f"Histogram of Attempts for Codebreaker {codebreaker_version} vs Codemaker {codemaker_version}"
    )
    plt.show()


def show_gain(codemaker_version: int, version1: int, version2: int, nbr_of_game: int):
    """
    Displays a scatter plot of the gain (difference in attempts) between two versions of a codebreaker.
    Each game initializes the codemaker only once so both codebreakers play on the same solution.
    """
    if nbr_of_game <= 0:
        raise ValueError("Number of games must be positive.")

    gains = []
    codemaker_module = get_codemaker_module(codemaker_version)

    for _ in range(nbr_of_game):
        codemaker_module.init()  # Ensure both codebreakers solve the same solution
        score1 = play(codemaker_version, version1, False, True)
        score2 = play(codemaker_version, version2, False, True)
        gains.append(score1 - score2)

    plt.style.use("seaborn-v0_8-darkgrid")
    plt.scatter(range(1, nbr_of_game + 1), gains, color="orange", alpha=0.7)
    plt.axhline(y=0, color="red", linestyle="--", linewidth=1)  # Baseline at y=0
    plt.xlabel("Game Number")
    plt.ylabel("Gain (Attempts Difference)")
    plt.title(
        f"Gain Between Codebreaker {version2} and Codebreaker {version1} vs Codemaker {codemaker_version}"
    )
    plt.show()


# Example usage:
if __name__ == "__main__":
    show_histogram(1, 1, 1000)  # Runs properly
    # show_gain(1, 3, 2, 10)  # Raises an error if codemaker0 is used with codebreaker2
