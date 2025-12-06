import unittest
import sys
import os

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import User, Item, Sale

class POSTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()
            
            # Create test user
            user = User(username='testadmin', name='Test Admin', role='Admin')
            user.set_password('password')
            db.session.add(user)
            
            # Create test item
            item = Item(legacy_id=1000, name='Test Item', price=10.0, stock_quantity=5, type='sale')
            db.session.add(item)
            
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def test_login(self):
        response = self.login('testadmin', 'password')
        self.assertIn(b'Dashboard', response.data)

    def test_inventory_access(self):
        self.login('testadmin', 'password')
        response = self.app.get('/inventory')
        self.assertIn(b'Test Item', response.data)

    def test_pos_sale(self):
        self.login('testadmin', 'password')
        
        # Simulate sale
        cart_data = {
            'cart': [
                {'id': 1, 'quantity': 2}
            ]
        }
        
        response = self.app.post('/pos', json=cart_data)
        self.assertEqual(response.status_code, 200)
        
        with app.app_context():
            # Check stock reduction
            item = db.session.get(Item, 1)
            self.assertEqual(item.stock_quantity, 3) # 5 - 2 = 3
            
            # Check sale record
            sale = Sale.query.first()
            self.assertIsNotNone(sale)
            self.assertEqual(sale.total_amount, 20.0)

if __name__ == '__main__':
    unittest.main()
