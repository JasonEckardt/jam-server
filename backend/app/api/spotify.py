from app import db
from app.models.user import User
from datetime import datetime, timedelta, timezone
from flask import session
import os
import requests


def get_access_token(authorization_code: str) -> dict:
    spotify_request_access_token_url = "https://accounts.spotify.com/api/token"
    body = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
        "client_secret": os.getenv("SPOTIFY_CLIENT_SECRET"),
        "redirect_uri": os.getenv("SPOTIFY_REDIRECT_URI"),
    }
    response = requests.post(spotify_request_access_token_url, data=body)
    if response.status_code != 200:
        return {
            "error": f"Failed token refresh, {response.text}",
            "status": response.status_code,
        }
    return response.json()


def refresh_access_token(refresh_token: str) -> dict:
    url = "https://accounts.spotify.com/api/token"
    body = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
        "client_secret": os.getenv("SPOTIFY_CLIENT_SECRET"),
    }
    response = requests.post(url, data=body)
    if response.status_code != 200:
        return {
            "error": f"Failed token refresh, {response.text}",
            "status": response.status_code,
        }
    return response.json()


def get_current_user_token() -> str:
    user_id = session.get("user_id")
    if not user_id:
        return None

    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return None

    if user.is_expired():
        credentials = refresh_access_token(user.refresh_token)
        user.access_token = credentials["access_token"]
        if "refresh_token" in credentials:
            user.refresh_token = credentials["refresh_token"]

        user.expires_at = datetime.now(timezone.utc) + timedelta(
            seconds=credentials["expires_in"]
        )
        db.session.commit()

    return user.access_token


def request_api(url: str, headers: dict[str, str]) -> tuple[dict, int]:
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code != 200:
            return {"error": response.reason}, response.status_code
        return response.json(), 200
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500
