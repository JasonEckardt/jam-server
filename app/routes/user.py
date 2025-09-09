from config.spotify_urls import SpotifyAPI
from flask import Blueprint
import os
import requests
import urllib

user = Blueprint("user", __name__)


@user.route("/me")
def me():
    headers = {"Authorization": f"Bearer {os.getenv('token')}"}

    user_profile = requests.get(SpotifyAPI.USER_PROFILE, headers=headers)
    if user_profile.status_code != 200:
        return "Failed to fetch profile", 400

    profile = user_profile.json()
    return profile


@user.route("/library")
def library():
    headers = {"Authorization": f"Bearer {os.getenv('token')}"}
    limit_artists = 5
    limit_tracks = 20
    request_params_artists = {"limit": limit_artists}
    request_params_tracks = {"limit": limit_tracks}

    user_profile = requests.get(SpotifyAPI.USER_PROFILE, headers=headers)
    if user_profile.status_code != 200:
        return "Failed to fetch profile", 400

    user_top_artists_url = SpotifyAPI.get_user_top_items(
        "artists"
    ) + urllib.parse.urlencode(request_params_artists)
    user_top_tracks_url = SpotifyAPI.get_user_top_items(
        "tracks"
    ) + urllib.parse.urlencode(request_params_tracks)

    artists_request = requests.get(user_top_artists_url, headers=headers)
    artists = (
        artists_request.json().get("items", [])
        if artists_request.status_code == 200
        else []
    )

    tracks_request = requests.get(user_top_tracks_url, headers=headers)
    tracks = (
        tracks_request.json().get("items", [])
        if tracks_request.status_code == 200
        else []
    )

    return {"top_artists": artists, "top_tracks": tracks}


@user.route("/playlists")
def user_playlists():
    headers = {"Authorization": f"Bearer {os.getenv('token')}"}


@user.route("/tracks")
def user_tracks():
    return "User tracks:"
