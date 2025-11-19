from app import db
from app.api import spotify
from app.models.queue import Queue
from app.models.user import User
from flask import Blueprint, request, session
import config.spotify_urls as urls
import re
import uuid

queues = Blueprint("queues", __name__)


def extract_track_id(url):
    match = re.search(r"spotify\.com/track/([A-Za-z0-9_-]+)", url)
    if match:
        return match.group(1)
    return None


def get_or_create_queue(queue_id="main"):
    queue = db.session.get(Queue, queue_id)
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


@queues.route("/queues/<string:queue_id>", methods=["GET"])
def get_queue(queue_id: str):
    # Should be get_session and return 404 if session dne
    queue = db.session.get(Queue, queue_id)
    queue_data = []
    for track_id in queue.tracks:
        track, status_code = spotify.request_api(
            urls.track(track_id), headers=urls.get_headers()
        )
        if status_code != 200:
            return {"error": f"Failed to add track: {track['error']}"}
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


@queues.route("/queues/new/<string:queue_name>", methods=["POST"])
def create_queue(queue_name: str):
    queue_id = "main"
    queue = Queue(id=queue_id, name=queue_name, tracks=[])
    if queue:
        return {"error": f"Queue {queue_name}, {queue_id} already exists."}, 409
    db.session.add(queue)
    db.session.commit()
    return {"message": f"Created queue {queue_name} with id {queue_id}"}, 200


@queues.route("/queues/<string:queue_id>/tracks", methods=["POST"])
def add_track(queue_id: str):
    data = request.get_json(force=True)
    url = data.get("url")
    if not url:
        return {"error": "URL not provided"}, 400

    track_id = extract_track_id(url)
    if not track_id:
        return {"error": "Invalid track URL"}, 400

    user_id = session.get("user_id")
    if not user_id:
        return {"error": "User not logged in"}, 401

    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return {"error": "User not found"}, 404

    token = spotify.get_current_user_token()
    if not token or user.is_expired():
        token = spotify.refresh_access_token()

    if not token:
        return {"error": "Unable to obtain Spotify token"}, 401

    track_response, status_code = spotify.request_api(
        urls.track(track_id), headers={"Authorization": f"Bearer {token}"}
    )
    if status_code != 200:
        return {"error": f"Failed to get track: {track_response['error']}"}, 401

    queue = db.session.get(Queue, queue_id)
    queue.tracks.append(track_id)
    db.session.commit()

    return {"track_id": track_id}, 201


@queues.route("/queues/<queue_id>/clear", methods=["POST"])
def clear_queue(queue_id):
    #  TODO Make this admin only command
    queue = Queue.query.filter_by(id=queue_id).first()
    if not queue:
        return {"error": "Queue not found"}, 404

    queue.tracks = []
    db.session.commit()

    return f"Queue {queue_id} cleared", 200


@queues.route("/queues/<queue_id>/tracks/<track_id>", methods=["DELETE"])
def remove_track(queue_id: str, track_id: str):

    return {"removed_track_id": track_id}, 204
