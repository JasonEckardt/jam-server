import json
import pytest

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app


@pytest.fixture(autouse=True)
def test_env(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "test-secret")
    monkeypatch.setenv("CORS_ORIGINS", "*")
    monkeypatch.setenv("FRONTEND_URL", "http://localhost:3000")
    monkeypatch.setenv("BACKEND_URL", "http://localhost:5000")
    monkeypatch.setenv("SPOTIFY_CLIENT_ID", "dummy")
    monkeypatch.setenv("SPOTIFY_REDIRECT_URI", "http://localhost/callback")


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def client():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
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
