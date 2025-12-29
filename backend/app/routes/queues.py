from flask import Blueprint, session
from flask_socketio import emit, join_room, leave_room
from app import db, socketio
from app.models.queue import Queue
import re
from threading import Lock
import requests

queues = Blueprint("queues", __name__)
queue_lock = Lock()


def extract_track_id(url):
    """Extract Spotify track ID from a URL."""
    match = re.search(r"spotify\.com/track/([A-Za-z0-9_-]+)", url)
    return match.group(1) if match else None


def get_queue(queue_id):
    return db.session.get(Queue, queue_id)


def fetch_track_metadata(track_id, access_token):
    """Fetch track metadata from Spotify API."""
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        f"https://api.spotify.com/v1/tracks/{track_id}", headers=headers
    )

    if response.status_code != 200:
        print(f"Failed to fetch track {track_id}: {response.status_code}")
        return None

    data = response.json()

    # Transform to frontend format
    return {
        "id": data["id"],
        "name": data["name"],
        "artists": [artist["name"] for artist in data["artists"]],
        "album": data["album"]["name"],
        "duration_ms": data["duration_ms"],
        "images": data["album"]["images"],
        "pending": False,
    }


def get_queue_with_metadata(queue, access_token):
    """Get queue with full track metadata."""
    tracks = []
    for track_id in queue.tracks:
        track_data = fetch_track_metadata(track_id, access_token)
        if track_data:
            tracks.append(track_data)
    return tracks


@socketio.on("join_queue")
def ws_join_queue(data):
    """Client joins a queue; send full snapshot once."""
    print(f"Client joining queue: {data}")
    queue_id = data["queue_id"]
    join_room(queue_id)

    queue = get_queue(queue_id)
    if not queue:
        print(f"Queue {queue_id} not found")
        emit("error", {"error": f"Queue {queue_id} not found"})
        return

    # Get access token (adjust based on your auth implementation)
    access_token = session.get("access_token") or data.get("access_token")

    if not access_token:
        print("No access token available")
        emit("error", {"error": "No access token available"})
        return

    # Fetch full track metadata
    tracks = get_queue_with_metadata(queue, access_token)

    print(f"Sending queue snapshot with {len(tracks)} tracks")
    emit(
        "queue_snapshot",
        {
            "queue_id": queue.id,
            "tracks": tracks,  # Send full track objects, not just IDs
            "name": queue.name,
        },
    )


@socketio.on("leave_queue")
def ws_leave_queue(data):
    """Client leaves a queue room."""
    print(f"Client leaving queue: {data}")
    queue_id = data["queue_id"]
    leave_room(queue_id)


@socketio.on("add_track")
def ws_add_track(data):
    """Client requests to add a track by URL."""
    print(f"Adding track: {data}")
    queue_id = data["queue_id"]
    url = data.get("url")

    if not url:
        emit("error", {"error": "No URL provided"})
        return

    # Extract track ID from URL
    track_id = extract_track_id(url)
    if not track_id:
        print(f"Invalid Spotify URL: {url}")
        emit("error", {"error": "Invalid Spotify URL"})
        return

    queue = get_queue(queue_id)
    if not queue:
        emit("error", {"error": f"Queue {queue_id} not found"})
        return

    # Get access token
    access_token = session.get("access_token") or data.get("access_token")
    if not access_token:
        print("No access token available for add_track")
        emit("error", {"error": "No access token available"})
        return

    # Fetch track metadata
    track_data = fetch_track_metadata(track_id, access_token)
    if not track_data:
        emit("error", {"error": "Failed to fetch track metadata"})
        return

    with queue_lock:
        queue.tracks.append(track_id)
        db.session.commit()

    print(f"Track added successfully: {track_data['name']}")
    # Broadcast patch with full track object to everyone (including sender)
    emit(
        "queue_patch",
        {"event": "add", "track": track_data},  # Send full track object
        room=queue_id,
    )


@socketio.on("remove_track")
def ws_remove_track(data):
    """Remove a track from the queue."""
    print(f"Removing track: {data}")
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
        else:
            emit("error", {"error": "Track not found in queue"})
            return

    print(f"Track removed successfully: {track_id}")
    emit("queue_patch", {"event": "remove", "track_id": track_id}, room=queue_id)


@socketio.on("skip_track")
def ws_skip_track(data):
    """Skip the currently playing track (remove first track)."""
    print(f"Skipping track: {data}")
    queue_id = data["queue_id"]

    queue = get_queue(queue_id)
    if not queue:
        emit("error", {"error": f"Queue {queue_id} not found"})
        return

    with queue_lock:
        if queue.tracks:
            skipped_track = queue.tracks.pop(0)  # Remove first track
            db.session.commit()
            print(f"Skipped track: {skipped_track}")
        else:
            emit("error", {"error": "Queue is empty"})
            return

    emit("queue_patch", {"event": "skip"}, room=queue_id)


@socketio.on("move_track")
def ws_move_track(data):
    """Reorder tracks in the queue."""
    print(f"Moving track: {data}")
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
            print(f"Moved track from {old_index} to {new_index}")
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
    """Clear all tracks from the queue."""
    print(f"Clearing queue: {data}")
    queue_id = data["queue_id"]

    queue = get_queue(queue_id)
    if not queue:
        emit("error", {"error": f"Queue {queue_id} not found"})
        return

    with queue_lock:
        track_count = len(queue.tracks)
        queue.tracks = []
        db.session.commit()
        print(f"Cleared {track_count} tracks from queue")

    emit("queue_patch", {"event": "clear"}, room=queue_id)


@socketio.on("connect")
def handle_connect():
    """Handle client connection."""
    print("Client connected to WebSocket")


@socketio.on("disconnect")
def handle_disconnect():
    """Handle client disconnection."""
    print("Client disconnected from WebSocket")
