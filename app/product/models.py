from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from app import db
from app.sellers.models import Sellers


class Product(db.Model):
    __tablename__= 'product'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(100)) 
    stock = db.Column(db.Integer)
    seller_id=db.Column(db.Integer,db.ForeignKey('sellers.id'))
    
    tags = db.Column(db.String(500))
    price = db.Column(db.Float)
    
    description = db.Column(db.String(500))
    
    category = db.Column(db.String(500))
    

    def __init__(self, name, stock, price, description, category, tags, seller_id):
        self.name = name
        self.stock = stock
        self.price = price
        self.description = description
        self.category = category
        self.seller_id=seller_id
        
        self.tags = tags
        

    def __repr__(self):
        return '<Product\'s Id is: %d, Product\'s Name is: %r, Product\'s Price is: %s and Product left in stock is: %s and seller is %s>' %(self.id, self.name, self.price, self.stock,self.seller_id) 

