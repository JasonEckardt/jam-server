from app.routes.queue import store


def test_add_track_to_queue(client):
    response = client.post(
        "/queue",
        json={"url": "https://open.spotify.com/track/51xBj4q5DHdS27PyeplUwu"},
    )
    assert response.status_code == 201
    assert len(store.show()) > 0
    data = response.get_json()
    assert store.show()[0] == data["track_id"]
