from flask import Blueprint, render_template, request, url_for, session, redirect, send_from_directory
from app.mastermind import *


color_dic = {
  'R': 'firebrick',   # Rouge vif et contrasté
  'B': 'royalblue',   # Bleu intense
  'V': 'limegreen',   # Vert éclatant
  'J': 'yellow',      # Jaune vif
  'O': 'darkorange',  # Orange profond
  'N': 'black',       # Noir pour un fort contraste
  'M': 'sienna',      # Brun chaleureux
  'G': 'gray'      # Gris moderne
}




# Création d'un blueprint
main = Blueprint('main', __name__)

# Page d'accueil
@main.route("/", methods=['GET', 'POST'])
def index():
    

    # La fonction index() sera appelée quand l'utilisateur visite la racine ("/")
    return render_template("index.html")


# Pages de codebreaker 
def get_input_from_post():
    # Ici, ev peut être utilisé pour afficher des indices ou autre dans le template si nécessaire.
    # On récupère la combinaison saisie par l'utilisateur dans le formulaire.
    return request.form.get('combination', '').upper()

def flask_output(message):
    session.setdefault('attempts', []).append(message)

def get_nbr_of_try() -> int:
    session['nbr_of_try'] = session.get('nbr_of_try', 0) + 1
    return session['nbr_of_try']

def get_solution():
    solution = session.get('solution')
    return solution


def human_mode(codemakerversion):
    # Initialisation
    if codemakerversion != "human":
        codemaker = get_codemaker_module(codemakerversion)

    if request.method == 'GET':
        session['nbr_of_try'] = 0
        if codemakerversion != "human":
            codemaker.init()  # Appel de init() seulement lors de la première visite
            session['solution'] = codemaker.solution

    solution = get_solution()
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
    mode = "human"
    if request.method == "POST":
        combination = get_input_from_post()
        erreur = human_codebreaker.verif_combination(combination)

        # Si l'utilisateur a fait une erreur dans la combinaison
        if erreur: # gerer le message d'erreur 
            message = erreur
        else:
            # Évaluation de la combinaison
            (cplaced, iplaced), nbr_of_try = common.evaluation(combination, solution), get_nbr_of_try()
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
        solution=solution,
        nbr_of_line=nbr_of_line,
        mode=mode,
        codemakerversion=codemakerversion
    )

def auto_mode(mode, codemaker):
    session['attempts'] = []
    session['nbr_of_try'] = 0  # Réinitialiser le compteur d'essais
    length = common.LENGTH
    nbr_of_line = 10
    def flask_output(message):
        attempts = session.get("attempts", [])  # Récupérer la liste actuelle
        attempts.append(message)  # Ajouter le message
        session["attempts"] = attempts  # Mettre à jour la session
        session.modified = True  # Signaler à Flask que la session a changé

    # Appel de play_log pour générer les logs et remplir la session
    play_log(
        codemaker_version= 1 if codemaker == "human" else codemaker,  # Met la bonne version de ton codemaker et utilise la version 1 si c'est un humain
        codebreaker_version = mode,     # Met la bonne version du codebreaker automatique
        log_file=None,
        reset_solution=True,
        quiet=True,
        output_func = flask_output,
        human_solution = session.get("solution") if codemaker == "human" else False
    )

    # Après que play_log a modifié la session, on récupère la liste des messages
    attempts_not_paired = session.get('attempts', [])
    # Fusionner les éléments par paire
    attempts = list(zip(attempts_not_paired[::2], attempts_not_paired[1::2]))

    return render_template(
        "auto.html",
        message="Mode automatique terminé.",
        attempts=attempts,
        length=length,
        nbr_of_line=nbr_of_line
    )


@main.route("/game", methods=['GET', 'POST'])
def game():
    """
    Adaptation du jeu sans utiliser play, avec comptage des essais
    """
    mode = request.args.get("mode")  
    codemaker = request.args.get("codemaker")
    if mode == "human":
        return human_mode(codemaker)
    else:
        return auto_mode(mode, codemaker)



# Pages codemaker
def get_solution_from_post():
    return request.form.get('solution', '').upper()

@main.route("/human_codemaker", methods = ['GET', 'POST'])
def human_codemaker():
    """
    Selection d'une solution + demande si jouer contre un codebreaker humain ou pas 
    """
    colors_name = [color_dic[code] for code in common.COLORS]
    length = common.LENGTH
    mode = request.args.get("mode")  # Par défaut, le mode est humain
    if request.method == 'POST':
        session['solution'] = get_solution_from_post()
        return redirect(url_for('main.game', mode = mode, reset = "true", codemaker = "human"))
    return render_template(
        "human_codemaker.html",
        solution = session.get('solution'),
        length = length,
        colors_name = colors_name
    )

@main.route('/static/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('static/js', filename, mimetype='application/javascript')
