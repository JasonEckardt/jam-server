import pytest
from unittest.mock import patch, MagicMock
import os


class TestMe:
    """Tests for /me route"""

    def test_me_redirects_when_no_token(self, client):
        """Test /me redirects to login when no token available"""
        with patch("app.api.spotify.get_current_user_token", return_value=None):
            response = client.get("/me", follow_redirects=False)

            assert response.status_code == 302
            assert f"{os.getenv('BACKEND_URL')}/login" in response.location

    @patch("app.api.spotify.request_api")
    @patch("app.api.spotify.get_current_user_token")
    def test_me_returns_error_on_api_failure(
        self, mock_get_token, mock_request_api, client
    ):
        """Test /me returns error when Spotify API fails"""
        mock_get_token.return_value = "test_token"
        mock_request_api.return_value = ({"error": "API error"}, 500)

        response = client.get("/me")
        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data
        assert "Failed to login" in data["error"]

    @patch("app.api.spotify.request_api")
    @patch("app.api.spotify.get_current_user_token")
    def test_me_returns_error_when_user_id_missing_from_session(
        self, mock_get_token, mock_request_api, client, me_data
    ):
        """Test /me returns error when user_id not in session"""
        mock_get_token.return_value = "test_token"
        mock_request_api.return_value = (me_data, 200)

        response = client.get("/me")
        assert response.status_code == 401
        data = response.get_json()
        assert "error" in data
        assert "User ID missing from session" in data["error"]

    @patch("app.api.spotify.request_api")
    @patch("app.api.spotify.get_current_user_token")
    def test_me_returns_user_data_successfully(
        self, mock_get_token, mock_request_api, client, app, sample_user, me_data
    ):
        """Test /me returns user data with role and expiration"""
        mock_get_token.return_value = "test_token"
        mock_request_api.return_value = (me_data, 200)

        # Set user_id in session
        with client.session_transaction() as sess:
            sess["user_id"] = sample_user.user_id

        response = client.get("/me")
        assert response.status_code == 200

        data = response.get_json()
        assert data["id"] == me_data["id"]
        assert "expires_at" in data
        assert data["user_role"] == sample_user.user_role.title()


class TestPlaylists:
    """Tests for /playlists route"""

    @patch("app.api.spotify.request_api")
    def test_playlists_returns_error_on_api_failure(self, mock_request_api, client):
        """Test /playlists returns error when Spotify API fails"""
        mock_request_api.return_value = ({"error": "API error"}, 500)

        response = client.get("/playlists")
        assert response.status_code == 500
        assert b"Failed to fetch playlists" in response.data

    @patch("config.spotify_urls.get_headers")
    @patch("app.api.spotify.request_api")
    def test_playlists_returns_formatted_playlist_data(
        self, mock_request_api, mock_get_headers, client, playlists_data
    ):
        """Test /playlists returns properly formatted playlist data"""
        mock_get_headers.return_value = {"Authorization": "Bearer test_token"}
        mock_request_api.return_value = ({"items": playlists_data}, 200)

        response = client.get("/playlists")
        assert response.status_code == 200

        data = response.get_json()
        assert "playlists" in data
        assert len(data["playlists"]) == len(playlists_data)

        # Check first playlist structure if playlists exist
        if len(data["playlists"]) > 0:
            first_playlist = data["playlists"][0]
            assert "id" in first_playlist
            assert "name" in first_playlist
            assert "description" in first_playlist
            assert "images" in first_playlist
            assert "link" in first_playlist
            assert "owner" in first_playlist
            assert "track_count" in first_playlist
            assert first_playlist["link"].startswith("/playlists/")

    @patch("config.spotify_urls.get_headers")
    @patch("app.api.spotify.request_api")
    def test_playlists_returns_empty_list_when_no_playlists(
        self, mock_request_api, mock_get_headers, client
    ):
        """Test /playlists returns empty list when user has no playlists"""
        mock_get_headers.return_value = {"Authorization": "Bearer test_token"}
        mock_request_api.return_value = ({"items": []}, 200)

        response = client.get("/playlists")
        assert response.status_code == 200

        data = response.get_json()
        assert data["playlists"] == []


