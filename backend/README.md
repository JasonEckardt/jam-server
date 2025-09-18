# Jam Server Backend

## Structure
- `/api`: Utility functions for API
- `/models`: Database models
- `/routes`: Flask routes

> Naming convention? Singular for models, plural for routes?

## Usage Flow

- Admin logs into Spotify and sets a device for playback
- Redirect to player settings to enable private session to prevent polluting music recommendations. If not, warn the admin
- A session is made, others can join.
- A guest only needs to sign in if they want to import songs. Otherwise, you can paste URL (or search for songs but it needs implementation and testing).
- Admin can pause, skip, delete songs, add songs.
- Guests can add songs, vote to skip, vote to pause.
- Append-only music queue, pointer moves to next song after skipped or song ends. Music history can be view if the user scrolls up.
