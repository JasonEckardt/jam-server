from flask import Blueprint
import os

application = Blueprint("application", __name__)


@application.route("/")
def index():
    return f'Welcome to party jam! <a href="{os.getenv("BACKEND_URL")}/me">Login</a>'


@application.route("/status")
def status():
    return "Spotify Jam server v0.3.1 running"
