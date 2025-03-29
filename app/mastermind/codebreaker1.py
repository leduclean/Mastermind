import random

# On utilise un import relatif (`from . import common`)
# pour s'assurer que le module est bien importé,
# peu importe comment l'application est exécutée avec Flask.
# Cela évite les erreurs liées aux imports absolus.
from . import common

tried = set()


def init():
    """
    Initialise l'ensemble des tnetatives a chaque début de partie
    """
    global tried
    tried.clear()


def codebreaker(evaluation_p: tuple) -> str:
    """
    Génère une combinaison aléatoire non tentée auparavant.

    Args:
        evaluation_p (tuple[int, int]): L'évaluation précédente de la combinaison proposée.
            Cet argument est inclus pour des raisons de compatibilité avec les fonctions de test,
            mais il n'est pas utilisé dans cette implémentation.

    Returns:
        str: Une combinaison aléatoire non tentée auparavant.
    """
    global tried  # Ensemble des combinaisons déjà tentées

    while True:
        # Génère une combinaison aléatoire en choisissant des couleurs parmi `common.COLORS`
        to_try = "".join(random.choices(common.COLORS, k=common.LENGTH))

        # Vérifie si la combinaison n'a pas déjà été tentée
        if to_try not in tried:
            # Ajoute la combinaison à l'ensemble des combinaisons tentées
            tried.add(to_try)
            # Retourne la combinaison non tentée
            return to_try
