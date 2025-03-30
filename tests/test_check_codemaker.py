# -*- coding: utf-8 -*-
import unittest
from unittest.mock import mock_open, patch

import app.mastermind.common as common
from app.mastermind.check_codemaker import check_codemaker


class TestCheckCodemaker(unittest.TestCase):

    def setUp(self):
        # Mock de la fonction common.evaluation pour contrôler les résultats
        self.patcher = patch("app.mastermind.common.evaluation")
        self.mock_eval = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_valid_log_file(self):
        """Teste avec un fichier log valide"""
        log_content = "RVBJ\n(0,1)\nGNJG\n(2,0)\nNNJN\n(0,0)\nGRGG\n(3,0)\nGROG\n(2,0)\nGBGG\n(4,0)"

        # Configuration du mock pour evaluation
        self.mock_eval.side_effect = [(0, 1), (2, 0), (0, 0), (3, 0), (2, 0), (4, 0)]
        with patch("builtins.open", mock_open(read_data=log_content)):
            result = check_codemaker("dummy_log.txt")
            self.assertTrue(result)

            # Vérifie que evaluation a été appelée avec les bonnes valeurs
            self.mock_eval.assert_any_call("RVBJ", "GBGG")
            self.mock_eval.assert_any_call("GNJG", "GBGG")
            self.mock_eval.assert_any_call("NNJN", "GBGG")

    def test_invalid_log_file(self):
        """Teste avec un fichier log invalide (une évaluation incorrecte)"""
        log_content = "RVBJ\n(2, 1)\nJBVR\n(1, 3)\nRRRR\n(4, 0)\n"

        # Configuration du mock pour evaluation
        self.mock_eval.side_effect = [
            (2, 1),
            (0, 4),
            (4, 0),
        ]  # La deuxième évaluation ne correspond pas

        with patch("builtins.open", mock_open(read_data=log_content)):
            result = check_codemaker("dummy_log.txt")
            self.assertFalse(result)

    def test_empty_log_file(self):
        """Teste avec un fichier log vide"""
        with patch("builtins.open", mock_open(read_data="")):
            with self.assertRaises(IndexError):
                check_codemaker("empty_log.txt")

    def test_log_file_with_odd_lines(self):
        """Teste avec un nombre impair de lignes (sans la solution)"""
        log_content = "RVBJ\n(2, 1)\nJBVR\n"

        with patch("builtins.open", mock_open(read_data=log_content)):
            result = check_codemaker("dummy_log.txt")
            self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
