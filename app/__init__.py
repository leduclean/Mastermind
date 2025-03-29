# from  app.watch_scss import watch_scss
import os
import threading

from flask import Flask

# def start_scss_thread():
#     thread = threading.Thread(target = watch_scss, daemon=True)
#     thread.start()


def create_app():
    app = Flask(__name__)
    app.debug = False

    # if app.debug:
    #     start_scss_thread()

    from app.routes import main

    app.register_blueprint(main)
    return app


from app import create_app

app = create_app()
