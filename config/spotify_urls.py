class SpotifyAPI:
    BASE_URL = "https://api.spotify.com/v1"

    # user endpoints
    USER_PROFILE = f"{BASE_URL}/me"
    USER_TOP_ITEMS = f"{BASE_URL}/me/top"
    USER_PLAYLISTS = f"{BASE_URL}/me/playlists"
    USER_SAVED_TRACKS = f"{BASE_URL}/me/tracks"
    USER_SAVED_ALBUMS = f"{BASE_URL}/me/albums"

    # playlist endpoints
    PLAYLIST_TRACKS = f"{BASE_URL}/playlists/{{playlist_id}}/tracks"
    PLAYLIST_DETAILS = f"{BASE_URL}/playlists/{{playlist_id}}"

    # search and browse
    SEARCH = f"{BASE_URL}/search"
    RECOMMENDATIONS = f"{BASE_URL}/recommendations"

    # player endpoints
    PLAYER_STATE = f"{BASE_URL}/me/player"
    PLAYER_PLAY = f"{BASE_URL}/me/player/play"
    PLAYER_PAUSE = f"{BASE_URL}/me/player/pause"
    PLAYER_SKIP = f"{BASE_URL}/me/player/next"

    # album, artist, track details
    ALBUM_DETAILS = f"{BASE_URL}/albums/{{album_id}}"
    ARTIST_DETAILS = f"{BASE_URL}/artists/{{artist_id}}"
    ARTIST_TOP_TRACKS = f"{BASE_URL}/artists/{{artist_id}}/top-tracks"
    TRACK_DETAILS = f"{BASE_URL}/tracks/{{track_id}}"

    @classmethod
    def get_user_top_items(cls, item_type):
        """Get URL for user's top artists or tracks"""
        return f"{cls.USER_TOP_ITEMS}/{item_type}?"

    @classmethod
    def get_playlist_tracks(cls, playlist_id):
        """Get URL for specific playlist's tracks"""
        return cls.PLAYLIST_TRACKS.format(playlist_id=playlist_id)

    @classmethod
    def get_track_details(cls, track_id):
        """Get URL for specific track details"""
        return cls.TRACK_DETAILS.format(track_id=track_id)
