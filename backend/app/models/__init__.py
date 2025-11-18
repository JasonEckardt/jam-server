from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.models.queue import Queue
from app.models.track import Track
from app.models.user import User
