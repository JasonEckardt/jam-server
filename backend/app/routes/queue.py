from config.spotify_urls import urls
from flask import Blueprint, request
import re
import requests


## tmp ##
## This will be replaced with MySQL later
class QueueStore:
    def __init__(self):
        self._queue = []

    def show(self):
        return list(self._queue)

    def add(self, track_id):
        self._queue.append(track_id)

    def remove(self, track_id):
        if track_id in self._queue:
            self._queue.remove(track_id)


## @TODO Change the queue to be non-descructive, use a pointer to move through the queue! Append only

queue = Blueprint("queue", __name__)
store = QueueStore()


def extract_track_id(url):
    match = re.search(r"spotify\.com/track/([A-Za-z0-9_-]+)", url)
    if match:
        return match.group(1)
    return None


def get_track_info(track_id):
    track_info = requests.get(urls.track(track_id), headers=urls.get_headers())
    if track_info.status_code != 200:
        return {"error": "Failed to fetch profile"}, 400

    track = track_info.json()
    return track


@queue.route("/queue", methods=["GET"])
def get_queue():
    queue_data = []
    for track_id in store.show():
        track = get_track_info(track_id)
        queue_data.append(
            {
                "id": track.get("id"),
                "name": track.get("name"),
                "artists": [a.get("name") for a in track.get("artists", [])],
                "album": track.get("album", {}).get("name"),
                "duration_ms": track.get("duration_ms"),
                "images": track.get("album", {}).get("images", []),
            }
        )
    return {"queue": queue_data}


@queue.route("/queue", methods=["POST"])
def add_to_queue():
    data = request.json
    url = data.get("url")

    if not url:
        return {"error": "URL not provided"}, 400
    track_id = extract_track_id(url)

    if not track_id:
        return {"error": "Invalid track URL"}, 400

    response = requests.get(
        f"https://api.spotify.com/v1/tracks/{track_id}", headers=urls.get_headers()
    )
    if response.status_code != 200:
        return {
            "error": "Failed to fetch track",
            "status": response.status_code,
        }, 400

    store.add(track_id)
    return {"track_id": track_id}, 201


@queue.route("/queue/<track_id>", methods=["DELETE"])
def remove_from_queue(track_id):
    store.remove(track_id)
    return {"removed_track_id": track_id}
