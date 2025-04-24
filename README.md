# Mastermind - Interface graphique avec Flask

Ce projet propose une interface web interactive pour le jeu Mastermind, développée en Python avec le micro-framework Flask.

## Prérequis

- Python 3.9 ou version supérieure  
- pip (gestionnaire de paquets Python)  
- Accès à un terminal ou à un invite de commandes

## Installation

1. Créer un environnement virtuel (recommandé) :  
   ```bash
   python -m venv venv
   ```

2. (Windows uniquement) Autoriser l'exécution de scripts PowerShell :  
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. Activer l’environnement virtuel :  
   ```bash
   source venv/bin/activate     # Sur macOS / Linux  
   .\venv\Scripts\activate      # Sur Windows
   ```

4. Installer les dépendances :  
   ```bash
   pip install -r requirements.txt
   ```

## Lancer l’interface graphique

1. Depuis la racine du projet, lancez :  
   ```bash
   python run.py
   ```

2. Ouvrez l’URL affichée dans le terminal (généralement `http://127.0.0.1:5000`).

3. Personnalisation des paramètres du jeu :  
   - Dans `common.py`, modifiez la constante `LENGTH` pour ajuster le nombre de colonnes (valeur maximale : 8, attendez vous a ce que les delais d'attentes soit très longs pour les modes automatiques en raison des calculs nécessaires).
   - Vous pouvez réduire la liste `COLORS`, mais pas l’agrandir.  
   - L’interface s’adapte automatiquement à ces changements.

## Structure du projet et exécution des modules backend

Le projet utilise Flask, et le dossier `app/mastermind` est un package Python. Pour exécuter un module interne, placez-vous à la racine du projet et lancez :  
```bash
python -m app.mastermind.nom_du_module
```
Par exemple, pour exécuter le module `figures` :  
```bash
python -m app.mastermind.figures
```

## Tests

Les tests unitaires sont situés dans le dossier `tests` et utilisent la librairie `unittest`. Pour les lancer :  
```bash
python -m unittest discover -s tests
```

## Auteur

Projet réalisé dans le cadre d’un apprentissage personnel / universitaire.
