import pymysql

pymysql.install_as_MySQLdb()

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
socketio = SocketIO()


def create_app(test_config=None):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mysql+pymysql://spotifyuser:spotifypass@127.0.0.1:3306/spotifyjam"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
    }

    app.secret_key = os.getenv("SECRET_KEY")

    # Session config
    app.config.update(SESSION_COOKIE_SAMESITE="Lax", SESSION_COOKIE_SECURE=False)

    # CORS config
    frontend_url = os.getenv("FRONTEND_URL")
    if not frontend_url:
        print("FRONTEND_URL is not set! Using default http://localhost:5173")
        frontend_url = "http://localhost:5173"
    CORS(app, supports_credentials=True, origins=[frontend_url])

    # Initialize extensions
    db.init_app(app)
    socketio.init_app(
        app,
        cors_allowed_origins=[frontend_url],
        logger=True,
        engineio_logger=True,
    )

    if test_config:
        app.config.update(test_config)

    Migrate(app, db)

    from .routes.application import application
    from .routes.auth import auth
    from .routes.devices import devices
    from .routes.player import player
    from .routes.users import users
    from .routes.queues import queues

    app.register_blueprint(application)
    app.register_blueprint(auth)
    app.register_blueprint(devices)
    app.register_blueprint(player)
    app.register_blueprint(users)
    app.register_blueprint(queues)

    from app.models.queue import Queue
    from app.models.track import Track
    from app.models.user import User

    return app
