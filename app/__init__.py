from flask import Flask
from app.assets import compile_assets
import os 

def create_app():
    # Crée une instance de Flask.
    app = Flask(__name__)
    compile_assets(app)
    # Chargement de configurations (exemple d'une clé secrète)
    app.config['SECRET_KEY'] = 'ton_secret_key'

    # Enregistrement des routes ou blueprints
    from app.routes import main
    app.register_blueprint(main)

    return app