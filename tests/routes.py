# tests/test_routes.py
import urllib
from app import create_app

import pytest


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_login_redirect(client, monkeypatch):
    monkeypatch.setenv("SPOTIFY_CLIENT_ID", "test-client-id")
    monkeypatch.setenv("SPOTIFY_REDIRECT_URI", "http://localhost/callback")

    response = client.get("/login")
    assert response.status_code == 302  # redirect

    location = response.headers["Location"]
    assert location.startswith("https://accounts.spotify.com/authorize/?")

    # parse query string
    qs = urllib.parse.urlparse(location).query
    params = dict(urllib.parse.parse_qsl(qs))
    assert params["client_id"] == "test-client-id"
    assert params["redirect_uri"] == "http://localhost/callback"
    assert params["response_type"] == "code"
    assert "state" in params
    assert params["show_dialog"] == "true"
