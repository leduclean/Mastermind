import random
import unittest
from unittest.mock import patch

import app.mastermind.common as common
from app.mastermind.codebreaker1 import codebreaker, init, tried


class TestRandomCodeBreaker(unittest.TestCase):
    def setUp(self):
        """Réinitialise l'ensemble des tentatives avant chaque test."""
        init()

    def test_guess_format(self):
        """Vérifie que chaque proposition a 4 symboles et des couleurs valides."""
        guess = codebreaker((0, 0))  # `evaluation_p` simulé (non utilisé)
        self.assertEqual(
            len(guess), common.LENGTH, "La proposition doit avoir 4 symboles."
        )
        self.assertTrue(
            all(c in common.COLORS for c in guess), f"Couleurs invalides dans {guess}."
        )

    def test_no_duplicate_guesses(self):
        """Vérifie que le codebreaker ne propose pas deux fois la même combinaison."""
        guesses = set()
        for _ in range(50):  # 50 essais pour détecter une répétition (très improbable)
            guess = codebreaker((0, 0))
            self.assertNotIn(
                guess, guesses, f"La proposition {guess} a déjà été faite !"
            )
            guesses.add(guess)

    def test_init_resets_tried_set(self):
        """Vérifie que `init()` réinitialise bien l'ensemble des tentatives."""
        # Fait une première proposition
        first_guess = codebreaker((0, 0))
        self.assertIn(
            first_guess, tried, "La première proposition devrait être dans `tried`."
        )

        # Réinitialise et vérifie que `tried` est vide
        init()
        self.assertEqual(len(tried), 0, "`tried` devrait être vide après `init()`.")

    def test_unused_evaluation_p(self):
        """Vérifie que `evaluation_p` est ignoré (compatibilité)."""
        guess1 = codebreaker((0, 0))  # Feedback simulé (0, 0)
        guess2 = codebreaker((4, 0))  # Feedback simulé (4, 0) → devrait être ignoré
        self.assertNotEqual(
            guess1,
            guess2,
            "Les propositions ne devraient pas dépendre de `evaluation_p`.",
        )

    @patch("random.choices")
    def test_random_choices_called(self, mock_choices):
        """Vérifie que `random.choices` est appelé correctement."""
        mock_choices.return_value = ["R", "G", "B", "Y"]  # Force une valeur de retour
        guess = codebreaker((0, 0))
        mock_choices.assert_called_once_with(common.COLORS, k=common.LENGTH)
        self.assertEqual(guess, "RGBY", "Devrait retourner la valeur mockée.")


if __name__ == "__main__":
    unittest.main()
