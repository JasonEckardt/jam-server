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
