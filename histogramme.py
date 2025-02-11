import codebreaker0
import codemaker0
import common
import matplotlib.pyplot as plt

#TO DO: add doc 

NUMBER_OF_GAME = 100

def get_number_of_try()-> int:
    nbr_of_try = 0
    codemaker0.init() 
    maker_evaluation = None 
    while maker_evaluation!= common.LENGTH:
        nbr_of_try += 1 
        codemaker0.init()
        maker_evaluation = codemaker0.codemaker(codebreaker0.codebreaker(maker_evaluation))[0]
    return nbr_of_try

resultats = [get_number_of_try() for _ in range(NUMBER_OF_GAME)]
plt.hist(resultats, bins=range(min(resultats), max(resultats) + 2), align='left', edgecolor='orange')
plt.xlabel('Valeurs retournées')
plt.ylabel('Fréquence')
plt.title(f'Histogramme du nombre de partie nécessaire pour trouver la solution sur {NUMBER_OF_GAME} parties jouées')
plt.show()