from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, jsonify, make_response
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, DateField
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap
from app import db,app,login_manager
from flask_cors import CORS
from app.cart.models import Cart
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from wtforms.validators import InputRequired, Email, Length

mod_notification = Blueprint('notification', __name__)
# Bootstrap(app)

