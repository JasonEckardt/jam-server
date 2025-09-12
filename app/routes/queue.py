from flask import Blueprint

queue = Blueprint('queue', '__name__')

@queue.route('/queue', methods=['GET'])
def get_queue():
  return 'queue'

@queue.route('/queue', methods=['POST'])
def add_to_queue():
  return 'add <song_id> to queue'

@queue.route('/queue/<int:track_id', methods='DELETE')
def remove_from_queue(track_id):
  return f'delete {track_id}'
