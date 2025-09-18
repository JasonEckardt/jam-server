from app.routes.queues import queues
from flask import Blueprint
import config.spotify_urls as urls
import requests


player = Blueprint("player", __name__)


@player.route("/devices")
def devices():
    devices_request = requests.get(urls.DEVICES, headers=urls.get_headers())
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
    devices_response = requests.get(urls.DEVICES, headers=urls.get_headers())
    try:
        devices_data = devices_response.json()
        devices_list = devices_data.get("devices", [])
    except ValueError:
        devices_list = []

    if len(devices_list) == 0:
        return {"message": "No devices available for player"}, 400

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
def skip_player():
    queue = store.show()
    if not queue:
        return {"error": "Queue is empty"}, 400

    # Remove the current track
    store.remove(queue[0])

    updated_queue = store.show()
    if not updated_queue:
        # No next track, just pause playback
        requests.put(urls.PAUSE, headers=urls.get_headers())
        return {"status": "no next track", "player": None}

    # Play the next track
    next_track_id = updated_queue[0]
    data = {"uris": [f"spotify:track:{next_track_id}"]}
    response = requests.put(urls.PLAYBACK, headers=urls.get_headers(), json=data)

    if response.status_code == 204:
        # Fetch updated player state
        player_response = requests.get(urls.PLAYER, headers=urls.get_headers())
        player_data = (
            player_response.json() if player_response.status_code == 200 else None
        )
        return {"status": "playing next track", "player": player_data}
    else:
        try:
            error_data = response.json()
        except ValueError:
            error_data = {"message": "Failed to play next track"}
        return {"error": error_data, "code": response.status_code}


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
