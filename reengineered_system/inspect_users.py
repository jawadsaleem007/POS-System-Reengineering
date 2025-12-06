from app import app, db
from models import User
import os

print(f"DB URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

try:
    with app.app_context():
        users = User.query.all()
        print(f"Found {len(users)} users:")
        for u in users:
            print(f"Username: '{u.username}', Role: '{u.role}', Name: '{u.name}'")
except Exception as e:
    print(f"Error: {e}")
