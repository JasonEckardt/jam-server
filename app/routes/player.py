from flask import Blueprint

player =  Blueprint('player', '__name__')

@route.add('/player')
def player():
  return 'playback state'

@route.add('/player/play')
def play():
  return 'admin playback or guest vote resume playback'

@route.add('/player/pause'):
def pause():
  return 'admin pause or guest vote pause playback'

@route.add('/player/skip'):
def skip():
  return 'admin skip or guest vote skip'

@route.add('player/previous'):
## OPTIONAL ##
def previous():
  return '(or skip this feature since you can re-add to queue) admin previous song or guest vote previous song'

@route.add('/player/device'):
def device():
  return 'select playback device'
