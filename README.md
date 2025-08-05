# Mastermind – Web Interface with Flask

An interactive web interface for the classic Mastermind game, built in Python using the Flask micro-framework. Multiple versions of the Codebreaker and Codemaker engines have been implemented, from basic strategies up to Knuth’s five-guess algorithm.

## Prerequisites

- **Python 3.9** or higher
- **pip** (Python package installer)

## Installation

1. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate      # macOS / Linux
   .\venv\Scripts\activate       # Windows

2. **Install dependencies**


```pip install -r requirements.txt```

## Running the Application

From the project root, start the Flask server:
```python run.py```

Open the URL displayed in your browser (default: http://127.0.0.1:5000).

## Game Configuration
Edit app/mastermind/common.py to adjust:

- LENGTH: number of pegs (max 8)
- COLORS: available color options

The UI will adapt automatically to these settings.

## Project Structure

- **Game Logic Modules**: basic to advanced strategies (codebreaker1.py → codebreaker3.py), Codemaker implementations (codemaker1.py, codemaker2.py, …), Knuth’s five-guess algorithm in the most advanced version

- **Utility Modules**: common.py, figures.py, past_evaluations.py

- **UI Templates**: templates/*.html

- **Static Assets**: static/css, static/js

- **Unit Tests**: tests/

### Running Backend Modules
To execute any internal module directly:
```python -m app.mastermind.<module_name>```

For example:
```python -m app.mastermind.figures```

### Testing
Discover and run all unit tests:

```python -m unittest discover -s tests```

### Authors
Personal/university project at "La Prepa des INP" by Leandre LE DUC and Simon VAN BOMMEL
