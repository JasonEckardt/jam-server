import json
from pathlib import Path
from unittest.mock import patch, Mock

with open(
    Path(__file__).parent.parent / "data" / "playlists.json", "r", encoding="utf-8"
) as f:
    expected_playlists_data = json.load(f)

mock_api_input_data = {"items": []}
for p in expected_playlists_data["playlists"]:
    item = p.copy()
    item["tracks"] = {"total": item.pop("track_count")}
    del item["link"]
    mock_api_input_data["items"].append(item)


@patch("app.routes.users.requests.get")
def test_playlists_success(mock_get, client):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_api_input_data
    mock_get.return_value = mock_response

    response = client.get("/playlists")
    response_data = response.get_json()

    assert response.status_code == 200
    assert response_data == expected_playlists_data
    mock_get.assert_called_once()


@patch("app.routes.users.requests.get")
def test_playlists_api_error(mock_get, client):
    mock_response = Mock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    response = client.get("/playlists")
    response_data = response.get_json()

    assert response.status_code == 200
    assert response_data == {"playlists": []}
    mock_get.assert_called_once()


@patch("app.routes.users.requests.get")
def test_playlists_no_items(mock_get, client):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"items": []}
    mock_get.return_value = mock_response

    response = client.get("/playlists")
    response_data = response.get_json()

    assert response.status_code == 200
    assert response_data == {"playlists": []}
    mock_get.assert_called_once()
