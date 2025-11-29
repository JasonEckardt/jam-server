import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    db.session.query(User).delete()
    db.session.commit()
    print("All users deleted")
