from flask import Flask, redirect, request
import os
import requests
import urllib
import uuid


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


app = Flask(__name__)


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
    user_profile_url = "https://api.spotify.com/v1/me?"
    user_top_items_url = "https://api.spotify.com/v1/me/top/"
    audio_features_url = "https://api.spotify.com/v1/audio-features/"
    limit_tracks = 20
    headers = {"Authorization": f"Bearer {os.getenv('token')}"}
    request_params_artists = {"limit": limit_tracks}
    request_params_tracks = {"limit": 18}

    user_profile = requests.get(user_profile_url, headers=headers)
    if user_profile.status_code == 200:
        user_profile = user_profile.json()
        display_name = user_profile["display_name"]
        top_artists_url = (
            user_top_items_url
            + "artists?"
            + urllib.parse.urlencode(request_params_artists)
        )
        artists = requests.get(top_artists_url, headers=headers)
        if artists.status_code == 200:
            artists = artists.json()
            artists = artists["items"]
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


if __name__ == "__main__":
    app.run(debug=True)
