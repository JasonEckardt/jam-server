from app.api import spotify
from app.models.user import User
from flask import Blueprint, redirect, session
import config.spotify_urls as urls
import os
import requests

users = Blueprint("users", __name__)


@users.route("/me")
def me():
    token = spotify.get_current_user_token()
    if not token:
        return redirect(f"{os.getenv('BACKEND_URL')}/login")

    headers = {"Authorization": f"Bearer {token}"}
    user, status_code = spotify.request_api(urls.USER_PROFILE, headers)
    if status_code != 200:
        return {"Failed to login: {user}"}, status_code

    user_id = session.get("user_id")
    if not user_id:
        return {"error", "User ID missing from session"}, 401

    user_db = User.query.filter_by(user_id=user_id).first()
    if user_db:
        user["expires_at"] = user_db.expires_at.isoformat()
    # TODO: Also append user["user_role"] to data.
    return user


@users.route("/playlists")
def playlists():
    playlist_response, status_code = spotify.request_api(
        urls.USER_PLAYLISTS, headers=urls.get_headers()
    )
    if status_code != 200:
        return {
            "error": f"Failed to fetch playlists: {playlist_response['error']}"
        }, status_code

    playlists_data = playlist_response.get("items", [])
    playlists = [
        {
            "id": p.get("id"),
            "description": p.get("description"),
            "images": p.get("images"),
            "link": f"/playlists/{p.get('id')}",
            "name": p.get("name"),
            "owner": p.get("owner"),
            "track_count": p.get("tracks", {}).get("total"),
        }
        for p in playlists_data
    ]
    return {"playlists": playlists}, 200


@users.route("/playlists/<playlist_id>")
def playlist_tracks(playlist_id):
    playlist_tracks_response, status_code = requests.get(
        urls.playlist_tracks(playlist_id), headers=urls.get_headers()
    )

    if status_code != 200:
        return {
            "error": f"Failed to fetch tracks: {playlist_tracks_response['error']}"
        }, status_code

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


@users.route("/tracks")
def top_tracks():
    response, status_code = requests.get(
        urls.user_top_items("tracks"), headers=urls.get_headers()
    )

    if status_code != 200:
        return {
            "error": "Failed to fetch top tracks",
        }, status_code

    tracks = response.json().get("items", [])
    return {"tracks": tracks}
