from app import db
from app.api import spotify
from app.models.queue import Queue
from app.routes import queues
from flask import Blueprint
import config.spotify_urls as urls
import requests

player = Blueprint("player", __name__)
devices_data = dict()


@player.route("/devices")
def devices():
    devices_response, status = spotify.request_api(
        urls.DEVICES, headers=urls.get_headers()
    )
    return devices_response, status


@player.route("/devices/select/<string:id>", methods=["POST"])
def devices_select(id: str) -> dict:
    devices_response = spotify.request_api(urls.DEVICES, headers=urls.get_headers())

    devices_list = devices_response.get("devices", [])
    if not devices_list:
        return {"error": "Error getting devices."}, 400

    device_select = next((d for d in devices_list if d["id"] == id), None)
    if not device_select:
        return {"error": f"Device {id} not found."}, 404

    queue = db.session.get(Queue, "main")
    queue.active_device = device_select["id"]
    db.session.commit()

    return device_select


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
