from flask import Blueprint

application = Blueprint("application", __name__)


@application.route("/")
def index():
    return "Welcome to party jam!"


@application.route("/status")
def status():
    return "Spotify Jam server v0.2.0 running"
