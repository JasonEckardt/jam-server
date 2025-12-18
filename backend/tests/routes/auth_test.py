import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone, timedelta
from flask import session
import os
import urllib.parse


class TestCallback:
    """Tests for /callback route"""

    def test_callback_no_code(self, client):
        """Test callback without authorization code"""
        response = client.get("/callback")
        assert response.status_code == 400
        assert b"Malformed, no authorization code received" in response.data

    @patch("requests.get")
    @patch("app.api.spotify.get_access_token")
    def test_callback_access_token_error(
        self, mock_get_token, mock_requests, client, app
    ):
        """Test callback when Spotify returns an error"""
        mock_get_token.return_value = {"error": "invalid_grant"}

        response = client.get("/callback?code=test_code")
        assert response.status_code == 400
        assert b"Failed to get access token" in response.data

    @patch("requests.get")
    @patch("app.api.spotify.get_access_token")
    def test_callback_creates_first_admin_user(
        self, mock_get_token, mock_requests, client, app, me_data
    ):
        """Test callback creates first user as admin"""
        # Mock Spotify API responses
        mock_get_token.return_value = {
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "expires_in": 3600,
        }

        mock_response = MagicMock()
        mock_response.json.return_value = me_data
        mock_requests.return_value = mock_response

        response = client.get("/callback?code=test_code", follow_redirects=False)

        # Check redirect
        assert response.status_code == 302
        assert f"{os.getenv('FRONTEND_URL')}/me" in response.location

        # Check session
        with client.session_transaction() as sess:
            assert sess["user_id"] == me_data["id"]
            assert sess["token_info"]["access_token"] == "test_access_token"

        # Check database
        from app.models.user import User

        user = User.query.filter_by(user_id=me_data["id"]).first()
        assert user is not None
        assert user.user_role == "admin"
        assert user.access_token == "test_access_token"
        assert user.refresh_token == "test_refresh_token"

    @patch("requests.get")
    @patch("app.api.spotify.get_access_token")
    def test_callback_creates_regular_user_when_admin_exists(
        self, mock_get_token, mock_requests, client, app, sample_admin_user, me_data
    ):
        """Test callback creates regular user when admin already exists"""
        # Modify me_data to have a different user ID
        new_user_data = me_data.copy()
        new_user_data["id"] = "spotify_user_456"

        mock_get_token.return_value = {
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "expires_in": 3600,
        }

        mock_response = MagicMock()
        mock_response.json.return_value = new_user_data
        mock_requests.return_value = mock_response

        response = client.get("/callback?code=test_code", follow_redirects=False)

        assert response.status_code == 302

        from app.models.user import User

        user = User.query.filter_by(user_id="spotify_user_456").first()
        assert user is not None
        assert user.user_role == "user"

    @patch("requests.get")
    @patch("app.api.spotify.get_access_token")
    def test_callback_updates_existing_user(
        self, mock_get_token, mock_requests, client, app, sample_user, me_data
    ):
        """Test callback updates existing user's tokens"""
        new_access_token = "new_access_token"
        new_refresh_token = "new_refresh_token"

        # Use the sample_user's ID in me_data
        user_data = me_data.copy()
        user_data["id"] = sample_user.user_id

        mock_get_token.return_value = {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "expires_in": 3600,
        }

        mock_response = MagicMock()
        mock_response.json.return_value = user_data
        mock_requests.return_value = mock_response

        original_role = sample_user.user_role
        response = client.get("/callback?code=test_code", follow_redirects=False)

        assert response.status_code == 302

        from app.models.user import User

        user = User.query.filter_by(user_id=sample_user.user_id).first()
        assert user.access_token == new_access_token
        assert user.refresh_token == new_refresh_token
        assert user.user_role == original_role  # Role shouldn't change


class TestLogin:
    """Tests for /login route"""

    def test_login_redirects_to_spotify(self, client):
        """Test login redirects to Spotify authorization"""
        response = client.get("/login", follow_redirects=False)

        assert response.status_code == 302
        assert "accounts.spotify.com/authorize" in response.location
        assert os.getenv("SPOTIFY_CLIENT_ID") in response.location
        assert "response_type=code" in response.location
        assert "playlist-read-private" in response.location
        assert "user-read-playback-state" in response.location

    def test_login_includes_required_scopes(self, client):
        """Test login includes all required Spotify scopes"""
        response = client.get("/login", follow_redirects=False)

        required_scopes = [
            "playlist-read-private",
            "playlist-read-collaborative",
            "user-top-read",
            "user-read-recently-played",
            "user-library-read",
            "user-read-playback-state",
            "user-modify-playback-state",
        ]

        for scope in required_scopes:
            assert scope in response.location

    def test_login_includes_redirect_uri(self, client):
        """Test login includes correct redirect URI"""
        response = client.get("/login", follow_redirects=False)

        redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
        # URL encode the redirect URI for comparison
        encoded_redirect_uri = urllib.parse.quote(redirect_uri, safe="")
        assert encoded_redirect_uri in response.location


class TestLogout:
    """Tests for /logout route"""

    def test_logout_clears_session(self, client):
        """Test logout clears session data"""
        # Set up session
        with client.session_transaction() as sess:
            sess["user_id"] = "test_user"
            sess["token_info"] = {"access_token": "test_token"}

        response = client.get("/logout", follow_redirects=False)

        assert response.status_code == 302
        assert response.location == "/"

        # Check session is cleared
        with client.session_transaction() as sess:
            assert "user_id" not in sess
            assert "token_info" not in sess

    def test_logout_redirects_to_root(self, client):
        """Test logout redirects to root path"""
        response = client.get("/logout", follow_redirects=False)

        assert response.status_code == 302
        assert response.location == "/"
