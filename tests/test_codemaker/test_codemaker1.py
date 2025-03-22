import unittest
from unittest.mock import patch
import app.mastermind.codemaker1 as codemaker1
import app.mastermind.common as common

class Testcodemaker1(unittest.TestCase):
    
    @patch("random.choices")
    def test_init(self, mock_random_choices):
        """
        Vérifie que la fonction init() initialise correctement la variable solution.
        """
        # On force le retour de random.choices pour un test prévisible
        mock_random_choices.return_value = ['R', 'V', 'B', 'J']
        
        codemaker1.init()
        
        # Vérifier que solution a bien été initialisée avec la bonne valeur
        self.assertEqual(codemaker1.solution, "RVBJ", "La solution n'a pas été initialisée correctement.")
    
    def test_codemaker(self):
        """
        Vérifie que la fonction codemaker1() retourne une évaluation correcte.
        """
        codemaker1.solution = "RVBJ"  # On fixe une solution connue
        
        # Cas 1 : Combinaison identique à la solution
        self.assertEqual(codemaker1.codemaker("RVBJ"), (4, 0), "L'évaluation est incorrecte pour une combinaison exacte.")
        
        # Cas 2 : Combinaison avec une bonne couleur mal placée
        self.assertEqual(codemaker1.codemaker("VJRB"), (0, 4), "L'évaluation est incorrecte pour une combinaison avec 4 mal placés.")
        
        # Cas 3 : Combinaison avec 2 bien placés et 2 mal placés
        self.assertEqual(codemaker1.codemaker("RVJB"), (2, 2), "L'évaluation est incorrecte pour 2 bien placés et 2 mal placés.")
        
        # Cas 4 : Combinaison sans couleurs présentes
        self.assertEqual(codemaker1.codemaker("NNMM"), (0, 0), "L'évaluation est incorrecte pour une combinaison sans couleurs présentes.")
    



if __name__ == '__main__':
    unittest.main()

