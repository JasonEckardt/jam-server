BASE = "https://api.spotify.com/v1"


class urls:
    user_profile = f"{BASE}/me"
    user_playlists = f"{BASE}/me/playlists"
    user_top = f"{BASE}/me/top"
    user_tracks = f"{BASE}/me/tracks"
    user_albums = f"{BASE}/me/albums"

    # player
    player = f"{BASE}/me/player"
    devices = f"{BASE}/me/player/devices"
    playback = f"{BASE}/me/player/play"
    pause = f"{BASE}/me/player/pause"
    next = f"{BASE}/me/player/next"
    previous = f"{BASE}/me/player/previous"
    shuffle = f"{BASE}/me/player/shuffle"
    repeat = f"{BASE}/me/player/repeat"
    seek = f"{BASE}/me/player/seek"
    volume = f"{BASE}/me/player/volume"
    queue = f"{BASE}/me/player/queue"

    # search and browse
    search = f"{BASE}/search"
    recommendations = f"{BASE}/recommendations"

    # dynamic
    @staticmethod
    def playlist(id: str) -> str:
        return f"{BASE}/playlists/{id}"

    @staticmethod
    def playlist_tracks(id: str) -> str:
        return f"{BASE}/playlists/{id}/tracks"

    @staticmethod
    def track(id: str) -> str:
        return f"{BASE}/tracks/{id}"

    @staticmethod
    def artist(id: str) -> str:
        return f"{BASE}/artists/{id}"

    @staticmethod
    def artist_top_tracks(id: str) -> str:
        return f"{BASE}/artists/{id}/top-tracks"

    @staticmethod
    def album(id: str) -> str:
        return f"{BASE}/albums/{id}"

    @staticmethod
    def user_top_items(type: str) -> str:
        return f"{urls.top}/{type}"
