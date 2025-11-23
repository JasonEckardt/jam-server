from app import db
from app.api import spotify
from app.models.queue import Queue
from flask import Blueprint
import config.spotify_urls as urls
import requests

player = Blueprint("player", __name__)


@player.route("/player")
def player_state():
    player_state_response = requests.get(urls.PLAYER, headers=urls.get_headers())
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
def player_next():
    queue = db.session.get(Queue, "main")
    return queue


@player.route("/player/pause", methods=["POST"])
def pause_player():
    pause_player_response = requests.put(urls.PAUSE, headers=urls.get_headers())
    if pause_player_response.status_code == 200:
        return {"status": "paused"}
    return {"status_code": pause_player_response.status_code}


@player.route("/player/play", methods=["POST"])
def play_player():
    # First, get the active device ID from the queue
    queue = db.session.get(Queue, "main")
    if not queue.active_device:
        return {"error": "No active device selected."}, 400

    # Now, we need to check the private mode of the active device.
    # We will call the devices endpoint to get the list of devices and then check the active device's `is_private_session`.
    devices_response, status = spotify.request_api(
        urls.DEVICES, headers=urls.get_headers()
    )
    if status != 200:
        return {"error": "Failed to get devices."}, status

    devices_list = devices_response.get("devices", [])
    active_device = next(
        (d for d in devices_list if d["id"] == queue.active_device), None
    )
    if not active_device:
        return {"error": "Active device not found in the list."}, 400

    if not active_device.get("is_private_session", False):
        return {"error": "Private mode is not enabled."}, 403

    # If we passed the check, then proceed with the playback
    response = requests.put(urls.PLAYBACK, headers=urls.get_headers())

    if response.status_code == 204:  # success
        player_response = requests.get(urls.PLAYER, headers=urls.get_headers())
        if player_response.status_code == 200:
            return {"status": "playing", "player": player_response.json()}
        else:
            return {"status": "playing", "player": None}
    else:
        # Only try to parse JSON if there is content
        try:
            error_data = response.json()
        except ValueError:
            error_data = {"message": "Failed to resume playback"}
        return {"error": error_data, "code": response.status_code}
