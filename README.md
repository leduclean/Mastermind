# Mastermind - Interface Graphique avec Flask

Ce projet implémente une interface graphique pour le jeu Mastermind en utilisant Flask.

## Prérequis

- Python 3.9 ou supérieur
- Pip (gestionnaire de paquets Python)
- Accès à un terminal ou un prompt de commande

---

## Étapes d'installation

1. **Créer et activer un environnement virtuel** (recommandé) :
   ```sh
   python -m venv venv
   ```
2. **Activer l'exécution des scripts en ligne de commande (Windows)** :
   Si vous utilisez Windows, vous devez activer l'exécution de scripts PowerShell afin de pouvoir activer l'environnement virtuel. Pour ce faire, ouvrez une fenêtre PowerShell en tant qu'administrateur et exécutez la commande suivante :

   ```sh
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

   ```

3. Activer l'environnement virtuel

   ```
   source venv/bin/activate  # Sur macOS/Linux
   .\venv\Scripts\activate  # Sur Windows
   ```

4. **Installer les dépendances** :
   ```sh
   pip install -r requirements.txt
   ```

## Lancer l'interface graphique

1. Exécuter le script principal :

   ```sh
   python run.py
   ```

2. Ouvrir le lien affiché dans le terminal (généralement `http://127.0.0.1:5000`).

## Structure du projet et execution des fonctions tierces qui gère le backend et le mastermind

Le projet utilise Flask, et le dossier `mastermind` est un **package Python** . Ainsi, pour exécuter des fichiers internes, il faut utiliser la commande suivante :

```sh
python -m app.mastermind.[nomdufichiersansextension]
```

Exemple pour démarrer l'application :

```sh
python -m app.mastermind.figures
```

## Tests:

Nous avons fait une batterie de tests unitaires via la librairie unittest, ils sont situés dans le dossiers tests, pour exécuter les test:

```sh
python -m unittest discover -s tests
```
