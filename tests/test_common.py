# tests/test_codemaker.py
import unittest
import app.mastermind.common as common


class TestCommonFunctions(unittest.TestCase):
        
    def test_verif_combination(self):
        """ Teste la fonction verif_combination() """
        # Cas valides
        self.assertIsNone(common.verif_combination("RVJB"))  # Longueur correcte, couleurs valides
        
        # Cas invalides
        self.assertEqual(
            common.verif_combination("RVJ"), 
            "invalid combination : length 3 supposed to be 4"
        )  # Mauvaise longueur

        self.assertEqual(
            common.verif_combination("RVXZ"), 
            "invalid combination : color X doesn't exist"
        )  # Couleur invalide
    
    def test_evaluation(self):
        """ Teste la fonction evaluation() """
        # Cas standard
        self.assertEqual(common.evaluation("RVJB", "RVBR"), (2, 1))  # 2 bien placées, 2 mal placées
        self.assertEqual(common.evaluation("RRRR", "RRRR"), (4, 0))  # Tout bien placé
        self.assertEqual(common.evaluation("VVVV", "RRRR"), (0, 0))  # Rien de correct
        self.assertEqual(common.evaluation("RVBJ", "JBRV"), (0, 4))  # Tout est mal placé

        # Nouveaux cas de test
        self.assertEqual(common.evaluation("RGBJ", "RGBJ"), (4, 0))  # Toutes les couleurs bien placées
        self.assertEqual(common.evaluation("JRGB", "RGBJ"), (0, 4))  # Toutes les couleurs présentes mais mal placées
        self.assertEqual(common.evaluation("RGGB", "RGBJ"), (2, 1))  # Certaines couleurs bien placées, d'autres mal placées
        self.assertEqual(common.evaluation("JJJJ", "RGBJ"), (1, 0))  # Une seule couleur correcte bien placée
        self.assertEqual(common.evaluation("BJGR", "RGBJ"), (0, 4))  # Toutes les couleurs mal placées
        self.assertEqual(common.evaluation("RRRR", "RGBJ"), (1, 0))  # Couleurs répétées et mal placées

        # Vérifie que la fonction lève une erreur pour des tailles différentes et couleurs non présentes
        with self.assertRaises(AssertionError):
            common.evaluation("RRR", "RRRR")
            common.evaluation("RRRR", "RRR")
        with self.assertRaises(AssertionError):
            common.evaluation("RVKK", "RRRR")
            common.evaluation("RRRR", "RVKK")
        with self.assertRaises(AssertionError):
            common.evaluation("RGB", "RGBY")  # Longueurs différentes

    
    def test_donner_possibles(self):
        """ Teste la fonction donner_possibles() """
        tested_combination = "RVJB"
        evaluation_result = common.evaluation("RVJB", "RVBR")  # (2, 2)
        
        possible_combinations = common.donner_possibles(tested_combination, evaluation_result)

        # Vérifie que seules les combinaisons cohérentes avec l'évaluation restent
        for comb in possible_combinations:
            self.assertEqual(common.evaluation(tested_combination, comb), evaluation_result)

    def test_maj_possibles(self):
        """ Teste la fonction maj_possibles() """
        tested_combination = "RVJB"
        evaluation_result = common.evaluation("RVJB", "RVBR")  # (2,2)

        # Ensemble initial de combinaisons possibles
        possible_combinations = {"RVBR", "VVVV", "BBBB", "RRRR", "JBVR"}

        # Mise à jour des possibilités
        common.maj_possibles(possible_combinations, tested_combination, evaluation_result)

        # Vérifie que seules les combinaisons cohérentes restent
        for comb in possible_combinations:
            self.assertEqual(common.evaluation(tested_combination, comb), evaluation_result)


if __name__ == '__main__':
    unittest.main()

