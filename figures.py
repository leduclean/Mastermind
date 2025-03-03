import codemaker0
import common
import matplotlib.pyplot as plt

#TO DO: réfléchir au mieux entre diagramme de dispersion et histogramme pour la fonction show gain 


def get_number_of_try(codebreaker_version: int) -> int:
    """
    Renvoie le nombre d'essais nécessaire pour une version donnée au codebreaker afin de trouver la solution
    """
    nbr_of_try = 0
    maker_evaluation = None

    # Construit le nom du module à importer (par ex. "codebreaker0", "codebreaker1", etc.)
    module_name = f"codebreaker{codebreaker_version}"
    try:
        # Import du module en fonciton de la méthode choisie 
        codebreaker_module = __import__(module_name)
    except ImportError:
        raise ValueError(f"Module {module_name} non trouvé.")
    
    codebreaker_module.init() # on initialise le codebreaker afin de vider le set des combinaisons testées à la partie d'avant
    while maker_evaluation != common.LENGTH:
        nbr_of_try += 1
        # On appelle la fonction codebreaker de la version importée en passant l'évaluation précédente
        proposition = codebreaker_module.codebreaker(maker_evaluation)
        # codemaker0.codemaker renvoie un tuple : on récupère le premier élément (la valeur d'évaluation)
        maker_evaluation = codemaker0.codemaker(proposition)[0]
        
    return nbr_of_try

def show_histrogramme(version: int, nbr_of_game: int):
    """
    Affiche l'histrogramme du nombre d'essais nécessaire a un codebreaker d'une version donnée 
    pour trouver la solution pour un échantillon donné de nombre d'essais
    """
    resultats = []
    for _ in range(nbr_of_game):
        codemaker0.init() # on doit tester sur une nouvelle partie à chaque fois donc il faut reinitialiser la solution
        resultats.append(get_number_of_try(version))
    plt.hist(resultats, bins=range(min(resultats), max(resultats) + 2), align='left', edgecolor='orange')
    plt.xlabel('Valeurs retournées')
    plt.ylabel('Fréquence')
    plt.title(f'Histogramme du nombre de partie nécessaire à la version {version} pour trouver la solution sur {nbr_of_game} parties jouées')
    plt.show()

# show_histrogramme(0, 100)
# show_histrogramme(1, 100)

def get_gain(version1 : int, version2 : int)-> int:
    """
    Renvoie le gain de la version 2 par rapport à la version 1 calculé à de get_number_of_try()
    """
    return get_number_of_try(version1) - get_number_of_try(version2)


def show_gain(version1: int, version2: int, nbr_of_game: int):
    """
    Affiche le diagramme de dispersion des gains de la version2 par rapport à la version1 sur un nombre de partie jouées
    """
    gains = []
    for _ in range(nbr_of_game):
        codemaker0.init() # on doit tester sur une nouvelle partie à chaque fois donc il faut reinitialiser la solution
        gains.append(get_gain(version1, version2))
    # Création d'un diagramme de dispersion
    parties = list(range(1, nbr_of_game + 1))
    plt.scatter(parties, gains, color='orange')
    plt.xlabel('Numéro de partie')
    plt.ylabel('Gain')
    plt.title(f'Diagramme de dispersion du gain entre codebreaker{version1} et codebreaker{version2} sur {nbr_of_game} parties')
    plt.show()

# show_gain(0, 1, 100)