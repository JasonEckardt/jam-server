from app import create_app
import json
import pytest


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def playlists_data():
    return load_json("./tests/data/playlists.json").get("items", [])


@pytest.fixture
def playlist_tracks_data():
    return load_json("./tests/data/playlist_tracks.json").get("items", [])
