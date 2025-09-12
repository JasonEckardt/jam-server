# Spotify Jam Server

A self-hosted Spotify Jam server to play music with your friends! Share a queue with your friends and connect your Spotify account to import songs into the shared queue. Playback from a Raspberry Pi connected to speakers via Bluetooth or Aux.

## Usage

```sh
git clone
python3 -m venv .venv
. ./.venv/bin/activate
pip install -r requirements.txt
```

Setup your environment variables:
```
# .env
export SPOTIFY_CLIENT_ID='<your_client_id>'
export SPOTIFY_CLIENT_SECRET='<your_client_secret>'
export SPOTIFY_REDIRECT_URI='<your_redirect_uri>'
```

Run in project root:
```sh
python3 run.py
```

## Contributing

### Tests

```sh
python3 -m pytest tests/*
```
