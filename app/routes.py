from flask import Blueprint, render_template

# Création d'un blueprint
main = Blueprint('main', __name__)

@main.route("/")
def index():
    # La fonction index() sera appelée quand l'utilisateur visite la racine ("/")
    return render_template("index.html")