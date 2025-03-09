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


class FileLogger:
    """
    Logger qui écrit les messages dans un fichier texte.
    """
    def __init__(self, log_file: str):
        # Le fichier log est construit à partir du chemin et du nom fourni.
        self.log_file = f"app\\logs\\{log_file}.txt"
    
    def __call__(self, message: str):
        # Ouvre le fichier en mode "append" pour ajouter le message avec un saut de ligne.
        with open(self.log_file, "a") as f:
            f.write(message + "\n")


def play_log(codemaker_version, codebreaker_version: int, log_file: str, reset_solution=True, quiet=False, output_func = None, human_solution = False) -> int:
    """
    Joue une partie pour un codebreaker sur la solution déjà initialisée.
    Le codebreaker est réinitialisé pour chaque partie, tandis que le codemaker conserve la solution.
    
    La sortie (les logs) est réalisée via la fonction d'output passée en paramètre.
    Par défaut, si aucune fonction n'est fournie, les logs sont écrits dans un fichier texte à l'aide de FileLogger.
        int: nombre d'essais effectués.
    """
    check_compatibility(codemaker_version, codebreaker_version)
    
    if not human_solution:
        codemaker_module = get_codemaker_module(codemaker_version) 
            # Réinitialisation de la solution et du codebreaker
        if reset_solution:
            codemaker_module.init()

    codebreaker_module = get_codebreaker_module(codebreaker_version)
    


    codebreaker_module.init()

    if output_func is None:
        output_func = FileLogger(log_file)
    
    ev = None
    nbr_of_try = 0
    
    if not quiet:
        print('combinaisons de taille {}, couleurs disponibles {}'.format(common.LENGTH, common.COLORS))
    
    while True:
        combination = codebreaker_module.codebreaker(ev)
        ev = common.evaluation(combination, human_solution) if human_solution else codemaker_module.codemaker(combination) 
        nbr_of_try += 1
        
        # Enregistrement des logs via output_func
        output_func(combination)
        output_func(f"{ev[0]},{ev[1]}")
        
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
    play_log(1, 2, "nul")

