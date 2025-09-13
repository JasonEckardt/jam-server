from app.routes.queue import store
from config.spotify_urls import urls
from flask import Blueprint
import os
import requests


player = Blueprint("player", __name__)


# def next_track():
#     queue = store.show()
#     if queue:
#         store.remove(queue[0])
#         updated_queue = store.show()
#         if updated_queue:
#             play_track(updated_queue[0])


@player.route("/player")
def player_state():
    return "playback state"


@player.route("/player/devices")
def devices():
    headers = {"Authorization": f"Bearer {os.getenv('token')}"}
    devices_request = requests.get(urls.devices, headers=headers)
    if devices_request.status_code == 200:
        devices = devices_request.json().get("devices", [])
        return {"devices": devices}
    else:
        error = devices_request.json().get(
            "error",
            {
                "message": "Failed to fetch devices",
                "status": devices_request.status_code,
            },
        )
        return {"error": error, "code": devices_request.status_code}


# @player.route("/player/next", methods=["POST"])
# def skip():
#     next_track()
#     return {"status": "ok"}


@player.route("/player/pause", methods=["POST"])
def pause_route():
    headers = {"Authorization": f"Bearer {os.getenv('token')}"}
    response = requests.put(urls.pause, headers=headers)

    if response.status_code == 204:
        return {"status": "paused"}
    else:
        error = response.json().get("error", {"message": "Failed to pause track"})
        return {"error": error, "code": response.status_code}


@player.route("/player/play", methods=["POST"])
def play_route():
    if not store.show():
        return {"error": "No track to play"}, 400

    track_id = store.show()[0]
    headers = {"Authorization": f"Bearer {os.getenv('token')}"}
    data = {"uris": [f"spotify:track:{track_id}"]}

    response = requests.put(urls.playback, headers=headers, json=data)

    if response.status_code == 204:  # Spotify returns 204 for success
        return {"status": "playing"}
    else:
        error = response.json().get("error", {"message": "Failed to play track"})
        return {"error": error, "code": response.status_code}
