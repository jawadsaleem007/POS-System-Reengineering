import os
from app import app, db
from models import User, Item, Rental
from datetime import datetime

# Paths to legacy data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LEGACY_DB_DIR = os.path.join(BASE_DIR, '..', 'Database')

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%m/%d/%y')
    except ValueError:
        return None

def migrate_employees():
    print("Migrating Employees...")
    filepath = os.path.join(LEGACY_DB_DIR, 'employeeDatabase.txt')
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 5:
                user_id = parts[0]
                role = parts[1]
                first_name = parts[2]
                last_name = parts[3]
                password = parts[4]
                
                name = f"{first_name} {last_name}"
                
                # Check if user exists
                if not User.query.filter_by(username=user_id).first():
                    user = User(username=user_id, name=name, role=role)
                    user.set_password(password) # Hashes the password
                    db.session.add(user)
    db.session.commit()
    print("Employees migrated.")

def migrate_items():
    print("Migrating Items...")
    filepath = os.path.join(LEGACY_DB_DIR, 'itemDatabase.txt')
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r') as f:
        for line in f:
            parts = line.strip().split(' ')
            if len(parts) >= 4:
                item_id = int(parts[0])
                name = parts[1]
                price = float(parts[2])
                stock = int(parts[3])
                
                if not Item.query.get(item_id):
                    item = Item(id=item_id, name=name, price=price, stock_quantity=stock)
                    db.session.add(item)
    db.session.commit()
    print("Items migrated.")

def migrate_rentals():
    print("Migrating Rentals...")
    filepath = os.path.join(LEGACY_DB_DIR, 'rentalDatabase.txt')
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r') as f:
        for line in f:
            parts = line.strip().split(' ')
            if len(parts) > 1:
                phone = parts[0]
                rentals = parts[1:]
                
                for rental_str in rentals:
                    # Format: ItemID,Date,ReturnedBool
                    r_parts = rental_str.split(',')
                    if len(r_parts) == 3:
                        item_id = int(r_parts[0])
                        date_str = r_parts[1]
                        returned_str = r_parts[2]
                        
                        rental_date = parse_date(date_str)
                        is_returned = returned_str.lower() == 'true'
                        
                        if rental_date:
                            rental = Rental(
                                user_phone=phone,
                                item_id=item_id,
                                rental_date=rental_date,
                                is_returned=is_returned
                            )
                            db.session.add(rental)
    db.session.commit()
    print("Rentals migrated.")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        migrate_employees()
        migrate_items()
        migrate_rentals()
        print("Migration complete.")
