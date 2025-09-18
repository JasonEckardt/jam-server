from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mysql+pymysql://spotifyuser:spotifypass@127.0.0.1:3306/spotifyjam"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

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
