from app import db
from app.api import spotify
from app.models.user import User
import config.spotify_urls as urls
from datetime import datetime, timedelta, timezone
from flask import Blueprint, redirect, request, session
import os
import requests
import time
import urllib
import uuid


auth = Blueprint("auth", __name__)


@auth.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return {"error": "Malformed, no authorization code received"}, 400

    credentials = spotify.get_access_token(authorization_code=code)
    if "error" in credentials:
        return {"error": f"Failed to get access token: {credentials['error']}"}, 400

    headers = {"Authorization": f"Bearer {credentials['access_token']}"}
    user_profile = requests.get(urls.USER_PROFILE, headers=headers).json()
    spotify_uid = user_profile.get("id")
    expires_at = datetime.now(timezone.utc) + timedelta(
        seconds=credentials["expires_in"]
    )
    # Set the first user as an Admin
    admin_exists = User.query.filter_by(user_role="admin").first() is not None
    user = User.query.filter_by(user_id=spotify_uid).first()
    if user:
        user.access_token = credentials["access_token"]
        user.refresh_token = credentials["refresh_token"]
        user.expires_at = expires_at
    else:
        user = User(
            user_id=spotify_uid,
            access_token=credentials["access_token"],
            refresh_token=credentials["refresh_token"],
            expires_at=expires_at,
            user_role="admin" if not admin_exists else "user",
        )
        db.session.add(user)

    db.session.commit()
    session["token_info"] = credentials
    session["user_id"] = spotify_uid
    return redirect(f"{os.getenv('FRONTEND_URL')}/me")


@auth.route("/login")
def login():
    if os.getenv("FRONTEND_URL") is None:
        return {"error": "FRONTEND_URL environment variable is not set"}, 400
    temp_admin_scope = " user-read-playback-state user-modify-playback-state"

    authentication_request_params = {
        "response_type": "code",
        "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
        "redirect_uri": os.getenv("SPOTIFY_REDIRECT_URI"),
        "scope": "playlist-read-private playlist-read-collaborative user-top-read user-read-recently-played user-library-read"
        + temp_admin_scope,
        "state": str(uuid.uuid4()),
        "show_dialog": "true",
    }
    auth_url = "https://accounts.spotify.com/authorize/?" + urllib.parse.urlencode(
        authentication_request_params
    )
    return redirect(auth_url)


@auth.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@auth.route("/token")
def get_current_token():
    token_info = session.get("token_info")

    if not token_info:
        return ({"error": "Not logged in"}), 401

    # Optional: Check if token is expired
    # (Spotify tokens last 1 hour. You can add refresh logic here later)
    now = int(time.time())
    is_expired = token_info.get("expires_at", 0) - now < 60

    if is_expired:
        # For now, just return 401 so frontend knows to re-login
        # Later, you can implement auto-refresh using the refresh_token in DB
        return ({"error": "Token expired"}), 401

    return {
        "access_token": token_info.get("access_token"),
        "user_id": session.get("user_id"),
    }


# @auth.route("/login/admin")
# def login_admin():
#     # Lock with local app admin user and password
#     # Request a token with "user-read-playback-state user-modify-playback-state"

#     return NotImplemented
