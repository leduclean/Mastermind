import time
import os
import sass

scss_dir = 'app/static/scss'
css_dir = 'app/static/css'

input_file = os.path.join(scss_dir, 'human_player.scss')
output_file = os.path.join(css_dir, 'human_player.css')

# Fonction pour compiler le SCSS en CSS
def watch_scss():
    scss_file = input_file
    css_file = output_file
    last_mod = os.path.getmtime(scss_file)
    while True:
        time.sleep(1)
        new_mod = os.path.getmtime(scss_file)
        if new_mod != last_mod:
            compiled = sass.compile(filename=scss_file)
            with open(css_file, 'w') as f:
                f.write(compiled)
            print("SCSS recompilé !")
            last_mod = new_mod
