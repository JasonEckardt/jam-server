from flask import Blueprint

application = Blueprint("application", __name__)


def index():
    return "Welcome to party jam!"


def status():
    return "Spotify Jam server v0.2.0 running"
