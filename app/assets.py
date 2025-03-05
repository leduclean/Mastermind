import os
from flask_assets import Environment, Bundle

def compile_assets(app):
    """Configure and compile SCSS files into CSS."""
    assets = Environment(app)

    # Définir les chemins en fonction de la structure du projet
    scss_path = os.path.join(app.root_path, 'static', 'scss', 'style.scss')
    css_output_path = os.path.join(app.root_path, 'static', 'css')

    # Vérifier que le dossier CSS existe, sinon le créer
    if not os.path.exists(css_output_path):
        os.makedirs(css_output_path)

    # Vérifier que le fichier SCSS existe
    if not os.path.exists(scss_path):
        raise FileNotFoundError(f"Le fichier SCSS est introuvable : {scss_path}")

    # Configuration du bundle SCSS -> CSS
    scss = Bundle('scss/style.scss', filters='libsass', output='css/style.css')
    assets.register('scss_all', scss)
    scss.build()