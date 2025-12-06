from app import app, db
from models import User

with app.app_context():
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', name='System Admin', role='Admin')
        admin.set_password('admin')
        db.session.add(admin)
        print("Added user: admin / admin")
    else:
        print("User 'admin' already exists.")
    
    if not User.query.filter_by(username='cashier').first():
        cashier = User(username='cashier', name='System Cashier', role='Cashier')
        cashier.set_password('cashier')
        db.session.add(cashier)
        print("Added user: cashier / cashier")
    else:
        print("User 'cashier' already exists.")
    
    db.session.commit()
