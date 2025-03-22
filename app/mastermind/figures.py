from .play import get_codemaker_module, play
import matplotlib.pyplot as plt  # Assurez-vous d'avoir importé matplotlib si nécessaire

def show_histogram(codemaker_version: int, codebreaker_version: int, nbr_of_game: int):
    """
    Affiche un histogramme du nombre d'essais nécessaires pour qu'un codebreaker d'une version donnée
    trouve la solution. Pour chaque partie, on réinitialise le codemaker afin d'obtenir une nouvelle solution.
    """
    resultats = []
    codemaker_module = get_codemaker_module(codemaker_version)

    for _ in range(nbr_of_game):
        codemaker_module.init()  # Nouvelle solution pour chaque partie
        resultats.append(play(codemaker_version, codebreaker_version, False, True))

    plt.hist(resultats, bins=range(min(resultats), max(resultats) + 2), align='left', edgecolor='orange')
    plt.xlabel("Nombre d'essais")
    plt.ylabel("Fréquence")
    plt.title(f'Histogramme des essais pour codebreaker{codebreaker_version} contre codemaker{codemaker_version}')
    plt.show()

def show_gain(codemaker_version: int, version1: int, version2: int, nbr_of_game: int):
    """
    Affiche un diagramme de dispersion du gain (différence d'essais) entre deux versions de codebreaker.
    Pour chaque partie, le codemaker est initialisé une seule fois afin que les deux codebreaker jouent sur la même solution.
    """
    gains = []
    codemaker_module = get_codemaker_module(codemaker_version)

    for _ in range(nbr_of_game):
        codemaker_module.init()  # Même solution pour les deux codebreaker
        score1 = play(codemaker_version, version1, False, True)
        score2 = play(codemaker_version, version2, False, True)
        gains.append(score1 - score2)

    plt.scatter(range(1, nbr_of_game + 1), gains, color='orange')
    plt.xlabel('Numéro de partie')
    plt.ylabel('Gain')
    plt.title(f'Gain entre codebreaker{version2} et codebreaker{version1} contre codemaker{codemaker_version}')
    plt.show()

# Exemples d'utilisation :
if __name__ == "__main__":   
    # show_histogram(1, 2, 100)  # Fonctionnera
    show_gain(1, 1, 2, 100)     # Lève une erreur si codemaker0 est utilisé avec codebreaker2 
