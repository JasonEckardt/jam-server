from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


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

    # TODO: dev setting? probably not production ready
    app.config.update(SESSION_COOKIE_SAMESITE="Lax", SESSION_COOKIE_SECURE=False)
    CORS(app, supports_credentials=True, origins=[os.getenv("FRONTEND_URL")])
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    Migrate(app, db)

    from .routes.application import application
    from .routes.auth import auth
    from .routes.player import player
    from .routes.queues import queues
    from .routes.users import users

    app.register_blueprint(application)
    app.register_blueprint(auth)
    app.register_blueprint(player)
    app.register_blueprint(queues)
    app.register_blueprint(users)

    return app
