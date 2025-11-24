from datetime import datetime, timezone
from app import db
from sqlalchemy import JSON
from sqlalchemy.ext.mutable import MutableList
import uuid


class Queue(db.Model):
    __tablename__ = "queues"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False)
    active_device = db.Column(db.String(64), nullable=True)
    now_playing = db.Column(db.String(64), nullable=True)
    progress_ms = db.Column(db.Integer, nullable=True)
    tracks = db.Column(MutableList.as_mutable(JSON), default=list)
    users = db.Column(MutableList.as_mutable(JSON), default=list)
    created_at = db.Column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
