# app/user.py
import os
import requests
from flask import Blueprint

user = Blueprint("user", __name__)


@user.route("/me")
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
        artists_resp.json().get("items", []) if artists_resp.status_code == 200 else []
    )

    return {"display_name": display_name, "top_artists": artists}


@user.route("/library")
def library():
    return "User library"


@user.route("/playlists")
def user_playlists():
    return "User playlists:"


@user.route("/tracks")
def user_tracks():
    return "User tracks:"
