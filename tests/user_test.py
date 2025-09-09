# test_user.py
import pytest
import json


@pytest.fixture
def client():
    from app import create_app

    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


class DummyResponse:
    def __init__(self, data, status=200):
        self._data = data
        self.status_code = status

    def json(self):
        return self._data


def test_library_success(client, monkeypatch):
    def mock_get(url, headers=None):
        if "me" in url:  # user profile
            return DummyResponse({"id": "123"})
        if "top/artists" in url:
            return DummyResponse({"items": [{"name": "Artist1"}]})
        if "top/tracks" in url:
            return DummyResponse({"items": [{"name": "Track1"}]})
        return DummyResponse({}, status=404)

    monkeypatch.setattr("requests.get", mock_get)
    monkeypatch.setenv("token", "fake-token")

    response = client.get("/library")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert "top_artists" in data
    assert "top_tracks" in data
    assert len(data["top_tracks"]) > 0
    assert len(data["top_artists"]) > 0
    assert data["top_artists"][0]["name"] == "Artist1"
    assert data["top_tracks"][0]["name"] == "Track1"
