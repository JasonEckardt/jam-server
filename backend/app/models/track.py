from app import db


class Track(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    artists = db.Column(db.String(64))
    duration_ms = db.Column(db.String(64))
    images = db.Column(db.String(64))


"""
  "id": track.get("id"),
  "name": track.get("name"),
  "artists": [a.get("name") for a in track.get("artists", [])],
  "album": track.get("album", {}).get("name"),
  "duration_ms": track.get("duration_ms"),
  "images": track.get("album", {}).get("images", []),
"""
