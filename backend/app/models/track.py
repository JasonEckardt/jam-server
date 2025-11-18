from app import db


class Track(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    artists = db.Column(db.String(64))
    duration_ms = db.Column(db.String(64))
    images = db.Column(db.String(64))
