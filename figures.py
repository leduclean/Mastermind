import importlib
import common
import matplotlib.pyplot as plt

def get_codebreaker_module(version: int):
    """Importe dynamiquement le module codebreaker de la version donnée."""
    try:
        return importlib.import_module(f"codebreaker{version}")
    except ImportError:
        raise ValueError(f"Module codebreaker{version} non trouvé.")

def get_codemaker_module(version: int):
    """Importe dynamiquement le module codemaker de la version donnée."""
    try:
        return importlib.import_module(f"codemaker{version}")
    except ImportError:
        raise ValueError(f"Module codemaker{version} non trouvé.")

def check_compatibility(codemaker_version: int, codebreaker_version: int):
    """
    Vérifie que le couple codemaker/codebreaker est compatible.
    On lève une erreur si l'on tente de jouer codemaker0 avec codebreaker2,
    car codebreaker2 a besoin d'une évaluation complète.
    """
    if codemaker_version == 0 and codebreaker_version == 2:
        raise ValueError("Incompatibilité détectée : codebreaker2 nécessite une évaluation complète et ne peut pas être utilisé avec codemaker0.")

def play_game(codemaker_module, codebreaker_module, codemaker_version: int, codebreaker_version: int) -> int:
    """
    Joue une partie pour un codebreaker donné sur la solution déjà initialisée dans le module codemaker.
    Le codebreaker est réinitialisé pour chaque partie, tandis que le codemaker conserve la solution.
    """
    check_compatibility(codemaker_version, codebreaker_version)
    
    codebreaker_module.init()  # Réinitialisation du codebreaker
    nbr_of_try = 0
    maker_evaluation = None

    # Premier coup
    proposition = codebreaker_module.codebreaker(maker_evaluation)
    maker_evaluation = codemaker_module.codemaker(proposition)
    nbr_of_try += 1

    while maker_evaluation[0] != common.LENGTH:
        nbr_of_try += 1
        proposition = codebreaker_module.codebreaker(maker_evaluation)
        maker_evaluation = codemaker_module.codemaker(proposition)

    return nbr_of_try

def get_number_of_try(codemaker_version: int, codebreaker_version: int) -> int:
    """
    Renvoie le nombre d'essais nécessaires pour qu'un codebreaker (version donnée)
    trouve la solution présente dans le module codemaker (déjà initialisé).
    """
    check_compatibility(codemaker_version, codebreaker_version)
    codebreaker_module = get_codebreaker_module(codebreaker_version)
    codemaker_module = get_codemaker_module(codemaker_version)
    return play_game(codemaker_module, codebreaker_module, codemaker_version, codebreaker_version)

def show_histogram(codemaker_version: int, codebreaker_version: int, nbr_of_game: int):
    """
    Affiche un histogramme du nombre d'essais nécessaires pour qu'un codebreaker d'une version donnée
    trouve la solution. Pour chaque partie, on réinitialise le codemaker afin d'obtenir une nouvelle solution.
    """
    resultats = []
    codemaker_module = get_codemaker_module(codemaker_version)

    for _ in range(nbr_of_game):
        codemaker_module.init()  # Nouvelle solution pour chaque partie
        resultats.append(get_number_of_try(codemaker_version, codebreaker_version))

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
    # Vérification de la compatibilité pour chaque codebreaker
    check_compatibility(codemaker_version, version1)
    check_compatibility(codemaker_version, version2)

    gains = []
    codemaker_module = get_codemaker_module(codemaker_version)

    for _ in range(nbr_of_game):
        codemaker_module.init()  # Même solution pour les deux codebreaker
        score1 = play_game(codemaker_module, get_codebreaker_module(version1), codemaker_version, version1)
        score2 = play_game(codemaker_module, get_codebreaker_module(version2), codemaker_version, version2)
        gains.append(score1 - score2)

    plt.scatter(range(1, nbr_of_game + 1), gains, color='orange')
    plt.xlabel('Numéro de partie')
    plt.ylabel('Gain')
    plt.title(f'Gain entre codebreaker{version2} et codebreaker{version1} contre codemaker{codemaker_version}')
    plt.show()

# Exemples d'utilisation :
# show_histogram(0, 1, 100)  # Fonctionnera
# show_gain(0, 1, 2, 100)     # Lève une erreur si codemaker0 est utilisé avec codebreaker2
