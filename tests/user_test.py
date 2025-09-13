from unittest.mock import patch
from types import SimpleNamespace


@patch("requests.get")
def test_user_playlists(mock_get, client, playlists_data):
    mock_get.side_effect = [
        SimpleNamespace(status_code=200, json=lambda *a, **k: {"id": "user123"}),
        SimpleNamespace(
            status_code=200, json=lambda *a, **k: {"items": playlists_data}
        ),
    ]

    response = client.get("/playlists")
    assert response.status_code == 200
    data = response.get_json()
    assert "playlists" in data
    assert isinstance(data["playlists"], list)
    if data["playlists"]:
        pl = data["playlists"][0]
        for key in [
            "id",
            "description",
            "images",
            "link",
            "name",
            "owner",
            "track_count",
        ]:
            assert key in pl
        assert pl["link"] == f"/playlists/{pl['id']}"


@patch("requests.get")
def test_playlist_tracks(mock_get, client, playlist_tracks_data):
    mock_get.return_value = SimpleNamespace(
        status_code=200, json=lambda *a, **k: {"items": playlist_tracks_data}
    )

    response = client.get("/playlists/test_playlist_id")
    assert response.status_code == 200
    data = response.get_json()
    assert "playlist_tracks" in data
    assert isinstance(data["playlist_tracks"], list)
    if data["playlist_tracks"]:
        track = data["playlist_tracks"][0]
        for key in ["id", "name", "artists", "album", "duration_ms", "preview_url"]:
            assert key in track
        assert isinstance(track["artists"], list)
