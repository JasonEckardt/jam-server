import pytest
from app import create_app
from app.models.queue import Queue
from unittest.mock import patch, MagicMock


@patch("app.routes.queues.Queue.query.get")
@patch("app.routes.queues.db.session.commit")
def test_get_session(mock_commit, mock_get, client):
    mock_queue = MagicMock()
    mock_queue.id = "test"
    mock_queue.name = "Test Queue"
    mock_queue.tracks = ["123"]
    mock_queue.current_track = None
    mock_queue.created_at.isoformat.return_value = "2025-01-01T00:00:00"

    mock_get.return_value = mock_queue

    response = client.get("/queues/test")
    assert response.status_code == 200
    assert response.json["queue_id"] == "test"


@patch("app.routes.queues.Queue.query.all")
def test_list_queues(mock_all, client):
    mock_queue = MagicMock()
    mock_queue.id = "main"
    mock_queue.name = "Main"
    mock_queue.tracks = []
    mock_queue.current_track = None
    mock_queue.created_at.isoformat.return_value = "2025-01-01T00:00:00"

    mock_all.return_value = [mock_queue]

    response = client.get("/queues/")
    assert response.status_code == 200
    assert len(response.json["queues"]) == 1
