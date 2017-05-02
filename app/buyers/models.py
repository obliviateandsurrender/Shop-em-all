from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from app import db

class Buyers(UserMixin,db.Model):
    __tablename__ = 'buyers'
    # Define the fields here
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(3), unique=True)
    phone_Number = db.Column(db.String(20))
    address = db.Column(db.String(200))
    birthdate = db.Column(db.Date)
    password = db.Column(db.String(800))
    	
    
    def __init__(self, username, email, password, phone_Number, address, birthdate):
        self.username = username
        self.email = email
        self.phone_Number = phone_Number
        self.address = address
        self.birthdate = birthdate
        self.password= password
    def __repr__(self):
        return '<Buyer\'s Id is: %d, Buyer\'s Name is: %r & Buyer\'s Email is: %r>>' %(self.id, self.username, self.email)
