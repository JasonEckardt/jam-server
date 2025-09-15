import os

BASE = "https://api.spotify.com/v1"

# User endpoints
USER_PROFILE = f"{BASE}/me"
USER_PLAYLISTS = f"{BASE}/me/playlists"
USER_TOP = f"{BASE}/me/top"
USER_TRACKS = f"{BASE}/me/tracks"
USER_ALBUMS = f"{BASE}/me/albums"

# Player endpoints
PLAYER = f"{BASE}/me/player"
DEVICES = f"{BASE}/me/player/devices"
PLAYBACK = f"{BASE}/me/player/play"
PAUSE = f"{BASE}/me/player/pause"
NEXT = f"{BASE}/me/player/next"
PREVIOUS = f"{BASE}/me/player/previous"
SHUFFLE = f"{BASE}/me/player/shuffle"
REPEAT = f"{BASE}/me/player/repeat"
SEEK = f"{BASE}/me/player/seek"
VOLUME = f"{BASE}/me/player/volume"
QUEUE = f"{BASE}/me/player/queue"

# Search and browse
SEARCH = f"{BASE}/search"
RECOMMENDATIONS = f"{BASE}/recommendations"


# Dynamic endpoint functions
def album(id: str) -> str:
    return f"{BASE}/albums/{id}"


def artist(id: str) -> str:
    return f"{BASE}/artists/{id}"


def artist_top_tracks(id: str) -> str:
    return f"{BASE}/artists/{id}/top-tracks"


def playlist(id: str) -> str:
    return f"{BASE}/playlists/{id}"


def playlist_tracks(id: str) -> str:
    return f"{BASE}/playlists/{id}/tracks"


def track(id: str) -> str:
    return f"{BASE}/tracks/{id}"


def user_top_items(type: str) -> str:
    return f"{USER_TOP}/{type}"


def get_headers() -> dict:
    return {"Authorization": f"Bearer {os.getenv('token')}"}
