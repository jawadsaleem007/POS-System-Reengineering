from app import app
from models import User

with app.app_context():
    u = User.query.filter_by(username='110001').first()
    if u:
        print(f"User found: {u.username}")
        print(f"Hash: {u.password_hash}")
        is_valid = u.check_password('1')
        print(f"Password '1' valid? {is_valid}")
    else:
        print("User '110001' not found")
