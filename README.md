#  Jam Server

A self-hosted Jam server for playing music with friends! Share a queue, connect Spotify accounts to import songs, and stream playback from a one lightweight computer such as a Raspberry Pi connected to speakers via Bluetooth or Aux.

**Tech Stack:**
- Flask (API and backend)
- Vite + React (frontend)
- MySQL (storage)

## Getting Started

### Prerequisites

- Python 3.x
- Docker and Docker Compose
- Spotify Developer Account (for API credentials)

### Installation

1. **Clone the repository and navigate to the backend directory:**
   ```sh
   cd ./backend
   ```

2. **Create a virtual environment and install dependencies:**
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**

   Create a `.env` file in the backend directory:
   ```env
   SPOTIFY_CLIENT_ID='<your_client_id>'
   SPOTIFY_CLIENT_SECRET='<your_client_secret>'
   SPOTIFY_REDIRECT_URI='<your_redirect_uri>'
   ```

4. **Start Docker containers:**
   ```sh
   cd ../docker
   docker compose up -d
   ```

5. **Initialize the database:**
   ```sh
   cd ../backend
   flask db upgrade
   ```

### Running the Development Server

A convenience script is provided to run Docker, Flask, and Vite simultaneously:

```sh
cd scripts
./dev.sh
```

> **Note:** Run `exit.sh` only if the dev script didn't completely exit all programs.

## Development

### Database Migrations

When updating models:
```sh
flask db migrate -m '<description of changes>'
flask db upgrade
```

To rollback:
```sh
flask db downgrade
```

### Running Tests

```sh
cd backend
python3 -m pytest tests/*
```

Or use the convenience script:
```sh
cd scripts
./test.sh
```

### Docker Management

To stop containers:
```sh
docker compose down
# or stop a specific container
docker compose down <container_name>
```

> **Security Note:** Using `ports:` in docker-compose.yaml exposes ports to `0.0.0.0` by default.

## API Usage

You must be logged in to use these endpoints. Visit `http://127.0.0.1:5000/login` first.

### Create a Queue

```sh
curl -X POST http://localhost:5000/queues/<queue_name>
```

Example:
```sh
curl -X POST http://localhost:5000/queues/main
```

### Add a Track to Queue

```sh
curl -X POST http://127.0.0.1:5000/queues/main/tracks \
  -H "Content-Type: application/json" \
  -b "session=<session_key_from_cookies>" \
  -d '{"url": "https://open.spotify.com/track/7vDj5t3DOFDbOkHyjb1wYB"}'
```

View the queue at: `http://127.0.0.1:5000/queues/main`

### Play Current Song

Check available devices at: `http://127.0.0.1:5000/player/devices`

```sh
curl -X POST http://127.0.0.1:5000/player/play
```

Response:
```json
{
  "status": "playing"
}
```

### Clear Queue

```sh
curl -X POST http://127.0.0.1:5000/queues/main/clear
```

## API Response Examples

### `/playlists/<playlist_id>`

```json
{
  "album": "Tchaikovsky: Swan Lake Suites",
  "artists": [
    "Pyotr Ilyich Tchaikovsky",
    "Czech Symphony Orchestra",
    "Michaela Rózsa Růžičková"
  ],
  "duration_ms": 180379,
  "id": "<track_id>",
  "name": "Swan Lake (Suite), Op. 20a, TH.219: I. Scene - Swan Theme",
  "preview_url": null
}
```

### `/playlists`

```json
{
  "playlists": [
    {
      "description": "Best classical music to study, chill, and relax...",
      "id": "1234",
      "images": [
        {
          "height": null,
          "url": "https://image-cdn-fa.spotifycdn.com/image/<image_id>",
          "width": null
        }
      ],
      "link": "/playlists/<some>",
      "name": "Classical Bangers 🎹🎻",
      "owner": {
        "display_name": "Classical Bangers",
        "id": "1234",
        "type": "user"
      },
      "track_count": 456
    }
  ]
}
```

### `/me`

```json
{
  "display_name": "TechBase",
  "external_urls": {
    "spotify": "<profile_url>"
  },
  "followers": {
    "href": null,
    "total": 1
  },
  "id": "<user_id>",
  "images": [
    {
      "height": 300,
      "url": "<image_url>",
      "width": 300
    }
  ],
  "type": "user",
  "uri": "spotify:user:<user_id>"
}
```

### `/devices`

```json
{
  "devices": [
    {
      "id": "<device_id>",
      "is_active": true,
      "is_private_session": false,
      "is_restricted": false,
      "name": "<device_name>",
      "supports_volume": true,
      "type": "Computer",
      "volume_percent": 100
    }
  ]
}
```

## Contributing

Contributions are welcome! Please ensure all tests pass before submitting a pull request either running `pytest` or using `scripts/test.py`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
