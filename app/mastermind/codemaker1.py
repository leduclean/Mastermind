import random

# On utilise un import relatif (`from . import common`)
# pour s'assurer que le module est bien importé,
# peu importe comment l'application est exécutée avec Flask.
# Cela évite les erreurs liées aux imports absolus.
from . import common


def init():
    """
    Cette fonction, appellée à chaque début de partie, initialise un certain nombre de
    variables utilisées par le codemaker
    """
    global solution
    solution = "".join(random.choices(common.COLORS, k=common.LENGTH))


def codemaker(combinaison):
    """
    Cette fonction corrige la combinaison proposée par le codebreaker
    (donnée en argument)
    """
    global solution
    return common.evaluation(combinaison, solution)
