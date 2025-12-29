import json
import pytest
from datetime import datetime, timezone, timedelta

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(autouse=True)
def test_env(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "test-secret")
    monkeypatch.setenv("CORS_ORIGINS", "*")
    monkeypatch.setenv("FRONTEND_URL", "http://localhost:5173")
    monkeypatch.setenv("BACKEND_URL", "http://localhost:5000")
    monkeypatch.setenv("SPOTIFY_CLIENT_ID", "dummy")
    monkeypatch.setenv("SPOTIFY_REDIRECT_URI", "http://localhost/callback")
    monkeypatch.setenv("SPOTIFY_CLIENT_SECRET", "dummy_secret")


def load_json(path):
    # Get the directory where conftest.py is located
    test_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(test_dir, path)
    with open(full_path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def app():
    """Create application for the tests."""
    from app import create_app, db

    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "SECRET_KEY": "test-secret",
    }

    app = create_app(test_config)

    # Push application context
    ctx = app.app_context()
    ctx.push()

    # Create tables
    db.create_all()

    yield app

    # Cleanup
    db.session.remove()
    db.drop_all()
    ctx.pop()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def sample_admin_user(app):
    """Create a sample admin user for testing."""
    from app import db
    from app.models.user import User

    user = User(
        user_id="admin_123",
        access_token="admin_token",
        refresh_token="admin_refresh",
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
        user_role="admin",
    )
    db.session.add(user)
    db.session.commit()
    yield user


@pytest.fixture
def sample_user(app):
    """Create a sample regular user for testing."""
    from app import db
    from app.models.user import User

    user = User(
        user_id="user_123",
        access_token="user_token",
        refresh_token="user_refresh",
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
        user_role="user",
    )
    db.session.add(user)
    db.session.commit()
    yield user


@pytest.fixture
def me_data():
    """Load sample /me endpoint data"""
    return load_json("data/me.json")


@pytest.fixture
def playlists_data():
    return load_json("data/playlists.json").get("items", [])


@pytest.fixture
def playlist_tracks_data():
    return load_json("data/playlist_tracks.json").get("items", [])
