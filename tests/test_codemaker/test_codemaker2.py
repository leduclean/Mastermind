import unittest
import app.mastermind.codemaker2 as codemaker2
import app.mastermind.common as common
import app.mastermind.past_evaluations as past_evaluations


class TestCodemaker2(unittest.TestCase):

    def setUp(self):
        """
        Initialise les variables globales avant chaque test.
        """
        codemaker2.solution = "RRRR"
        codemaker2.possible_combinations = {"RRRR", "VVVV", "VVRR"}
        codemaker2.permanent_combinations = {"RRRR", "VVVV", "VVRR", "BBBB"}
        past_evaluations.dict_backtracking = {}

    def test_exact_match(self):
        """
        Teste si une combinaison identique à la solution donne (4,0).
        """
        result = codemaker2.codemaker("RRRR")
        self.assertEqual(result, (4, 0), "Erreur: la combinaison exacte ne retourne pas (4,0)")

    def test_partial_match(self):
        """
        Teste si une combinaison avec 2 couleurs bien placées retourne (2,0).
        """
        result = codemaker2.codemaker("VVRR")
        self.assertEqual(result, (2, 0), "Erreur: la combinaison partielle ne retourne pas (2,0)")

    def test_no_match(self):
        """
        Teste si une combinaison sans correspondance retourne (0,0).
        """
        result = codemaker2.codemaker("BBBB")
        self.assertEqual(result, (0, 0), "Erreur: la combinaison sans correspondance ne retourne pas (0,0)")

    def test_solution_update_difficulty(self):
        """
        Vérifie que la solution mise à jour est la plus difficile à deviner.
        """
        codemaker2.codemaker("VVRR")

        # La nouvelle solution doit appartenir à l'ensemble des solutions possibles
        self.assertIn(codemaker2.solution, codemaker2.possible_combinations,
                      "Erreur: la solution mise à jour n'est pas dans les possibilités.")

        # Vérifier que la nouvelle solution maximise le pire cas (simulation)
        worst_case_sizes = []
        for test_combination in codemaker2.possible_combinations:
            evaluation_groups = {}
            for comb in codemaker2.permanent_combinations:
                eval_result = common.evaluation(test_combination, comb)
                if eval_result not in evaluation_groups:
                    evaluation_groups[eval_result] = []
                evaluation_groups[eval_result].append(comb)
            worst_case_sizes.append(max(len(group) for group in evaluation_groups.values()))

        self.assertEqual(codemaker2.solution, max(codemaker2.possible_combinations, key=lambda x: worst_case_sizes),
                         "Erreur: la solution mise à jour n'est pas optimisée pour maximiser la difficulté.")

    def test_evaluation_storage(self):
        """
        Vérifie que les évaluations sont stockées pour éviter des recalculs.
        """
        codemaker2.codemaker("VVVV")
        self.assertIn(("VVVV", "RRRR"), past_evaluations.dict_backtracking,
                      "Erreur: l'évaluation n'a pas été enregistrée.")
        self.assertIn(("RRRR", "VVVV"), past_evaluations.dict_backtracking,
                      "Erreur: l'évaluation inverse n'a pas été enregistrée.")


if __name__ == '__main__':
    unittest.main()
