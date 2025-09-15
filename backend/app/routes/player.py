from app.routes.queue import store
from config.spotify_urls import urls
from flask import Blueprint
import requests


player = Blueprint("player", __name__)


# def next_track():
#     queue = store.show()
#     if queue:
#         store.remove(queue[0])
#         updated_queue = store.show()
#         if updated_queue:
#             play_track(updated_queue[0])


@player.route("/devices")
def devices():
    devices_request = requests.get(urls.devices, headers=urls.get_headers())
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


@player.route("/player")
def player_state():
    devices_response = requests.get(urls.devices, headers=urls.get_headers())
    try:
        devices_data = devices_response.json()
        devices_list = devices_data.get("devices", [])
    except ValueError:
        devices_list = []

    if len(devices_list) == 0:
        return {"message": "No devices available for player"}, 400

    player_state_response = requests.get(urls.player, headers=urls.get_headers())
    try:
        data = player_state_response.json()
    except ValueError:
        data = {"message": "Failed to get player"}

    if player_state_response.status_code == 200:
        return data
    else:
        error = data.get("error", data)
        return {"error": error, "code": player_state_response.status_code}


@player.route("/player/next", methods=["POST"])
def skip():
    next_track()
    return {"status": "ok"}


@player.route("/player/pause", methods=["POST"])
def pause_player():
    pause_player_response = requests.put(urls.pause, headers=urls.get_headers())
    if pause_player_response.status_code == 200:
        return {"status": "paused"}
    return {"status_code": pause_player_response.status_code}


@player.route("/player/play", methods=["POST"])
def play_player():
    if not store.show():
        return {"error": "No track to play"}, 400

    track_id = store.show()[0]
    data = {"uris": [f"spotify:track:{track_id}"]}

    response = requests.put(urls.playback, headers=urls.get_headers(), json=data)

    if response.status_code == 204:
        return {"status": "playing"}
    else:
        error = response.json().get("error", {"message": "Failed to play track"})
        return {"error": error, "code": response.status_code}
