from flask import Blueprint, request, session
from flask_socketio import emit, join_room
from app import db, socketio
from app.models.queue import Queue
from app.models.user import User
import re
from threading import Lock

queues_bp = Blueprint("queues", __name__)
queue_lock = Lock()


def extract_track_id(url):
    """Extract Spotify track ID from a URL."""
    match = re.search(r"spotify\.com/track/([A-Za-z0-9_-]+)", url)
    return match.group(1) if match else None


def get_queue(queue_id):
    return db.session.get(Queue, queue_id)


@socketio.on("join_queue")
def ws_join_queue(data):
    """Client joins a queue; send full snapshot once."""
    queue_id = data["queue_id"]

    join_room(queue_id)

    queue = get_queue(queue_id)
    if not queue:
        emit("error", {"error": f"Queue {queue_id} not found"})
        return

    emit(
        "queue_snapshot",
        {"queue_id": queue.id, "tracks": queue.tracks, "name": queue.name},
    )


@socketio.on("add_track")
def ws_add_track(data):
    """Client requests to add a track."""
    queue_id = data["queue_id"]
    track_id = data["track_id"]

    queue = get_queue(queue_id)
    if not queue:
        emit("error", {"error": f"Queue {queue_id} not found"})
        return

    with queue_lock:
        queue.tracks.append(track_id)
        db.session.commit()

    # Broadcast patch to everyone (including sender)
    emit("queue_patch", {"event": "add", "track_id": track_id}, room=queue_id)


@socketio.on("remove_track")
def ws_remove_track(data):
    queue_id = data["queue_id"]
    track_id = data["track_id"]

    queue = get_queue(queue_id)
    if not queue:
        emit("error", {"error": f"Queue {queue_id} not found"})
        return

    with queue_lock:
        if track_id in queue.tracks:
            queue.tracks.remove(track_id)
            db.session.commit()

    emit("queue_patch", {"event": "remove", "track_id": track_id}, room=queue_id)


@socketio.on("move_track")
def ws_move_track(data):
    """Reorder tracks in the queue."""
    queue_id = data["queue_id"]
    old_index = data["from"]
    new_index = data["to"]

    queue = get_queue(queue_id)
    if not queue:
        emit("error", {"error": f"Queue {queue_id} not found"})
        return

    with queue_lock:
        try:
            track = queue.tracks.pop(old_index)
            queue.tracks.insert(new_index, track)
            db.session.commit()
        except IndexError:
            emit("error", {"error": "Invalid index"})
            return

    emit(
        "queue_patch",
        {"event": "move", "from": old_index, "to": new_index},
        room=queue_id,
    )


@socketio.on("clear_queue")
def ws_clear_queue(data):
    queue_id = data["queue_id"]

    queue = get_queue(queue_id)
    if not queue:
        emit("error", {"error": f"Queue {queue_id} not found"})
        return

    with queue_lock:
        queue.tracks = []
        db.session.commit()

    emit("queue_patch", {"event": "clear"}, room=queue_id)
