from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from app import db

class Sellers(UserMixin,db.Model):
    __tablename__= 'sellers'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(200))
    email = db.Column(db.String(50),unique=True)
    phone_Number = db.Column(db.Integer)
    website = db.Column(db.String(100))
    password = db.Column(db.String(800))
    
    
    def __init__(self,username, email, phone_Number, website, password):
        self.username = username
        self.email = email
        self.phone_Number = phone_Number
        self.website = website
        self.password = password    
       

    def __repr__(self):
        return '<Seller\'s Id is: %d, Seller\'s Name is: %r, Seller\'s Email is: %r>>' %(self.id,self.username, self.email)

