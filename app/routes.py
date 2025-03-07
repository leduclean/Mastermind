from flask import Blueprint, render_template, request, url_for, session
from app.mastermind import *


color_dic = {
    'R': 'red',          # Rouge
    'B': 'blue',         # Bleu
    'V': 'green',        # Vert
    'J': 'yellow',       # Jaune
    'O': 'orange',       # Orange
    'N': 'black',
    'M': 'brown',
    'G': 'grey'

}


# Création d'un blueprint
main = Blueprint('main', __name__)


@main.route("/", methods=['GET', 'POST'])
def index():
    

    # La fonction index() sera appelée quand l'utilisateur visite la racine ("/")
    return render_template("index.html")



def get_input_from_post():
    # Ici, ev peut être utilisé pour afficher des indices ou autre dans le template si nécessaire.
    # On récupère la combinaison saisie par l'utilisateur dans le formulaire.
    return request.form.get('combination', '').upper()

def flask_output(message):
    session.setdefault('attempts', []).append(message)

def play_step(combination: str):
    solution = session.get('solution')
    ev = common.evaluation(combination, solution)
    session['nbr_of_try'] = session.get('nbr_of_try', 0) + 1
    return ev, session['nbr_of_try']



def human_mode():
        # Initialisation

    if request.method == 'GET':
        codemaker0.init()  # Appel de init() seulement lors de la première visite
        session['codemaker_initialized'] = True  # Marquer que l'initialisation a été faite
        session['nbr_of_try'] =0
        session['solution'] = codemaker0.solution

    solution = session.get('solution')
    message = ""
    win_message = ""
    combination = ""
    length = common.LENGTH
    colors_name = [color_dic[code] for code in common.COLORS]
    colors = ", ".join(common.COLORS)
    cplaced = None
    iplaced = None
    nbr_of_try = ""
    nbr_of_line = 10

    if request.method == "POST":
        combination = get_input_from_post()
        erreur = human_codebreaker.verif_combination(combination)

        # Si l'utilisateur a fait une erreur dans la combinaison
        if erreur:
            message = erreur
        else:
            message = f"Combination accepted: {combination}"

            # Évaluation de la combinaison
            (cplaced, iplaced), nbr_of_try = play_step(combination)[0] ,play_step(combination)[1]

            # Si la combinaison est correcte, affichage du message de victoire
            if cplaced >= common.LENGTH:
                win_message = f"Bravo ! Trouvé {combination} en {nbr_of_try} essais"
                session.pop('nbr_of_try')  # On réinitialise les essais une fois le jeu gagné


    # Retourner le template avec les variables nécessaires
    return render_template(
        "human_player.html", 
        combination=combination, 
        message=message, 
        length=length, 
        colors=colors, 
        cplaced=cplaced, 
        iplaced=iplaced, 
        colors_name=colors_name, 
        win_message=win_message, 
        nbr_of_try=nbr_of_try,
        solution = solution,
        nbr_of_line=nbr_of_line
    )

def auto_mode():
    session['attempts'] = []  # Réinitialisation de l'historique
    session['nbr_of_try'] = 0  # Réinitialiser le compteur d'essais
    lenght = common.LENGTH
    nbr_of_line = 10
    # colors_name = [color_dic[code] for code in common.COLORS]
    # colors = ", ".join(common.COLORS)
    def flask_output(message):
        session.setdefault('attempts', []).append(message)

    play(
        codemaker_version=1,  # Met la bonne version de ton codemaker
        codebreaker_version=2,  # Met la bonne version du codebreaker automatique
        reset_solution=True,
        output=flask_output,
        get_input=None,  # Pas d'input utilisateur
        quiet=False
    )

    return render_template(
        "auto.html",
        message="Mode automatique terminé.",
        attempts=session.get('attempts', []),
        lenght = lenght,
        nbr_of_line=nbr_of_line

    )


@main.route("/game", methods=['GET', 'POST'])
def game():
    """
    Adaptation du jeu sans utiliser play, avec comptage des essais
    """
    mode = request.args.get("mode", "human")  # Par défaut, le mode est humain
    if mode == "human":
        return human_mode()
    elif mode == "auto":
        return auto_mode()
    else:
        return "Mode invalide", 400  # Erreur si le mode n'est pas reconnu
    
