#!/usr/bin/env python3
# On utilise un import relatif (`from . import common`)  
# pour s'assurer que le module est bien importé,  
# peu importe comment l'application est exécutée avec Flask.  
# Cela évite les erreurs liées aux imports absolus.  
from . import common


def init():
    return

def codebreaker(__):  # Inutile d'affiche la correction reçue, la boucle principale de jeu s'en charge
    while True:
        combination = input("Saisir combination: ")  # On lit une combination au clavier au lieu d'appeler le codebreaker (qui sera donc joué par un humain)
        if len(combination) != common.LENGTH:
            print("combination invalide (longueur {} au lieu de {})".format(len(combination), common.LENGTH))
            continue
        for c in combination:
            if c not in common.COLORS:
                print("combination invalide (couleur {} n'existe pas)".format(c))
                continue
        return combination 
     
    
def verif_combination(combination):
    """Vérifie la validité de la combination saisie par l'utilisateur."""
    if len(combination) != common.LENGTH:
        return f"combination invalide : longueur {len(combination)} au lieu de {common.LENGTH}"
    for c in combination:
        if c not in common.COLORS:
            return f"combination invalide : couleur {c} n'existe pas"
    return None  # Pas d'erreur

