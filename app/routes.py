# app/routes.py
import os, uuid, urllib, requests
from flask import redirect, request
from app.api import get_access_token


def register(app):

    @app.route("/")
    def index():
        return "Welcome to Party Jam!"

    @app.route("/status")
    def status():
        return "Spotify server v.0.1.0 running"

    @app.route("/login")
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

    @app.route("/callback")
    def callback():
        code = request.args.get("code")
        if not code:
            return "No authorization code received", 400
        credentials = get_access_token(authorization_code=code)
        os.environ["token"] = credentials["access_token"]
        return redirect("/me")

    @app.route("/me")
    def me():
        user_profile_url = "https://api.spotify.com/v1/me"
        user_top_items_url = "https://api.spotify.com/v1/me/top/artists?limit=20"
        headers = {"Authorization": f"Bearer {os.getenv('token')}"}

        user_profile = requests.get(user_profile_url, headers=headers)
        if user_profile.status_code != 200:
            return "Failed to fetch profile", 400

        profile = user_profile.json()
        display_name = profile.get("display_name")

        artists_resp = requests.get(user_top_items_url, headers=headers)
        artists = (
            artists_resp.json().get("items", [])
            if artists_resp.status_code == 200
            else []
        )

        return {"display_name": display_name, "top_artists": artists}

    @app.route("/library")
    def library():
        return "User library"

    @app.route("/playlists")
    def user_playlists():
        return "User playlists:"

    @app.route("/tracks")
    def user_tracks():
        return "User tracks:"
