from datetime import datetime, timezone
from app import db
from sqlalchemy import JSON
from sqlalchemy.ext.mutable import MutableList


class Queue(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    current_track = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    tracks = db.Column(MutableList.as_mutable(JSON), default=list)
    users = db.Column(MutableList.as_mutable(JSON), default=list)
