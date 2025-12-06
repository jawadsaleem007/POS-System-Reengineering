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
    print('Migrating Employees...')
    filepath = os.path.join(LEGACY_DB_DIR, 'employeeDatabase.txt')
    if not os.path.exists(filepath):
        print(f'File not found: {filepath}')
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
                
                name = f'{first_name} {last_name}'
                
                # Check if user exists
                if not User.query.filter_by(username=user_id).first():
                    user = User(username=user_id, name=name, role=role)
                    user.set_password(password) # Hashes the password
                    db.session.add(user)
    db.session.commit()
    print('Employees migrated.')

def migrate_sale_items():
    print('Migrating Sale Items...')
    filepath = os.path.join(LEGACY_DB_DIR, 'itemDatabase.txt')
    if not os.path.exists(filepath):
        print(f'File not found: {filepath}')
        return

    with open(filepath, 'r') as f:
        for line in f:
            parts = line.strip().split(' ')
            if len(parts) >= 4:
                item_id = int(parts[0])
                name = parts[1]
                price = float(parts[2])
                stock = int(parts[3])
                
                if not Item.query.filter_by(legacy_id=item_id, type='sale').first():
                    item = Item(legacy_id=item_id, name=name, price=price, stock_quantity=stock, type='sale')
                    db.session.add(item)
    db.session.commit()
    print("Sale Items migrated.")

def migrate_rentable_items():
    print('Migrating Rentable Items...')
    filepath = os.path.join(LEGACY_DB_DIR, 'rentalDatabase.txt')
    if not os.path.exists(filepath):
        print(f'File not found: {filepath}')
        return

    with open(filepath, 'r') as f:
        for line in f:
            parts = line.strip().split(' ')
            if len(parts) >= 4:
                item_id = int(parts[0])
                name = parts[1]
                price = float(parts[2])
                stock = int(parts[3])
                
                if not Item.query.filter_by(legacy_id=item_id, type='rental').first():
                    item = Item(legacy_id=item_id, name=name, price=price, stock_quantity=stock, type='rental')
                    db.session.add(item)
    db.session.commit()
    print("Rentable Items migrated.")

def migrate_active_rentals():
    print("Migrating Active Rentals History...")
    filepath = os.path.join(LEGACY_DB_DIR, 'userDatabase.txt')
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    unique_lines = set()
    with open(filepath, 'r') as f:
        # Skip header
        next(f, None)
        for line in f:
            stripped_line = line.strip()
            if stripped_line and stripped_line not in unique_lines:
                unique_lines.add(stripped_line)
                
                parts = stripped_line.split(' ')
                if len(parts) > 1:
                    phone = parts[0]
                    rentals = parts[1:]
                    
                    for rental_str in rentals:
                        # Format: ItemID,Date,ReturnedBool
                        r_parts = rental_str.split(',')
                        if len(r_parts) == 3:
                            legacy_item_id = int(r_parts[0])
                            date_str = r_parts[1]
                            returned_str = r_parts[2]
                            
                            rental_date = parse_date(date_str)
                            is_returned = returned_str.lower() == 'true'
                            
                            if rental_date:
                                # Check if item exists (it should be in rentable items now)
                                item = Item.query.filter_by(legacy_id=legacy_item_id, type='rental').first()
                                if item:
                                    rental = Rental(user_phone=phone, item_id=item.id, rental_date=rental_date, is_returned=is_returned)
                                    db.session.add(rental)
    db.session.commit()
    print('Active Rentals History migrated.')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        migrate_employees()
        migrate_sale_items()
        migrate_rentable_items()
        migrate_active_rentals()
        print('Migration complete.')
