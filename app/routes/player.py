from app.routes.queue import store
from config.spotify_urls import SpotifyAPI
from flask import Blueprint
import os
import requests


player = Blueprint("player", __name__)


def device():
    return "select playback device"


def next_track():
    queue = store.show()
    if queue:
        store.remove(queue[0])
        updated_queue = store.show()
        if updated_queue:
            play(updated_queue[0])


def play(track_id=None):
    if not track_id:
        return {"error": "No track to play"}, 400

    headers = {"Authorization": f"Bearer {os.getenv('token')}"}
    data = {"uris": [f"spotify:track:{track_id}"]}

    response = requests.put(SpotifyAPI.PLAYBACK_URL, headers=headers, json=data)
    return response.status_code


@player.route("/player")
def player_state():
    return "playback state"


@player.route("/player/next", methods=["POST"])
def skip():
    next_track()
    return {"status": "ok"}


def pause():
    return "admin pause or guest vote pause playback"


@player.route("/player/play", methods=["POST"])
def play_route():
    if store.show():
        play(store.show()[0])
    return {"status": "playing"}