class TestPlaylistTracks:
    """Tests for /playlists/<playlist_id> route"""

    @patch("requests.get")
    def test_playlist_tracks_returns_error_on_api_failure(
        self, mock_requests_get, client
    ):
        """Test /playlists/<id> returns error when Spotify API fails"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"error": "API error"}
        mock_requests_get.return_value = (mock_response, 500)

        response = client.get("/playlists/test_playlist_id")
        assert response.status_code == 500

    @patch("config.spotify_urls.get_headers")
    @patch("requests.get")
    def test_playlist_tracks_returns_formatted_track_data(
        self, mock_requests_get, mock_get_headers, client, playlist_tracks_data
    ):
        """Test /playlists/<id> returns properly formatted track data"""
        mock_get_headers.return_value = {"Authorization": "Bearer test_token"}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": playlist_tracks_data}
        mock_requests_get.return_value = (mock_response, 200)

        response = client.get("/playlists/test_playlist_id")
        assert response.status_code == 200

        data = response.get_json()
        assert "playlist_tracks" in data

        # Check track structure
        if len(data["playlist_tracks"]) > 0:
            first_track = data["playlist_tracks"][0]
            assert "id" in first_track
            assert "name" in first_track
            assert "artists" in first_track
            assert "album" in first_track
            assert "duration_ms" in first_track
            assert "preview_url" in first_track
            assert isinstance(first_track["artists"], list)

    @patch("config.spotify_urls.get_headers")
    @patch("requests.get")
    def test_playlist_tracks_handles_empty_playlist(
        self, mock_requests_get, mock_get_headers, client
    ):
        """Test /playlists/<id> handles empty playlist"""
        mock_get_headers.return_value = {"Authorization": "Bearer test_token"}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        mock_requests_get.return_value = (mock_response, 200)

        response = client.get("/playlists/empty_playlist")
        assert response.status_code == 200

        data = response.get_json()
        assert data["playlist_tracks"] == []


class TestTopTracks:
    """Tests for /tracks route"""

    @patch("app.api.spotify.request_api")
    def test_top_tracks_returns_error_on_api_failure(self, mock_request_api, client):
        """Test /tracks returns error when Spotify API fails"""
        mock_request_api.return_value = ({"error": "API error"}, 500)

        response = client.get("/tracks")
        assert response.status_code == 500
        assert b"Failed to fetch top tracks" in response.data

    @patch("config.spotify_urls.get_headers")
    @patch("app.api.spotify.request_api")
    def test_top_tracks_returns_tracks_without_markets(
        self, mock_request_api, mock_get_headers, client
    ):
        """Test /tracks returns tracks with available_markets removed"""
        mock_get_headers.return_value = {"Authorization": "Bearer test_token"}

        tracks_with_markets = [
            {
                "id": "track1",
                "name": "Test Track",
                "available_markets": ["US", "CA", "UK"],
                "album": {
                    "name": "Test Album",
                    "available_markets": ["US", "CA", "UK"],
                },
            }
        ]

        mock_request_api.return_value = ({"items": tracks_with_markets}, 200)

        response = client.get("/tracks")
        assert response.status_code == 200

        data = response.get_json()
        assert "tracks" in data
        assert len(data["tracks"]) > 0

        # Verify available_markets are removed
        first_track = data["tracks"][0]
        assert "available_markets" not in first_track
        assert "available_markets" not in first_track["album"]

    @patch("config.spotify_urls.get_headers")
    @patch("app.api.spotify.request_api")
    def test_top_tracks_returns_empty_list_when_no_tracks(
        self, mock_request_api, mock_get_headers, client
    ):
        """Test /tracks returns empty list when user has no top tracks"""
        mock_get_headers.return_value = {"Authorization": "Bearer test_token"}
        mock_request_api.return_value = ({"items": []}, 200)

        response = client.get("/tracks")
        assert response.status_code == 200

        data = response.get_json()
        assert data["tracks"] == []
