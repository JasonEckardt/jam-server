from flask import Blueprint

player =  Blueprint('player', __name__)

@player.route('/player')
def player_state():
  return 'playback state'

@player.route('/player/play')
def play():
  return 'admin playback or guest vote resume playback'

@player.route('/player/pause')
def pause():
  return 'admin pause or guest vote pause playback'

@player.route('/player/skip')
def skip():
  return 'admin skip or guest vote skip'

@player.route('/player/previous')
## OPTIONAL ##
def previous():
  return '(or skip this feature since you can re-add to queue) admin previous song or guest vote previous song'

@player.route('/player/device')
def device():
  return 'select playback device'
