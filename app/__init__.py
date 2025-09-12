from flask import Flask
from .routes.application import application
from .routes.auth import auth
from .routes.player import player
from .routes.queue import queue
from .routes.user import user


def create_app():
    app = Flask(__name__)
    app.register_blueprint(application)
    app.register_blueprint(auth)
    app.register_blueprint(player)
    app.register_blueprint(queue)
    app.register_blueprint(user)

    return app
