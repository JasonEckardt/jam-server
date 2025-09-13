from app.routes.queue import store
from unittest.mock import patch


def test_add_track_order(client):
    store._queue.clear()

    with patch("app.routes.queue.requests.get") as mock_get:
        mock_get.return_value.status_code = 200

        response1 = client.post(
            "/queue", json={"url": "https://open.spotify.com/track/track1"}
        )
        assert response1.status_code == 201

        response2 = client.post(
            "/queue", json={"url": "https://open.spotify.com/track/track2"}
        )
        assert response2.status_code == 201

    queue_list = store.show()
    assert queue_list == ["track1", "track2"]


def test_add_track_to_queue(client):
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        response = client.post(
            "/queue",
            json={"url": "https://open.spotify.com/track/51xBj4q5DHdS27PyeplUwu"},
        )
    assert response.status_code == 201
    assert len(store.show()) > 0


def test_add_valid_and_invalid_tracks(client):
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        response = client.post(
            "/queue", json={"url": "https://open.spotify.com/track/valid"}
        )
        assert response.status_code == 201
        assert response.get_json()["track_id"] == "valid"

        mock_get.return_value.status_code = 404
        response2 = client.post(
            "/queue", json={"url": "https://open.spotify.com/track/invalid"}
        )
        assert response2.status_code == 400
        assert "Track does not exist" in response2.get_json()["error"]


def test_remove_track_from_queue(client):
    store._queue.clear()
    store.add("track1")
    store.add("track2")
    store.add("track3")

    response = client.delete("/queue/track1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["removed_track_id"] == "track1"

    remaining_queue = store.show()
    assert remaining_queue == ["track2", "track3"]

    response2 = client.delete("/queue/track3")
    assert response2.status_code == 200
    data2 = response2.get_json()
    assert data2["removed_track_id"] == "track3"
    assert store.show() == ["track2"]

    response3 = client.delete("/queue/nonexistent")
    assert response3.status_code == 200
    assert store.show() == ["track2"]
