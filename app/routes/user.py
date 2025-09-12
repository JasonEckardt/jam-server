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
    limit_artists = 10
    limit_tracks = 10
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

    user_profile = requests.get(SpotifyAPI.USER_PROFILE, headers=headers)
    if user_profile.status_code != 200:
        return "Failed to fetch profile", 400

    playlists_request = requests.get(SpotifyAPI.USER_PLAYLISTS, headers=headers)
    playlists_data = (
        playlists_request.json().get("items", [])
        if playlists_request.status_code == 200
        else []
    )

    playlists = []
    for playlist in playlists_data:
        playlists.append(
            {
                "id": playlist.get("id"),
                "description": playlist.get("description"),
                "images": playlist.get("images"),
                "link": f"/playlists/{playlist.get('id')}",
                "name": playlist.get("name"),
                "owner": playlist.get("owner"),
                "track_count": playlist.get("tracks", {}).get("total"),
            }
        )

    return {"playlists": playlists}

@user.route("/playlists/<playlist_id>")
def playlist_tracks(playlist_id):
    headers = {"Authorization": f"Bearer {os.getenv('token')}"}
    tracks_request = requests.get(SpotifyAPI.get_playlist_tracks(playlist_id), headers=headers)

    if tracks_request.status_code != 200:
        return "Failed to fetch tracks", 400

    tracks_data = tracks_request.json().get("items", [])

    playlist_tracks = []
    for item in tracks_data:
        track = item.get("track", {})
        playlist_tracks.append(
            {
                "id": track.get("id"),
                "name": track.get("name"),
                "artists": [a.get("name") for a in track.get("artists", [])],
                "album": track.get("album", {}).get("name"),
                "duration_ms": track.get("duration_ms"),
                "preview_url": track.get("preview_url"),
            }
        )

    return {"palylist_tracks": playlist_tracks}



@user.route("/tracks")
def user_tracks():
    return "User tracks:"
