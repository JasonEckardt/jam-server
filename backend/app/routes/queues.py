from flask import Blueprint, request
from app import db
from app.api import spotify
from app.models.queue import Queue
import config.spotify_urls as urls
import re

queues = Blueprint("queues", __name__)


def extract_track_id(url):
    match = re.search(r"spotify\.com/track/([A-Za-z0-9_-]+)", url)
    if match:
        return match.group(1)
    return None


def get_or_create_queue(queue_id="main"):
    queue = Queue.query.get(queue_id)
    if not queue:
        # we may want to ask the admin for session name
        queue = Queue(id=queue_id, name="Main Session", tracks=[])
        db.session.add(queue)
        db.session.commit()
    return queue


@queues.route("/queues/")
def list_queues():
    queues = Queue.query.all()
    queues_list = []
    for q in queues:
        queues_list.append(
            {
                "id": q.id,
                "name": q.name,
                "current_track": q.current_track,
                "queue_length": len(q.tracks),
                "created_at": q.created_at.isoformat(),
            }
        )
    if len(queues_list) == 0:
        q = get_or_create_queue()
    queues_list.append(
        {
            "id": q.id,
            "name": q.name,
            "current_track": q.current_track,
            "queue_length": len(q.tracks),
            "created_at": q.created_at.isoformat(),
        }
    )
    return {"queues": queues_list}, 200


@queues.route("/queues/<queue_id>", methods=["GET"])
def get_queue(queue_id):
    # Should be get_session and return 404 if session dne
    queue = get_or_create_queue(queue_id)
    queue_data = []
    for track_id in queue.tracks:
        track = spotify.request_api(urls.track(track_id), headers=urls.get_headers())
        if "error" in track:
            return track
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
    return {"queue_id": queue.id, "name": queue.name, "tracks": queue_data}


@queues.route("/queues/<queue_id>/tracks", methods=["POST"])
def add_track(queue_id):
    data = request.json

    url = data.get("url")
    if not url:
        return {"error": "URL not provided"}

    track_id = extract_track_id(url)
    if not track_id:
        return {"error": "Invalid track URL"}

    track_response = spotify.request_api(
        urls.track(track_id), headers=urls.get_headers()
    )
    if "error" in track_response:
        return track_response, 401
    queue = get_or_create_queue(queue_id)
    queue.tracks.append(track_id)
    db.session.commit()

    return {"track_id": track_id}, 201


@queues.route("/queues/<queue_id>/tracks/<track_id>", methods=["DELETE"])
def remove_track(queue_id, track_id):

    return {"removed_track_id": track_id}, 204
