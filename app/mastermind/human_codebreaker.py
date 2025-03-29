#!/usr/bin/env python3
# On utilise un import relatif (`from . import common`)
# pour s'assurer que le module est bien importé,
# peu importe comment l'application est exécutée avec Flask.
# Cela évite les erreurs liées aux imports absolus.
from . import common


def init():
    return


def codebreaker(
    __,
):  # Inutile d'affiche la correction reçue, la boucle principale de jeu s'en charge
    while True:
        combination = input("Saisir combinaison: ")  # Saisie par l'utilisateur
        error_message = common.verif_combination(
            combination
        )  # Vérification de la validité
        if error_message:
            print(
                error_message
            )  # Affichage du message d'erreur si la combinaison est invalide
            continue

        return combination  # Retourne la combinaison valide
