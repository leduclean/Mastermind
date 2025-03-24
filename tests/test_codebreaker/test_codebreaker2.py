# -*- coding: utf-8 -*-

import unittest
import random
import itertools
from unittest.mock import patch
import app.mastermind.common as common
from app.mastermind.codebreaker2 import codebreaker, init, possible_combinations, last_guess

class TestSmartCodeBreaker(unittest.TestCase):
    def setUp(self):
        """Réinitialise le codebreaker avant chaque test."""
        init()

    # def test_initial_possible_combinations(self):
    #     """Vérifie que toutes les combinaisons possibles sont générées au départ."""
    #     init()
    #     expected_combinations = set(map(''.join, itertools.product(common.COLORS, repeat=common.LENGTH)))
    #     self.assertEqual(possible_combinations, expected_combinations)
    #     self.assertIsNone(last_guess)

    def test_guess_format(self):
        """Vérifie que chaque proposition a le bon format."""
        guess = codebreaker(None)  # Premier essai
        self.assertEqual(len(guess), common.LENGTH)
        self.assertTrue(all(c in common.COLORS for c in guess))

    def test_combination_reduction(self):
        """Vérifie que les combinaisons impossibles sont bien éliminées."""
        # Premier guess
        first_guess = codebreaker(None)
        
        # Simule un feedback (1 bon emplacement, 1 bonne couleur mal placée)
        feedback = (1, 1)
        second_guess = codebreaker(feedback)
        
        # Vérifie que le nombre de combinaisons possibles a diminué
        self.assertLess(len(possible_combinations), len(set(map(''.join, itertools.product(common.COLORS, repeat=common.LENGTH)))))
        
        # Vérifie que toutes les combinaisons restantes sont cohérentes avec le feedback
        for combo in possible_combinations:
            self.assertEqual(common.evaluation(first_guess, combo), feedback)

    # @patch("random.choice")
    # def test_random_choice_called(self, mock_choice):
    #     """Vérifie que random.choice est appelé correctement."""
    #     mock_choice.return_value = 'RRRR'  # Valeur fixe pour le test
    #     guess = codebreaker(None)
    #     mock_choice.assert_called_once_with(list(possible_combinations))
    #     self.assertEqual(guess, 'RRRR')

    def test_full_solution_finding(self):
        """Teste que le codebreaker peut trouver la solution."""
        secret = 'RGBJ'  # Solution à trouver
        init()  # Réinitialise
        
        for attempt in range(20):  # On limite à 20 essais
            guess = codebreaker(None if attempt == 0 else common.evaluation(guess, secret))
            if guess == secret:
                break
        else:
            self.fail(f"Solution non trouvée en 20 essais. Dernière proposition: {guess}")

if __name__ == '__main__':
    unittest.main()