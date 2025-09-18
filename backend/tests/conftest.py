from app import create_app
import json
import pytest


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def client():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # in-memory DB for tests
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }
    app = create_app(test_config)
    with app.app_context():
        from app import db

        db.create_all()
        with app.test_client() as client:
            yield client
        db.drop_all()


@pytest.fixture
def playlists_data():
    return load_json("./tests/data/playlists.json").get("items", [])


@pytest.fixture
def playlist_tracks_data():
    return load_json("./tests/data/playlist_tracks.json").get("items", [])
