import os
import requests

def get_access_token(authorization_code: str):
    spotify_request_access_token_url = "https://accounts.spotify.com/api/token"
    body = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
        "client_secret": os.getenv("SPOTIFY_CLIENT_SECRET"),
        "redirect_uri": os.getenv("SPOTIFY_REDIRECT_URI"),
    }
    response = requests.post(spotify_request_access_token_url, data=body)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(
            f"Failed to obtain access token: {response.status_code}, {response.text}"
        )

