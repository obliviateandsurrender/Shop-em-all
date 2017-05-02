from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from app import db
from app.buyers.models import Buyers
from app.product.models import Product

class Cart(db.Model):
    __tablename__= 'cart'
    id = db.Column(db.Integer, primary_key = True,autoincrement=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('buyers.id'))
    product_id = db.Column(db.Integer,db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    amount = db.Column(db.Float)
    status = db.Column(db.Boolean)
    name=db.Column(db.String(200))

    def __init__(self, buyer_id, product_id, quantity, amount, status,name):
        self.buyer_id = buyer_id
        self.product_id = product_id
        self.quantity = quantity
        self.amount = amount
        self.status = status
        self.name=name
    
    def __repr__(self):
        return '<Id is %s and buyer id is %s' %(self.id,self.buyer_id)
