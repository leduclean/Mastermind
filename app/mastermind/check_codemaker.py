# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 12:46:54 2025

@author: Simon
"""
# On utilise un import relatif (`from . import common`)
# pour s'assurer que le module est bien importé,
# peu importe comment l'application est exécutée avec Flask.
# Cela évite les erreurs liées aux imports absolus.
from . import common


def check_codemaker(log_file):
    with open(log_file, "r") as log:
        lines = log.readlines()

        # si fichier est vide
        if not lines:
            raise IndexError("Fichier log vide.")

        # si le nombre de lignes est impair, alors le format est invalide
        if len(lines) % 2 != 0:
            return False

        # conversion de la dernière ligne en tuple pour comparaison
        try:
            last_eval = tuple(map(int, lines[-1].strip().strip("()").split(",")))
        except Exception as e:
            raise ValueError("Format de la dernière ligne invalide.") from e

        if last_eval != (4, 0):
            return False

        # recupération de la solution nettoyée
        solution = lines[-2].strip()

        for i in range(0, len(lines) - 1, 2):
            tried = lines[i].strip()
            try:
                # conversion de l'évaluation en tuple en supprimant d'abord les parenthèses
                ev = tuple(map(int, lines[i + 1].strip().strip("()").split(",")))
            except Exception as e:
                raise ValueError("Format d'évaluation invalide dans le log.") from e

            if ev != common.evaluation(tried, solution):
                return False

    return True
