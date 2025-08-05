#!/usr/bin/env python3

import random

# On utilise un import relatif (`from . import common`)
# pour s'assurer que le module est bien importé,
# peu importe comment l'application est exécutée avec Flask.
# Cela évite les erreurs liées aux imports absolus.
from . import common  # N'utilisez pas la syntaxe "form random import XXX"


def init():
    """
    Une fonction qui ne fait rien... pour cette version triviale.
    Pour vos codebreaker plus avancés, c'est ici que vous pouvez initialiser
    un certain nombre de variables à chaque début de partie.
    """
    return


def codebreaker(evaluation_p: tuple):
    """
    L'argument evaluation_p est l'évaluation qu'on reçoit pour la dernière
    combinaison qu'on a proposée (et vaut None si c'est le premier coup de la
    partie). Cette version triviale n'utilise pas cette information, puisqu'elle joue au hasard.
    """
    return "".join(random.choices(common.COLORS, k=common.LENGTH))
