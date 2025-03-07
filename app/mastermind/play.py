#!/usr/bin/env python3
import importlib
from . import common



# TO DO : passer les commentaires en anglais 
def get_codebreaker_module(version: int):
    """Importe dynamiquement le module codebreaker de la version donnée."""
    try:
        return importlib.import_module(f"app.mastermind.codebreaker{version}")
    except ImportError:
        raise ValueError(f"Module codebreaker{version} non trouvé.")

def get_codemaker_module(version: int):
    """Importe dynamiquement le module codemaker de la version donnée."""
    try:
        return importlib.import_module(f"app.mastermind.codemaker{version}")
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

def play(codemaker_version: int, codebreaker_version: int, reset_solution=True, quiet = False, output=print, get_input=None) -> int:
    """
    Joue une partie pour un codebreaker donné.
    
    c'est un mode automatique, get_input reste None et le codebreaker génère ses combinaisons.
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
        output("Combinaisons de taille {} avec couleurs disponibles : {}".format(common.LENGTH, common.COLORS))

    while True:
        # Si get_input est défini, on l'utilise pour récupérer l'input,
        # sinon, le codebreaker automatique génère sa combinaison.
        if get_input is not None:
            combination = get_input(ev)
        else:
            combination = codebreaker_module.codebreaker(ev)

        ev = codemaker_module.codemaker(combination)
        nbr_of_try += 1

        if not quiet:
            output("Essai {} : {} ({} bien placées, {} mal placées)".format(nbr_of_try, combination, ev[0], ev[1]))

        if ev[0] >= common.LENGTH:
            if not quiet:
                output("Bravo ! Trouvé {} en {} essais".format(combination, nbr_of_try))
            return nbr_of_try


def play_log(codemaker_version: int, codebreaker_version: int, log_file: str, reset_solution = True, quiet = False) -> int:
    """
    Joue une partie pour un codebreaker donné sur la solution déjà initialisée dans le module codemaker.
    Le codebreaker est réinitialisé pour chaque partie, tandis que le codemaker conserve la solution.
    """
    check_compatibility(codemaker_version, codebreaker_version)
    codemaker_module, codebreaker_module = get_codemaker_module(codemaker_version), get_codebreaker_module(codebreaker_version)

    
    # Permet de pouvoir comparer deux codebreaker sur la meme solution
    if reset_solution:
        codemaker_module.init()
    codebreaker_module.init()  # Réinitialisation du codebreaker
    ev = None
    nbr_of_try = 0 
        ##### Seule chose qui change du programme play
    with open(f"app\logs\{log_file}.txt", 'w') as log:
        if not quiet:
            print('combinations de taille {}, couleurs disponibles {}'.format(common.LENGTH, common.COLORS))
        while True:
            combination = codebreaker_module.codebreaker(ev)
            ev = codemaker_module.codemaker(combination)
            nbr_of_try += 1
            log.write(combination + "\n")
            log.write(f"{ev[0]},{ev[1]} \n")
            if not quiet:
                print("Essai {} : {} ({},{})".format(nbr_of_try, combination, ev[0], ev[1]))
            if ev[0] >= common.LENGTH:
                if not quiet:
                    print("Bravo ! Trouvé {} en {} essais".format(combination, nbr_of_try))
                return nbr_of_try


# Pour ne pas executer ces fonctions lors des imports 
if __name__ == "__main__":
    print("Ce fichier play.py est exécuté directement.")
    # appelle des fonctions ici 
    play_log(1, 2, "random")

