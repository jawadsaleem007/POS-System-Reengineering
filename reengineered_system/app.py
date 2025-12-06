from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Item, Rental, Sale, SaleItem, Coupon, SaleReturn
import os
from datetime import datetime

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'pos.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'reengineering_project_secret_key'

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/')
@login_required
def index():
    return render_template('index.html', user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/inventory')
@login_required
def inventory():
    items = Item.query.all()
    return render_template('inventory.html', items=items)

@app.route('/inventory/add', methods=['GET', 'POST'])
@login_required
def add_item():
    if request.method == 'POST':
        name = request.form.get('name')
        price = float(request.form.get('price'))
        stock = int(request.form.get('stock'))
        
        new_item = Item(name=name, price=price, stock_quantity=stock)
        db.session.add(new_item)
        db.session.commit()
        flash('Item added successfully.')
        return redirect(url_for('inventory'))
    return render_template('edit_item.html', item=None)

@app.route('/inventory/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    item = db.session.get(Item, item_id)
    if request.method == 'POST':
        item.name = request.form.get('name')
        item.price = float(request.form.get('price'))
        item.stock_quantity = int(request.form.get('stock'))
        db.session.commit()
        flash('Item updated successfully.')
        return redirect(url_for('inventory'))
    return render_template('edit_item.html', item=item)

@app.route('/inventory/delete/<int:item_id>')
@login_required
def delete_item(item_id):
    item = db.session.get(Item, item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        flash('Item deleted.')
    return redirect(url_for('inventory'))

@app.route('/sales_history')
@login_required
def sales_history():
    if current_user.role != 'Admin':
        return redirect(url_for('index'))
    sales = Sale.query.order_by(Sale.date.desc()).all()
    return render_template('sales_history.html', sales=sales)

@app.route('/return_sale/<int:sale_id>', methods=['GET', 'POST'])
@login_required
def return_sale(sale_id):
    sale = db.session.get(Sale, sale_id)
    if request.method == 'POST':
        reason = request.form.get('reason')
        refund_amount = float(request.form.get('refund_amount'))
        
        # Create return record
        return_record = SaleReturn(sale_id=sale.id, reason=reason, refund_amount=refund_amount)
        db.session.add(return_record)
        
        # Restock items
        for sale_item in sale.items:
            item = db.session.get(Item, sale_item.item_id)
            if item:
                item.stock_quantity += sale_item.quantity
        
        db.session.commit()
        flash('Sale returned and items restocked.')
        return redirect(url_for('sales_history'))
    
    return render_template('return_sale.html', sale=sale)

@app.route('/pos', methods=['GET', 'POST'])
@login_required
def pos():
    if request.method == 'POST':
        data = request.json
        cart = data.get('cart', [])
        coupon_code = data.get('coupon', '').strip()
        
        total = 0
        discount = 0
        
        # Calculate subtotal first
        temp_total = 0
        for cart_item in cart:
            item = db.session.get(Item, cart_item['id'])
            if item:
                temp_total += item.price * cart_item['quantity']
        
        # Apply Coupon
        if coupon_code:
            coupon = Coupon.query.filter_by(code=coupon_code, is_active=True).first()
            if coupon:
                discount = temp_total * coupon.discount_percent
            else:
                return {'error': 'Invalid coupon code'}, 400

        sale = Sale(total_amount=0, cashier_id=current_user.id)
        db.session.add(sale)
        
        for cart_item in cart:
            item = db.session.get(Item, cart_item['id'])
            if item and item.stock_quantity >= cart_item['quantity']:
                sale_item = SaleItem(
                    sale=sale,
                    item_id=item.id,
                    quantity=cart_item['quantity'],
                    price_at_sale=item.price
                )
                item.stock_quantity -= cart_item['quantity']
                total += item.price * cart_item['quantity']
                db.session.add(sale_item)
            else:
                return {'error': f'Insufficient stock for {item.name}'}, 400
        
        sale.total_amount = total - discount
        db.session.commit()
        return {'success': True, 'sale_id': sale.id, 'discount': discount, 'final_total': sale.total_amount}
        
    items = Item.query.filter(Item.stock_quantity > 0).all()
    return render_template('pos.html', items=items)

@app.route('/rentals')
@login_required
def rentals():
    active_rentals = Rental.query.filter_by(is_returned=False).all()
    return render_template('rentals.html', rentals=active_rentals)

@app.route('/return_rental/<int:rental_id>')
@login_required
def return_rental(rental_id):
    rental = db.session.get(Rental, rental_id)
    if rental:
        rental.is_returned = True
        rental.return_date = datetime.utcnow()
        db.session.commit()
        flash('Item returned successfully.')
    return redirect(url_for('rentals'))

@app.route('/employees')
@login_required
def employees():
    if current_user.role != 'Admin':
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('index'))
    
    users = User.query.all()
    return render_template('employees.html', users=users)

@app.route('/employees/add', methods=['GET', 'POST'])
@login_required
def add_employee():
    if current_user.role != 'Admin':
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        name = request.form.get('name')
        role = request.form.get('role')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
        else:
            new_user = User(username=username, name=name, role=role)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Employee added successfully.')
            return redirect(url_for('employees'))
    return render_template('edit_employee.html', user=None)

@app.route('/employees/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_employee(user_id):
    if current_user.role != 'Admin':
        return redirect(url_for('index'))
        
    user = db.session.get(User, user_id)
    if request.method == 'POST':
        user.name = request.form.get('name')
        user.role = request.form.get('role')
        password = request.form.get('password')
        if password:
            user.set_password(password)
        db.session.commit()
        flash('Employee updated successfully.')
        return redirect(url_for('employees'))
    return render_template('edit_employee.html', user=user)

@app.route('/employees/delete/<int:user_id>')
@login_required
def delete_employee(user_id):
    if current_user.role != 'Admin':
        return redirect(url_for('index'))
        
    user = db.session.get(User, user_id)
    if user and user.id != current_user.id: # Prevent self-deletion
        db.session.delete(user)
        db.session.commit()
        flash('Employee deleted.')
    else:
        flash('Cannot delete yourself or user not found.')
    return redirect(url_for('employees'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
