from app import app, db
from models import Coupon, SaleReturn

with app.app_context():
    db.create_all()
    print("Database schema updated.")
    
    # Add some default coupons if they don't exist
    if not Coupon.query.filter_by(code='SAVE10').first():
        db.session.add(Coupon(code='SAVE10', discount_percent=0.10))
        db.session.add(Coupon(code='WELCOME20', discount_percent=0.20))
        db.session.commit()
        print("Default coupons added.")
