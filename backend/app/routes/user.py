from app.api import spotify
from flask import Blueprint
import config.spotify_urls as urls
import requests

user = Blueprint("user", __name__)


@user.route("/me")
def me():
    user = spotify.request_api(urls.USER_PROFILE, urls.get_headers())
    return user


@user.route("/playlists")
def playlists():
    playlists_request = requests.get(urls.USER_PLAYLISTS, headers=urls.get_headers())
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
    playlist_tracks_response = requests.get(
        urls.playlist_tracks(playlist_id), headers=urls.get_headers()
    )

    if playlist_tracks_response.status_code != 200:
        return "Failed to fetch tracks", 400

    tracks_data = playlist_tracks_response.json().get("items", [])

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

    return {"playlist_tracks": playlist_tracks}


@user.route("/tracks")
def top_tracks():
    response = requests.get(urls.user_top_items("tracks"), headers=urls.get_headers())

    if response.status_code != 200:
        return {
            "error": "Failed to fetch top tracks",
            "status": response.status_code,
        }, response.status_code

    tracks = response.json().get("items", [])
    return {"tracks": tracks}
