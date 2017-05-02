from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from app import db
from app.buyers.models import Buyers
from app.product.models import Product
        
class Comments(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    body = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('buyers.id'))
    product_id = db.Column(db.Integer ,db.ForeignKey('product.id'))

    def __init__(self,user_id, body, product_id):
        self.user_id=user_id
        self.product_id=product_id
        self.body=body
        

    def __repr__(self):
        return '<You bitch:this is a comment>' 