# -*- coding: utf-8 -*-

import unittest
import itertools
from unittest.mock import patch, MagicMock
import app.mastermind.common as common
import app.mastermind.past_evaluations as past_evaluations
from app.mastermind.codebreaker3 import (codebreaker, init, possible_combinations,
                                        permanent_combinations, last_guess, first_guess,
                                        Optimization)

class TestCodeBreaker3(unittest.TestCase):
    def setUp(self):
        """Réinitialise le codebreaker avant chaque test."""
        init()
        past_evaluations.reset_dict()

    def test_initial_state(self):
        """Vérifie l'initialisation correcte des variables globales."""
        self.assertEqual(len(possible_combinations), 0)
        self.assertEqual(possible_combinations, permanent_combinations)
        self.assertIsNone(last_guess)
        self.assertTrue(Optimization)

    def test_first_guess(self):
        """Vérifie que le premier guess suit le pattern optimal."""
        expected = ''.join([common.COLORS[i % len(common.COLORS)] for i in range(common.LENGTH)])
        self.assertEqual(first_guess(), expected)

    def test_minimax_algorithm(self):
        """Vérifie que l'algorithme choisit bien la combinaison qui minimise le pire cas."""
        # Setup initial state
        init()
        test_combinations = {'RRRR', 'GGGG', 'BBBB'}
        possible_combinations.update(test_combinations)
        permanent_combinations.update(test_combinations)
        
        # Mock common.evaluation pour contrôler les résultats
        with patch('app.mastermind.common.evaluation') as mock_eval:
            mock_eval.side_effect = [
                (1, 0), (0, 1), (0, 0),  # RRRR vs autres
                (0, 2), (1, 0), (0, 1),   # GGGG vs autres
                (0, 0), (0, 1), (1, 0)     # BBBB vs autres
            ]
            
            # Premier guess
            guess = codebreaker(None)
            
            # Le meilleur choix devrait être celui qui donne la plus petite partition maximale
            # Dans