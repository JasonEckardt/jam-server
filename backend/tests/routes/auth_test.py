from app.api import spotify
import urllib


def test_login_redirect(client, monkeypatch):
    monkeypatch.setenv("SPOTIFY_CLIENT_ID", "test-client-id")
    monkeypatch.setenv("SPOTIFY_REDIRECT_URI", "http://localhost/callback")

    response = client.get("/login")
    # redirect
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
    assert "error" in data
    assert data["error"] == "Malformed, no authorization code received"


def test_callback_invalid_code(client, monkeypatch):
    def mock_get_access_token(authorization_code):
        return {"error": "invalid_grant"}

    monkeypatch.setattr(spotify, "get_access_token", mock_get_access_token)

    response = client.get("/callback?code=badcode")
    assert response.status_code == 400
