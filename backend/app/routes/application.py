from flask import Blueprint
import os

application = Blueprint("application", __name__)


@application.route("/")
def index():
    return (
        f'Welcome to the party jam! <a href="{os.getenv("BACKEND_URL")}/me">Login</a>'
    )


@application.route("/status")
def status():
    return "Party Jam server v0.5.0 running"
