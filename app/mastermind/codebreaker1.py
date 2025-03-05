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
    Génère une combinaison aléatoire non tentée. Par soucis de compatibilité avec les foncitons
    de test, on lui passe aussi l'evaluation précèdente en argument même si elle ne sera pas prise en compte
    """
    global tried
    while 1:
        to_try = ''.join(random.choices(common.COLORS, k = common.LENGTH))
        if to_try not in tried:
            tried.add(to_try)
            return to_try