from unittest.mock import patch, MagicMock


@patch("app.routes.queues.Queue.query.get")
@patch("app.routes.queues.db.session.commit")
def test_get_session(mock_commit, mock_get, client):
    mock_queue = MagicMock()
    mock_queue.id = "test"
    mock_queue.name = "Test Queue"
    mock_queue.tracks = ["123"]
    mock_queue.now_playing = None
    mock_queue.created_at.isoformat.return_value = "2025-01-01T00:00:00"

    mock_get.return_value = mock_queue

    response = client.get("/queues/test")
    assert response.status_code == 200
    assert response.json["queue_id"] == "main"


@patch("app.routes.queues.Queue.query.all")
def test_get_queue_endpoint(mock_all, client):
    mock_queue = MagicMock()
    mock_queue.id = "main"
    mock_queue.name = "Main"
    mock_queue.tracks = []
    mock_queue.created_at.isoformat.return_value = "2025-01-01T00:00:00"

    mock_all.return_value = [mock_queue]

    response = client.get("/queues/main")
    assert response.status_code == 200
    data = response.get_json()
    assert data["now_playing"] is None
