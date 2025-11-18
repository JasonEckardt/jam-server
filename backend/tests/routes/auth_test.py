import urllib
from app.api import spotify
from app.models import User
from datetime import datetime, timezone


def test_login_redirect(client, monkeypatch):
    monkeypatch.setenv("SPOTIFY_CLIENT_ID", "test-client-id")
    monkeypatch.setenv("SPOTIFY_REDIRECT_URI", "http://localhost/callback")

    response = client.get("/login")
    assert response.status_code == 302

    location = response.headers["Location"]
    assert location.startswith("https://accounts.spotify.com/authorize/?")

    qs = urllib.parse.urlparse(location).query
    params = dict(urllib.parse.parse_qsl(qs))

    assert params["client_id"] == "test-client-id"
    assert params["redirect_uri"] == "http://localhost/callback"
    assert params["response_type"] == "code"
    assert "state" in params
    assert params["show_dialog"] == "true"


def test_callback_missing_code(client):
    response = client.get("/callback")
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Malformed, no authorization code received"


def test_callback_invalid_code(client, monkeypatch):
    def mock_get_access_token(authorization_code):
        return {"error": "invalid_grant"}

    monkeypatch.setattr(spotify, "get_access_token", mock_get_access_token)

    response = client.get("/callback?code=badcode")
    assert response.status_code == 400


def test_callback_success_new_user(client, monkeypatch):
    def mock_get_access_token(authorization_code):
        return {
            "access_token": "a1",
            "refresh_token": "r1",
            "expires_in": 3600,
        }

    def mock_user_profile(url, headers):
        class R:
            def json(self):
                return {"id": "spotify123"}

        return R()

    monkeypatch.setattr(spotify, "get_access_token", mock_get_access_token)
    monkeypatch.setattr("requests.get", mock_user_profile)

    response = client.get("/callback?code=goodcode")
    assert response.status_code == 302

    user = User.query.filter_by(user_id="spotify123").first()
    user.expires_at = user.expires_at.replace(tzinfo=timezone.utc)
    assert user is not None
    assert user.access_token == "a1"
    assert user.refresh_token == "r1"
    assert user.expires_at > datetime.now(timezone.utc)

    with client.session_transaction() as sess:
        assert sess["user_id"] == "spotify123"


def test_logout_clears_session_and_redirects(client, monkeypatch):
    monkeypatch.setenv("BACKEND_URL", "http://localhost")

    with client.session_transaction() as sess:
        sess["user_id"] = "abc123"

    response = client.get("/logout")
    assert response.status_code == 302
    assert response.headers["Location"] == "http://localhost/login"

    with client.session_transaction() as sess:
        assert "user_id" not in sess
