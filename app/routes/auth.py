from flask import Blueprint, redirect, request
import os
import requests
import urllib
import uuid


auth = Blueprint("auth", __name__)


def get_access_token(authorization_code: str):
    spotify_request_access_token_url = "https://accounts.spotify.com/api/token"
    body = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
        "client_secret": os.getenv("SPOTIFY_CLIENT_SECRET"),
        "redirect_uri": os.getenv("SPOTIFY_REDIRECT_URI"),
    }
    response = requests.post(spotify_request_access_token_url, data=body)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f"Failed to obtain access token: {response.status_code}, {response.text}"
        )


@auth.route("/login")
def login():
    authentication_request_params = {
        "response_type": "code",
        "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
        "redirect_uri": os.getenv("SPOTIFY_REDIRECT_URI"),
        "scope": "playlist-read-private playlist-read-collaborative user-top-read user-read-recently-played user-library-read",
        "state": str(uuid.uuid4()),
        "show_dialog": "true",
    }
    auth_url = "https://accounts.spotify.com/authorize/?" + urllib.parse.urlencode(
        authentication_request_params
    )
    return redirect(auth_url)


@auth.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "No authorization code received", 400
    credentials = get_access_token(authorization_code=code)
    os.environ["token"] = credentials["access_token"]
    return redirect("/me")
