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
    user = spotify.request_api(urls.USER_PROFILE, headers)
    if "error" in user:
        return user, user.get("status", 502)

    user_id = session.get("user_id")
    if not user_id:
        raise Exception(f"user_id missing for {user}")

    user_db = User.query.filter_by(user_id=user_id).first()
    if user_db:
        user["expires_at"] = user_db.expires_at.isoformat()

    return user


@users.route("/playlists")
def playlists():
    response = spotify.request_api(urls.USER_PLAYLISTS, headers=urls.get_headers())
    if "error" in response:
        return response, response.get("status", 502)

    playlists_data = response.get("items", [])
    playlists = []

    for p in playlists_data:
        playlists.append(
            {
                "id": p.get("id"),
                "description": p.get("description"),
                "images": p.get("images"),
                "link": f"/playlists/{p.get('id')}",
                "name": p.get("name"),
                "owner": p.get("owner"),
                "track_count": p.get("tracks", {}).get("total"),
            }
        )

    return {"playlists": playlists}


@users.route("/playlists/<playlist_id>")
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


@users.route("/tracks")
def top_tracks():
    response = requests.get(urls.user_top_items("tracks"), headers=urls.get_headers())

    if response.status_code != 200:
        return {
            "error": "Failed to fetch top tracks",
            "status": response.status_code,
        }, response.status_code

    tracks = response.json().get("items", [])
    return {"tracks": tracks}
