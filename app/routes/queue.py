from flask import Blueprint, request
import re

## tmp ##
## This will be replaced with MySQL later
class QueueStore:
  def __init__(self):
    self._queue= []

  def show(self):
    return list(self._queue)

  def add(self, track_id):
    self._queue.append(track_id)

  def remove(self, track_id):
    if track_id in self._queue:
      self._queue.remove(track_id)

def extract_track_id(url):
    """
    Extracts the track ID from a Spotify track URL.
    Returns None if not found.
    """
    match = re.search(r"spotify\.com/track/([A-Za-z0-9]+)", url)
    if match:
        return match.group(1)
    return None


queue = Blueprint('queue', __name__)
store = QueueStore()

@queue.route('/queue', methods=['GET'])
def get_queue():
  return {'queue': store.show()}

@queue.route('/queue', methods=['POST'])
def add_to_queue():
    data = request.json
    url = data.get('url')
    if not url:
        return {"error": "URL not provided"}, 400
    track_id = extract_track_id(url)
    if not track_id:
        return {"error": "Invalid track URL"}, 400
    store.add(track_id)
    return {"track_id": track_id}, 201

@queue.route('/queue/<int:track_id>', methods=['DELETE'])
def remove_from_queue(track_id):
  return f'delete {track_id}'
