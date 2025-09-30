# Spotify Jam Server

A self-hosted Spotify Jam server to play music with your friends! Share a queue with your friends and connect your Spotify account to import songs into the shared queue. Playback from a Raspberry Pi connected to speakers via Bluetooth or Aux.

- Flask for API and backend
- Vite + React for frontend
- MySQL for storage

Docker Compose is used for development and production currently in `docker/` directory.

## Usage

### Dev commands

A script is provided to run `docker`, `flask`, and `vite`,
```sh
$ cd <PROJECT_ROOT>/scripts
$ ./dev.sh
```

> Running `exit.sh` is not necessary unless the script did not completely exit all programs.

### Dependencies

Install dependencies for
- MySQL

```sh
sudo apt update
sudo apt install pkg-config default-libmysqlclient-dev build-essential
```

```sh
$ git clone
$ python3 -m venv .venv
$ . ./.venv/bin/activate
$ pip install -r requirements.txt
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
$ python3 run.py
```

## Docker

1. Install [Docker Engine](https://docs.docker.com/engine/install/ubuntu/)
2. `cd` to the `docker/` directory in project root
3. Run `docker compose up -d`
4. If there are multiple docker compose files you can specify with `-f` flag

> Using `ports:` in the YAML file exposes ports to `0.0.0.0` by default!

To bring down docker containers

```sh
$ docker compose down
# or
$ docker compose down <container_name>
```

## Contributing

### Flask Migration commands

When updating models
```sh
$ flask db migrate -m '<message>'
$ flask db upgrade
```

To rollback
```sh
$ flask db downgrade
```

### Tests

```sh
$ cd <PROJECT_ROOT>/backend
$ python3 -m pytest tests/*
```
or
```sh
$ cd <PROJECT_ROOT>/scripts
$ ./test.sh
```

### Some testing commands

You must be logged in to run these commands through http://127.0.0.1:5000/login

#### Add to queue

To add a song to the queue,

```sh
$ curl -X POST http://127.0.0.1:5000/queues/main/tracks \
  -H "Content-Type: application/json" \
  -b "session=<session_key_from_cookies_storage>" \
  -d '{"url": "https://open.spotify.com/track/7vDj5t3DOFDbOkHyjb1wYB"}'
```

and observe [127.0.0.1/queues/main](http://127.0.0.1:5000/queues/main)

#### Play current song

To play the current song with a device.

> Check what devices are available in [127.0.0.1/player/devices](http://127.0.0.1:5000/player/devices)

```sh
$ curl -X POST http://127.0.0.1:5000/player/play
{
  "status": "playing"
}
```

#### Clear queue

```sh
$ curl -X POST http://127.0.0.1:5000/queues/main/clear
```

### JSON examples
#### `/playlists/<playlist_id>`

```js
{
      "album": "Tchaikovsky: Swan Lake Suites",
      "artists": [
        "Pyotr Ilyich Tchaikovsky",
        "Czech Symphony Orchestra",
        "Michaela R\u00f3zsa R\u016f\u017ei\u010dkov\u00e1"
      ],
      "duration_ms": 180379,
      "id": "6JyihARD2zGUa4uB4NfQiv",
      "name": "Swan Lake (Suite), Op. 20a, TH.219: I. Scene - Swan Theme",
      "preview_url": null
    },
```

#### `/playlists`

```js
{
  "playlists": [
    {
      "description": "Best classical music to study, chill, and relax. From Bach, Mozart, Vivaldi, Beethoven, Chopin, Debussy, Satie, Tchaikovsky, to Christmas Classics. Peaceful piano to Orchestras from Baroque to Romantic and Modern. From opera to chamber to symphony, all in one playlist. Only the best. Enjoy!",
      "id": "27Zm1P410dPfedsdoO9fqm",
      "images": [
        {
          "height": null,
          "url": "https://image-cdn-fa.spotifycdn.com/image/ab67706c0000da841d36875da61b27546bdec036",
          "width": null
        }
      ],
      "link": "/playlists/27Zm1P410dPfedsdoO9fqm",
      "name": "Classical Bangers \ud83c\udfb9\ud83c\udfbb",
      "owner": {
        "display_name": "Classical Bangers",
        "external_urls": {
          "spotify": "https://open.spotify.com/user/11102108940"
        },
        "href": "https://api.spotify.com/v1/users/11102108940",
        "id": "11102108940",
        "type": "user",
        "uri": "spotify:user:11102108940"
      },
      "track_count": 456
    },
  ]
}
```

#### `/me`

```js
{
  "display_name": "TechBase",
  "external_urls": {
    "spotify": "<some_url>"
  },
  "followers": {
    "href": null,
    "total": 1
  },
  "href": "<some_url>",
  "id": "<some_id>",
  "images": [
    {
      "height": 300,
      "url": "<some_url>",
      "width": 300
    },
    {
      "height": 64,
      "url": "<some_url>",
      "width": 64
    }
  ],
  "type": "user",
  "uri": "spotify:user:<some_url>"
}
```

#### `/devices`

```js
{
  "devices": [
    {
      "id": "05c3320cdf0ccef3f838b005799c85ee79edba4d",
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
