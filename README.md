# Spotify Jam Server

A self-hosted Spotify Jam server to play music with your friends! Share a queue with your friends and connect your Spotify account to import songs into the shared queue. Playback from a Raspberry Pi connected to speakers via Bluetooth or Aux.

- Flask for API and backend
- Vite + React for frontend
- MySQL for storage

## Issues to Address

- The admin user set as playback will have their music recommendations ruined
- There is no generic 'playback' user at the moment
- Playback without authentication & premium may get this project in trouble with Spotify
- Parsing and downloading music and caching music is a pain in the ass

## Usage

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

## Contributing

### Tests

```sh
$ python3 -m pytest tests/*
```
or
```sh
. scripts/test.sh
```

### Some testing commands

You must be logged in to run these commands through http://localhost:5000/login

#### Add to queue

To add a song to the queue,

```sh
$ curl -X POST http://localhost:5000/queue \
  -H "Content-Type: application/json" \
  -d '{"url": "https://open.spotify.com/track/7vDj5t3DOFDbOkHyjb1wYB"}'
```

and observe [localhost/queue](http://localhost:5000/queue)

#### Play current song

To play the current song with a device.

> Check what devices are available in [localhost/player/devices](http://localhost:5000/player/devices)

```sh
$ curl -X POST http://localhost:5000/player/play
{
  "status": "playing"
}
```

### JSON examples

```js
// http://<redirect_uri>/playlists/27Zm1P410dPfedsdoO9fqm
// ...
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
// ...
```

```js
// http://<redirect_uri>/playlists
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
// ...
```

```js
// http://<redirect_uri>/me
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
